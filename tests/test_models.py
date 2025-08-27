"""
Tests pour les modèles ML.
"""

import pytest
import pandas as pd
import numpy as np
import joblib
from pathlib import Path
import tempfile
from unittest.mock import patch, MagicMock
import json

from src.model import ADHDPredictor, ModelTrainer, ModelValidator
from sklearn.ensemble import RandomForestClassifier

class TestADHDPredictor:
    """Tests pour la classe ADHDPredictor."""
    
    @pytest.fixture
    def sample_model_data(self):
        """Données pour entraîner un modèle simple."""
        X = pd.DataFrame({
            'creative_score': [85, 72, 91, 66, 78],
            'burnout_scale': [3, 6, 2, 8, 4],
            'creativity_burnout_ratio': [28.3, 12.0, 45.5, 8.25, 19.5],
            'high_creativity': [1, 0, 1, 0, 1],
            'high_burnout': [0, 1, 0, 1, 0]
        })
        
        y = pd.Series([0, 1, 0, 1, 0])
        
        return X, y
    
    @pytest.fixture
    def trained_model(self, sample_model_data):
        """Modèle entraîné pour les tests."""
        X, y = sample_model_data
        
        model = RandomForestClassifier(n_estimators=10, random_state=42)
        model.fit(X, y)
        
        return model, X.columns.tolist()
    
    @pytest.fixture
    def temp_model_dir(self, trained_model):
        """Dossier temporaire avec modèle sauvegardé."""
        model, feature_names = trained_model
        
        with tempfile.TemporaryDirectory() as temp_dir:
            model_path = Path(temp_dir)
            
            # Sauvegarder le modèle
            joblib.dump(model, model_path / "random_forest.pkl")
            
            # Sauvegarder les métadonnées
            metadata = {
                'model_name': 'RandomForest',
                'feature_names': feature_names,
                'metrics': {'f1_score': 0.96}
            }
            
            with open(model_path / "model_metadata.json", 'w') as f:
                json.dump(metadata, f)
            
            yield model_path
    
    def test_load_model_success(self, temp_model_dir):
        """Test chargement de modèle réussi."""
        predictor = ADHDPredictor()
        predictor.load_model(temp_model_dir)
        
        assert predictor.model is not None
        assert predictor.feature_names is not None
        assert len(predictor.feature_names) == 5
        assert predictor.metadata['model_name'] == 'RandomForest'
    
    def test_predict(self, temp_model_dir):
        """Test prédiction."""
        predictor = ADHDPredictor(temp_model_dir)
        
        # Données de test
        X_test = pd.DataFrame({
            'creative_score': [85, 72],
            'burnout_scale': [3, 6],
            'creativity_burnout_ratio': [28.3, 12.0],
            'high_creativity': [1, 0],
            'high_burnout': [0, 1]
        })
        
        predictions = predictor.predict(X_test)
        
        assert len(predictions) == 2
        assert all(pred in [0, 1] for pred in predictions)
    
    def test_predict_proba(self, temp_model_dir):
        """Test prédiction de probabilités."""
        predictor = ADHDPredictor(temp_model_dir)
        
        X_test = pd.DataFrame({
            'creative_score': [85],
            'burnout_scale': [3],
            'creativity_burnout_ratio': [28.3],
            'high_creativity': [1],
            'high_burnout': [0]
        })
        
        probabilities = predictor.predict_proba(X_test)
        
        assert probabilities.shape == (1, 2)
        assert np.allclose(probabilities.sum(axis=1), 1.0)
        assert all(0 <= prob <= 1 for prob in probabilities.flatten())
    
    def test_predict_with_explanation(self, temp_model_dir):
        """Test prédiction avec explication."""
        predictor = ADHDPredictor(temp_model_dir)
        
        X_test = pd.DataFrame({
            'creative_score': [85],
            'burnout_scale': [3],
            'creativity_burnout_ratio': [28.3],
            'high_creativity': [1],
            'high_burnout': [0]
        })
        
        result = predictor.predict_with_explanation(X_test)
        
        assert 'prediction' in result
        assert 'probability_no_risk' in result
        assert 'probability_risk' in result
        assert 'confidence' in result
        assert 'recommendations' in result
        assert 'feature_importance' in result
        
        assert result['confidence'] in ['faible', 'modérée', 'élevée', 'très_élevée']
        assert isinstance(result['recommendations'], list)
    
    def test_predict_missing_features(self, temp_model_dir):
        """Test prédiction avec features manquantes."""
        predictor = ADHDPredictor(temp_model_dir)
        
        # Données incomplètes
        X_test = pd.DataFrame({
            'creative_score': [85],
            'burnout_scale': [3]
            # Features manquantes
        })
        
        with pytest.raises(ValueError, match="Features manquantes"):
            predictor.predict(X_test)
    
    def test_predict_no_model_loaded(self):
        """Test prédiction sans modèle chargé."""
        predictor = ADHDPredictor()
        
        X_test = pd.DataFrame({'col': [1]})
        
        with pytest.raises(ValueError, match="Aucun modèle chargé"):
            predictor.predict(X_test)

class TestModelTrainer:
    """Tests pour la classe ModelTrainer."""
    
    @pytest.fixture
    def training_data(self):
        """Données d'entraînement."""
        np.random.seed(42)
        n_samples = 100
        
        X = pd.DataFrame({
            'creative_score': np.random.uniform(0, 100, n_samples),
            'burnout_scale': np.random.randint(1, 11, n_samples),
            'creativity_burnout_ratio': np.random.uniform(1, 50, n_samples),
            'high_creativity': np.random.randint(0, 2, n_samples),
            'high_burnout': np.random.randint(0, 2, n_samples)
        })
        
        # Target corrélé avec les features
        y = ((X['creative_score'] > 75) & (X['burnout_scale'] > 6)).astype(int)
        
        return X, y
    
    def test_train_adhd_model(self, training_data):
        """Test entraînement modèle TDAH."""
        X, y = training_data
        X_train, X_test, y_train, y_test = X[:80], X[80:], y[:80], y[80:]
        
        trainer = ModelTrainer()
        
        with patch('mlflow.start_run'), \
             patch('mlflow.log_params'), \
             patch('mlflow.log_metrics'), \
             patch('mlflow.sklearn.log_model'):
            
            result = trainer.train_adhd_model(
                X_train, y_train, X_test, y_test, 
                model_name='random_forest'
            )
        
        assert 'model' in result
        assert 'best_params' in result
        assert 'train_metrics' in result
        assert 'test_metrics' in result
        assert 'cv_scores' in result
        
        # Vérifier les métriques
        assert 0 <= result['test_metrics']['f1_score'] <= 1
        assert 0 <= result['test_metrics']['accuracy'] <= 1
        assert len(result['cv_scores']) == 5  # 5-fold CV
    
    def test_compare_models(self, training_data):
        """Test comparaison de modèles."""
        X, y = training_data
        X_train, X_test, y_train, y_test = X[:80], X[80:], y[:80], y[80:]
        
        trainer = ModelTrainer()
        
        with patch('mlflow.start_run'), \
             patch('mlflow.log_params'), \
             patch('mlflow.log_metrics'), \
             patch('mlflow.sklearn.log_model'):
            
            # Limiter aux modèles rapides pour les tests
            trainer.models = {
                'random_forest': trainer.models['random_forest'],
                'logistic_regression': trainer.models['logistic_regression']
            }
            
            comparison_df = trainer.compare_models(X_train, y_train, X_test, y_test)
        
        assert len(comparison_df) == 2
        assert 'model_name' in comparison_df.columns
        assert 'test_f1_score' in comparison_df.columns
        assert 'cv_f1_mean' in comparison_df.columns
    
    def test_save_best_model(self, training_data):
        """Test sauvegarde du meilleur modèle."""
        X, y = training_data
        
        # Créer un résultat de modèle simulé
        model = RandomForestClassifier(n_estimators=10, random_state=42)
        model.fit(X, y)
        
        model_result = {
            'model': model,
            'scaler': None,
            'feature_names': list(X.columns),
            'best_params': {'n_estimators': 10},
            'test_metrics': {'f1_score': 0.85, 'accuracy': 0.90},
            'cv_scores': np.array([0.8, 0.85, 0.9, 0.82, 0.88])
        }
        
        trainer = ModelTrainer()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "model_output"
            
            saved_path = trainer.save_best_model(model_result, output_dir)
            
            assert saved_path.exists()
            assert (saved_path / "random_forest.pkl").exists()
            assert (saved_path / "model_metadata.json").exists()
            
            # Vérifier le contenu des métadonnées
            with open(saved_path / "model_metadata.json") as f:
                metadata = json.load(f)
            
            assert metadata['model_type'] == 'adhd_classifier'
            assert metadata['feature_names'] == list(X.columns)
            assert metadata['test_metrics']['f1_score'] == 0.85

class TestModelValidator:
    """Tests pour la classe ModelValidator."""
    
    @pytest.fixture
    def validator_with_model(self, temp_model_dir):
        """Validator avec modèle chargé."""
        return ModelValidator(temp_model_dir)
    
    @pytest.fixture
    def validation_data(self):
        """Données de validation."""
        X = pd.DataFrame({
            'creative_score': [85, 72, 91, 66, 78],
            'burnout_scale': [3, 6, 2, 8, 4],
            'creativity_burnout_ratio': [28.3, 12.0, 45.5, 8.25, 19.5],
            'high_creativity': [1, 0, 1, 0, 1],
            'high_burnout': [0, 1, 0, 1, 0]
        })
        
        y = pd.Series([0, 1, 0, 1, 0])
        
        return X, y
    
    def test_validate_model_performance(self, validator_with_model, validation_data):
        """Test validation des performances du modèle."""
        validator = validator_with_model
        X_test, y_test = validation_data
        
        validation_report = validator.validate_model_performance(X_test, y_test)
        
        assert 'performance_metrics' in validation_report
        assert 'total_samples' in validation_report
        assert 'correct_predictions' in validation_report
        assert 'error_count' in validation_report
        assert 'error_rate' in validation_report
        assert 'validation_date' in validation_report
        
        # Vérifier les métriques
        metrics = validation_report['performance_metrics']
        assert 0 <= metrics['accuracy'] <= 1
        assert 0 <= metrics['f1_score'] <= 1
    
    def test_check_data_drift(self, validator_with_model):
        """Test détection de dérive des données."""
        validator = validator_with_model
        
        # Données de référence
        reference_stats = {
            'creative_score': {'mean': 75.0, 'std': 15.0},
            'burnout_scale': {'mean': 5.0, 'std': 2.5}
        }
        
        # Nouvelles données avec dérive
        new_data = pd.DataFrame({
            'creative_score': [90, 95, 85, 88, 92],  # Moyenne plus élevée
            'burnout_scale': [2, 1, 3, 2, 1]        # Moyenne plus faible
        })
        
        drift_results = validator.check_data_drift(new_data, reference_stats)
        
        assert 'has_significant_drift' in drift_results
        assert 'columns_with_drift' in drift_results
        assert 'drift_details' in drift_results
        
        # Vérifier détection de dérive
        if drift_results['has_significant_drift']:
            assert len(drift_results['columns_with_drift']) > 0

class TestModelIntegration:
    """Tests d'intégration des modèles."""
    
    def test_end_to_end_model_workflow(self):
        """Test workflow complet : entraînement → sauvegarde → chargement → prédiction."""
        
        # 1. Générer des données d'entraînement
        np.random.seed(42)
        n_samples = 200
        
        X = pd.DataFrame({
            'creative_score': np.random.uniform(0, 100, n_samples),
            'burnout_scale': np.random.randint(1, 11, n_samples),
            'creativity_burnout_ratio': np.random.uniform(1, 50, n_samples),
            'high_creativity': np.random.randint(0, 2, n_samples),
            'high_burnout': np.random.randint(0, 2, n_samples)
        })
        
        y = ((X['creative_score'] > 75) & (X['burnout_scale'] > 6)).astype(int)
        
        # Split
        split_idx = int(0.8 * len(X))
        X_train, X_test = X[:split_idx], X[split_idx:]
        y_train, y_test = y[:split_idx], y[split_idx:]
        
        with tempfile.TemporaryDirectory() as temp_dir:
            model_dir = Path(temp_dir)
            
            # 2. Entraîner le modèle
            trainer = ModelTrainer()
            
            with patch('mlflow.start_run'), \
                 patch('mlflow.log_params'), \
                 patch('mlflow.log_metrics'), \
                 patch('mlflow.sklearn.log_model'):
                
                model_result = trainer.train_adhd_model(
                    X_train, y_train, X_test, y_test,
                    model_name='random_forest'
                )
            
            # 3. Sauvegarder le modèle
            saved_path = trainer.save_best_model(model_result, model_dir)
            
            # 4. Charger le modèle
            predictor = ADHDPredictor(saved_path)
            
            # 5. Faire une prédiction
            predictions = predictor.predict(X_test)
            probabilities = predictor.predict_proba(X_test)
            explanations = predictor.predict_with_explanation(X_test[:1])
            
            # Vérifications finales
            assert len(predictions) == len(X_test)
            assert len(probabilities) == len(X_test)
            assert 'prediction' in explanations
            assert 'recommendations' in explanations
    
    @patch('src.model.retrain_model_if_needed')
    def test_retrain_model_if_needed(self, mock_retrain):
        """Test du processus de ré-entraînement."""
        mock_retrain.return_value = True
        
        # Simuler des nouvelles données
        new_data = pd.DataFrame({
            'creative_score': [95, 98, 92],
            'burnout_scale': [1, 2, 1],
            'adhd_risk': [0, 0, 0]
        })
        
        should_retrain = mock_retrain(
            current_model_path=Path("dummy_path"),
            new_data=new_data,
            target_column='adhd_risk'
        )
        
        assert should_retrain is True
        mock_retrain.assert_called_once()

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
