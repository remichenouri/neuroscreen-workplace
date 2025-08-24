# NeuroInsight Hub - Version Workspace Professionnelle
# Application Streamlit avec design moderne et fonctionnalités RH avancées

import os
import json
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

# --- CONFIGURATION AVANCÉE ---
st.set_page_config(
    page_title="NeuroInsight Hub - Workspace",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.ubisoft.com',
        'Report a bug': "https://www.ubisoft.com",
        'About': "# NeuroInsight Hub\nPlateforme RH de gestion de la neurodiversité - Ubisoft"
    }
)

# --- DONNÉES ENRICHIES ---
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
        "productivity_increase": 18.5,
        "roi_percentage": 312,
        "cost_savings": 145000,
        "training_completion": 94.7
    },
    "adhd_statistics": {
        "global_prevalence": 5.0,
        "france_adults": 3.0,
        "france_children": 3.5,
        "male_female_ratio": 2.3,
        "persistence_adulthood": 66.0,
        "comorbidity_rate": 50.0,
        "workplace_challenges": {
            "Difficultés d'attention": 87.3,
            "Gestion du temps": 78.6,
            "Organisation": 82.1,
            "Impulsivité": 69.4
        },
        "success_factors": {
            "Structure claire": 94.2,
            "Feedback régulier": 89.1,
            "Pauses fréquentes": 85.7,
            "Environnement calme": 91.3
        }
    },
    "autism_statistics": {
        "global_prevalence": 1.0,
        "employment_rate": 22.0,
        "unemployment_rate": 85.0,
        "europe_population": 7000000,
        "workplace_participation": 42.0,
        "strengths": {
            "Attention aux détails": 94.2,
            "Reconnaissance de motifs": 89.7,
            "Raisonnement logique": 91.3,
            "Fiabilité": 88.9,
            "Expertise technique": 92.1,
            "Qualité du travail": 95.3
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
            {"region": "Occitanie", "tdah": 3.3, "autism": 0.8, "population": 5800000},
            {"region": "Grand Est", "tdah": 3.0, "autism": 0.9, "population": 5500000}
        ]
    },
    "performance_data": [
        {"department": "Développement", "productivity": 125, "engagement": 94, "wellbeing": 88, "neurodiverse_ratio": 28.1, "innovation": 9.2},
        {"department": "Design UX/UI", "productivity": 122, "engagement": 91, "wellbeing": 85, "neurodiverse_ratio": 32.5, "innovation": 9.4},
        {"department": "Data Science", "productivity": 118, "engagement": 89, "wellbeing": 82, "neurodiverse_ratio": 35.2, "innovation": 8.9},
        {"department": "QA Testing", "productivity": 128, "engagement": 87, "wellbeing": 90, "neurodiverse_ratio": 41.3, "innovation": 7.8},
        {"department": "Marketing", "productivity": 115, "engagement": 82, "wellbeing": 79, "neurodiverse_ratio": 19.3, "innovation": 8.1},
        {"department": "Finance", "productivity": 108, "engagement": 76, "wellbeing": 81, "neurodiverse_ratio": 11.8, "innovation": 7.1},
        {"department": "RH", "productivity": 112, "engagement": 85, "wellbeing": 87, "neurodiverse_ratio": 16.4, "innovation": 8.3}
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
        {"condition": "ADHD", "accommodation": "Environnement de travail calme", "impact": 8.5, "cost": "Faible", "implementation": "1 semaine"},
        {"condition": "ADHD", "accommodation": "Pauses régulières (15min/2h)", "impact": 7.8, "cost": "Aucun", "implementation": "Immédiat"},
        {"condition": "ADHD", "accommodation": "Outils numériques d'organisation", "impact": 9.1, "cost": "Moyen", "implementation": "2 semaines"},
        {"condition": "ADHD", "accommodation": "Instructions écrites détaillées", "impact": 8.3, "cost": "Aucun", "implementation": "Immédiat"},
        {"condition": "Autism", "accommodation": "Instructions écrites détaillées", "impact": 9.2, "cost": "Faible", "implementation": "1 jour"},
        {"condition": "Autism", "accommodation": "Horaires de travail flexibles", "impact": 8.7, "cost": "Faible", "implementation": "1 semaine"},
        {"condition": "Autism", "accommodation": "Réduction des stimuli sensoriels", "impact": 8.9, "cost": "Moyen", "implementation": "2 semaines"},
        {"condition": "Autism", "accommodation": "Communication prévisible et structurée", "impact": 9.0, "cost": "Aucun", "implementation": "Immédiat"}
    ],
    "recent_activities": [
        {"time": "Il y a 2h", "message": "Nouveau screening TDAH complété - Score: 67%", "type": "assessment", "priority": "medium"},
        {"time": "Il y a 4h", "message": "3 accommodations implémentées avec succès", "type": "accommodation", "priority": "high"},
        {"time": "Il y a 6h", "message": "Rapport mensuel généré et envoyé", "type": "report", "priority": "low"},
        {"time": "Il y a 1j", "message": "Formation managers neurodiversité - 15 participants", "type": "training", "priority": "high"},
        {"time": "Il y a 2j", "message": "5 nouveaux candidats évalués", "type": "recruitment", "priority": "medium"}
    ]
}

# --- STYLES CSS AVANCÉS ---
def apply_professional_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Variables CSS professionnelles */
    :root {
        --primary-color: #1a1a1a;
        --secondary-color: #2c2c2c;
        --accent-color: #c4bc74;
        --accent-hover: #b5ac65;
        --success-color: #10b981;
        --warning-color: #f59e0b;
        --error-color: #ef4444;
        --info-color: #3b82f6;
        --background-light: #f8fafc;
        --background-card: #ffffff;
        --text-primary: #0f172a;
        --text-secondary: #64748b;
        --border-color: #e2e8f0;
        --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        --gradient-primary: linear-gradient(135deg, #c4bc74 0%, #b5ac65 100%);
        --gradient-dark: linear-gradient(135deg, #1a1a1a 0%, #2c2c2c 100%);
    }

    /* Reset et base */
    .stApp {
        font-family: 'Inter', sans-serif;
        background: var(--background-light);
    }

    /* Sidebar moderne */
    .css-1d391kg {
        background: var(--gradient-dark) !important;
        border-right: 1px solid var(--border-color);
    }

    .css-1d391kg .stSelectbox label {
        color: white !important;
        font-weight: 500;
        font-size: 14px;
    }

    .css-1d391kg .stMarkdown {
        color: white;
    }

    .css-1d391kg h2 {
        color: var(--accent-color) !important;
        font-size: 18px !important;
        font-weight: 600 !important;
        margin-bottom: 1rem !important;
    }

    .css-1d391kg h3 {
        color: white !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        margin-top: 1.5rem !important;
    }

    /* Métriques professionnelles */
    [data-testid="metric-container"] {
        background: var(--background-card);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: var(--shadow-sm);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }

    [data-testid="metric-container"]:before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: var(--gradient-primary);
    }

    [data-testid="metric-container"]:hover {
        box-shadow: var(--shadow-md);
        transform: translateY(-2px);
    }

    [data-testid="metric-container"] [data-testid="metric-label"] {
        font-size: 14px !important;
        font-weight: 500 !important;
        color: var(--text-secondary) !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    [data-testid="metric-container"] [data-testid="metric-value"] {
        font-size: 28px !important;
        font-weight: 700 !important;
        color: var(--text-primary) !important;
        line-height: 1.2;
    }

    /* Headers avec gradient */
    h1, h2 {
        background: var(--gradient-primary);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700 !important;
        line-height: 1.2 !important;
    }

    h1 {
        font-size: 2.5rem !important;
        margin-bottom: 0.5rem !important;
    }

    h2 {
        font-size: 1.875rem !important;
        margin-top: 2rem !important;
        margin-bottom: 1rem !important;
    }

    h3 {
        color: var(--text-primary) !important;
        font-weight: 600 !important;
        font-size: 1.25rem !important;
        margin-bottom: 1rem !important;
    }

    /* Boutons modernes */
    .stButton button {
        background: var(--gradient-primary);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
        font-size: 14px;
        transition: all 0.3s ease;
        box-shadow: var(--shadow-sm);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .stButton button:hover {
        box-shadow: var(--shadow-md);
        transform: translateY(-2px);
        background: linear-gradient(135deg, #b5ac65 0%, #a89c58 100%);
    }

    /* Formulaires élégants */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {
        border: 2px solid var(--border-color);
        border-radius: 8px;
        padding: 0.75rem;
        font-size: 14px;
        transition: border-color 0.3s ease;
    }

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div > select:focus {
        border-color: var(--accent-color);
        outline: none;
        box-shadow: 0 0 0 3px rgba(196, 188, 116, 0.1);
    }

    /* Messages d'état stylisés */
    .stSuccess {
        background: rgba(16, 185, 129, 0.1) !important;
        border: 1px solid var(--success-color) !important;
        border-radius: 8px !important;
        border-left: 4px solid var(--success-color) !important;
    }

    .stWarning {
        background: rgba(245, 158, 11, 0.1) !important;
        border: 1px solid var(--warning-color) !important;
        border-radius: 8px !important;
        border-left: 4px solid var(--warning-color) !important;
    }

    .stError {
        background: rgba(239, 68, 68, 0.1) !important;
        border: 1px solid var(--error-color) !important;
        border-radius: 8px !important;
        border-left: 4px solid var(--error-color) !important;
    }

    .stInfo {
        background: rgba(59, 130, 246, 0.1) !important;
        border: 1px solid var(--info-color) !important;
        border-radius: 8px !important;
        border-left: 4px solid var(--info-color) !important;
    }

    /* Expanders modernes */
    .streamlit-expanderHeader {
        background: var(--background-card) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
        padding: 1rem !important;
        transition: all 0.3s ease;
    }

    .streamlit-expanderHeader:hover {
        background: var(--background-light) !important;
        box-shadow: var(--shadow-sm);
    }

    .streamlit-expanderContent {
        border: 1px solid var(--border-color) !important;
        border-top: none !important;
        border-radius: 0 0 8px 8px !important;
        background: var(--background-card) !important;
    }

    /* Tableaux professionnels */
    .stDataFrame {
        border-radius: 12px !important;
        overflow: hidden !important;
        box-shadow: var(--shadow-sm) !important;
        border: 1px solid var(--border-color) !important;
    }

    .stDataFrame table {
        font-size: 14px !important;
    }

    .stDataFrame th {
        background: var(--background-light) !important;
        font-weight: 600 !important;
        color: var(--text-primary) !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        padding: 1rem !important;
    }

    .stDataFrame td {
        padding: 0.75rem 1rem !important;
        border-bottom: 1px solid var(--border-color) !important;
    }

    /* Progress bars */
    .stProgress > div > div > div {
        background: var(--gradient-primary) !important;
        border-radius: 4px !important;
    }

    /* Tabs modernes */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: var(--background-card);
        padding: 4px;
        border-radius: 12px;
        border: 1px solid var(--border-color);
    }

    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding: 0 24px;
        background: transparent;
        border-radius: 8px;
        color: var(--text-secondary);
        font-weight: 500;
        transition: all 0.3s ease;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background: var(--background-light);
        color: var(--text-primary);
    }

    .stTabs [aria-selected="true"] {
        background: var(--gradient-primary) !important;
        color: white !important;
    }

    /* Cards */
    .metric-card {
        background: var(--background-card);
        border: 1px solid var(--border-color);
        border-radius: 16px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: var(--shadow-sm);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }

    .metric-card:hover {
        box-shadow: var(--shadow-md);
        transform: translateY(-4px);
    }

    .metric-card:before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: var(--gradient-primary);
    }

    /* Sliders */
    .stSlider > div > div > div {
        color: var(--accent-color) !important;
    }

    /* Checkboxes */
    .stCheckbox > label > span {
        color: var(--text-primary) !important;
        font-weight: 500;
    }

    /* Selectboxes dans sidebar */
    .css-1d391kg .stSelectbox > div > div {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 8px !important;
    }

    /* Footer */
    .footer {
        margin-top: 4rem;
        padding: 2rem 0;
        border-top: 1px solid var(--border-color);
        text-align: center;
        color: var(--text-secondary);
        font-size: 14px;
    }

    /* Custom classes */
    .highlight-card {
        background: var(--gradient-primary);
        color: white;
        padding: 2rem;
        border-radius: 16px;
        margin: 1rem 0;
        box-shadow: var(--shadow-lg);
    }

    .stat-badge {
        display: inline-block;
        background: var(--accent-color);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin: 0.25rem;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER PROFESSIONNEL ---
def render_header():
    col1, col2, col3 = st.columns([2, 3, 1])
    
    with col1:
        st.markdown("""
        <div style="display: flex; align-items: center; gap: 1rem;">
            <div style="background: linear-gradient(135deg, #c4bc74 0%, #b5ac65 100%); 
                        width: 60px; height: 60px; border-radius: 12px; 
                        display: flex; align-items: center; justify-content: center; 
                        font-size: 24px; color: white; font-weight: bold;">🧠</div>
            <div>
                <h1 style="margin: 0; font-size: 24px;">NeuroInsight Hub</h1>
                <p style="margin: 0; color: #64748b; font-size: 14px;">Workspace RH - Neurodiversité</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # KPIs rapides en header
        metric_col1, metric_col2, metric_col3 = st.columns(3)
        with metric_col1:
            st.markdown(f"""
            <div style="text-align: center; padding: 1rem; background: white; border-radius: 8px; border: 1px solid #e2e8f0;">
                <div style="font-size: 24px; font-weight: bold; color: #1a1a1a;">{DATA['company_metrics']['neurodiverse_employees']}</div>
                <div style="font-size: 12px; color: #64748b; text-transform: uppercase;">Employés Neurodivers</div>
            </div>
            """, unsafe_allow_html=True)
        
        with metric_col2:
            st.markdown(f"""
            <div style="text-align: center; padding: 1rem; background: white; border-radius: 8px; border: 1px solid #e2e8f0;">
                <div style="font-size: 24px; font-weight: bold; color: #10b981;">{DATA['company_metrics']['roi_percentage']}%</div>
                <div style="font-size: 12px; color: #64748b; text-transform: uppercase;">ROI Programme</div>
            </div>
            """, unsafe_allow_html=True)
        
        with metric_col3:
            st.markdown(f"""
            <div style="text-align: center; padding: 1rem; background: white; border-radius: 8px; border: 1px solid #e2e8f0;">
                <div style="font-size: 24px; font-weight: bold; color: #c4bc74;">{DATA['company_metrics']['satisfaction_score']}/5</div>
                <div style="font-size: 12px; color: #64748b; text-transform: uppercase;">Satisfaction</div>
            </div>
            """, unsafe_allow_html=True)
    
    with col3:
        # Logo Ubisoft
        st.image("https://logos-world.net/wp-content/uploads/2021/01/Ubisoft-Logo.png", width=100)

# --- SIDEBAR AMÉLIORÉE ---
def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 2rem 1rem; border-bottom: 1px solid rgba(255,255,255,0.1); margin-bottom: 2rem;">
            <div style="background: linear-gradient(135deg, #c4bc74 0%, #b5ac65 100%); 
                        width: 60px; height: 60px; border-radius: 50%; 
                        display: flex; align-items: center; justify-content: center; 
                        font-size: 24px; color: white; margin: 0 auto 1rem;">🧠</div>
            <h2 style="color: white; margin: 0; font-size: 20px;">NeuroInsight Hub</h2>
            <p style="color: #c4bc74; margin: 0; font-size: 14px;">Plateforme RH Professionnelle</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation
        st.markdown("## 🎯 Navigation")
        
        modules = [
            ("🏠", "Dashboard Principal"),
            ("🧠", "Module TDAH"), 
            ("🎯", "Module Autisme"),
            ("📊", "Observatoire Données"),
            ("🔬", "NeuroScreen Évaluations"),
            ("🏢", "Gestion Workplace"),
            ("👥", "Recrutement Neurodiversité"),
            ("📈", "Analytics & Reporting")
        ]
        
        page = st.selectbox(
            "Sélectionner un module",
            options=[f"{icon} {name}" for icon, name in modules],
            format_func=lambda x: x
        )
        
        # Métriques sidebar avec style amélioré
        st.markdown("---")
        st.markdown("### 📊 Métriques Temps Réel")
        
        # Métrique avec indicateur de tendance
        for label, value, delta, color in [
            ("Employés Neurodivers", DATA['company_metrics']['neurodiverse_employees'], "+12", "#10b981"),
            ("Taux de Rétention", f"{DATA['company_metrics']['retention_rate']}%", "+2.3%", "#3b82f6"),
            ("Score Satisfaction", f"{DATA['company_metrics']['satisfaction_score']}/5", "+0.3", "#c4bc74")
        ]:
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 8px; margin-bottom: 0.5rem;">
                <div style="color: white; font-size: 18px; font-weight: bold;">{value}</div>
                <div style="color: #c4bc74; font-size: 12px; margin-bottom: 0.5rem;">{label}</div>
                <div style="color: {color}; font-size: 11px;">↗ {delta}</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Alertes importantes
        st.markdown("### 🚨 Alertes Importantes")
        st.markdown("""
        <div style="background: rgba(245, 158, 11, 0.2); border: 1px solid #f59e0b; 
                    border-radius: 8px; padding: 1rem; margin-bottom: 1rem;">
            <div style="color: #f59e0b; font-weight: bold; font-size: 12px;">⚠️ ATTENTION</div>
            <div style="color: white; font-size: 14px;">5 demandes d'accommodation en attente</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Progression mensuelle
        st.markdown("### 📈 Progression Mensuelle")
        progress_value = 73
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 8px;">
            <div style="color: white; font-size: 14px; margin-bottom: 0.5rem;">Objectifs Atteints</div>
            <div style="background: rgba(255,255,255,0.2); height: 8px; border-radius: 4px; overflow: hidden;">
                <div style="background: linear-gradient(90deg, #c4bc74, #b5ac65); height: 100%; width: {progress_value}%;"></div>
            </div>
            <div style="color: #c4bc74; font-size: 12px; margin-top: 0.5rem;">{progress_value}% complété</div>
        </div>
        """, unsafe_allow_html=True)
        
        return page

# --- DASHBOARD PRINCIPAL AMÉLIORÉ ---
def dashboard_principal():
    st.markdown("# 🏠 Dashboard Principal")
    st.markdown("*Vue d'ensemble de la neurodiversité en entreprise*")
    
    # KPIs principaux avec design moderne
    st.markdown("### 📊 Métriques Clés")
    
    col1, col2, col3, col4 = st.columns(4)
    
    metrics_data = [
        ("👥 Total Employés", DATA['company_metrics']['total_employees'], "↗ +3.2%", "#3b82f6"),
        ("🧠 Employés Neurodivers", f"{DATA['company_metrics']['neurodiverse_employees']} ({DATA['company_metrics']['neurodiverse_percentage']}%)", "↗ +2.1%", "#10b981"),
        ("📈 Productivité", f"+{DATA['company_metrics']['productivity_increase']}%", "↗ +5.3%", "#c4bc74"),
        ("💰 ROI", f"{DATA['company_metrics']['roi_percentage']}%", "↗ +45%", "#f59e0b")
    ]
    
    for i, (label, value, delta, color) in enumerate(metrics_data):
        with [col1, col2, col3, col4][i]:
            st.markdown(f"""
            <div class="metric-card">
                <div style="color: {color}; font-size: 14px; font-weight: 600; margin-bottom: 0.5rem; text-transform: uppercase;">{label}</div>
                <div style="font-size: 32px; font-weight: bold; color: #1a1a1a; margin-bottom: 0.5rem;">{value}</div>
                <div style="color: #10b981; font-size: 14px; font-weight: 500;">{delta}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Section graphiques avec layout amélioré
    col1, col2 = st.columns([1.2, 1])
    
    with col1:
        st.markdown("### 📈 Performance par Département")
        
        # Graphique performance amélioré
        df_perf = pd.DataFrame(DATA['performance_data'])
        
        fig_performance = go.Figure()
        
        # Barres de productivité
        fig_performance.add_trace(go.Bar(
            name='Productivité',
            x=df_perf['department'],
            y=df_perf['productivity'],
            marker=dict(
                color='#c4bc74',
                line=dict(color='#b5ac65', width=1)
            ),
            text=df_perf['productivity'],
            textposition='auto',
            hovertemplate='<b>%{x}</b><br>Productivité: %{y}%<extra></extra>'
        ))
        
        # Ligne d'engagement
        fig_performance.add_trace(go.Scatter(
            name='Engagement',
            x=df_perf['department'],
            y=df_perf['engagement'],
            mode='lines+markers',
            line=dict(color='#10b981', width=3),
            marker=dict(size=8, color='#10b981'),
            yaxis='y2',
            hovertemplate='<b>%{x}</b><br>Engagement: %{y}%<extra></extra>'
        ))
        
        fig_performance.update_layout(
            title={
                'text': 'Productivité et Engagement par Département',
                'x': 0.5,
                'font': {'size': 16, 'family': 'Inter'}
            },
            xaxis_title='Département',
            yaxis_title='Productivité (%)',
            yaxis2=dict(
                title='Engagement (%)',
                overlaying='y',
                side='right'
            ),
            hovermode='x unified',
            template='plotly_white',
            height=400,
            font=dict(family='Inter'),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        st.plotly_chart(fig_performance, use_container_width=True)
    
    with col2:
        st.markdown("### 🎯 Répartition Neurodiversité")
        
        # Donut chart moderne
        labels = ['TDAH', 'Autisme', 'Dyslexie', 'Autres conditions']
        values = [
            DATA['company_metrics']['adhd_employees'],
            DATA['company_metrics']['autism_employees'],
            DATA['company_metrics']['dyslexia_employees'],
            DATA['company_metrics']['neurodiverse_employees'] - 
            DATA['company_metrics']['adhd_employees'] - 
            DATA['company_metrics']['autism_employees'] - 
            DATA['company_metrics']['dyslexia_employees']
        ]
        
        colors = ['#c4bc74', '#3b82f6', '#10b981', '#f59e0b']
        
        fig_donut = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=0.6,
            marker=dict(colors=colors, line=dict(color='white', width=2)),
            textinfo='label+percent',
            textfont=dict(size=12, family='Inter'),
            hovertemplate='<b>%{label}</b><br>%{value} employés (%{percent})<extra></extra>'
        )])
        
        fig_donut.update_layout(
            title={
                'text': 'Distribution des Conditions',
                'x': 0.5,
                'font': {'size': 16, 'family': 'Inter'}
            },
            height=400,
            font=dict(family='Inter'),
            showlegend=True,
            legend=dict(
                orientation="v",
                yanchor="middle",
                y=0.5,
                xanchor="left",
                x=1.05
            )
        )
        
        # Annotation au centre
        fig_donut.add_annotation(
            text=f"<b>{DATA['company_metrics']['neurodiverse_employees']}</b><br>Total",
            x=0.5, y=0.5,
            font_size=20,
            showarrow=False
        )
        
        st.plotly_chart(fig_donut, use_container_width=True)
    
    # Section activités avec design amélioré
    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        st.markdown("### 📋 Activités Récentes")
        
        for activity in DATA['recent_activities']:
            icon = {
                "assessment": "🔍", 
                "accommodation": "🔧", 
                "report": "📊", 
                "training": "🎓", 
                "recruitment": "👤"
            }
            
            priority_colors = {
                "high": "#ef4444",
                "medium": "#f59e0b", 
                "low": "#10b981"
            }
            
            color = priority_colors.get(activity['priority'], "#64748b")
            
            st.markdown(f"""
            <div style="background: white; border-left: 4px solid {color}; 
                        padding: 1rem; margin-bottom: 0.5rem; border-radius: 0 8px 8px 0; 
                        box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                <div style="display: flex; align-items: center; gap: 1rem;">
                    <div style="font-size: 24px;">{icon.get(activity['type'], '•')}</div>
                    <div style="flex: 1;">
                        <div style="font-weight: 500; color: #1a1a1a; margin-bottom: 0.25rem;">
                            {activity['message']}
                        </div>
                        <div style="font-size: 12px; color: #64748b;">
                            {activity['time']} • Priorité: {activity['priority']}
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 🎯 Objectifs du Mois")
        
        objectives = [
            {"name": "Screenings TDAH", "current": 23, "target": 30, "color": "#c4bc74"},
            {"name": "Accommodations", "current": 18, "target": 20, "color": "#3b82f6"},
            {"name": "Formations", "current": 12, "target": 15, "color": "#10b981"},
            {"name": "Évaluations", "current": 8, "target": 10, "color": "#f59e0b"}
        ]
        
        for obj in objectives:
            progress = (obj['current'] / obj['target']) * 100
            st.markdown(f"""
            <div style="background: white; padding: 1rem; margin-bottom: 1rem; 
                        border-radius: 8px; border: 1px solid #e2e8f0;">
                <div style="display: flex; justify-content: between; margin-bottom: 0.5rem;">
                    <span style="font-weight: 500; color: #1a1a1a;">{obj['name']}</span>
                    <span style="color: {obj['color']}; font-weight: bold;">{obj['current']}/{obj['target']}</span>
                </div>
                <div style="background: #f1f5f9; height: 8px; border-radius: 4px; overflow: hidden;">
                    <div style="background: {obj['color']}; height: 100%; width: {progress}%; transition: width 0.3s ease;"></div>
                </div>
                <div style="font-size: 12px; color: #64748b; margin-top: 0.25rem;">{progress:.1f}% complété</div>
            </div>
            """, unsafe_allow_html=True)

# --- MODULE TDAH AMÉLIORÉ ---
def module_tdah():
    st.markdown("# 🧠 Module TDAH")
    st.markdown("*Trouble du Déficit de l'Attention avec ou sans Hyperactivité*")
    
    # Header avec statistiques clés
    col1, col2, col3, col4 = st.columns(4)
    
    stats = [
        ("Prévalence Mondiale", "5.0%", "#3b82f6"),
        ("Adultes France", "3.0%", "#10b981"),
        ("Ratio H/F", "2.3:1", "#c4bc74"),
        ("Persistance Adulte", "66%", "#f59e0b")
    ]
    
    for i, (label, value, color) in enumerate(stats):
        with [col1, col2, col3, col4][i]:
            st.markdown(f"""
            <div style="text-align: center; background: white; padding: 1.5rem; 
                        border-radius: 12px; border: 1px solid #e2e8f0; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                <div style="color: {color}; font-size: 28px; font-weight: bold; margin-bottom: 0.5rem;">{value}</div>
                <div style="color: #64748b; font-size: 14px; font-weight: 500;">{label}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Onglets avec design moderne
    tab1, tab2, tab3, tab4 = st.tabs([
        "📋 Screening Interactif", 
        "📊 Statistiques", 
        "🎯 Accommodations", 
        "📈 Suivi & Analytics"
    ])
    
    with tab1:
        st.markdown("### 🔍 Screening TDAH Professionnel")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("""
            <div class="highlight-card">
                <h4 style="color: white; margin-bottom: 1rem;">🎯 Information Importante</h4>
                <p style="color: white; margin: 0;">
                Ce screening est un outil d'aide au dépistage basé sur les critères cliniques reconnus. 
                Il ne remplace pas un diagnostic médical professionnel.
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background: white; padding: 2rem; border-radius: 16px; 
                        border: 1px solid #e2e8f0; text-align: center;">
                <div style="font-size: 48px; margin-bottom: 1rem;">🧠</div>
                <div style="font-size: 18px; font-weight: bold; color: #1a1a1a; margin-bottom: 0.5rem;">
                    Évaluation TDAH
                </div>
                <div style="color: #64748b; font-size: 14px;">
                    Basée sur DSM-5
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Questionnaire interactif amélioré
        with st.expander("🚀 Démarrer l'Évaluation TDAH", expanded=False):
            scores = {"inattention": 0, "hyperactivity": 0, "impulsivity": 0}
            
            st.markdown("""
            <div style="background: #f8fafc; padding: 1.5rem; border-radius: 8px; border: 1px solid #e2e8f0; margin-bottom: 2rem;">
                <h5 style="color: #1a1a1a; margin-bottom: 1rem;">📝 Instructions</h5>
                <p style="color: #64748b; margin: 0;">
                Évaluez chaque affirmation selon votre expérience des <strong>6 derniers mois</strong> :
                </p>
                <ul style="color: #64748b; margin-top: 0.5rem;">
                    <li><strong>0:</strong> Jamais ou rarement</li>
                    <li><strong>1:</strong> Parfois</li>
                    <li><strong>2:</strong> Souvent</li>
                    <li><strong>3:</strong> Très souvent</li>
                    <li><strong>4:</strong> Constamment</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            # Questions avec design amélioré
            for i, item in enumerate(DATA['screening_questions']['adhd']):
                category_colors = {
                    "inattention": "#3b82f6",
                    "hyperactivity": "#10b981", 
                    "impulsivity": "#f59e0b"
                }
                
                color = category_colors.get(item['category'], "#64748b")
                category_name = {
                    "inattention": "Inattention",
                    "hyperactivity": "Hyperactivité",
                    "impulsivity": "Impulsivité"
                }.get(item['category'], item['category'])
                
                st.markdown(f"""
                <div style="background: white; padding: 1.5rem; margin-bottom: 1rem; 
                            border-radius: 12px; border: 1px solid #e2e8f0; 
                            border-left: 4px solid {color};">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                        <span style="font-weight: 500; color: #1a1a1a;">Question {i+1}/8</span>
                        <span class="stat-badge" style="background: {color};">{category_name}</span>
                    </div>
                    <p style="color: #1a1a1a; font-size: 16px; margin-bottom: 1rem; font-weight: 500;">
                        {item['q']}
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                score = st.slider(
                    f"Niveau pour la question {i+1}",
                    min_value=0, max_value=4, value=0,
                    key=f"adhd_{i}",
                    help=f"Catégorie: {category_name}"
                )
                scores[item['category']] += score * item['weight']
            
            # Bouton d'évaluation stylé
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                if st.button("🔬 Analyser les Résultats", use_container_width=True):
                    total_score = sum(scores.values())
                    max_possible = len(DATA['screening_questions']['adhd']) * 4 * 1.2
                    percentage = (total_score / max_possible) * 100
                    
                    st.markdown("### 📊 Résultats de l'Évaluation")
                    
                    # Résultats avec design professionnel
                    if percentage >= 60:
                        st.markdown(f"""
                        <div style="background: rgba(239, 68, 68, 0.1); border: 2px solid #ef4444; 
                                    border-radius: 16px; padding: 2rem; margin: 2rem 0;">
                            <div style="text-align: center;">
                                <div style="font-size: 48px; margin-bottom: 1rem;">⚠️</div>
                                <div style="font-size: 32px; font-weight: bold; color: #ef4444; margin-bottom: 1rem;">
                                    {percentage:.1f}%
                                </div>
                                <div style="font-size: 18px; font-weight: 600; color: #1a1a1a; margin-bottom: 1rem;">
                                    Probabilité Élevée de TDAH
                                </div>
                                <div style="color: #64748b;">
                                    Recommandation : Consultation avec un professionnel de santé pour évaluation approfondie
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    elif percentage >= 40:
                        st.markdown(f"""
                        <div style="background: rgba(245, 158, 11, 0.1); border: 2px solid #f59e0b; 
                                    border-radius: 16px; padding: 2rem; margin: 2rem 0;">
                            <div style="text-align: center;">
                                <div style="font-size: 48px; margin-bottom: 1rem;">⚠️</div>
                                <div style="font-size: 32px; font-weight: bold; color: #f59e0b; margin-bottom: 1rem;">
                                    {percentage:.1f}%
                                </div>
                                <div style="font-size: 18px; font-weight: 600; color: #1a1a1a; margin-bottom: 1rem;">
                                    Indicateurs Modérés
                                </div>
                                <div style="color: #64748b;">
                                    Recommandation : Suivi et mise en place d'accommodations préventives
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div style="background: rgba(16, 185, 129, 0.1); border: 2px solid #10b981; 
                                    border-radius: 16px; padding: 2rem; margin: 2rem 0;">
                            <div style="text-align: center;">
                                <div style="font-size: 48px; margin-bottom: 1rem;">✅</div>
                                <div style="font-size: 32px; font-weight: bold; color: #10b981; margin-bottom: 1rem;">
                                    {percentage:.1f}%
                                </div>
                                <div style="font-size: 18px; font-weight: 600; color: #1a1a1a; margin-bottom: 1rem;">
                                    Probabilité Faible
                                </div>
                                <div style="color: #64748b;">
                                    Aucune action immédiate nécessaire
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Répartition par catégorie
                    st.markdown("### 📊 Analyse Détaillée par Catégorie")
                    
                    col1, col2, col3 = st.columns(3)
                    categories = ["inattention", "hyperactivity", "impulsivity"]
                    category_names = ["Inattention", "Hyperactivité", "Impulsivité"]
                    category_colors = ["#3b82f6", "#10b981", "#f59e0b"]
                    
                    for i, (cat, name, color) in enumerate(zip(categories, category_names, category_colors)):
                        with [col1, col2, col3][i]:
                            cat_percentage = (scores[cat] / total_score * 100) if total_score > 0 else 0
                            st.markdown(f"""
                            <div style="background: white; padding: 1.5rem; border-radius: 12px; 
                                        border: 1px solid #e2e8f0; text-align: center; 
                                        border-top: 4px solid {color};">
                                <div style="font-size: 24px; font-weight: bold; color: {color}; margin-bottom: 0.5rem;">
                                    {cat_percentage:.0f}%
                                </div>
                                <div style="color: #1a1a1a; font-weight: 500;">{name}</div>
                            </div>
                            """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("### 📊 Statistiques et Données Cliniques TDAH")
        
        # Graphique défis workplace avec amélioration
        challenges = DATA['adhd_statistics']['workplace_challenges']
        
        fig_challenges = go.Figure()
        
        fig_challenges.add_trace(go.Bar(
            x=list(challenges.keys()),
            y=list(challenges.values()),
            marker=dict(
                color=['#ef4444', '#f59e0b', '#3b82f6', '#10b981'],
                line=dict(color='white', width=1)
            ),
            text=[f"{v}%" for v in challenges.values()],
            textposition='auto',
            textfont=dict(color='white', size=14, family='Inter'),
            hovertemplate='<b>%{x}</b><br>%{y}% des employés TDAH<extra></extra>'
        ))
        
        fig_challenges.update_layout(
            title={
                'text': 'Défis Principaux en Milieu Professionnel',
                'x': 0.5,
                'font': {'size': 18, 'family': 'Inter'}
            },
            xaxis_title='Type de Défi',
            yaxis_title='Pourcentage d\'Employés Concernés (%)',
            template='plotly_white',
            height=400,
            font=dict(family='Inter'),
            showlegend=False
        )
        
        st.plotly_chart(fig_challenges, use_container_width=True)
        
        # Facteurs de succès
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🎯 Facteurs de Succès au Travail")
            success_factors = DATA['adhd_statistics']['success_factors']
            
            for factor, percentage in success_factors.items():
                st.markdown(f"""
                <div style="background: white; padding: 1rem; margin-bottom: 0.5rem; 
                            border-radius: 8px; border: 1px solid #e2e8f0;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="color: #1a1a1a; font-weight: 500;">{factor}</span>
                        <span style="color: #10b981; font-weight: bold;">{percentage}%</span>
                    </div>
                    <div style="background: #f1f5f9; height: 6px; border-radius: 3px; margin-top: 0.5rem;">
                        <div style="background: #10b981; height: 100%; width: {percentage}%; border-radius: 3px;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("#### 📈 Données Épidémiologiques")
            
            epidemio_data = [
                ("Prévalence mondiale", "5.0%", "Population générale"),
                ("Adultes France", "3.0%", "Diagnostics confirmés"),
                ("Persistance à l'âge adulte", "66%", "Depuis l'enfance"),
                ("Comorbidités", "50%", "Autres troubles"),
                ("Ratio Hommes/Femmes", "2.3:1", "Chez les adultes")
            ]
            
            for title, value, desc in epidemio_data:
                st.markdown(f"""
                <div style="background: white; padding: 1rem; margin-bottom: 0.5rem; 
                            border-radius: 8px; border: 1px solid #e2e8f0;">
                    <div style="font-weight: 600; color: #1a1a1a; margin-bottom: 0.25rem;">{title}</div>
                    <div style="font-size: 24px; font-weight: bold; color: #c4bc74; margin-bottom: 0.25rem;">{value}</div>
                    <div style="color: #64748b; font-size: 12px;">{desc}</div>
                </div>
                """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown("### 🎯 Accommodations Workplace Recommandées")
        
        tdah_accommodations = [acc for acc in DATA['workplace_accommodations'] if acc['condition'] == 'ADHD']
        
        for acc in tdah_accommodations:
            # Couleur selon l'impact
            if acc['impact'] >= 9:
                impact_color = "#10b981"
                impact_label = "Impact Élevé"
            elif acc['impact'] >= 7.5:
                impact_color = "#f59e0b"
                impact_label = "Impact Modéré"
            else:
                impact_color = "#3b82f6"
                impact_label = "Impact Faible"
            
            # Couleur selon le coût
            cost_colors = {"Aucun": "#10b981", "Faible": "#f59e0b", "Moyen": "#ef4444"}
            cost_color = cost_colors[acc['cost']]
            
            with st.expander(f"🔧 {acc['accommodation']}", expanded=False):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f"""
                    <div style="text-align: center; padding: 1rem; background: white; 
                                border-radius: 8px; border: 2px solid {impact_color};">
                        <div style="font-size: 28px; font-weight: bold; color: {impact_color};">
                            {acc['impact']}/10
                        </div>
                        <div style="color: #64748b; font-size: 12px; margin-top: 0.5rem;">
                            {impact_label}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div style="text-align: center; padding: 1rem; background: white; 
                                border-radius: 8px; border: 2px solid {cost_color};">
                        <div style="font-size: 18px; font-weight: bold; color: {cost_color};">
                            {acc['cost']}
                        </div>
                        <div style="color: #64748b; font-size: 12px; margin-top: 0.5rem;">
                            Niveau de Coût
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    st.markdown(f"""
                    <div style="text-align: center; padding: 1rem; background: white; 
                                border-radius: 8px; border: 2px solid #3b82f6;">
                        <div style="font-size: 18px; font-weight: bold; color: #3b82f6;">
                            {acc['implementation']}
                        </div>
                        <div style="color: #64748b; font-size: 12px; margin-top: 0.5rem;">
                            Temps d'Implémentation
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Bouton d'action
                if st.button(f"✅ Recommander cette accommodation", key=f"recommend_{acc['accommodation']}"):
                    st.success(f"✅ Accommodation '{acc['accommodation']}' ajoutée aux recommandations !")
    
    with tab4:
        st.markdown("### 📈 Suivi et Analytics TDAH")
        
        # Simulation de données d'évolution
        dates = pd.date_range(start='2024-01-01', periods=12, freq='M')
        
        # Données plus réalistes
        base_attention = 60
        base_organisation = 55
        base_productivite = 65
        
        attention_scores = []
        organisation_scores = []
        productivite_scores = []
        
        for i in range(12):
            # Amélioration progressive avec variations
            improvement_factor = i * 0.8 + np.random.normal(0, 2)
            
            attention = min(100, max(30, base_attention + improvement_factor + np.random.normal(0, 3)))
            organisation = min(100, max(30, base_organisation + improvement_factor + np.random.normal(0, 2.5)))
            productivite = min(100, max(30, base_productivite + improvement_factor + np.random.normal(0, 3.5)))
            
            attention_scores.append(attention)
            organisation_scores.append(organisation)
            productivite_scores.append(productivite)
        
        progress_data = {
            'Date': dates,
            'Attention': attention_scores,
            'Organisation': organisation_scores,
            'Productivité': productivite_scores
        }
        
        df_progress = pd.DataFrame(progress_data)
        
        fig_progress = go.Figure()
        
        # Ligne attention
        fig_progress.add_trace(go.Scatter(
            x=df_progress['Date'],
            y=df_progress['Attention'],
            mode='lines+markers',
            name='Attention',
            line=dict(color='#3b82f6', width=3),
            marker=dict(size=8),
            hovertemplate='<b>Attention</b><br>Date: %{x}<br>Score: %{y:.1f}%<extra></extra>'
        ))
        
        # Ligne organisation
        fig_progress.add_trace(go.Scatter(
            x=df_progress['Date'],
            y=df_progress['Organisation'],
            mode='lines+markers',
            name='Organisation',
            line=dict(color='#10b981', width=3),
            marker=dict(size=8),
            hovertemplate='<b>Organisation</b><br>Date: %{x}<br>Score: %{y:.1f}%<extra></extra>'
        ))
        
        # Ligne productivité
        fig_progress.add_trace(go.Scatter(
            x=df_progress['Date'],
            y=df_progress['Productivité'],
            mode='lines+markers',
            name='Productivité',
            line=dict(color='#c4bc74', width=3),
            marker=dict(size=8),
            hovertemplate='<b>Productivité</b><br>Date: %{x}<br>Score: %{y:.1f}%<extra></extra>'
        ))
        
        fig_progress.update_layout(
            title={
                'text': 'Évolution des Métriques TDAH (Moyenne des Employés)',
                'x': 0.5,
                'font': {'size': 18, 'family': 'Inter'}
            },
            xaxis_title='Période',
            yaxis_title='Score (%)',
            hovermode='x unified',
            template='plotly_white',
            height=500,
            font=dict(family='Inter'),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        # Zone d'amélioration
        fig_progress.add_shape(
            type="rect",
            x0=dates[0], x1=dates[-1],
            y0=75, y1=100,
            fillcolor="rgba(16, 185, 129, 0.1)",
            line=dict(width=0),
            layer="below"
        )
        
        fig_progress.add_annotation(
            x=dates[6], y=87.5,
            text="Zone d'Excellence",
            showarrow=False,
            font=dict(size=12, color="#10b981")
        )
        
        st.plotly_chart(fig_progress, use_container_width=True)
        
        # KPIs d'amélioration
        col1, col2, col3 = st.columns(3)
        
        current_scores = [attention_scores[-1], organisation_scores[-1], productivite_scores[-1]]
        initial_scores = [attention_scores[0], organisation_scores[0], productivite_scores[0]]
        improvements = [(curr - init) for curr, init in zip(current_scores, initial_scores)]
        
        metrics = ["Attention", "Organisation", "Productivité"]
        colors = ["#3b82f6", "#10b981", "#c4bc74"]
        
        for i, (metric, current, improvement, color) in enumerate(zip(metrics, current_scores, improvements, colors)):
            with [col1, col2, col3][i]:
                st.markdown(f"""
                <div style="background: white; padding: 2rem; border-radius: 16px; 
                            border: 1px solid #e2e8f0; text-align: center; 
                            border-top: 4px solid {color};">
                    <div style="color: {color}; font-size: 28px; font-weight: bold; margin-bottom: 0.5rem;">
                        {current:.1f}%
                    </div>
                    <div style="color: #1a1a1a; font-weight: 600; margin-bottom: 0.5rem;">{metric}</div>
                    <div style="color: #10b981; font-size: 14px; font-weight: 500;">
                        {'+' if improvement > 0 else ''}{improvement:.1f}% cette année
                    </div>
                </div>
                """, unsafe_allow_html=True)

# --- FONCTION PRINCIPALE ---
def main():
    # Application du CSS
    apply_professional_css()
    
    # Header professionnel
    render_header()
    
    # Sidebar
    page = render_sidebar()
    
    # Routing des modules
    if "Dashboard Principal" in page:
        dashboard_principal()
    elif "Module TDAH" in page:
        module_tdah()
    # ... autres modules à implémenter
    
    # Footer professionnel
    st.markdown("""
    <div class="footer">
        <p>© 2025 Ubisoft Entertainment - NeuroInsight Hub Workspace | Version 2.1 Professional</p>
        <p style="font-size: 12px; margin-top: 0.5rem;">
            Plateforme RH de gestion de la neurodiversité • Données sécurisées • Conforme RGPD
        </p>
    </div>
    """, unsafe_allow_html=True)

# --- EXECUTION ---
if __name__ == "__main__":
    main()
