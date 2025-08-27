"""
Pipeline ETL pour Ubisoft People Analytics.
"""

import pandas as pd
import numpy as np
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union
from datetime import datetime, timedelta
import sqlalchemy as sa
from sqlalchemy import create_engine, text
import os
from dataclasses import dataclass
from src.utils.data_processing import DataProcessor, validate_data_quality

logger = logging.getLogger(__name__)

@dataclass
class ETLConfig:
    """Configuration pour le pipeline ETL."""
    database_url: str
    raw_data_path: Path
    processed_data_path: Path
    batch_size: int = 1000
    validation_threshold: float = 0.8
    backup_enabled: bool = True

class UbisoftETLPipeline:
    """Pipeline ETL principal pour les données RH Ubisoft."""
    
    def __init__(self, config: ETLConfig):
        self.config = config
        self.engine = create_engine(config.database_url)
        self.data_processor = DataProcessor()
        self.execution_log = []
        
    def extract_from_csv(self, file_path: Union[str, Path]) -> pd.DataFrame:
        """Extraire les données depuis un fichier CSV."""
        try:
            df = pd.read_csv(file_path)
            logger.info(f"Extraction CSV réussie: {len(df)} lignes depuis {file_path}")
            
            self._log_step("extract_csv", "success", {
                'source_file': str(file_path),
                'rows_extracted': len(df),
                'columns': list(df.columns)
            })
            
            return df
            
        except Exception as e:
            logger.error(f"Erreur extraction CSV: {e}")
            self._log_step("extract_csv", "error", {'error': str(e)})
            raise
    
    def extract_from_database(self, query: str, 
                            params: Optional[Dict] = None) -> pd.DataFrame:
        """Extraire les données depuis la base de données."""
        try:
            df = pd.read_sql(query, self.engine, params=params)
            logger.info(f"Extraction DB réussie: {len(df)} lignes")
            
            self._log_step("extract_db", "success", {
                'rows_extracted': len(df),
                'query': query[:100] + "..." if len(query) > 100 else query
            })
            
            return df
            
        except Exception as e:
            logger.error(f"Erreur extraction DB: {e}")
            self._log_step("extract_db", "error", {'error': str(e)})
            raise
    
    def extract_hr_data(self, source_type: str = "csv") -> pd.DataFrame:
        """Extraire toutes les données RH selon le type de source."""
        
        if source_type == "csv":
            # Extraction depuis fichiers CSV
            data_files = {
                'employees': self.config.raw_data_path / 'employees.csv',
                'assessments': self.config.raw_data_path / 'assessments.csv',
                'performance': self.config.raw_data_path / 'performance.csv'
            }
            
            dataframes = {}
            for name, file_path in data_files.items():
                if file_path.exists():
                    dataframes[name] = self.extract_from_csv(file_path)
                else:
                    logger.warning(f"Fichier non trouvé: {file_path}")
            
            # Joindre les données
            if 'employees' in dataframes:
                df = dataframes['employees']
                
                if 'assessments' in dataframes:
                    df = df.merge(dataframes['assessments'], 
                                on='employee_id', how='left')
                
                if 'performance' in dataframes:
                    df = df.merge(dataframes['performance'], 
                                on='employee_id', how='left')
                
                return df
            else:
                raise FileNotFoundError("Fichier employees.csv requis")
                
        elif source_type == "database":
            # Extraction depuis base de données
            query = """
            SELECT 
                e.employee_id,
                e.department,
                e.hire_date,
                e.status,
                a.creative_score,
                a.burnout_scale,
                a.communication_style,
                a.assessment_date,
                p.productivity_score,
                p.innovation_index
            FROM employees e
            LEFT JOIN assessments a ON e.employee_id = a.employee_id
            LEFT JOIN performance p ON e.employee_id = p.employee_id
            WHERE e.status = 'active'
            """
            
            return self.extract_from_database(query)
        
        else:
            raise ValueError(f"Type de source non supporté: {source_type}")
    
    def transform_employee_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Transformer les données d'employés."""
        logger.info("Début transformation des données")
        
        # Validation initiale
        quality_report = validate_data_quality(df)
        if quality_report['data_quality_score'] < self.config.validation_threshold * 100:
            logger.warning(f"Qualité des données faible: {quality_report['data_quality_score']:.1f}%")
        
        # Pipeline de transformation
        df_transformed = df.copy()
        
        # 1. Nettoyage de base
        df_transformed = self.data_processor.clean_employee_data(df_transformed)
        
        # 2. Gestion des valeurs manquantes
        df_transformed = self.data_processor.handle_missing_values(df_transformed)
        
        # 3. Feature engineering
        df_transformed = self.data_processor.engineer_features(df_transformed)
        
        # 4. Encodage des variables catégorielles
        df_transformed = self.data_processor.encode_categorical_variables(df_transformed)
        
        # 5. Détection des outliers
        outliers = self.data_processor.detect_outliers(df_transformed)
        if outliers:
            logger.info(f"Outliers détectés dans {len(outliers)} colonnes")
            
            # Traitement conservateur des outliers (cap au 99e percentile)
            for col, outlier_indices in outliers.items():
                if len(outlier_indices) < len(df_transformed) * 0.05:  # < 5% outliers
                    p99 = df_transformed[col].quantile(0.99)
                    p1 = df_transformed[col].quantile(0.01)
                    df_transformed[col] = df_transformed[col].clip(p1, p99)
        
        # 6. Validation finale
        self._validate_transformed_data(df_transformed)
        
        self._log_step("transform", "success", {
            'input_rows': len(df),
            'output_rows': len(df_transformed),
            'input_columns': len(df.columns),
            'output_columns': len(df_transformed.columns),
            'outliers_detected': len(outliers)
        })
        
        logger.info(f"Transformation terminée: {len(df_transformed)} lignes, {len(df_transformed.columns)} colonnes")
        
        return df_transformed
    
    def load_to_database(self, df: pd.DataFrame, 
                        table_name: str,
                        if_exists: str = 'replace') -> bool:
        """Charger les données dans la base de données."""
        try:
            # Backup si nécessaire
            if self.config.backup_enabled and if_exists == 'replace':
                self._backup_table(table_name)
            
            # Chargement par batch pour de gros datasets
            total_rows = len(df)
            batch_size = self.config.batch_size
            
            for i in range(0, total_rows, batch_size):
                batch_df = df.iloc[i:i + batch_size]
                batch_df.to_sql(
                    table_name, 
                    self.engine, 
                    if_exists='append' if i > 0 else if_exists,
                    index=False,
                    method='multi'
                )
                
                logger.info(f"Batch {i//batch_size + 1}/{(total_rows-1)//batch_size + 1} chargé")
            
            # Vérification post-chargement
            verification_query = f"SELECT COUNT(*) as count FROM {table_name}"
            result = pd.read_sql(verification_query, self.engine)
            loaded_count = result.iloc[0]['count']
            
            if loaded_count != total_rows:
                raise ValueError(f"Nombre de lignes incohérent: {loaded_count} vs {total_rows}")
            
            self._log_step("load_db", "success", {
                'table_name': table_name,
                'rows_loaded': total_rows,
                'batches': (total_rows-1)//batch_size + 1
            })
            
            logger.info(f"Chargement DB réussi: {total_rows} lignes dans {table_name}")
            return True
            
        except Exception as e:
            logger.error(f"Erreur chargement DB: {e}")
            self._log_step("load_db", "error", {'error': str(e)})
            raise
    
    def load_to_csv(self, df: pd.DataFrame, 
                   file_path: Union[str, Path]) -> bool:
        """Charger les données dans un fichier CSV."""
        try:
            file_path = Path(file_path)
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Backup si le fichier existe
            if file_path.exists() and self.config.backup_enabled:
                backup_path = file_path.with_suffix(f'.backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv')
                file_path.rename(backup_path)
                logger.info(f"Backup créé: {backup_path}")
            
            df.to_csv(file_path, index=False)
            
            # Vérification
            verification_df = pd.read_csv(file_path)
            if len(verification_df) != len(df):
                raise ValueError(f"Nombre de lignes incohérent après écriture")
            
            self._log_step("load_csv", "success", {
                'file_path': str(file_path),
                'rows_saved': len(df)
            })
            
            logger.info(f"Sauvegarde CSV réussie: {len(df)} lignes dans {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"Erreur sauvegarde CSV: {e}")
            self._log_step("load_csv", "error", {'error': str(e)})
            raise
    
    def run_full_pipeline(self, source_type: str = "csv",
                         output_table: str = "processed_employee_data") -> Dict:
        """Exécuter le pipeline ETL complet."""
        
        pipeline_start = datetime.now()
        logger.info("=== DÉBUT PIPELINE ETL ===")
        
        try:
            # 1. Extract
            logger.info("Phase 1: Extraction")
            raw_data = self.extract_hr_data(source_type)
            
            # 2. Transform
            logger.info("Phase 2: Transformation")
            processed_data = self.transform_employee_data(raw_data)
            
            # 3. Load
            logger.info("Phase 3: Chargement")
            
            # Chargement DB
            self.load_to_database(processed_data, output_table)
            
            # Chargement fichier de backup
            backup_file = self.config.processed_data_path / f"{output_table}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            self.load_to_csv(processed_data, backup_file)
            
            pipeline_end = datetime.now()
            execution_time = (pipeline_end - pipeline_start).total_seconds()
            
            # Résumé de l'exécution
            summary = {
                'status': 'success',
                'execution_time_seconds': execution_time,
                'start_time': pipeline_start.isoformat(),
                'end_time': pipeline_end.isoformat(),
                'input_rows': len(raw_data),
                'output_rows': len(processed_data),
                'data_quality_improvement': self._calculate_quality_improvement(raw_data, processed_data),
                'steps_executed': len(self.execution_log),
                'output_table': output_table,
                'backup_file': str(backup_file)
            }
            
            logger.info(f"=== PIPELINE ETL TERMINÉ - {execution_time:.2f}s ===")
            logger.info(f"Données traitées: {len(raw_data)} → {len(processed_data)} lignes")
            
            return summary
            
        except Exception as e:
            logger.error(f"=== ÉCHEC PIPELINE ETL: {e} ===")
            
            summary = {
                'status': 'failed',
                'error': str(e),
                'execution_time_seconds': (datetime.now() - pipeline_start).total_seconds(),
                'start_time': pipeline_start.isoformat(),
                'steps_executed': len(self.execution_log)
            }
            
            raise Exception(f"Pipeline ETL échoué: {e}")
    
    def _validate_transformed_data(self, df: pd.DataFrame):
        """Valider les données transformées."""
        
        # Vérifications de base
        if df.empty:
            raise ValueError("Dataset vide après transformation")
        
        if 'employee_id' not in df.columns:
            raise ValueError("Colonne employee_id manquante")
        
        # Vérifier les duplicatas d'employee_id
        if df['employee_id'].duplicated().any():
            raise ValueError("Employee_id dupliqués détectés")
        
        # Vérifier les ranges de valeurs
        if 'creative_score' in df.columns:
            if not df['creative_score'].between(0, 100).all():
                raise ValueError("Creative_score hors range [0, 100]")
        
        if 'burnout_scale' in df.columns:
            if not df['burnout_scale'].between(1, 10).all():
                raise ValueError("Burnout_scale hors range [1, 10]")
        
        # Vérifier le pourcentage de valeurs manquantes
        missing_pct = (df.isnull().sum().sum() / df.size) * 100
        if missing_pct > 20:  # Plus de 20% de valeurs manquantes
            logger.warning(f"Pourcentage élevé de valeurs manquantes: {missing_pct:.1f}%")
    
    def _backup_table(self, table_name: str):
        """Créer un backup de la table."""
        try:
            backup_table = f"{table_name}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            with self.engine.connect() as conn:
                # Vérifier si la table existe
                result = conn.execute(text(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'"))
                if result.fetchone():
                    # Créer le backup
                    conn.execute(text(f"CREATE TABLE {backup_table} AS SELECT * FROM {table_name}"))
                    logger.info(f"Backup table créé: {backup_table}")
                    
        except Exception as e:
            logger.warning(f"Impossible de créer le backup: {e}")
    
    def _calculate_quality_improvement(self, before_df: pd.DataFrame, 
                                     after_df: pd.DataFrame) -> Dict[str, float]:
        """Calculer l'amélioration de la qualité des données."""
        
        before_quality = validate_data_quality(before_df)
        after_quality = validate_data_quality(after_df)
        
        improvement = {
            'missing_values_reduction': before_quality['missing_values_pct'] - after_quality['missing_values_pct'],
            'duplicate_reduction': before_quality['duplicate_rows_pct'] - after_quality['duplicate_rows_pct'],
            'quality_score_improvement': after_quality['data_quality_score'] - before_quality['data_quality_score']
        }
        
        return improvement
    
    def _log_step(self, step_name: str, status: str, details: Dict):
        """Logger une étape du pipeline."""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'step': step_name,
            'status': status,
            'details': details
        }
        
        self.execution_log.append(log_entry)
    
    def get_pipeline_status(self) -> Dict:
        """Obtenir le statut du pipeline."""
        return {
            'total_steps': len(self.execution_log),
            'successful_steps': len([step for step in self.execution_log if step['status'] == 'success']),
            'failed_steps': len([step for step in self.execution_log if step['status'] == 'error']),
            'last_execution': self.execution_log[-1] if self.execution_log else None,
            'execution_log': self.execution_log
        }

def run_daily_etl():
    """Fonction pour exécution quotidienne du pipeline ETL."""
    
    # Configuration
    config = ETLConfig(
        database_url=os.getenv("DATABASE_URL", "sqlite:///ubisoft_analytics.db"),
        raw_data_path=Path("data/raw"),
        processed_data_path=Path("data/processed"),
        batch_size=1000,
        validation_threshold=0.8,
        backup_enabled=True
    )
    
    # Initialiser et lancer le pipeline
    pipeline = UbisoftETLPipeline(config)
    
    try:
        result = pipeline.run_full_pipeline(
            source_type="csv",
            output_table="daily_employee_analytics"
        )
        
        logger.info("ETL quotidien terminé avec succès")
        return result
        
    except Exception as e:
        logger.error(f"Échec ETL quotidien: {e}")
        raise

if __name__ == "__main__":
    # Configuration logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Lancer ETL
    result = run_daily_etl()
    print(f"Pipeline terminé: {result['status']}")
