"""
Utilitaires de visualisation pour Ubisoft People Analytics.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
from typing import Dict, List, Tuple, Optional, Any
import warnings
warnings.filterwarnings('ignore')

# Configuration du style
plt.style.use('ggplot')
sns.set_palette("husl")

class AnalyticsVisualizer:
    """Classe principale pour les visualisations analytics."""
    
    def __init__(self, theme: str = 'ubisoft'):
        self.theme = theme
        self.color_palette = self._get_color_palette()
    
    def _get_color_palette(self) -> Dict[str, str]:
        """Palette de couleurs Ubisoft."""
        palettes = {
            'ubisoft': {
                'primary': '#0099FF',
                'secondary': '#FF6B35',
                'success': '#28A745',
                'warning': '#FFC107',
                'danger': '#DC3545',
                'info': '#17A2B8',
                'dark': '#343A40',
                'light': '#F8F9FA'
            },
            'default': px.colors.qualitative.Set3
        }
        return palettes.get(self.theme, palettes['default'])
    
    def plot_employee_distribution(self, df: pd.DataFrame) -> go.Figure:
        """Graphique de distribution des employés."""
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Distribution Créativité', 'Distribution Burnout', 
                          'Risque TDAH', 'Répartition Départements'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"type": "domain"}]]
        )
        
        # Histogramme créativité
        fig.add_trace(
            go.Histogram(x=df['creative_score'], name='Creative Score', 
                        marker_color=self.color_palette['primary']),
            row=1, col=1
        )
        
        # Histogramme burnout
        fig.add_trace(
            go.Histogram(x=df['burnout_scale'], name='Burnout Scale',
                        marker_color=self.color_palette['warning']),
            row=1, col=2
        )
        
        # Bar chart TDAH
        adhd_counts = df['adhd_risk'].value_counts()
        fig.add_trace(
            go.Bar(x=['Pas de risque', 'Risque TDAH'], 
                   y=[adhd_counts.get(0, 0), adhd_counts.get(1, 0)],
                   name='ADHD Risk',
                   marker_color=[self.color_palette['success'], self.color_palette['danger']]),
            row=2, col=1
        )
        
        # Pie chart départements
        if 'department' in df.columns:
            dept_counts = df['department'].value_counts()
            fig.add_trace(
                go.Pie(labels=dept_counts.index, values=dept_counts.values,
                       name="Départements"),
                row=2, col=2
            )
        
        fig.update_layout(
            title_text="Vue d'ensemble des Données Employés",
            showlegend=False,
            height=600
        )
        
        return fig
    
    def plot_correlation_heatmap(self, df: pd.DataFrame) -> go.Figure:
        """Heatmap des corrélations."""
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        corr_matrix = df[numeric_cols].corr()
        
        fig = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.columns,
            colorscale='RdYlBu',
            zmid=0,
            text=corr_matrix.round(3).values,
            texttemplate="%{text}",
            textfont={"size": 10},
            hoverongaps=False
        ))
        
        fig.update_layout(
            title="Matrice de Corrélation",
            width=600,
            height=600
        )
        
        return fig
    
    def plot_performance_metrics(self, metrics: Dict[str, float]) -> go.Figure:
        """Graphique radar des métriques de performance."""
        
        categories = list(metrics.keys())
        values = list(metrics.values())
        
        # Normaliser les valeurs pour le radar (0-1)
        normalized_values = []
        for key, value in metrics.items():
            if key in ['accuracy', 'precision', 'recall', 'f1_score', 'roc_auc']:
                normalized_values.append(value)  # Déjà entre 0-1
            else:
                normalized_values.append(min(1, value))  # Cap à 1
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=normalized_values + [normalized_values[0]],  # Fermer le cercle
            theta=categories + [categories[0]],
            fill='toself',
            name='Performance Modèle',
            line_color=self.color_palette['primary']
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1]
                )),
            showlegend=False,
            title="Métriques de Performance du Modèle"
        )
        
        return fig
    
    def plot_roi_analysis(self, roi_data: Dict[str, float]) -> go.Figure:
        """Analyse ROI avec graphiques financiers."""
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Coûts vs Économies', 'ROI Temporel', 
                          'Breakdown Financier', 'Payback Period'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"type": "domain"}, {"secondary_y": False}]]
        )
        
        # Coûts vs économies
        categories = ['Coût Implementation', 'Économies Annuelles']
        values = [roi_data['implementation_cost'], roi_data['annual_savings']]
        colors = [self.color_palette['danger'], self.color_palette['success']]
        
        fig.add_trace(
            go.Bar(x=categories, y=values, marker_color=colors, name='Coûts/Économies'),
            row=1, col=1
        )
        
        # ROI temporel (projection 5 ans)
        years = list(range(1, 6))
        cumulative_benefit = [
            roi_data['annual_savings'] * year - roi_data['implementation_cost']
            for year in years
        ]
        
        fig.add_trace(
            go.Scatter(x=years, y=cumulative_benefit, mode='lines+markers',
                      name='Bénéfice Cumulé', line_color=self.color_palette['primary']),
            row=1, col=2
        )
        
        # Breakdown pie chart
        breakdown_labels = ['Réduction Turnover', 'Augmentation Productivité', 
                           'Innovation Boost', 'Bien-être']
        breakdown_values = [1200000, 950000, 180000, 85000]  # Exemple de données
        
        fig.add_trace(
            go.Pie(labels=breakdown_labels, values=breakdown_values, name="Breakdown"),
            row=2, col=1
        )
        
        # Payback period
        payback_months = roi_data.get('payback_period_months', 12)
        months = list(range(1, int(payback_months) + 2))
        investment_recovery = [
            min(roi_data['implementation_cost'], 
                roi_data['annual_savings'] / 12 * month)
            for month in months
        ]
        
        fig.add_trace(
            go.Scatter(x=months, y=investment_recovery, mode='lines+markers',
                      name='Récupération Investment', line_color=self.color_palette['success']),
            row=2, col=2
        )
        
        fig.update_layout(
            title_text="Analyse ROI Complète",
            showlegend=False,
            height=800
        )
        
        return fig
    
    def plot_team_analytics(self, team_data: Dict[str, Any]) -> go.Figure:
        """Dashboard analytics d'équipe."""
        
        fig = make_subplots(
            rows=2, cols=3,
            subplot_titles=('Taille Équipe', 'Diversité', 'Performance', 
                          'Risques', 'Bien-être', 'Recommandations'),
            specs=[[{"type": "indicator"}, {"type": "domain"}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"type": "indicator"}, {"secondary_y": False}]]
        )
        
        # Indicateur taille équipe
        fig.add_trace(
            go.Indicator(
                mode="gauge+number",
                value=team_data['team_size'],
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Employés"},
                gauge={'axis': {'range': [None, 50]},
                       'bar': {'color': self.color_palette['primary']}}
            ),
            row=1, col=1
        )
        
        # Pie diversité
        if 'diversity_metrics' in team_data:
            diversity_labels = ['Neurodivergent', 'Neurotypique']
            neuro_pct = team_data.get('risk_assessment', {}).get('adhd_risk_percentage', 15)
            diversity_values = [neuro_pct, 100 - neuro_pct]
            
            fig.add_trace(
                go.Pie(labels=diversity_labels, values=diversity_values, 
                       name="Diversité Neuro"),
                row=1, col=2
            )
        
        # Performance metrics
        if 'performance_metrics' in team_data:
            perf_metrics = team_data['performance_metrics']
            metrics_names = list(perf_metrics.keys())
            metrics_values = list(perf_metrics.values())
            
            fig.add_trace(
                go.Bar(x=metrics_names, y=metrics_values, 
                       marker_color=self.color_palette['success'], name='Performance'),
                row=1, col=3
            )
        
        # Risques
        if 'risk_assessment' in team_data:
            risk_data = team_data['risk_assessment']
            risk_names = list(risk_data.keys())
            risk_values = list(risk_data.values())
            
            fig.add_trace(
                go.Bar(x=risk_names, y=risk_values,
                       marker_color=self.color_palette['warning'], name='Risques'),
                row=2, col=1
            )
        
        # Indicateur bien-être
        wellbeing_score = 100 - (team_data.get('risk_assessment', {}).get('average_burnout', 5) * 10)
        fig.add_trace(
            go.Indicator(
                mode="gauge+number+delta",
                value=wellbeing_score,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Bien-être (%)"},
                delta={'reference': 80},
                gauge={'axis': {'range': [None, 100]},
                       'bar': {'color': self.color_palette['success']},
                       'steps': [
                           {'range': [0, 50], 'color': "lightgray"},
                           {'range': [50, 80], 'color': "gray"}],
                       'threshold': {'line': {'color': "red", 'width': 4},
                                   'thickness': 0.75, 'value': 90}}
            ),
            row=2, col=2
        )
        
        fig.update_layout(
            title_text="Analytics d'Équipe",
            showlegend=False,
            height=700
        )
        
        return fig
    
    def create_streamlit_dashboard(self, data: Dict[str, Any]):
        """Créer un dashboard Streamlit interactif."""
        
        st.title("🎯 Ubisoft People Analytics Dashboard")
        
        # Métriques principales
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="Employés Analysés",
                value=data.get('total_employees', 0),
                delta="+12 ce mois"
            )
        
        with col2:
            risk_pct = data.get('high_risk_percentage', 0)
            st.metric(
                label="Risque TDAH (%)",
                value=f"{risk_pct:.1f}%",
                delta="-2.1%" if risk_pct < 20 else "+1.5%",
                delta_color="inverse"
            )
        
        with col3:
            creative_avg = data.get('average_creative_score', 0)
            st.metric(
                label="Score Créativité Moyen",
                value=f"{creative_avg:.1f}",
                delta="+3.2"
            )
        
        with col4:
            roi = data.get('estimated_roi_percentage', 0)
            st.metric(
                label="ROI Estimé (%)",
                value=f"{roi:.0f}%",
                delta="+15%"
            )
        
        # Graphiques principaux
        col1, col2 = st.columns(2)
        
        with col1:
            if 'employee_data' in data:
                fig_dist = self.plot_employee_distribution(data['employee_data'])
                st.plotly_chart(fig_dist, use_container_width=True)
        
        with col2:
            if 'correlation_data' in data:
                fig_corr = self.plot_correlation_heatmap(data['correlation_data'])
                st.plotly_chart(fig_corr, use_container_width=True)
        
        # Analyse ROI
        if 'roi_data' in data:
            st.subheader("📊 Analyse ROI")
            fig_roi = self.plot_roi_analysis(data['roi_data'])
            st.plotly_chart(fig_roi, use_container_width=True)
        
        # Analytics par équipe
        if 'team_analytics' in data:
            st.subheader("👥 Analytics d'Équipe")
            
            # Sélecteur d'équipe
            teams = list(data['team_analytics'].keys())
            selected_team = st.selectbox("Sélectionner une équipe", teams)
            
            if selected_team:
                team_data = data['team_analytics'][selected_team]
                fig_team = self.plot_team_analytics(team_data)
                st.plotly_chart(fig_team, use_container_width=True)
        
        # Alertes
        if 'alerts' in data and data['alerts']:
            st.subheader("🚨 Alertes")
            for alert in data['alerts']:
                alert_type = alert.get('type', 'info')
                if alert_type == 'critical':
                    st.error(alert['message'])
                elif alert_type == 'warning':
                    st.warning(alert['message'])
                else:
                    st.info(alert['message'])

def create_matplotlib_report(data: pd.DataFrame, output_path: str):
    """Créer un rapport PDF avec matplotlib."""
    
    fig, axes = plt.subplots(3, 2, figsize=(15, 18))
    fig.suptitle('Rapport Ubisoft People Analytics', fontsize=16, fontweight='bold')
    
    # Distribution créativité
    axes[0, 0].hist(data['creative_score'], bins=20, alpha=0.7, color='skyblue')
    axes[0, 0].set_title('Distribution Score Créativité')
    axes[0, 0].set_xlabel('Score')
    axes[0, 0].set_ylabel('Fréquence')
    
    # Distribution burnout
    axes[0, 1].hist(data['burnout_scale'], bins=10, alpha=0.7, color='salmon')
    axes[0, 1].set_title('Distribution Burnout')
    axes[0, 1].set_xlabel('Niveau')
    axes[0, 1].set_ylabel('Fréquence')
    
    # Scatter créativité vs burnout
    colors = ['red' if risk else 'blue' for risk in data['adhd_risk']]
    axes[1, 0].scatter(data['creative_score'], data['burnout_scale'], c=colors, alpha=0.6)
    axes[1, 0].set_title('Créativité vs Burnout (Rouge = Risque TDAH)')
    axes[1, 0].set_xlabel('Score Créativité')
    axes[1, 0].set_ylabel('Niveau Burnout')
    
    # Box plot par département
    if 'department' in data.columns:
        data.boxplot(column='creative_score', by='department', ax=axes[1, 1])
        axes[1, 1].set_title('Créativité par Département')
    
    # Corrélations
    numeric_cols = data.select_dtypes(include=[np.number]).columns
    corr_matrix = data[numeric_cols].corr()
    im = axes[2, 0].imshow(corr_matrix, cmap='RdYlBu', aspect='auto')
    axes[2, 0].set_xticks(range(len(corr_matrix.columns)))
    axes[2, 0].set_yticks(range(len(corr_matrix.columns)))
    axes[2, 0].set_xticklabels(corr_matrix.columns, rotation=45)
    axes[2, 0].set_yticklabels(corr_matrix.columns)
    axes[2, 0].set_title('Matrice de Corrélation')
    plt.colorbar(im, ax=axes[2, 0])
    
    # Métriques finales
    adhd_pct = data['adhd_risk'].mean() * 100
    avg_creativity = data['creative_score'].mean()
    avg_burnout = data['burnout_scale'].mean()
    
    axes[2, 1].text(0.1, 0.8, f'Risque TDAH: {adhd_pct:.1f}%', fontsize=12, transform=axes[2, 1].transAxes)
    axes[2, 1].text(0.1, 0.6, f'Créativité Moyenne: {avg_creativity:.1f}', fontsize=12, transform=axes[2, 1].transAxes)
    axes[2, 1].text(0.1, 0.4, f'Burnout Moyen: {avg_burnout:.1f}', fontsize=12, transform=axes[2, 1].transAxes)
    axes[2, 1].set_title('Métriques Résumé')
    axes[2, 1].axis('off')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    return output_path
