# NeuroInsight Hub - Version Workspace Complète
# Application Streamlit dense intégrant TDAH, Autisme, et Observatoire

import os
import json
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

# --- CONFIGURATION ---
st.set_page_config(
    page_title="NeuroInsight Hub - Workspace",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- BASE_DIR ET DONNÉES ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Données complètes intégrées (remplace metrics.json)
DATA = {
    "company_metrics": {
        "total_employees": 1247,
        "neurodiverse_employees": 187,
        "neurodiverse_percentage": 15.0,
        "adhd_employees": 89,
        "autism_employees": 52,
        "dyslexia_employees": 46,
        "retention_rate": 92.3,
        "satisfaction_score": 4.2,
        "productivity_increase": 18.5
    },
    "adhd_statistics": {
        "global_prevalence": 5.0,
        "france_adults": 3.0,
        "france_children": 3.5,
        "male_female_ratio": 2.3,
        "persistence_adulthood": 66.0,
        "comorbidity_rate": 50.0,
        "workplace_challenges": {
            "attention_difficulties": 87.3,
            "time_management": 78.6,
            "organization": 82.1,
            "impulsivity": 69.4
        }
    },
    "autism_statistics": {
        "global_prevalence": 1.0,
        "employment_rate": 22.0,
        "unemployment_rate": 85.0,
        "europe_population": 7000000,
        "workplace_participation": 42.0,
        "strengths": {
            "attention_to_detail": 94.2,
            "pattern_recognition": 89.7,
            "logical_reasoning": 91.3,
            "reliability": 88.9
        }
    },
    "observatoire_data": {
        "france_prevalence_evolution": [
            {"year": 2020, "tdah": 2.8, "autism": 0.8},
            {"year": 2021, "tdah": 3.1, "autism": 0.9},
            {"year": 2022, "tdah": 3.3, "autism": 0.95},
            {"year": 2023, "tdah": 3.5, "autism": 1.0},
            {"year": 2024, "tdah": 3.7, "autism": 1.1}
        ],
        "regional_data": [
            {"region": "Île-de-France", "tdah": 3.2, "autism": 1.1, "population": 12000000},
            {"region": "PACA", "tdah": 3.4, "autism": 0.9, "population": 5000000},
            {"region": "Nouvelle-Aquitaine", "tdah": 3.1, "autism": 1.0, "population": 6000000},
            {"region": "Occitanie", "tdah": 3.3, "autism": 0.8, "population": 5800000}
        ]
    },
    "performance_data": [
        {"department": "IT", "productivity": 118, "engagement": 89, "wellbeing": 85, "neurodiverse_ratio": 22.4},
        {"department": "Design", "productivity": 125, "engagement": 94, "wellbeing": 88, "neurodiverse_ratio": 28.1},
        {"department": "Finance", "productivity": 108, "engagement": 76, "wellbeing": 81, "neurodiverse_ratio": 11.8},
        {"department": "Marketing", "productivity": 115, "engagement": 82, "wellbeing": 79, "neurodiverse_ratio": 19.3},
        {"department": "Support", "productivity": 102, "engagement": 78, "wellbeing": 83, "neurodiverse_ratio": 15.7}
    ],
    "screening_questions": {
        "adhd": [
            {"q": "Avez-vous souvent du mal à prêter attention aux détails?", "category": "inattention", "weight": 1.2},
            {"q": "Avez-vous des difficultés à maintenir votre attention?", "category": "inattention", "weight": 1.3},
            {"q": "Vous sentez-vous souvent agité(e)?", "category": "hyperactivity", "weight": 1.1},
            {"q": "Avez-vous tendance à interrompre les autres?", "category": "impulsivity", "weight": 1.0},
            {"q": "Avez-vous du mal à organiser vos tâches?", "category": "inattention", "weight": 1.1},
            {"q": "Évitez-vous les tâches nécessitant un effort mental soutenu?", "category": "inattention", "weight": 1.2},
            {"q": "Perdez-vous souvent vos affaires?", "category": "inattention", "weight": 0.9},
            {"q": "Êtes-vous facilement distrait(e) par des stimuli externes?", "category": "inattention", "weight": 1.1}
        ],
        "autism": [
            {"q": "Trouvez-vous difficile de maintenir une conversation?", "category": "social", "weight": 1.4},
            {"q": "Êtes-vous sensible aux sons, lumières ou textures?", "category": "sensory", "weight": 1.2},
            {"q": "Préférez-vous des routines établies?", "category": "routines", "weight": 1.3},
            {"q": "Avez-vous des intérêts très spécialisés?", "category": "interests", "weight": 1.1},
            {"q": "Avez-vous du mal à comprendre les expressions faciales?", "category": "social", "weight": 1.2},
            {"q": "Les changements vous perturbent-ils facilement?", "category": "routines", "weight": 1.0}
        ]
    },
    "workplace_accommodations": [
        {"condition": "ADHD", "accommodation": "Environnement calme", "impact": 8.5, "cost": "Faible"},
        {"condition": "ADHD", "accommodation": "Pauses régulières", "impact": 7.8, "cost": "Aucun"},
        {"condition": "ADHD", "accommodation": "Outils numériques d'organisation", "impact": 9.1, "cost": "Moyen"},
        {"condition": "Autism", "accommodation": "Instructions écrites détaillées", "impact": 9.2, "cost": "Faible"},
        {"condition": "Autism", "accommodation": "Horaires flexibles", "impact": 8.7, "cost": "Faible"},
        {"condition": "Autism", "accommodation": "Réduction stimuli sensoriels", "impact": 8.9, "cost": "Moyen"}
    ],
    "recent_activities": [
        {"time": "Il y a 2h", "message": "Nouveau screening TDAH complété", "type": "assessment"},
        {"time": "Il y a 4h", "message": "Accommodations mises en place pour 3 employés", "type": "accommodation"},
        {"time": "Il y a 6h", "message": "Rapport mensuel généré", "type": "report"},
        {"time": "Il y a 1j", "message": "Formation managers neurodiversité", "type": "training"},
        {"time": "Il y a 2j", "message": "5 nouveaux candidats évalués", "type": "recruitment"}
    ]
}

# --- INTERFACE PRINCIPALE ---
def main():
    # Logo et titre
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("# 🧠 NeuroInsight Hub - Workspace")
        st.markdown("### *Plateforme complète de gestion de la neurodiversité*")
    
    with col2:
        st.image("https://logos-world.net/wp-content/uploads/2021/01/Ubisoft-Logo.png", width=120)

    # Sidebar Navigation
    st.sidebar.markdown("## 🎯 Navigation")
    page = st.sidebar.selectbox(
        "Sélectionner un module",
        [
            "🏠 Dashboard Principal",
            "🧠 Module TDAH", 
            "🎯 Module Autisme",
            "📊 Observatoire Données",
            "🔬 NeuroScreen Évaluations",
            "🏢 Gestion Workplace",
            "👥 Recrutement Neurodiversité",
            "📈 Analytics & Reporting"
        ]
    )
    
    # Métriques sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 Métriques Rapides")
    st.sidebar.metric("Employés Neurodivers", f"{DATA['company_metrics']['neurodiverse_employees']}")
    st.sidebar.metric("Taux de Rétention", f"{DATA['company_metrics']['retention_rate']}%")
    st.sidebar.metric("Score Satisfaction", f"{DATA['company_metrics']['satisfaction_score']}/5")
    
    # Router vers les modules
    if page == "🏠 Dashboard Principal":
        dashboard_principal()
    elif page == "🧠 Module TDAH":
        module_tdah()
    elif page == "🎯 Module Autisme":
        module_autisme()
    elif page == "📊 Observatoire Données":
        observatoire_donnees()
    elif page == "🔬 NeuroScreen Évaluations":
        neuroscreen_evaluations()
    elif page == "🏢 Gestion Workplace":
        gestion_workplace()
    elif page == "👥 Recrutement Neurodiversité":
        recrutement_neurodiversite()
    elif page == "📈 Analytics & Reporting":
        analytics_reporting()

# --- DASHBOARD PRINCIPAL ---
def dashboard_principal():
    st.markdown("## 🏠 Dashboard Principal")
    
    # KPIs principaux
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "👥 Total Employés", 
            DATA['company_metrics']['total_employees'],
            delta="↗ +3.2%"
        )
    
    with col2:
        st.metric(
            "🧠 Employés Neurodivers", 
            f"{DATA['company_metrics']['neurodiverse_employees']} ({DATA['company_metrics']['neurodiverse_percentage']}%)",
            delta="↗ +2.1%"
        )
    
    with col3:
        st.metric(
            "📈 Augmentation Productivité", 
            f"{DATA['company_metrics']['productivity_increase']}%",
            delta="↗ +5.3%"
        )
    
    with col4:
        st.metric(
            "⭐ Score Bien-être", 
            f"{DATA['company_metrics']['satisfaction_score']}/5",
            delta="↗ +0.3"
        )
    
    st.markdown("---")
    
    # Graphiques principaux
    col1, col2 = st.columns(2)
    
    with col1:
        # Répartition neurodiversité
        fig_pie = go.Figure(data=[go.Pie(
            labels=['TDAH', 'Autisme', 'Dyslexie', 'Autres'],
            values=[
                DATA['company_metrics']['adhd_employees'],
                DATA['company_metrics']['autism_employees'], 
                DATA['company_metrics']['dyslexia_employees'],
                DATA['company_metrics']['neurodiverse_employees'] - 
                DATA['company_metrics']['adhd_employees'] - 
                DATA['company_metrics']['autism_employees'] - 
                DATA['company_metrics']['dyslexia_employees']
            ],
            hole=0.4
        )])
        fig_pie.update_layout(title="Répartition des Conditions Neurodivergentes")
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # Performance par département
        df_perf = pd.DataFrame(DATA['performance_data'])
        fig_bar = px.bar(
            df_perf, 
            x='department', 
            y=['productivity', 'engagement', 'wellbeing'],
            title="Performance par Département",
            color_discrete_sequence=['#c4bc74', '#223c4c', '#aca45c']
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # Activités récentes
    st.markdown("### 📋 Activités Récentes")
    for activity in DATA['recent_activities']:
        icon = {"assessment": "🔍", "accommodation": "🔧", "report": "📊", "training": "🎓", "recruitment": "👤"}
        st.markdown(f"**{activity['time']}** - {icon.get(activity['type'], '•')} {activity['message']}")

# --- MODULE TDAH ---
def module_tdah():
    st.markdown("## 🧠 Module TDAH - Trouble du Déficit de l'Attention/Hyperactivité")
    
    # Onglets
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Screening", "📊 Statistiques", "🎯 Accommodations", "📈 Suivi"])
    
    with tab1:
        st.markdown("### 🔍 Screening TDAH")
        st.info("**Prévalence**: 5% population mondiale • 3% adultes France • Ratio M/F: 2.3:1")
        
        # Questionnaire interactif
        with st.expander("🔴 Démarrer le Screening TDAH", expanded=False):
            scores = {"inattention": 0, "hyperactivity": 0, "impulsivity": 0}
            
            st.markdown("**Répondez aux questions suivantes (0=Jamais, 4=Très souvent):**")
            
            for i, item in enumerate(DATA['screening_questions']['adhd']):
                score = st.slider(
                    f"{i+1}. {item['q']}", 
                    min_value=0, max_value=4, value=0, 
                    key=f"adhd_{i}"
                )
                scores[item['category']] += score * item['weight']
            
            if st.button("📊 Calculer le Résultat"):
                total_score = sum(scores.values())
                max_possible = len(DATA['screening_questions']['adhd']) * 4 * 1.2
                percentage = (total_score / max_possible) * 100
                
                st.markdown("### 🎯 Résultats du Screening")
                
                if percentage >= 60:
                    st.error(f"**Score: {percentage:.1f}%** - Probabilité élevée de TDAH. Recommandation: Évaluation approfondie.")
                elif percentage >= 40:
                    st.warning(f"**Score: {percentage:.1f}%** - Indicateurs modérés. Recommandation: Suivi et accommodations préventives.")
                else:
                    st.success(f"**Score: {percentage:.1f}%** - Probabilité faible. Aucune action immédiate nécessaire.")
                
                # Répartition par catégorie
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Inattention", f"{(scores['inattention']/total_score*100):.0f}%" if total_score > 0 else "0%")
                with col2:
                    st.metric("Hyperactivité", f"{(scores['hyperactivity']/total_score*100):.0f}%" if total_score > 0 else "0%")
                with col3:
                    st.metric("Impulsivité", f"{(scores['impulsivity']/total_score*100):.0f}%" if total_score > 0 else "0%")
    
    with tab2:
        st.markdown("### 📊 Statistiques TDAH")
        
        # Métriques clés
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Prévalence Mondiale", "5.0%")
        with col2:
            st.metric("Adultes France", "3.0%")
        with col3:
            st.metric("Persistance Adulte", "66.0%")
        with col4:
            st.metric("Comorbidités", "50.0%")
        
        # Graphique défis workplace
        challenges = DATA['adhd_statistics']['workplace_challenges']
        fig_challenges = go.Figure([go.Bar(
            x=list(challenges.keys()),
            y=list(challenges.values()),
            marker_color='#c4bc74'
        )])
        fig_challenges.update_layout(title="Défis Principaux en Milieu Professionnel (%)")
        st.plotly_chart(fig_challenges, use_container_width=True)
    
    with tab3:
        st.markdown("### 🎯 Accommodations Recommandées")
        
        tdah_accommodations = [acc for acc in DATA['workplace_accommodations'] if acc['condition'] == 'ADHD']
        
        for acc in tdah_accommodations:
            with st.expander(f"🔧 {acc['accommodation']}", expanded=False):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**Impact Score**: {acc['impact']}/10")
                    st.progress(acc['impact']/10)
                with col2:
                    st.markdown(f"**Coût**: {acc['cost']}")
                    color = {"Aucun": "green", "Faible": "orange", "Moyen": "red"}[acc['cost']]
                    st.markdown(f":{color}[●] Niveau de coût")
    
    with tab4:
        st.markdown("### 📈 Suivi et Évolution")
        
        # Graphique d'évolution simulé
        dates = pd.date_range(start='2024-01-01', periods=12, freq='M')
        progress_data = {
            'Date': dates,
            'Attention': np.random.normal(70, 10, 12).cumsum() / 12 + 50,
            'Organisation': np.random.normal(65, 8, 12).cumsum() / 12 + 45,
            'Productivité': np.random.normal(75, 12, 12).cumsum() / 12 + 55
        }
        
        df_progress = pd.DataFrame(progress_data)
        fig_progress = px.line(
            df_progress, 
            x='Date', 
            y=['Attention', 'Organisation', 'Productivité'],
            title="Évolution des Métriques TDAH (Moyenne des employés)"
        )
        st.plotly_chart(fig_progress, use_container_width=True)

# --- MODULE AUTISME ---
def module_autisme():
    st.markdown("## 🎯 Module Autisme - Troubles du Spectre Autistique")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Évaluation", "💪 Forces", "🛠️ Accommodations", "📊 Analytics"])
    
    with tab1:
        st.markdown("### 🔍 Évaluation Autisme")
        st.info("**Emploi**: 22% taux d'emploi • 85% chômage • 7M personnes en Europe")
        
        with st.expander("🟢 Démarrer l'Évaluation Autisme", expanded=False):
            autism_scores = {"social": 0, "sensory": 0, "routines": 0, "interests": 0}
            
            for i, item in enumerate(DATA['screening_questions']['autism']):
                score = st.slider(
                    f"{i+1}. {item['q']}", 
                    min_value=0, max_value=4, value=0,
                    key=f"autism_{i}"
                )
                autism_scores[item['category']] += score * item['weight']
            
            if st.button("📊 Évaluer"):
                total = sum(autism_scores.values())
                max_score = len(DATA['screening_questions']['autism']) * 4 * 1.4
                percentage = (total / max_score) * 100
                
                st.markdown("### 🎯 Profil Autisme")
                
                if percentage >= 55:
                    st.warning(f"**Score: {percentage:.1f}%** - Traits autistiques significatifs détectés.")
                elif percentage >= 35:
                    st.info(f"**Score: {percentage:.1f}%** - Quelques traits présents. Suivi recommandé.")
                else:
                    st.success(f"**Score: {percentage:.1f}%** - Peu de traits détectés.")
                
                # Radar chart des domaines
                categories = list(autism_scores.keys())
                values = [autism_scores[cat] for cat in categories]
                
                fig_radar = go.Figure()
                fig_radar.add_trace(go.Scatterpolar(
                    r=values,
                    theta=categories,
                    fill='toself',
                    name='Profil'
                ))
                fig_radar.update_layout(
                    polar=dict(radialaxis=dict(visible=True, range=[0, max(values)])),
                    title="Profil par Domaines"
                )
                st.plotly_chart(fig_radar, use_container_width=True)
    
    with tab2:
        st.markdown("### 💪 Forces et Talents Autistiques")
        
        strengths = DATA['autism_statistics']['strengths']
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("🎯 Attention aux Détails", f"{strengths['attention_to_detail']}%")
            st.metric("🔍 Reconnaissance Motifs", f"{strengths['pattern_recognition']}%")
        
        with col2:
            st.metric("🧠 Raisonnement Logique", f"{strengths['logical_reasoning']}%")
            st.metric("✅ Fiabilité", f"{strengths['reliability']}%")
        
        # Graphique des forces
        fig_strengths = go.Figure([go.Bar(
            x=list(strengths.keys()),
            y=list(strengths.values()),
            marker_color='#223c4c',
            text=[f"{v}%" for v in strengths.values()],
            textposition='auto'
        )])
        fig_strengths.update_layout(title="Pourcentage d'Employés Autistes Excellant dans Chaque Domaine")
        st.plotly_chart(fig_strengths, use_container_width=True)
        
        st.success("**Opportunités**: Rôles analytiques, QA, développement, recherche, audit")
    
    with tab3:
        st.markdown("### 🛠️ Accommodations Workplace")
        
        autism_accommodations = [acc for acc in DATA['workplace_accommodations'] if acc['condition'] == 'Autism']
        
        for i, acc in enumerate(autism_accommodations):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**{acc['accommodation']}**")
                st.progress(acc['impact']/10)
                st.caption(f"Impact: {acc['impact']}/10 • Coût: {acc['cost']}")
            with col2:
                if st.button(f"Implémenter", key=f"impl_autism_{i}"):
                    st.success("✅ Programmé")
    
    with tab4:
        st.markdown("### 📊 Analytics Autisme")
        
        # Données simulées d'engagement
        departments = ['IT', 'Design', 'Finance', 'Support']
        autism_success = [95, 88, 76, 82]
        neurotypical_success = [78, 79, 84, 80]
        
        fig_comparison = go.Figure()
        fig_comparison.add_trace(go.Bar(
            name='Employés Autistes',
            x=departments,
            y=autism_success,
            marker_color='#c4bc74'
        ))
        fig_comparison.add_trace(go.Bar(
            name='Employés Neurotypiques',
            x=departments,
            y=neurotypical_success,
            marker_color='#aca45c'
        ))
        
        fig_comparison.update_layout(
            title='Comparaison Performance par Département (%)',
            barmode='group'
        )
        st.plotly_chart(fig_comparison, use_container_width=True)

# --- OBSERVATOIRE DONNÉES ---
def observatoire_donnees():
    st.markdown("## 📊 Observatoire des Données Neurodiversité")
    
    tab1, tab2, tab3 = st.tabs(["📈 Évolution France", "🗺️ Données Régionales", "🌍 Comparaisons Internationales"])
    
    with tab1:
        st.markdown("### 📈 Évolution de la Prévalence en France")
        
        # Graphique évolution temporelle
        df_evolution = pd.DataFrame(DATA['observatoire_data']['france_prevalence_evolution'])
        
        fig_evolution = go.Figure()
        fig_evolution.add_trace(go.Scatter(
            x=df_evolution['year'],
            y=df_evolution['tdah'],
            mode='lines+markers',
            name='TDAH',
            line=dict(color='#c4bc74', width=3)
        ))
        fig_evolution.add_trace(go.Scatter(
            x=df_evolution['year'],
            y=df_evolution['autism'],
            mode='lines+markers',
            name='Autisme',
            line=dict(color='#223c4c', width=3)
        ))
        
        fig_evolution.update_layout(
            title='Évolution de la Prévalence (%): 2020-2024',
            xaxis_title='Année',
            yaxis_title='Prévalence (%)',
            hovermode='x unified'
        )
        st.plotly_chart(fig_evolution, use_container_width=True)
        
        # Métriques clés
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("TDAH 2024", "3.7%", "+0.2%")
        with col2:
            st.metric("Autisme 2024", "1.1%", "+0.1%")
        with col3:
            st.metric("Total Neurodivers", "4.8%", "+0.3%")
    
    with tab2:
        st.markdown("### 🗺️ Données Régionales France")
        
        df_regional = pd.DataFrame(DATA['observatoire_data']['regional_data'])
        
        # Graphique régional
        fig_regional = go.Figure()
        fig_regional.add_trace(go.Bar(
            name='TDAH',
            x=df_regional['region'],
            y=df_regional['tdah'],
            marker_color='#c4bc74'
        ))
        fig_regional.add_trace(go.Bar(
            name='Autisme',
            x=df_regional['region'],
            y=df_regional['autism'],
            marker_color='#223c4c'
        ))
        
        fig_regional.update_layout(
            title='Prévalence par Région (%)',
            xaxis_tickangle=-45,
            barmode='group'
        )
        st.plotly_chart(fig_regional, use_container_width=True)
        
        # Tableau détaillé
        st.markdown("### 📋 Données Détaillées par Région")
        df_display = df_regional.copy()
        df_display['population_formatted'] = df_display['population'].apply(lambda x: f"{x:,}")
        df_display['estimated_tdah'] = (df_display['tdah'] / 100 * df_display['population']).astype(int)
        df_display['estimated_autism'] = (df_display['autism'] / 100 * df_display['population']).astype(int)
        
        st.dataframe(
            df_display[['region', 'population_formatted', 'tdah', 'autism', 'estimated_tdah', 'estimated_autism']],
            column_config={
                "region": "Région",
                "population_formatted": "Population",
                "tdah": st.column_config.NumberColumn("TDAH (%)", format="%.1f%%"),
                "autism": st.column_config.NumberColumn("Autisme (%)", format="%.1f%%"),
                "estimated_tdah": "Est. TDAH",
                "estimated_autism": "Est. Autisme"
            }
        )
    
    with tab3:
        st.markdown("### 🌍 Comparaisons Internationales")
        
        # Données internationales simulées
        countries_data = {
            'Pays': ['France', 'Allemagne', 'UK', 'Suède', 'Espagne', 'Italie'],
            'TDAH': [3.5, 4.2, 3.9, 4.8, 3.1, 2.9],
            'Autisme': [1.0, 1.2, 1.4, 1.3, 0.8, 0.9],
            'Support_Workplace': [6.2, 8.1, 7.8, 9.2, 5.4, 4.9]
        }
        
        df_international = pd.DataFrame(countries_data)
        
        # Graphique comparatif
        fig_intl = go.Figure()
        
        fig_intl.add_trace(go.Scatter(
            x=df_international['TDAH'],
            y=df_international['Autisme'],
            mode='markers+text',
            text=df_international['Pays'],
            textposition="top center",
            marker=dict(
                size=df_international['Support_Workplace']*5,
                color=df_international['Support_Workplace'],
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="Support Workplace")
            )
        ))
        
        fig_intl.update_layout(
            title='Prévalence TDAH vs Autisme par Pays (taille = support workplace)',
            xaxis_title='TDAH (%)',
            yaxis_title='Autisme (%)'
        )
        st.plotly_chart(fig_intl, use_container_width=True)

# --- NEUROSCREEN ÉVALUATIONS ---
def neuroscreen_evaluations():
    st.markdown("## 🔬 NeuroScreen - Évaluations Neuroscientifiques")
    
    st.info("🧠 **NeuroScreen** utilise des tests cognitifs standardisés pour évaluer les fonctions neuropsychologiques")
    
    tab1, tab2, tab3 = st.tabs(["🧪 Tests Disponibles", "📊 Nouvelle Évaluation", "📈 Résultats"])
    
    with tab1:
        st.markdown("### 🧪 Batterie de Tests NeuroScreen")
        
        tests = [
            {
                "name": "Attention Soutenue",
                "domain": "Attention", 
                "duration": 15,
                "description": "Mesure la capacité à maintenir l'attention sur une tâche répétitive"
            },
            {
                "name": "Mémoire de Travail",
                "domain": "Mémoire",
                "duration": 10, 
                "description": "Évalue la capacité à manipuler l'information en mémoire à court terme"
            },
            {
                "name": "Flexibilité Cognitive",
                "domain": "Fonctions Exécutives",
                "duration": 12,
                "description": "Mesure l'adaptation aux changements de règles et de contexte"
            },
            {
                "name": "Vitesse de Traitement",
                "domain": "Vitesse Cognitive",
                "duration": 8,
                "description": "Évalue la rapidité de traitement de l'information visuelle"
            },
            {
                "name": "Inhibition",
                "domain": "Contrôle Cognitif",
                "duration": 10,
                "description": "Mesure la capacité à supprimer des réponses automatiques"
            }
        ]
        
        for test in tests:
            with st.expander(f"🔬 {test['name']} ({test['duration']} min)", expanded=False):
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.markdown(f"**Domaine**: {test['domain']}")
                    st.markdown(f"**Description**: {test['description']}")
                with col2:
                    if st.button(f"Lancer Test", key=f"start_{test['name']}"):
                        st.success("✅ Test programmé")
    
    with tab2:
        st.markdown("### 📊 Nouvelle Évaluation Complète")
        
        col1, col2 = st.columns(2)
        with col1:
            employee_id = st.text_input("ID Employé")
            test_reason = st.selectbox("Raison de l'évaluation", [
                "Screening initial", 
                "Suivi périodique", 
                "Demande d'accommodation",
                "Évaluation post-formation"
            ])
        
        with col2:
            priority = st.selectbox("Priorité", ["Standard", "Urgente", "Recherche"])
            notes = st.text_area("Notes additionnelles")
        
        if st.button("🚀 Lancer Évaluation Complète"):
            # Simulation d'une évaluation
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            import time
            
            for i in range(100):
                progress_bar.progress(i + 1)
                if i < 20:
                    status_text.text('Initialisation des tests...')
                elif i < 50:
                    status_text.text('Tests cognitifs en cours...')
                elif i < 80:
                    status_text.text('Analyse des résultats...')
                else:
                    status_text.text('Génération du rapport...')
                time.sleep(0.02)
            
            st.success("✅ Évaluation terminée! Rapport disponible dans l'onglet Résultats.")
    
    with tab3:
        st.markdown("### 📈 Résultats et Interprétations")
        
        # Simulation de résultats
        if st.selectbox("Sélectionner un rapport", ["Rapport #2024-001", "Rapport #2024-002", "Rapport #2024-003"]):
            
            # Scores simulés
            scores = {
                'Attention Soutenue': np.random.normal(85, 15),
                'Mémoire de Travail': np.random.normal(78, 12),
                'Flexibilité Cognitive': np.random.normal(82, 10),
                'Vitesse de Traitement': np.random.normal(75, 18),
                'Inhibition': np.random.normal(88, 8)
            }
            
            # Radar chart des résultats
            fig_results = go.Figure()
            fig_results.add_trace(go.Scatterpolar(
                r=list(scores.values()),
                theta=list(scores.keys()),
                fill='toself',
                name='Scores'
            ))
            fig_results.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 100]
                    )),
                title="Profil Cognitif NeuroScreen"
            )
            st.plotly_chart(fig_results, use_container_width=True)
            
            # Interprétations
            st.markdown("### 🔍 Interprétations")
            
            for domain, score in scores.items():
                col1, col2 = st.columns([1, 2])
                with col1:
                    if score >= 85:
                        st.success(f"{domain}: {score:.0f}")
                    elif score >= 70:
                        st.warning(f"{domain}: {score:.0f}")
                    else:
                        st.error(f"{domain}: {score:.0f}")
                
                with col2:
                    if score >= 85:
                        st.write("✅ Performance supérieure - Force identifiée")
                    elif score >= 70:
                        st.write("⚠️ Performance moyenne - Surveillance recommandée") 
                    else:
                        st.write("🚨 Difficultés détectées - Accommodations nécessaires")

# --- GESTION WORKPLACE ---
def gestion_workplace():
    st.markdown("## 🏢 Gestion Workplace - Accommodations & Support")
    
    tab1, tab2, tab3, tab4 = st.tabs(["🔧 Accommodations", "📝 Demandes", "📊 Suivi", "🎯 Impact"])
    
    with tab1:
        st.markdown("### 🔧 Catalogue d'Accommodations")
        
        # Filtre par condition
        condition_filter = st.selectbox("Filtrer par condition", ["Toutes", "ADHD", "Autism", "Dyslexie"])
        
        accommodations = DATA['workplace_accommodations']
        if condition_filter != "Toutes":
            accommodations = [acc for acc in accommodations if acc['condition'] == condition_filter]
        
        for acc in accommodations:
            with st.expander(f"🛠️ {acc['accommodation']} ({acc['condition']})", expanded=False):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Impact Score", f"{acc['impact']}/10")
                    st.progress(acc['impact']/10)
                
                with col2:
                    cost_color = {"Aucun": "green", "Faible": "orange", "Moyen": "red"}[acc['cost']]
                    st.markdown(f"**Coût**: :{cost_color}[{acc['cost']}]")
                
                with col3:
                    if st.button(f"Recommander", key=f"rec_{acc['accommodation']}"):
                        st.success("✅ Ajouté aux recommandations")
    
    with tab2:
        st.markdown("### 📝 Nouvelles Demandes d'Accommodation")
        
        with st.form("nouvelle_demande"):
            col1, col2 = st.columns(2)
            
            with col1:
                employee_name = st.text_input("Nom de l'employé")
                condition = st.selectbox("Condition", ["TDAH", "Autisme", "Dyslexie", "Autre"])
                department = st.selectbox("Département", ["IT", "Design", "Finance", "Marketing", "Support"])
            
            with col2:
                urgency = st.selectbox("Urgence", ["Normale", "Élevée", "Critique"])
                requested_accommodation = st.text_area("Accommodation demandée")
                justification = st.text_area("Justification")
            
            submitted = st.form_submit_button("📤 Soumettre la Demande")
            
            if submitted:
                st.success("✅ Demande soumise avec succès! ID: ACC-2024-" + str(np.random.randint(1000, 9999)))
    
    with tab3:
        st.markdown("### 📊 Suivi des Accommodations")
        
        # Statut des accommodations
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("🔄 En Cours", "12", "+3")
        with col2:
            st.metric("✅ Implémentées", "28", "+8")
        with col3:
            st.metric("⏳ En Attente", "5", "-2")
        with col4:
            st.metric("📊 Taux Succès", "94%", "+2%")
        
        # Timeline des accommodations
        st.markdown("#### 📅 Timeline Récente")
        timeline_data = [
            {"date": "2024-01-15", "action": "Accommodation approved", "employee": "Marie D.", "type": "ADHD"},
            {"date": "2024-01-14", "action": "New request submitted", "employee": "Jean P.", "type": "Autism"},
            {"date": "2024-01-13", "action": "Implementation completed", "employee": "Sophie L.", "type": "Dyslexia"},
            {"date": "2024-01-12", "action": "Assessment scheduled", "employee": "Paul M.", "type": "ADHD"}
        ]
        
        for item in timeline_data:
            st.markdown(f"**{item['date']}** - {item['action']} ({item['employee']}) - *{item['type']}*")
    
    with tab4:
        st.markdown("### 🎯 Mesure d'Impact")
        
        # Métriques d'impact
        col1, col2 = st.columns(2)
        
        with col1:
            # Satisfaction avant/après
            satisfaction_data = {
                'Période': ['Avant Accommodations', 'Après Accommodations'],
                'Score': [3.2, 4.4]
            }
            fig_satisfaction = px.bar(
                satisfaction_data, 
                x='Période', 
                y='Score',
                title="Impact sur la Satisfaction (Score/5)",
                color_discrete_sequence=['#c4bc74']
            )
            st.plotly_chart(fig_satisfaction, use_container_width=True)
        
        with col2:
            # Productivité par type d'accommodation
            productivity_data = {
                'Accommodation': ['Environnement calme', 'Horaires flexibles', 'Outils numériques'],
                'Amélioration': [23, 31, 28]
            }
            fig_productivity = px.bar(
                productivity_data,
                x='Accommodation',
                y='Amélioration',
                title="Amélioration Productivité (%)",
                color_discrete_sequence=['#223c4c']
            )
            st.plotly_chart(fig_productivity, use_container_width=True)
        
        # ROI des accommodations
        st.markdown("#### 💰 Retour sur Investissement")
        
        roi_metrics = {
            "Coût Total Accommodations": "€45,320",
            "Augmentation Productivité": "+18.5%", 
            "Réduction Turnover": "-34%",
            "ROI Estimé": "312%"
        }
        
        col1, col2, col3, col4 = st.columns(4)
        for i, (metric, value) in enumerate(roi_metrics.items()):
            [col1, col2, col3, col4][i].metric(metric, value)

# --- RECRUTEMENT NEURODIVERSITÉ ---
def recrutement_neurodiversite():
    st.markdown("## 👥 Recrutement Neurodiversité - Processus Inclusifs")
    
    tab1, tab2, tab3 = st.tabs(["🎯 Guide Recrutement", "📊 Pipeline", "📈 Métriques"])
    
    with tab1:
        st.markdown("### 🎯 Guide de Recrutement Inclusif")
        
        # Checklist recrutement
        st.markdown("#### ✅ Checklist Processus Inclusif")
        
        checklist = [
            "Description de poste claire et spécifique",
            "Canaux de diffusion diversifiés", 
            "Processus de candidature flexible",
            "Entretiens adaptés (questions concrètes)",
            "Évaluation basée sur les compétences",
            "Feedback constructif systématique",
            "Accompagnement lors de l'intégration"
        ]
        
        for item in checklist:
            st.checkbox(item, value=True)
        
        # Bonnes pratiques par étape
        with st.expander("📝 Rédaction d'Offres Inclusives", expanded=False):
            st.markdown("""
            **À faire:**
            - Utiliser un langage clair et direct
            - Lister les compétences essentielles uniquement
            - Mentionner l'engagement diversité
            - Proposer des accommodations
            
            **À éviter:**
            - Jargon et métaphores
            - Listes interminables de qualifications
            - Références à la "culture fit"
            - Exigences non essentielles
            """)
        
        with st.expander("🎤 Conduite d'Entretiens Adaptés", expanded=False):
            st.markdown("""
            **Techniques recommandées:**
            - Questions concrètes et spécifiques
            - Exemples de situations réelles
            - Tests pratiques plutôt que théoriques
            - Environnement calme et prévisible
            
            **Questions à privilégier:**
            - "Décrivez comment vous aborderiez cette tâche"
            - "Montrez-nous votre processus de résolution"
            - "Quels outils utilisez-vous pour vous organiser?"
            """)
    
    with tab2:
        st.markdown("### 📊 Pipeline de Recrutement")
        
        # Funnel de recrutement
        funnel_data = {
            'Étape': ['Candidatures', 'Présélection', 'Entretien 1', 'Test Technique', 'Entretien Final', 'Offres'],
            'Candidats Neurodivers': [156, 89, 67, 58, 43, 35],
            'Candidats Standard': [1240, 620, 310, 248, 186, 124]
        }
        
        fig_funnel = go.Figure()
        
        fig_funnel.add_trace(go.Funnel(
            name='Candidats Neurodivers',
            y=funnel_data['Étape'],
            x=funnel_data['Candidats Neurodivers'],
            textinfo="value+percent initial"
        ))
        
        st.plotly_chart(fig_funnel, use_container_width=True)
        
        # Taux de conversion
        st.markdown("#### 📈 Taux de Conversion")
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Candidatures → Entretiens", "43%", "+8% vs standard")
            st.metric("Entretiens → Offres", "52%", "+12% vs standard")
        
        with col2:
            st.metric("Acceptation Offres", "89%", "+15% vs standard") 
            st.metric("Rétention 12 mois", "93%", "+18% vs standard")
    
    with tab3:
        st.markdown("### 📈 Métriques de Performance")
        
        # Performance post-embauche
        perf_data = {
            'Métrique': ['Performance Éval.', 'Innovation Score', 'Satisfaction Manager', 'Collaboration'],
            'Neurodivers': [4.3, 8.7, 4.1, 3.9],
            'Moyenne': [3.8, 7.2, 3.9, 4.2]
        }
        
        fig_perf = go.Figure()
        fig_perf.add_trace(go.Bar(
            name='Employés Neurodivers',
            x=perf_data['Métrique'],
            y=perf_data['Neurodivers'],
            marker_color='#c4bc74'
        ))
        fig_perf.add_trace(go.Bar(
            name='Moyenne Générale',
            x=perf_data['Métrique'],
            y=perf_data['Moyenne'],
            marker_color='#aca45c'
        ))
        
        fig_perf.update_layout(
            title='Performance Post-Recrutement (Score/5 ou /10)',
            barmode='group'
        )
        st.plotly_chart(fig_perf, use_container_width=True)
        
        # Sources de recrutement efficaces
        st.markdown("#### 🎯 Sources de Recrutement les Plus Efficaces")
        
        source_data = {
            'Source': ['Partenariats Asso.', 'Sites Spécialisés', 'Cooptation', 'Universités', 'LinkedIn'],
            'Candidatures': [45, 38, 29, 34, 67],
            'Embauches': [12, 8, 9, 6, 8],
            'Taux_Succès': [26.7, 21.1, 31.0, 17.6, 11.9]
        }
        
        df_sources = pd.DataFrame(source_data)
        
        fig_sources = go.Figure()
        fig_sources.add_trace(go.Scatter(
            x=df_sources['Candidatures'],
            y=df_sources['Embauches'],
            mode='markers+text',
            text=df_sources['Source'],
            textposition="top center",
            marker=dict(
                size=df_sources['Taux_Succès'],
                color=df_sources['Taux_Succès'],
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="Taux de Succès (%)")
            )
        ))
        
        fig_sources.update_layout(
            title='Efficacité des Sources de Recrutement',
            xaxis_title='Nombre de Candidatures',
            yaxis_title='Nombre d\'Embauches'
        )
        st.plotly_chart(fig_sources, use_container_width=True)

# --- ANALYTICS & REPORTING ---
def analytics_reporting():
    st.markdown("## 📈 Analytics & Reporting - Insights Avancés")
    
    tab1, tab2, tab3 = st.tabs(["📊 Dashboard Exécutif", "📋 Rapports", "🔮 Prédictions"])
    
    with tab1:
        st.markdown("### 📊 Dashboard Exécutif")
        
        # KPIs Exécutifs
        kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
        
        with kpi_col1:
            st.metric("ROI Programme", "312%", "+45%")
        with kpi_col2:
            st.metric("Coût par Accommodation", "€1,620", "-€230")
        with kpi_col3:
            st.metric("Temps Implémentation", "12 jours", "-3 jours")
        with kpi_col4:
            st.metric("Score Maturité", "8.2/10", "+1.1")
        
        # Graphique tendances business
        col1, col2 = st.columns(2)
        
        with col1:
            # Evolution ROI
            months = ['Jan', 'Fev', 'Mar', 'Avr', 'Mai', 'Juin']
            roi_evolution = [180, 210, 245, 278, 295, 312]
            
            fig_roi = go.Figure()
            fig_roi.add_trace(go.Scatter(
                x=months, 
                y=roi_evolution,
                mode='lines+markers',
                line=dict(color='#c4bc74', width=3),
                fill='tonexty'
            ))
            fig_roi.update_layout(title="Évolution ROI Programme (%)")
            st.plotly_chart(fig_roi, use_container_width=True)
        
        with col2:
            # Répartition investissements
            invest_data = {
                'Catégorie': ['Accommodations', 'Formation', 'Outils Tech', 'Évaluations'],
                'Montant': [45320, 23400, 18750, 12300]
            }
            
            fig_invest = px.pie(
                invest_data, 
                values='Montant', 
                names='Catégorie',
                title="Répartition des Investissements (€)"
            )
            st.plotly_chart(fig_invest, use_container_width=True)
    
    with tab2:
        st.markdown("### 📋 Génération de Rapports")
        
        # Générateur de rapports
        col1, col2 = st.columns(2)
        
        with col1:
            report_type = st.selectbox("Type de Rapport", [
                "Rapport Mensuel Complet",
                "Analyse ROI Détaillée", 
                "Évaluation Accommodations",
                "Performance par Département",
                "Rapport de Conformité"
            ])
            
            period = st.selectbox("Période", [
                "Dernier Mois",
                "Dernier Trimestre", 
                "6 Derniers Mois",
                "Année Courante"
            ])
        
        with col2:
            format_output = st.selectbox("Format", ["PDF", "Excel", "PowerPoint"])
            recipients = st.multiselect("Destinataires", [
                "Direction RH", "CEO", "Managers", "Équipe Neurodiversité"
            ])
        
        if st.button("🚀 Générer le Rapport"):
            progress = st.progress(0)
            status = st.empty()
            
            import time
            for i in range(100):
                progress.progress(i + 1)
                if i < 30:
                    status.text("Collecte des données...")
                elif i < 60:
                    status.text("Génération des graphiques...")
                elif i < 90:
                    status.text("Compilation du rapport...")
                else:
                    status.text("Finalisation...")
                time.sleep(0.02)
            
            st.success("✅ Rapport généré avec succès!")
            st.download_button(
                "📥 Télécharger le Rapport",
                data="Rapport généré - Données confidentielles",
                file_name=f"rapport_neurodiversite_{datetime.now().strftime('%Y%m%d')}.pdf"
            )
    
    with tab3:
        st.markdown("### 🔮 Analytics Prédictifs")
        
        # Prédictions basées sur l'IA
        st.info("🤖 Modèles prédictifs basés sur l'historique et les tendances actuelles")
        
        # Prédiction besoins accommodations
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📈 Prédiction Demandes d'Accommodations")
            
            pred_months = ['Juil', 'Août', 'Sept', 'Oct', 'Nov', 'Dec']
            current = [8, 12, 15, 11, 9, 14]
            predicted = [16, 18, 22, 19, 17, 21]
            
            fig_pred = go.Figure()
            fig_pred.add_trace(go.Scatter(
                x=pred_months, 
                y=current,
                mode='lines+markers',
                name='Historique',
                line=dict(color='#223c4c')
            ))
            fig_pred.add_trace(go.Scatter(
                x=pred_months, 
                y=predicted,
                mode='lines+markers',
                name='Prédiction',
                line=dict(color='#c4bc74', dash='dash')
            ))
            fig_pred.update_layout(title="Demandes Mensuelles Prévues")
            st.plotly_chart(fig_pred, use_container_width=True)
        
        with col2:
            st.markdown("#### 🎯 Recommandations IA")
            
            recommendations = [
                {"priority": "Haute", "action": "Augmenter budget accommodations de 25%"},
                {"priority": "Moyenne", "action": "Former 3 managers supplémentaires"},
                {"priority": "Moyenne", "action": "Développer partenariat avec asso. autisme"},
                {"priority": "Faible", "action": "Mettre à jour politique diversité"}
            ]
            
            for rec in recommendations:
                priority_color = {"Haute": "🔴", "Moyenne": "🟡", "Faible": "🟢"}
                st.markdown(f"{priority_color[rec['priority']]} **{rec['priority']}**: {rec['action']}")
        
        # Modèle de risque de turnover
        st.markdown("#### ⚠️ Analyse de Risque de Turnover")
        
        risk_data = {
            'Employé': ['Emp001', 'Emp023', 'Emp045', 'Emp067', 'Emp089'],
            'Condition': ['TDAH', 'Autisme', 'TDAH', 'Dyslexie', 'Autisme'],
            'Risque': [25, 65, 15, 45, 80],
            'Facteurs': [
                'Charge de travail élevée',
                'Accommodations insuffisantes', 
                'Adaptation en cours',
                'Changement d\'équipe',
                'Problèmes sensoriels'
            ]
        }
        
        df_risk = pd.DataFrame(risk_data)
        
        fig_risk = px.bar(
            df_risk, 
            x='Employé', 
            y='Risque',
            color='Condition',
            title="Risque de Turnover par Employé (%)"
        )
        st.plotly_chart(fig_risk, use_container_width=True)
        
        # Actions recommandées
        st.markdown("**Actions Immédiates Recommandées:**")
        for _, row in df_risk[df_risk['Risque'] > 50].iterrows():
            st.warning(f"🚨 {row['Employé']} ({row['Condition']}) - Risque {row['Risque']}%: {row['Facteurs']}")

# --- STYLES CSS ---
def apply_custom_css():
    st.markdown("""
    <style>
    /* Variables CSS */
    :root {
        --primary-color: #000000;
        --accent-color: #c4bc74;
        --dark-bg: #041e28;
        --text-light: #ffffff;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: var(--dark-bg);
    }
    
    /* Metrics styling */
    [data-testid="metric-container"] {
        background-color: rgba(196, 188, 116, 0.1);
        border: 1px solid var(--accent-color);
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Headers */
    h1, h2, h3 {
        color: var(--primary-color);
        font-weight: 600;
    }
    
    /* Buttons */
    .stButton button {
        background-color: var(--accent-color);
        color: var(--primary-color);
        border: none;
        border-radius: 0.25rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        background-color: #b5ac65;
        transform: translateY(-1px);
    }
    
    /* Success/Warning/Error messages */
    .stSuccess {
        background-color: rgba(0, 128, 0, 0.1);
        border-left: 4px solid green;
    }
    
    .stWarning {
        background-color: rgba(255, 165, 0, 0.1);
        border-left: 4px solid orange;
    }
    
    .stError {
        background-color: rgba(255, 0, 0, 0.1);
        border-left: 4px solid red;
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background-color: rgba(196, 188, 116, 0.05);
        border-radius: 0.25rem;
    }
    
    /* Tables */
    .stDataFrame {
        border-radius: 0.5rem;
        overflow: hidden;
    }
    </style>
    """, unsafe_allow_html=True)

# --- EXECUTION ---
if __name__ == "__main__":
    apply_custom_css()
    main()

    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align:center; margin-top:50px; color:#888;'>"
        "© 2025 Ubisoft – NeuroInsight Hub Workspace | Version 2.0"
        "</div>",
        unsafe_allow_html=True
    )