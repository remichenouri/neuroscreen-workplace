"""
Classes et fonctions pour la gestion des modèles ML.
"""

import pandas as pd
import numpy as np
import joblib
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Union, Any
from datetime import datetime
import logging

from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
import mlflow
import mlflow.sklearn

logger = logging.getLogger(__name__)

class ADHDPredictor:
    """Modèle de prédiction du risque TDAH."""
    
    def __init__(self, model_path: Optional[Path] = None):
        self.model = None
        self.scaler = None
        self.feature_names = None
        self.metadata = {}
        
        if model_path and model_path.exists():
            self.load_model(model_path)
    
    def load_model(self, model_path: Path):
        """Charger un modèle pré-entraîné."""
        try:
            self.model = joblib.load(model_path / "random_forest.pkl")
            
            # Charger le scaler si disponible
            scaler_path = model_path / "scaler.pkl"
            if scaler_path.exists():
                self.scaler = joblib.load(scaler_path)
            
            # Charger les métadonnées
            metadata_path = model_path / "model_metadata.json"
            if metadata_path.exists():
                with open(metadata_path, 'r') as f:
                    self.metadata = json.load(f)
                    self.feature_names = self.metadata.get('feature_names', [])
            
            logger.info(f"Modèle chargé depuis {model_path}")
            
        except Exception as e:
            logger.error(f"Erreur chargement modèle: {e}")
            raise
    
    def predict(self, X: Union[pd.DataFrame, np.ndarray]) -> np.ndarray:
        """Prédire le risque TDAH."""
        if self.model is None:
            raise ValueError("Aucun modèle chargé")
        
        # Préprocessing
        X_processed = self._preprocess_input(X)
        
        # Prédiction
        predictions = self.model.predict(X_processed)
        
        return predictions
    
    def predict_proba(self, X: Union[pd.DataFrame, np.ndarray]) -> np.ndarray:
        """Prédire les probabilités."""
        if self.model is None:
            raise ValueError("Aucun modèle chargé")
        
        X_processed = self._preprocess_input(X)
        probabilities = self.model.predict_proba(X_processed)
        
        return probabilities
    
    def predict_with_explanation(self, X: Union[pd.DataFrame, np.ndarray]) -> Dict[str, Any]:
        """Prédiction avec explication."""
        predictions = self.predict(X)
        probabilities = self.predict_proba(X)
        
        # Feature importance pour l'explication
        if hasattr(self.model, 'feature_importances_'):
            feature_importance = dict(zip(
                self.feature_names,
                self.model.feature_importances_
            ))
        else:
            feature_importance = {}
        
        results = []
        for i, (pred, prob) in enumerate(zip(predictions, probabilities)):
            
            # Générer des recommandations
            recommendations = self._generate_recommendations(pred, prob[1] if len(prob) > 1 else prob[0])
            
            result = {
                'prediction': int(pred),
                'probability_no_risk': float(prob[0]) if len(prob) > 1 else float(1 - prob[0]),
                'probability_risk': float(prob[1]) if len(prob) > 1 else float(prob[0]),
                'confidence': self._calculate_confidence(prob),
                'recommendations': recommendations,
                'feature_importance': feature_importance
            }
            
            results.append(result)
        
        return results[0] if len(results) == 1 else results
    
    def _preprocess_input(self, X: Union[pd.DataFrame, np.ndarray]) -> np.ndarray:
        """Préprocesser les données d'entrée."""
        
        if isinstance(X, pd.DataFrame):
            # Vérifier que les features requises sont présentes
            if self.feature_names:
                missing_features = set(self.feature_names) - set(X.columns)
                if missing_features:
                    raise ValueError(f"Features manquantes: {missing_features}")
                
                X = X[self.feature_names]
            
            X_processed = X.values
        else:
            X_processed = X
        
        # Appliquer le scaling si disponible
        if self.scaler:
            X_processed = self.scaler.transform(X_processed)
        
        return X_processed
    
    def _calculate_confidence(self, probabilities: np.ndarray) -> str:
        """Calculer le niveau de confiance."""
        max_prob = np.max(probabilities)
        
        if max_prob >= 0.9:
            return "très_élevée"
        elif max_prob >= 0.8:
            return "élevée"
        elif max_prob >= 0.7:
            return "modérée"
        else:
            return "faible"
    
    def _generate_recommendations(self, prediction: int, risk_probability: float) -> List[str]:
        """Générer des recommandations basées sur la prédiction."""
        
        recommendations = []
        
        if prediction == 1 or risk_probability > 0.5:
            if risk_probability > 0.8:
                recommendations.extend([
                    "Évaluation clinique recommandée",
                    "Aménagements de poste prioritaires",
                    "Suivi rapproché avec les RH"
                ])
            else:
                recommendations.extend([
                    "Surveillance des indicateurs de performance",
                    "Considérer des aménagements préventifs",
                    "Formation des managers sur la neurodiversité"
                ])
            
            # Recommandations spécifiques
            recommendations.extend([
                "Environnement de travail calme",
                "Pauses régulières",
                "Instructions écrites claires",
                "Flexibilité horaires si possible"
            ])
        else:
            recommendations.extend([
                "Maintenir l'environnement actuel",
                "Surveillance périodique",
                "Promouvoir les bonnes pratiques"
            ])
        
        return recommendations

class ModelTrainer:
    """Classe pour l'entraînement des modèles."""
    
    def __init__(self, mlflow_tracking_uri: Optional[str] = None):
        self.models = {
            'random_forest': RandomForestClassifier(random_state=42, class_weight='balanced'),
            'gradient_boosting': GradientBoostingClassifier(random_state=42),
            'logistic_regression': LogisticRegression(random_state=42, class_weight='balanced'),
            'svm': SVC(random_state=42, class_weight='balanced', probability=True)
        }
        
        self.param_grids = {
            'random_forest': {
                'n_estimators': [100, 200, 300],
                'max_depth': [5, 10, 15, None],
                'min_samples_split': [2, 5, 10],
                'min_samples_leaf': [1, 2, 4]
            },
            'gradient_boosting': {
                'n_estimators': [100, 200],
                'learning_rate': [0.05, 0.1, 0.15],
                'max_depth': [3, 5, 7]
            },
            'logistic_regression': {
                'C': [0.1, 1, 10, 100],
                'penalty': ['l1', 'l2'],
                'solver': ['liblinear']
            },
            'svm': {
                'C': [0.1, 1, 10],
                'kernel': ['rbf', 'linear'],
                'gamma': ['scale', 'auto']
            }
        }
        
        if mlflow_tracking_uri:
            mlflow.set_tracking_uri(mlflow_tracking_uri)
    
    def train_adhd_model(self, X_train: pd.DataFrame, y_train: pd.Series,
                        X_test: pd.DataFrame, y_test: pd.Series,
                        model_name: str = 'random_forest') -> Dict[str, Any]:
        """Entraîner un modèle TDAH."""
        
        if model_name not in self.models:
            raise ValueError(f"Modèle non supporté: {model_name}")
        
        logger.info(f"Entraînement du modèle {model_name}")
        
        with mlflow.start_run(run_name=f"{model_name}_adhd"):
            
            # Préparation des données
            scaler = None
            if model_name in ['logistic_regression', 'svm']:
                scaler = StandardScaler()
                X_train_scaled = scaler.fit_transform(X_train)
                X_test_scaled = scaler.transform(X_test)
            else:
                X_train_scaled = X_train
                X_test_scaled = X_test
            
            # Grid Search
            model = self.models[model_name]
            param_grid = self.param_grids[model_name]
            
            grid_search = GridSearchCV(
                model, param_grid, cv=5, scoring='f1',
                n_jobs=-1, verbose=1
            )
            
            grid_search.fit(X_train_scaled, y_train)
            best_model = grid_search.best_estimator_
            
            # Évaluation
            from src.utils.metrics import ModelMetrics
            
            train_pred = best_model.predict(X_train_scaled)
            test_pred = best_model.predict(X_test_scaled)
            test_prob = best_model.predict_proba(X_test_scaled)[:, 1]
            
            train_metrics = ModelMetrics.compute_classification_metrics(y_train, train_pred)
            test_metrics = ModelMetrics.compute_classification_metrics(y_test, test_pred, test_prob)
            
            # Cross-validation
            cv_scores = cross_val_score(best_model, X_train_scaled, y_train, cv=5, scoring='f1')
            
            # Log MLflow
            mlflow.log_params(grid_search.best_params_)
            mlflow.log_metrics({f"train_{k}": v for k, v in train_metrics.items()})
            mlflow.log_metrics({f"test_{k}": v for k, v in test_metrics.items()})
            mlflow.log_metrics({
                'cv_f1_mean': cv_scores.mean(),
                'cv_f1_std': cv_scores.std()
            })
            
            mlflow.sklearn.log_model(best_model, "model")
            if scaler:
                mlflow.sklearn.log_model(scaler, "scaler")
            
            # Résultat
            result = {
                'model': best_model,
                'scaler': scaler,
                'best_params': grid_search.best_params_,
                'train_metrics': train_metrics,
                'test_metrics': test_metrics,
                'cv_scores': cv_scores,
                'feature_names': list(X_train.columns)
            }
            
            logger.info(f"Entraînement terminé - F1 Test: {test_metrics['f1_score']:.3f}")
            
            return result
    
    def compare_models(self, X_train: pd.DataFrame, y_train: pd.Series,
                      X_test: pd.DataFrame, y_test: pd.Series) -> pd.DataFrame:
        """Comparer tous les modèles."""
        
        results = []
        
        for model_name in self.models.keys():
            logger.info(f"Entraînement {model_name}...")
            
            try:
                result = self.train_adhd_model(X_train, y_train, X_test, y_test, model_name)
                
                row = {
                    'model_name': model_name,
                    **{f"train_{k}": v for k, v in result['train_metrics'].items()},
                    **{f"test_{k}": v for k, v in result['test_metrics'].items()},
                    'cv_f1_mean': result['cv_scores'].mean(),
                    'cv_f1_std': result['cv_scores'].std()
                }
                
                results.append(row)
                
            except Exception as e:
                logger.error(f"Erreur entraînement {model_name}: {e}")
        
        comparison_df = pd.DataFrame(results)
        
        # Sauvegarder la comparaison
        comparison_df.to_csv('model_comparison.csv', index=False)
        
        return comparison_df
    
    def save_best_model(self, model_result: Dict[str, Any], 
                       output_dir: Path) -> Path:
        """Sauvegarder le meilleur modèle."""
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Sauvegarder le modèle
        model_path = output_dir / "random_forest.pkl"
        joblib.dump(model_result['model'], model_path)
        
        # Sauvegarder le scaler si présent
        if model_result.get('scaler'):
            scaler_path = output_dir / "scaler.pkl"
            joblib.dump(model_result['scaler'], scaler_path)
        
        # Sauvegarder les métadonnées
        metadata = {
            'model_type': 'adhd_classifier',
            'training_date': datetime.now().isoformat(),
            'feature_names': model_result['feature_names'],
            'best_params': model_result['best_params'],
            'test_metrics': model_result['test_metrics'],
            'cv_scores': {
                'mean': float(model_result['cv_scores'].mean()),
                'std': float(model_result['cv_scores'].std())
            }
        }
        
        metadata_path = output_dir / "model_metadata.json"
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        logger.info(f"Modèle sauvegardé dans {output_dir}")
        
        return output_dir

class ModelValidator:
    """Validation et monitoring des modèles."""
    
    def __init__(self, model_path: Path):
        self.predictor = ADHDPredictor(model_path)
    
    def validate_model_performance(self, test_data: pd.DataFrame,
                                 test_labels: pd.Series) -> Dict[str, Any]:
        """Valider les performances du modèle."""
        
        predictions = self.predictor.predict(test_data)
        probabilities = self.predictor.predict_proba(test_data)
        
        from src.utils.metrics import ModelMetrics
        
        metrics = ModelMetrics.compute_classification_metrics(
            test_labels, predictions, probabilities[:, 1]
        )
        
        # Analyse des erreurs
        errors = test_labels != predictions
        error_indices = test_data[errors].index.tolist()
        
        validation_report = {
            'performance_metrics': metrics,
            'total_samples': len(test_data),
            'correct_predictions': int(np.sum(test_labels == predictions)),
            'error_count': int(np.sum(errors)),
            'error_rate': float(np.mean(errors)),
            'error_indices': error_indices[:10],  # Premiers 10 erreurs
            'validation_date': datetime.now().isoformat()
        }
        
        return validation_report
    
    def check_data_drift(self, new_data: pd.DataFrame,
                        reference_stats: Dict[str, Any]) -> Dict[str, Any]:
        """Détecter la dérive des données."""
        
        drift_results = {}
        
        for column in new_data.select_dtypes(include=[np.number]).columns:
            if column in reference_stats:
                new_mean = new_data[column].mean()
                new_std = new_data[column].std()
                
                ref_mean = reference_stats[column]['mean']
                ref_std = reference_stats[column]['std']
                
                # Calculer la dérive
                mean_drift = abs(new_mean - ref_mean) / ref_mean if ref_mean != 0 else 0
                std_drift = abs(new_std - ref_std) / ref_std if ref_std != 0 else 0
                
                drift_results[column] = {
                    'mean_drift': mean_drift,
                    'std_drift': std_drift,
                    'significant_drift': mean_drift > 0.1 or std_drift > 0.2
                }
        
        overall_drift = {
            'has_significant_drift': any(result['significant_drift'] for result in drift_results.values()),
            'columns_with_drift': [col for col, result in drift_results.items() if result['significant_drift']],
            'drift_details': drift_results,
            'check_date': datetime.now().isoformat()
        }
        
        return overall_drift

def retrain_model_if_needed(current_model_path: Path,
                           new_data: pd.DataFrame,
                           target_column: str,
                           drift_threshold: float = 0.1) -> bool:
    """Ré-entraîner le modèle si nécessaire."""
    
    validator = ModelValidator(current_model_path)
    
    # Charger les stats de référence
    metadata_path = current_model_path / "model_metadata.json"
    if not metadata_path.exists():
        logger.warning("Pas de métadonnées de référence - ré-entraînement recommandé")
        return True
    
    with open(metadata_path, 'r') as f:
        metadata = json.load(f)
    
    reference_stats = metadata.get('reference_stats', {})
    
    if not reference_stats:
        logger.warning("Pas de stats de référence - ré-entraînement recommandé")
        return True
    
    # Vérifier la dérive
    drift_results = validator.check_data_drift(new_data, reference_stats)
    
    if drift_results['has_significant_drift']:
        logger.info(f"Dérive détectée dans: {drift_results['columns_with_drift']}")
        return True
    
    # Vérifier les performances si on a les labels
    if target_column in new_data.columns:
        X_new = new_data.drop(columns=[target_column])
        y_new = new_data[target_column]
        
        validation = validator.validate_model_performance(X_new, y_new)
        
        current_f1 = validation['performance_metrics']['f1_score']
        baseline_f1 = metadata.get('test_metrics', {}).get('f1_score', 0.8)
        
        if current_f1 < baseline_f1 - 0.05:  # Baisse de 5% de F1
            logger.info(f"Performance dégradée: F1 {current_f1:.3f} vs baseline {baseline_f1:.3f}")
            return True
    
    logger.info("Pas de ré-entraînement nécessaire")
    return False
