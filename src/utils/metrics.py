"""
Métriques et indicateurs pour Ubisoft People Analytics.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Any, Optional
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, average_precision_score, confusion_matrix,
    classification_report, balanced_accuracy_score, matthews_corrcoef
)
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class ModelMetrics:
    """Métriques de performance des modèles ML."""
    
    @staticmethod
    def compute_classification_metrics(y_true: np.ndarray, 
                                     y_pred: np.ndarray, 
                                     y_prob: Optional[np.ndarray] = None) -> Dict[str, float]:
        """Calculer toutes les métriques de classification."""
        metrics = {
            'accuracy': accuracy_score(y_true, y_pred),
            'precision': precision_score(y_true, y_pred, average='weighted', zero_division=0),
            'recall': recall_score(y_true, y_pred, average='weighted', zero_division=0),
            'f1_score': f1_score(y_true, y_pred, average='weighted', zero_division=0),
            'balanced_accuracy': balanced_accuracy_score(y_true, y_pred),
            'matthews_correlation': matthews_corrcoef(y_true, y_pred)
        }
        
        if y_prob is not None and len(np.unique(y_true)) == 2:
            metrics.update({
                'roc_auc': roc_auc_score(y_true, y_prob),
                'average_precision': average_precision_score(y_true, y_prob)
            })
        
        return metrics
    
    @staticmethod
    def generate_classification_report_dict(y_true: np.ndarray, 
                                          y_pred: np.ndarray,
                                          target_names: Optional[List[str]] = None) -> Dict:
        """Générer un rapport de classification détaillé."""
        return classification_report(y_true, y_pred, target_names=target_names, 
                                   output_dict=True, zero_division=0)
    
    @staticmethod
    def compute_confusion_matrix_metrics(y_true: np.ndarray, 
                                       y_pred: np.ndarray) -> Dict[str, Any]:
        """Calculer les métriques de la matrice de confusion."""
        cm = confusion_matrix(y_true, y_pred)
        
        if cm.shape == (2, 2):  # Classification binaire
            tn, fp, fn, tp = cm.ravel()
            metrics = {
                'true_positives': tp,
                'true_negatives': tn,
                'false_positives': fp,
                'false_negatives': fn,
                'sensitivity': tp / (tp + fn) if (tp + fn) > 0 else 0,
                'specificity': tn / (tn + fp) if (tn + fp) > 0 else 0,
                'positive_predictive_value': tp / (tp + fp) if (tp + fp) > 0 else 0,
                'negative_predictive_value': tn / (tn + fn) if (tn + fn) > 0 else 0,
                'false_positive_rate': fp / (fp + tn) if (fp + tn) > 0 else 0,
                'false_negative_rate': fn / (fn + tp) if (fn + tp) > 0 else 0
            }
        else:
            metrics = {
                'confusion_matrix': cm.tolist(),
                'total_samples': cm.sum(),
                'correct_predictions': np.trace(cm),
                'incorrect_predictions': cm.sum() - np.trace(cm)
            }
        
        return metrics

class BusinessMetrics:
    """Métriques business et RH."""
    
    @staticmethod
    def calculate_roi_metrics(baseline_costs: Dict[str, float],
                            improved_costs: Dict[str, float],
                            implementation_cost: float,
                            time_period_months: int = 12) -> Dict[str, float]:
        """Calculer les métriques ROI."""
        
        # Calcul des économies
        total_baseline = sum(baseline_costs.values())
        total_improved = sum(improved_costs.values())
        annual_savings = (total_baseline - total_improved) * (12 / time_period_months)
        
        # ROI calculations
        roi_percentage = ((annual_savings - implementation_cost) / implementation_cost) * 100
        payback_months = implementation_cost / (annual_savings / 12) if annual_savings > 0 else float('inf')
        
        metrics = {
            'total_baseline_cost': total_baseline,
            'total_improved_cost': total_improved,
            'annual_savings': annual_savings,
            'implementation_cost': implementation_cost,
            'net_benefit': annual_savings - implementation_cost,
            'roi_percentage': roi_percentage,
            'payback_period_months': payback_months,
            'benefit_cost_ratio': annual_savings / implementation_cost if implementation_cost > 0 else 0
        }
        
        return metrics
    
    @staticmethod
    def calculate_hr_kpis(employee_data: pd.DataFrame,
                         period_start: datetime,
                         period_end: datetime) -> Dict[str, float]:
        """Calculer les KPI RH."""
        
        # Filtrer par période
        df = employee_data[
            (employee_data['date'] >= period_start) & 
            (employee_data['date'] <= period_end)
        ].copy()
        
        total_employees = len(df['employee_id'].unique())
        
        kpis = {
            'total_employees': total_employees,
            'neurodivergent_percentage': 0,
            'average_creative_score': 0,
            'average_burnout_level': 0,
            'retention_rate': 0,
            'productivity_index': 0,
            'well_being_score': 0
        }
        
        if total_employees > 0:
            if 'adhd_risk' in df.columns:
                adhd_cases = df['adhd_risk'].sum()
                autism_cases = df.get('autism_risk', pd.Series([0])).sum()
                kpis['neurodivergent_percentage'] = ((adhd_cases + autism_cases) / total_employees) * 100
            
            if 'creative_score' in df.columns:
                kpis['average_creative_score'] = df['creative_score'].mean()
            
            if 'burnout_scale' in df.columns:
                kpis['average_burnout_level'] = df['burnout_scale'].mean()
            
            # Simulated metrics (in real scenario, would be calculated from actual data)
            if 'status' in df.columns:
                active_employees = len(df[df['status'] == 'active'])
                kpis['retention_rate'] = (active_employees / total_employees) * 100
            
            # Productivity index (composite score)
            if 'creative_score' in df.columns and 'burnout_scale' in df.columns:
                productivity_scores = df['creative_score'] / (df['burnout_scale'] + 1)
                kpis['productivity_index'] = productivity_scores.mean()
            
            # Well-being score (inverse of burnout)
            if 'burnout_scale' in df.columns:
                kpis['well_being_score'] = (11 - df['burnout_scale']).mean()
        
        return kpis
    
    @staticmethod
    def calculate_team_analytics(team_data: pd.DataFrame) -> Dict[str, Any]:
        """Analyser les métriques d'équipe."""
        analytics = {
            'team_size': len(team_data),
            'diversity_metrics': {},
            'performance_metrics': {},
            'risk_assessment': {},
            'recommendations': []
        }
        
        if len(team_data) > 0:
            # Métriques de diversité
            if 'department' in team_data.columns:
                dept_diversity = len(team_data['department'].unique())
                analytics['diversity_metrics']['department_diversity'] = dept_diversity
            
            # Métriques de performance
            if 'creative_score' in team_data.columns:
                analytics['performance_metrics']['average_creativity'] = team_data['creative_score'].mean()
                analytics['performance_metrics']['creativity_std'] = team_data['creative_score'].std()
            
            # Évaluation des risques
            if 'adhd_risk' in team_data.columns:
                adhd_risk_pct = (team_data['adhd_risk'].sum() / len(team_data)) * 100
                analytics['risk_assessment']['adhd_risk_percentage'] = adhd_risk_pct
                
                if adhd_risk_pct > 30:
                    analytics['recommendations'].append("Considérer des aménagements TDAH pour l'équipe")
            
            if 'burnout_scale' in team_data.columns:
                avg_burnout = team_data['burnout_scale'].mean()
                analytics['risk_assessment']['average_burnout'] = avg_burnout
                
                if avg_burnout > 7:
                    analytics['recommendations'].append("Niveau de burnout élevé - intervention recommandée")
        
        return analytics

class DiversityMetrics:
    """Métriques de diversité et inclusion."""
    
    @staticmethod
    def calculate_inclusion_index(employee_data: pd.DataFrame) -> Dict[str, float]:
        """Calculer l'index d'inclusion."""
        
        index_components = {
            'representation_score': 0,
            'accommodation_score': 0,
            'performance_parity_score': 0,
            'retention_score': 0,
            'overall_inclusion_index': 0
        }
        
        if len(employee_data) > 0:
            # Score de représentation (% de neurodivergents)
            if 'adhd_risk' in employee_data.columns or 'autism_risk' in employee_data.columns:
                neurodiverse_count = 0
                if 'adhd_risk' in employee_data.columns:
                    neurodiverse_count += employee_data['adhd_risk'].sum()
                if 'autism_risk' in employee_data.columns:
                    neurodiverse_count += employee_data['autism_risk'].sum()
                
                representation_pct = (neurodiverse_count / len(employee_data)) * 100
                index_components['representation_score'] = min(100, representation_pct * 5)  # Normalisé
            
            # Score d'accommodation (basé sur les aménagements en place)
            if 'accommodations' in employee_data.columns:
                accommodated_pct = (employee_data['accommodations'].notna().sum() / len(employee_data)) * 100
                index_components['accommodation_score'] = accommodated_pct
            else:
                index_components['accommodation_score'] = 50  # Score par défaut
            
            # Score de parité de performance
            if 'creative_score' in employee_data.columns and 'adhd_risk' in employee_data.columns:
                neurodiverse_avg = employee_data[employee_data['adhd_risk'] == 1]['creative_score'].mean()
                neurotypical_avg = employee_data[employee_data['adhd_risk'] == 0]['creative_score'].mean()
                
                if pd.notna(neurodiverse_avg) and pd.notna(neurotypical_avg):
                    parity_ratio = neurodiverse_avg / neurotypical_avg
                    index_components['performance_parity_score'] = min(100, parity_ratio * 100)
            
            # Score de rétention (simulé)
            index_components['retention_score'] = 85  # Valeur par défaut
            
            # Index global (moyenne pondérée)
            weights = {
                'representation_score': 0.25,
                'accommodation_score': 0.30,
                'performance_parity_score': 0.25,
                'retention_score': 0.20
            }
            
            overall_score = sum(
                index_components[key] * weight 
                for key, weight in weights.items()
            )
            index_components['overall_inclusion_index'] = overall_score
        
        return index_components

def calculate_model_drift(baseline_metrics: Dict[str, float],
                         current_metrics: Dict[str, float],
                         threshold: float = 0.05) -> Dict[str, Any]:
    """Détecter la dérive du modèle."""
    
    drift_analysis = {
        'has_drift': False,
        'drift_metrics': {},
        'severity': 'none',
        'affected_metrics': []
    }
    
    for metric_name in baseline_metrics.keys():
        if metric_name in current_metrics:
            baseline_value = baseline_metrics[metric_name]
            current_value = current_metrics[metric_name]
            
            # Calculer la dérive relative
            if baseline_value != 0:
                relative_drift = abs(current_value - baseline_value) / abs(baseline_value)
            else:
                relative_drift = abs(current_value - baseline_value)
            
            drift_analysis['drift_metrics'][metric_name] = {
                'baseline': baseline_value,
                'current': current_value,
                'absolute_drift': abs(current_value - baseline_value),
                'relative_drift': relative_drift,
                'exceeds_threshold': relative_drift > threshold
            }
            
            if relative_drift > threshold:
                drift_analysis['has_drift'] = True
                drift_analysis['affected_metrics'].append(metric_name)
    
    # Déterminer la sévérité
    if drift_analysis['has_drift']:
        max_drift = max(
            drift_analysis['drift_metrics'][metric]['relative_drift']
            for metric in drift_analysis['affected_metrics']
        )
        
        if max_drift > 0.2:
            drift_analysis['severity'] = 'critical'
        elif max_drift > 0.1:
            drift_analysis['severity'] = 'high'
        elif max_drift > 0.05:
            drift_analysis['severity'] = 'moderate'
        else:
            drift_analysis['severity'] = 'low'
    
    return drift_analysis

def generate_metrics_dashboard_data(employee_data: pd.DataFrame,
                                  predictions: np.ndarray,
                                  actual_outcomes: Optional[np.ndarray] = None) -> Dict[str, Any]:
    """Générer les données pour le dashboard de métriques."""
    
    dashboard_data = {
        'timestamp': datetime.now().isoformat(),
        'summary_stats': {},
        'model_performance': {},
        'business_impact': {},
        'alerts': []
    }
    
    # Statistiques résumé
    dashboard_data['summary_stats'] = {
        'total_employees_analyzed': len(employee_data),
        'high_risk_adhd_count': int(np.sum(predictions)),
        'high_risk_adhd_percentage': float(np.mean(predictions) * 100),
        'average_creative_score': float(employee_data.get('creative_score', pd.Series([0])).mean()),
        'average_burnout_level': float(employee_data.get('burnout_scale', pd.Series([0])).mean())
    }
    
    # Performance du modèle (si outcomes disponibles)
    if actual_outcomes is not None:
        model_metrics = ModelMetrics.compute_classification_metrics(
            actual_outcomes, predictions
        )
        dashboard_data['model_performance'] = model_metrics
    
    # Impact business (calculé)
    risk_employees = np.sum(predictions)
    estimated_intervention_cost = risk_employees * 2000  # €2k par employé
    estimated_savings = risk_employees * 8000 * 0.23  # Réduction turnover 23%
    
    dashboard_data['business_impact'] = {
        'employees_needing_support': int(risk_employees),
        'estimated_intervention_cost_eur': estimated_intervention_cost,
        'estimated_annual_savings_eur': estimated_savings,
        'estimated_roi_percentage': ((estimated_savings - estimated_intervention_cost) / estimated_intervention_cost * 100) if estimated_intervention_cost > 0 else 0
    }
    
    # Alertes automatiques
    if dashboard_data['summary_stats']['high_risk_adhd_percentage'] > 25:
        dashboard_data['alerts'].append({
            'type': 'warning',
            'message': f"Taux de risque TDAH élevé: {dashboard_data['summary_stats']['high_risk_adhd_percentage']:.1f}%",
            'priority': 'high'
        })
    
    if dashboard_data['summary_stats']['average_burnout_level'] > 7:
        dashboard_data['alerts'].append({
            'type': 'critical',
            'message': f"Niveau de burnout critique: {dashboard_data['summary_stats']['average_burnout_level']:.1f}/10",
            'priority': 'critical'
        })
    
    return dashboard_data
