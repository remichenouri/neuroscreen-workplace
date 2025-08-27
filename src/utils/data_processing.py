"""
Utilitaires de traitement des données pour Ubisoft People Analytics.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional, Union
from sklearn.preprocessing import StandardScaler, LabelEncoder, MinMaxScaler
from sklearn.impute import SimpleImputer, KNNImputer
import logging

logger = logging.getLogger(__name__)

class DataProcessor:
    """Classe principale pour le traitement des données."""
    
    def __init__(self):
        self.scalers = {}
        self.encoders = {}
        self.imputers = {}
        
    def clean_employee_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Nettoyer les données d'employés."""
        df_clean = df.copy()
        
        # Supprimer les doublons
        initial_rows = len(df_clean)
        df_clean = df_clean.drop_duplicates(subset=['employee_id'])
        if len(df_clean) < initial_rows:
            logger.info(f"Supprimé {initial_rows - len(df_clean)} doublons")
        
        # Valider les ranges
        if 'creative_score' in df_clean.columns:
            df_clean['creative_score'] = df_clean['creative_score'].clip(0, 100)
        
        if 'burnout_scale' in df_clean.columns:
            df_clean['burnout_scale'] = df_clean['burnout_scale'].clip(1, 10)
        
        # Nettoyer les chaînes de caractères
        string_cols = df_clean.select_dtypes(include=['object']).columns
        for col in string_cols:
            if col != 'employee_id':
                df_clean[col] = df_clean[col].str.strip().str.lower()
        
        return df_clean
    
    def handle_missing_values(self, df: pd.DataFrame, strategy: str = 'auto') -> pd.DataFrame:
        """Gérer les valeurs manquantes."""
        df_imputed = df.copy()
        
        # Séparer les colonnes numériques et catégorielles
        numeric_cols = df_imputed.select_dtypes(include=[np.number]).columns
        categorical_cols = df_imputed.select_dtypes(include=['object']).columns
        
        # Imputation numérique
        if len(numeric_cols) > 0:
            if strategy == 'auto':
                # KNN pour les petits datasets, median pour les gros
                if len(df_imputed) < 1000:
                    imputer = KNNImputer(n_neighbors=5)
                    imputer_name = 'knn_numeric'
                else:
                    imputer = SimpleImputer(strategy='median')
                    imputer_name = 'median_numeric'
            else:
                imputer = SimpleImputer(strategy=strategy)
                imputer_name = f'{strategy}_numeric'
            
            df_imputed[numeric_cols] = imputer.fit_transform(df_imputed[numeric_cols])
            self.imputers[imputer_name] = imputer
        
        # Imputation catégorielle
        if len(categorical_cols) > 0:
            imputer = SimpleImputer(strategy='most_frequent')
            df_imputed[categorical_cols] = imputer.fit_transform(df_imputed[categorical_cols])
            self.imputers['mode_categorical'] = imputer
        
        return df_imputed
    
    def engineer_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Créer des features dérivées."""
        df_features = df.copy()
        
        # Features de ratio
        if 'creative_score' in df_features.columns and 'burnout_scale' in df_features.columns:
            df_features['creativity_burnout_ratio'] = (
                df_features['creative_score'] / (df_features['burnout_scale'] + 1)
            )
        
        # Features binaires basées sur quantiles
        numeric_cols = ['creative_score', 'burnout_scale']
        for col in numeric_cols:
            if col in df_features.columns:
                q75 = df_features[col].quantile(0.75)
                q25 = df_features[col].quantile(0.25)
                df_features[f'{col}_high'] = (df_features[col] > q75).astype(int)
                df_features[f'{col}_low'] = (df_features[col] < q25).astype(int)
        
        # Features d'interaction
        if 'department' in df_features.columns and 'creative_score' in df_features.columns:
            dept_creativity = df_features.groupby('department')['creative_score'].transform('mean')
            df_features['creativity_vs_dept_avg'] = (
                df_features['creative_score'] - dept_creativity
            )
        
        # Features temporelles (si date disponible)
        if 'hire_date' in df_features.columns:
            df_features['hire_date'] = pd.to_datetime(df_features['hire_date'])
            df_features['tenure_years'] = (
                (pd.Timestamp.now() - df_features['hire_date']).dt.days / 365.25
            )
            df_features['hire_month'] = df_features['hire_date'].dt.month
            df_features['hire_quarter'] = df_features['hire_date'].dt.quarter
        
        return df_features
    
    def encode_categorical_variables(self, df: pd.DataFrame, 
                                   method: str = 'label') -> pd.DataFrame:
        """Encoder les variables catégorielles."""
        df_encoded = df.copy()
        categorical_cols = df_encoded.select_dtypes(include=['object']).columns
        
        for col in categorical_cols:
            if col == 'employee_id':  # Garder l'ID original
                continue
                
            if method == 'label':
                encoder = LabelEncoder()
                df_encoded[f'{col}_encoded'] = encoder.fit_transform(df_encoded[col])
                self.encoders[col] = encoder
            elif method == 'onehot':
                # One-hot encoding avec limitation des catégories
                top_categories = df_encoded[col].value_counts().head(10).index
                for category in top_categories:
                    df_encoded[f'{col}_{category}'] = (df_encoded[col] == category).astype(int)
        
        return df_encoded
    
    def scale_numerical_features(self, df: pd.DataFrame, 
                                method: str = 'standard') -> pd.DataFrame:
        """Normaliser les features numériques."""
        df_scaled = df.copy()
        
        # Identifier les colonnes à scaler (exclure les binaires et l'ID)
        numeric_cols = df_scaled.select_dtypes(include=[np.number]).columns
        binary_cols = [col for col in numeric_cols if df_scaled[col].nunique() == 2]
        cols_to_scale = [col for col in numeric_cols if col not in binary_cols and 
                        not col.endswith('_risk') and col != 'employee_id']
        
        if len(cols_to_scale) > 0:
            if method == 'standard':
                scaler = StandardScaler()
            elif method == 'minmax':
                scaler = MinMaxScaler()
            else:
                raise ValueError(f"Méthode de scaling non supportée: {method}")
            
            df_scaled[cols_to_scale] = scaler.fit_transform(df_scaled[cols_to_scale])
            self.scalers[method] = scaler
        
        return df_scaled
    
    def detect_outliers(self, df: pd.DataFrame, 
                       method: str = 'iqr') -> Dict[str, List]:
        """Détecter les outliers."""
        outliers = {}
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            if method == 'iqr':
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                outlier_mask = (df[col] < lower_bound) | (df[col] > upper_bound)
            
            elif method == 'zscore':
                z_scores = np.abs((df[col] - df[col].mean()) / df[col].std())
                outlier_mask = z_scores > 3
            
            outlier_indices = df[outlier_mask].index.tolist()
            if outlier_indices:
                outliers[col] = outlier_indices
        
        return outliers
    
    def prepare_ml_dataset(self, df: pd.DataFrame, 
                          target_col: str) -> Tuple[pd.DataFrame, pd.Series]:
        """Préparer le dataset pour le ML."""
        # Pipeline complet
        df_processed = self.clean_employee_data(df)
        df_processed = self.handle_missing_values(df_processed)
        df_processed = self.engineer_features(df_processed)
        df_processed = self.encode_categorical_variables(df_processed)
        
        # Séparer features et target
        feature_cols = [col for col in df_processed.columns 
                       if col not in ['employee_id', target_col]]
        
        X = df_processed[feature_cols]
        y = df_processed[target_col]
        
        # Scaling final
        X = self.scale_numerical_features(X)
        
        logger.info(f"Dataset préparé: {X.shape[0]} échantillons, {X.shape[1]} features")
        
        return X, y

def validate_data_quality(df: pd.DataFrame) -> Dict[str, Union[bool, float, int]]:
    """Valider la qualité des données."""
    quality_report = {
        'total_rows': len(df),
        'total_columns': len(df.columns),
        'missing_values_pct': (df.isnull().sum().sum() / df.size) * 100,
        'duplicate_rows': df.duplicated().sum(),
        'duplicate_rows_pct': (df.duplicated().sum() / len(df)) * 100,
        'numeric_columns': len(df.select_dtypes(include=[np.number]).columns),
        'categorical_columns': len(df.select_dtypes(include=['object']).columns),
        'memory_usage_mb': df.memory_usage(deep=True).sum() / 1024**2,
        'data_quality_score': 0.0
    }
    
    # Calculer un score de qualité
    score = 100
    score -= quality_report['missing_values_pct'] * 2  # -2 points par % manquant
    score -= quality_report['duplicate_rows_pct'] * 3  # -3 points par % dupliqué
    quality_report['data_quality_score'] = max(0, min(100, score))
    
    return quality_report

def create_data_profile(df: pd.DataFrame) -> pd.DataFrame:
    """Créer un profil détaillé des données."""
    profile = []
    
    for col in df.columns:
        col_info = {
            'column': col,
            'dtype': str(df[col].dtype),
            'non_null_count': df[col].count(),
            'null_count': df[col].isnull().sum(),
            'null_percentage': (df[col].isnull().sum() / len(df)) * 100,
            'unique_count': df[col].nunique(),
            'unique_percentage': (df[col].nunique() / len(df)) * 100
        }
        
        if df[col].dtype in ['int64', 'float64']:
            col_info.update({
                'mean': df[col].mean(),
                'median': df[col].median(),
                'std': df[col].std(),
                'min': df[col].min(),
                'max': df[col].max(),
                'skewness': df[col].skew(),
                'kurtosis': df[col].kurtosis()
            })
        else:
            col_info.update({
                'most_frequent': df[col].mode().iloc[0] if not df[col].mode().empty else None,
                'most_frequent_count': df[col].value_counts().iloc[0] if len(df[col].value_counts()) > 0 else 0
            })
        
        profile.append(col_info)
    
    return pd.DataFrame(profile)
