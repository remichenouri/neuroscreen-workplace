"""
Tests pour les utilitaires.
"""

import pytest
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from unittest.mock import patch, MagicMock
import tempfile
from pathlib import Path

from src.utils.data_processing import DataProcessor, validate_data_quality, create_data_profile
from src.utils.metrics import ModelMetrics, BusinessMetrics, DiversityMetrics, calculate_model_drift
from src.utils.visualization import AnalyticsVisualizer

class TestDataProcessingUtils:
    """Tests pour les utilitaires de traitement des données."""
    
    @pytest.fixture
    def sample_data(self):
        """Données d'exemple pour les tests."""
        return pd.DataFrame({
            'employee_id': ['E001', 'E002', 'E003', 'E004'],
            'creative_score': [85.5, 72.0, 91.2, 66.8],
            'burnout_scale': [3, 6, 2, 8],
            'department': ['Design', 'Dev', 'QA', 'Design'],
            'missing_column': [1.0, None, 3.0, None]
        })
    
    def test_validate_data_quality(self, sample_data):
        """Test validation de la qualité des données."""
        quality_report = validate_data_quality(sample_data)
        
        # Vérifier les clés du rapport
        expected_keys = [
            'total_rows', 'total_columns', 'missing_values_pct',
            'duplicate_rows', 'duplicate_rows_pct', 'numeric_columns',
            'categorical_columns', 'memory_usage_mb', 'data_quality_score'
        ]
        
        for key in expected_keys:
            assert key in quality_report
        
        # Vérifier les valeurs
        assert quality_report['total_rows'] == 4
        assert quality_report['total_columns'] == 5
        assert quality_report['missing_values_pct'] > 0  # Il y a des valeurs manquantes
        assert quality_report['data_quality_score'] >= 0
        assert quality_report['data_quality_score'] <= 100
    
    def test_create_data_profile(self, sample_data):
        """Test création du profil de données."""
        profile_df = create_data_profile(sample_data)
        
        # Vérifier la structure
        assert len(profile_df) == 5  # 5 colonnes
        assert 'column' in profile_df.columns
        assert 'dtype' in profile_df.columns
        assert 'non_null_count' in profile_df.columns
        assert 'null_count' in profile_df.columns
        assert 'unique_count' in profile_df.columns
        
        # Vérifier les données numériques
        creative_score_row = profile_df[profile_df['column'] == 'creative_score'].iloc[0]
        assert 'mean' in creative_score_row
        assert 'std' in creative_score_row
        
        # Vérifier les données catégorielles
        dept_row = profile_df[profile_df['column'] == 'department'].iloc[0]
        assert 'most_frequent' in dept_row

class TestMetricsUtils:
    """Tests pour les utilitaires de métriques."""
    
    @pytest.fixture
    def classification_data(self):
        """Données de classification pour les tests."""
        y_true = np.array([0, 1, 0, 1, 0, 1, 1, 0])
        y_pred = np.array([0, 1, 0, 1, 1, 1, 1, 0])
        y_prob = np.array([0.1, 0.9, 0.2, 0.8, 0.6, 0.7, 0.9, 0.3])
        
        return y_true, y_pred, y_prob
    
    def test_compute_classification_metrics(self, classification_data):
        """Test calcul des métriques de classification."""
        y_true, y_pred, y_prob = classification_data
        
        metrics = ModelMetrics.compute_classification_metrics(y_true, y_pred, y_prob)
        
        # Vérifier les métriques de base
        assert 'accuracy' in metrics
        assert 'precision' in metrics
        assert 'recall' in metrics
        assert 'f1_score' in metrics
        assert 'roc_auc' in metrics
        
        # Vérifier les ranges
        for metric_name, value in metrics.items():
            assert 0 <= value <= 1, f"{metric_name} hors range: {value}"
    
    def test_compute_confusion_matrix_metrics(self, classification_data):
        """Test métriques de matrice de confusion."""
        y_true, y_pred, _ = classification_data
        
        cm_metrics = ModelMetrics.compute_confusion_matrix_metrics(y_true, y_pred)
        
        # Vérifier les métriques binaires
        expected_keys = [
            'true_positives', 'true_negatives', 'false_positives', 'false_negatives',
            'sensitivity', 'specificity', 'positive_predictive_value'
        ]
        
        for key in expected_keys:
            assert key in cm_metrics
        
        # Vérifier la cohérence
        tp, tn, fp, fn = cm_metrics['true_positives'], cm_metrics['true_negatives'], \
                        cm_metrics['false_positives'], cm_metrics['false_negatives']
        
        assert tp + tn + fp + fn == len(y_true)
    
    def test_calculate_roi_metrics(self):
        """Test calcul des métriques ROI."""
        baseline_costs = {
            'recruitment': 100000,
            'training': 50000,
            'productivity_loss': 80000
        }
        
        improved_costs = {
            'recruitment': 70000,
            'training': 40000,
            'productivity_loss': 60000
        }
        
        roi_metrics = BusinessMetrics.calculate_roi_metrics(
            baseline_costs, improved_costs, implementation_cost=30000
        )
        
        # Vérifier les métriques ROI
        assert 'total_baseline_cost' in roi_metrics
        assert 'total_improved_cost' in roi_metrics
        assert 'annual_savings' in roi_metrics
        assert 'roi_percentage' in roi_metrics
        assert 'payback_period_months' in roi_metrics
        
        # Vérifier la logique
        assert roi_metrics['total_baseline_cost'] > roi_metrics['total_improved_cost']
        assert roi_metrics['annual_savings'] > 0
    
    def test_calculate_hr_kpis(self):
        """Test calcul des KPI RH."""
        from datetime import datetime, timedelta
        
        # Données RH simulées
        hr_data = pd.DataFrame({
            'employee_id': ['E001', 'E002', 'E003', 'E004'],
            'date': [datetime.now() - timedelta(days=i) for i in range(4)],
            'creative_score': [85, 72, 91, 66],
            'burnout_scale': [3, 6, 2, 8],
            'adhd_risk': [0, 1, 0, 1],
            'status': ['active', 'active', 'active', 'inactive']
        })
        
        period_start = datetime.now() - timedelta(days=30)
        period_end = datetime.now()
        
        kpis = BusinessMetrics.calculate_hr_kpis(hr_data, period_start, period_end)
        
        # Vérifier les KPI
        assert 'total_employees' in kpis
        assert 'neurodivergent_percentage' in kpis
        assert 'average_creative_score' in kpis
        assert 'average_burnout_level' in kpis
        
        assert kpis['total_employees'] > 0
        assert 0 <= kpis['neurodivergent_percentage'] <= 100
    
    def test_calculate_inclusion_index(self):
        """Test calcul de l'index d'inclusion."""
        employee_data = pd.DataFrame({
            'employee_id': ['E001', 'E002', 'E003', 'E004'],
            'adhd_risk': [0, 1, 0, 1],
            'creative_score': [85, 80, 75, 82]
        })
        
        inclusion_index = DiversityMetrics.calculate_inclusion_index(employee_data)
        
        # Vérifier les composantes
        expected_components = [
            'representation_score', 'accommodation_score',
            'performance_parity_score', 'retention_score',
            'overall_inclusion_index'
        ]
        
        for component in expected_components:
            assert component in inclusion_index
            assert 0 <= inclusion_index[component] <= 100

class TestModelDrift:
    """Tests pour la détection de dérive des modèles."""
    
    def test_calculate_model_drift_no_drift(self):
        """Test détection sans dérive."""
        baseline_metrics = {
            'accuracy': 0.85,
            'f1_score': 0.82,
            'precision': 0.80
        }
        
        current_metrics = {
            'accuracy': 0.86,
            'f1_score': 0.83,
            'precision': 0.81
        }
        
        drift_analysis = calculate_model_drift(baseline_metrics, current_metrics)
        
        assert drift_analysis['has_drift'] is False
        assert drift_analysis['severity'] == 'none'
        assert len(drift_analysis['affected_metrics']) == 0
    
    def test_calculate_model_drift_with_drift(self):
        """Test détection avec dérive significative."""
        baseline_metrics = {
            'accuracy': 0.85,
            'f1_score': 0.82
        }
        
        current_metrics = {
            'accuracy': 0.70,  # Baisse significative
            'f1_score': 0.65   # Baisse significative
        }
        
        drift_analysis = calculate_model_drift(
            baseline_metrics, current_metrics, threshold=0.05
        )
        
        assert drift_analysis['has_drift'] is True
        assert drift_analysis['severity'] in ['moderate', 'high', 'critical']
        assert len(drift_analysis['affected_metrics']) > 0

class TestVisualizationUtils:
    """Tests pour les utilitaires de visualisation."""
    
    @pytest.fixture
    def sample_viz_data(self):
        """Données pour les visualisations."""
        return pd.DataFrame({
            'employee_id': [f'E{i:03d}' for i in range(1, 101)],
            'creative_score': np.random.normal(75, 15, 100),
            'burnout_scale': np.random.randint(1, 11, 100),
            'adhd_risk': np.random.choice([0, 1], 100, p=[0.7, 0.3]),
            'autism_risk': np.random.choice([0, 1], 100, p=[0.9, 0.1]),
            'department': np.random.choice(['Design', 'Dev', 'QA', 'Marketing'], 100)
        })
    
    def test_analytics_visualizer_init(self):
        """Test initialisation du visualizer."""
        viz = AnalyticsVisualizer(theme='ubisoft')
        
        assert viz.theme == 'ubisoft'
        assert isinstance(viz.color_palette, dict)
        assert 'primary' in viz.color_palette
    
    def test_plot_employee_distribution(self, sample_viz_data):
        """Test graphique de distribution des employés."""
        viz = AnalyticsVisualizer()
        
        fig = viz.plot_employee_distribution(sample_viz_data)
        
        # Vérifier que la figure est créée
        assert fig is not None
        assert hasattr(fig, 'data')
        
        # Vérifier le nombre de traces (4 sous-graphiques)
        assert len(fig.data) >= 4
    
    def test_plot_correlation_heatmap(self, sample_viz_data):
        """Test heatmap des corrélations."""
        viz = AnalyticsVisualizer()
        
        fig = viz.plot_correlation_heatmap(sample_viz_data)
        
        assert fig is not None
        assert len(fig.data) == 1  # Une seule trace heatmap
    
    def test_plot_performance_metrics(self):
        """Test graphique radar des métriques."""
        viz = AnalyticsVisualizer()
        
        metrics = {
            'accuracy': 0.85,
            'precision': 0.82,
            'recall': 0.88,
            'f1_score': 0.85,
            'roc_auc': 0.92
        }
        
        fig = viz.plot_performance_metrics(metrics)
        
        assert fig is not None
        assert len(fig.data) == 1  # Une trace radar
    
    @patch('matplotlib.pyplot.savefig')
    @patch('matplotlib.pyplot.close')
    def test_create_matplotlib_report(self, mock_close, mock_savefig, sample_viz_data):
        """Test création de rapport matplotlib."""
        from src.utils.visualization import create_matplotlib_report
        
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "test_report.png"
            
            result_path = create_matplotlib_report(sample_viz_data, str(output_path))
            
            assert result_path == str(output_path)
            mock_savefig.assert_called_once()
            mock_close.assert_called_once()

class TestUtilsIntegration:
    """Tests d'intégration des utilitaires."""
    
    def test_data_processing_pipeline(self):
        """Test pipeline complet de traitement des données."""
        # Données brutes
        raw_data = pd.DataFrame({
            'employee_id': ['E001', 'E002', 'E003', 'E001'],  # Avec doublon
            'creative_score': [85, None, 91, 85],  # Avec valeur manquante
            'burnout_scale': [3, 6, 2, 3],
            'department': [' Design ', 'dev', 'QA', ' Design '],  # Inconsistant
            'hire_date': ['2020-01-15', '2021-03-10', '2019-11-20', '2020-01-15']
        })
        
        processor = DataProcessor()
        
        # Pipeline complet
        X, y = processor.prepare_ml_dataset(raw_data, 'burnout_scale')
        
        # Vérifications
        assert len(X) == 3  # Doublons supprimés
        assert X.isnull().sum().sum() == 0  # Pas de valeurs manquantes
        assert 'creativity_burnout_ratio' in X.columns  # Features créées
        assert 'department_encoded' in X.columns  # Variables encodées
    
    def test_metrics_and_visualization_integration(self):
        """Test intégration métriques et visualisation."""
        # Données de test
        y_true = np.random.choice([0, 1], 100)
        y_pred = np.random.choice([0, 1], 100)
        y_prob = np.random.uniform(0, 1, 100)
        
        # Calculer les métriques
        metrics = ModelMetrics.compute_classification_metrics(y_true, y_pred, y_prob)
        
        # Créer la visualisation
        viz = AnalyticsVisualizer()
        fig = viz.plot_performance_metrics(metrics)
        
        # Vérifier l'intégration
        assert fig is not None
        assert len(fig.data) > 0

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
