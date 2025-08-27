"""
Tests pour le pipeline ETL.
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import tempfile
import os
from unittest.mock import patch, MagicMock
import sqlite3

from src.etl import UbisoftETLPipeline, ETLConfig
from src.utils.data_processing import DataProcessor

class TestDataProcessor:
    """Tests pour la classe DataProcessor."""
    
    @pytest.fixture
    def sample_data(self):
        """Données d'exemple pour les tests."""
        return pd.DataFrame({
            'employee_id': ['E001', 'E002', 'E003', 'E001'],  # Avec doublon
            'creative_score': [85, 72, 91, 85],
            'burnout_scale': [3, 6, 2, 3],
            'department': [' Design ', 'DEV', 'qa', ' Design '],  # Avec espaces et casse
            'missing_col': [1, None, 3, 1]
        })
    
    def test_clean_employee_data(self, sample_data):
        """Test nettoyage des données."""
        processor = DataProcessor()
        cleaned_data = processor.clean_employee_data(sample_data)
        
        # Vérifier suppression des doublons
        assert len(cleaned_data) == 3
        assert cleaned_data['employee_id'].nunique() == 3
        
        # Vérifier nettoyage des chaînes
        assert all(cleaned_data['department'].str.islower())
        assert all(~cleaned_data['department'].str.contains(' '))
    
    def test_handle_missing_values(self, sample_data):
        """Test gestion des valeurs manquantes."""
        processor = DataProcessor()
        imputed_data = processor.handle_missing_values(sample_data)
        
        # Vérifier qu'il n'y a plus de valeurs manquantes
        assert imputed_data.isnull().sum().sum() == 0
    
    def test_engineer_features(self, sample_data):
        """Test création de features."""
        processor = DataProcessor()
        featured_data = processor.engineer_features(sample_data)
        
        # Vérifier création de features de ratio
        assert 'creativity_burnout_ratio' in featured_data.columns
        
        # Vérifier création de features binaires
        assert 'creative_score_high' in featured_data.columns
        assert 'burnout_scale_high' in featured_data.columns
    
    def test_encode_categorical_variables(self, sample_data):
        """Test encodage des variables catégorielles."""
        processor = DataProcessor()
        encoded_data = processor.encode_categorical_variables(sample_data)
        
        # Vérifier création de colonnes encodées
        assert 'department_encoded' in encoded_data.columns
        
        # Vérifier que l'encodage est numérique
        assert encoded_data['department_encoded'].dtype in [np.int64, np.int32]

class TestETLPipeline:
    """Tests pour le pipeline ETL principal."""
    
    @pytest.fixture
    def temp_config(self):
        """Configuration temporaire pour les tests."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            config = ETLConfig(
                database_url=f"sqlite:///{temp_path}/test.db",
                raw_data_path=temp_path / "raw",
                processed_data_path=temp_path / "processed",
                batch_size=100,
                validation_threshold=0.5,
                backup_enabled=False
            )
            
            # Créer les dossiers
            config.raw_data_path.mkdir(exist_ok=True)
            config.processed_data_path.mkdir(exist_ok=True)
            
            yield config
    
    @pytest.fixture
    def sample_csv_data(self, temp_config):
        """Créer des fichiers CSV de test."""
        
        # Données employés
        employees_data = pd.DataFrame({
            'employee_id': ['E001', 'E002', 'E003'],
            'department': ['Design', 'Dev', 'QA'],
            'hire_date': ['2020-01-15', '2021-03-10', '2019-11-20'],
            'status': ['active', 'active', 'active']
        })
        
        # Données évaluations
        assessments_data = pd.DataFrame({
            'employee_id': ['E001', 'E002', 'E003'],
            'creative_score': [85.0, 72.0, 91.0],
            'burnout_scale': [3, 6, 2],
            'communication_style': ['visual', 'analytical', 'social'],
            'assessment_date': ['2025-01-15', '2025-01-16', '2025-01-17']
        })
        
        # Sauvegarder les fichiers
        employees_data.to_csv(temp_config.raw_data_path / 'employees.csv', index=False)
        assessments_data.to_csv(temp_config.raw_data_path / 'assessments.csv', index=False)
        
        return employees_data, assessments_data
    
    def test_extract_from_csv(self, temp_config, sample_csv_data):
        """Test extraction depuis CSV."""
        pipeline = UbisoftETLPipeline(temp_config)
        
        # Test extraction fichier employés
        employees_df = pipeline.extract_from_csv(temp_config.raw_data_path / 'employees.csv')
        
        assert len(employees_df) == 3
        assert 'employee_id' in employees_df.columns
        assert 'department' in employees_df.columns
    
    def test_extract_hr_data(self, temp_config, sample_csv_data):
        """Test extraction complète des données RH."""
        pipeline = UbisoftETLPipeline(temp_config)
        
        hr_data = pipeline.extract_hr_data(source_type="csv")
        
        # Vérifier la jointure des données
        assert len(hr_data) == 3
        assert 'employee_id' in hr_data.columns
        assert 'creative_score' in hr_data.columns
        assert 'department' in hr_data.columns
    
    def test_transform_employee_data(self, temp_config, sample_csv_data):
        """Test transformation des données."""
        pipeline = UbisoftETLPipeline(temp_config)
        
        # Extraire les données brutes
        raw_data = pipeline.extract_hr_data(source_type="csv")
        
        # Transformer
        transformed_data = pipeline.transform_employee_data(raw_data)
        
        # Vérifier les transformations
        assert len(transformed_data) >= len(raw_data)  # Features ajoutées
        assert 'creativity_burnout_ratio' in transformed_data.columns
        assert 'department_encoded' in transformed_data.columns
        
        # Vérifier qu'il n'y a pas de valeurs manquantes
        assert transformed_data.isnull().sum().sum() == 0
    
    def test_load_to_database(self, temp_config, sample_csv_data):
        """Test chargement en base de données."""
        pipeline = UbisoftETLPipeline(temp_config)
        
        # Préparer des données test
        test_data = pd.DataFrame({
            'employee_id': ['E001', 'E002'],
            'score': [85, 72]
        })
        
        # Charger en DB
        success = pipeline.load_to_database(test_data, 'test_table')
        
        assert success is True
        
        # Vérifier le chargement
        verification_df = pd.read_sql('SELECT * FROM test_table', pipeline.engine)
        assert len(verification_df) == 2
        assert list(verification_df.columns) == ['employee_id', 'score']
    
    def test_load_to_csv(self, temp_config):
        """Test sauvegarde CSV."""
        pipeline = UbisoftETLPipeline(temp_config)
        
        test_data = pd.DataFrame({
            'col1': [1, 2, 3],
            'col2': ['A', 'B', 'C']
        })
        
        output_file = temp_config.processed_data_path / 'test_output.csv'
        success = pipeline.load_to_csv(test_data, output_file)
        
        assert success is True
        assert output_file.exists()
        
        # Vérifier le contenu
        loaded_data = pd.read_csv(output_file)
        pd.testing.assert_frame_equal(test_data, loaded_data)
    
    def test_run_full_pipeline(self, temp_config, sample_csv_data):
        """Test pipeline ETL complet."""
        pipeline = UbisoftETLPipeline(temp_config)
        
        result = pipeline.run_full_pipeline(
            source_type="csv",
            output_table="test_employee_data"
        )
        
        assert result['status'] == 'success'
        assert 'execution_time_seconds' in result
        assert result['input_rows'] == 3
        assert result['output_rows'] >= 3
        
        # Vérifier que la table a été créée
        verification_df = pd.read_sql('SELECT * FROM test_employee_data', pipeline.engine)
        assert len(verification_df) >= 3

class TestETLValidation:
    """Tests de validation des données ETL."""
    
    def test_validate_data_quality(self):
        """Test validation qualité des données."""
        from src.utils.data_processing import validate_data_quality
        
        # Données de bonne qualité
        good_data = pd.DataFrame({
            'col1': [1, 2, 3, 4, 5],
            'col2': ['A', 'B', 'C', 'D', 'E']
        })
        
        quality_report = validate_data_quality(good_data)
        
        assert quality_report['missing_values_pct'] == 0
        assert quality_report['duplicate_rows'] == 0
        assert quality_report['data_quality_score'] >= 90
    
    def test_validate_transformed_data_valid(self):
        """Test validation données transformées valides."""
        pipeline = UbisoftETLPipeline(
            ETLConfig(
                database_url="sqlite:///test.db",
                raw_data_path=Path("test"),
                processed_data_path=Path("test")
            )
        )
        
        valid_data = pd.DataFrame({
            'employee_id': ['E001', 'E002', 'E003'],
            'creative_score': [85, 72, 91],
            'burnout_scale': [3, 6, 2]
        })
        
        # Ne devrait pas lever d'exception
        pipeline._validate_transformed_data(valid_data)
    
    def test_validate_transformed_data_invalid(self):
        """Test validation données transformées invalides."""
        pipeline = UbisoftETLPipeline(
            ETLConfig(
                database_url="sqlite:///test.db",
                raw_data_path=Path("test"),
                processed_data_path=Path("test")
            )
        )
        
        # Données avec valeurs hors range
        invalid_data = pd.DataFrame({
            'employee_id': ['E001', 'E002'],
            'creative_score': [150, -10],  # Hors range [0, 100]
            'burnout_scale': [15, 0]       # Hors range [1, 10]
        })
        
        with pytest.raises(ValueError):
            pipeline._validate_transformed_data(invalid_data)

class TestETLErrors:
    """Tests de gestion d'erreurs ETL."""
    
    def test_extract_csv_file_not_found(self):
        """Test extraction avec fichier inexistant."""
        config = ETLConfig(
            database_url="sqlite:///test.db",
            raw_data_path=Path("nonexistent"),
            processed_data_path=Path("test")
        )
        
        pipeline = UbisoftETLPipeline(config)
        
        with pytest.raises(FileNotFoundError):
            pipeline.extract_from_csv("nonexistent_file.csv")
    
    def test_extract_database_connection_error(self):
        """Test extraction avec erreur de connexion DB."""
        config = ETLConfig(
            database_url="invalid://connection",
            raw_data_path=Path("test"),
            processed_data_path=Path("test")
        )
        
        with pytest.raises(Exception):  # Erreur de connexion
            pipeline = UbisoftETLPipeline(config)

@pytest.fixture
def pipeline_with_logs():
    """Pipeline avec logs d'exécution."""
    config = ETLConfig(
        database_url="sqlite:///test.db",
        raw_data_path=Path("test"),
        processed_data_path=Path("test")
    )
    
    pipeline = UbisoftETLPipeline(config)
    
    # Simuler quelques logs
    pipeline._log_step("test_step", "success", {"rows": 100})
    pipeline._log_step("another_step", "error", {"error": "Test error"})
    
    return pipeline

def test_get_pipeline_status(pipeline_with_logs):
    """Test récupération du statut du pipeline."""
    status = pipeline_with_logs.get_pipeline_status()
    
    assert status['total_steps'] == 2
    assert status['successful_steps'] == 1
    assert status['failed_steps'] == 1
    assert status['last_execution']['step'] == 'another_step'

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
