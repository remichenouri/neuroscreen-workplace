# NeuroInsight Hub - Workspace Dark Theme Corrigé
# Application Streamlit avec thème sombre professionnel sans problèmes d'affichage

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

# --- DONNÉES COMPLÈTES ---
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
    "performance_data": [
        {"department": "Développement", "productivity": 125, "engagement": 94, "wellbeing": 88, "neurodiverse_ratio": 28.1},
        {"department": "Design", "productivity": 122, "engagement": 91, "wellbeing": 85, "neurodiverse_ratio": 32.5},
        {"department": "Data Science", "productivity": 118, "engagement": 89, "wellbeing": 82, "neurodiverse_ratio": 35.2},
        {"department": "QA", "productivity": 128, "engagement": 87, "wellbeing": 90, "neurodiverse_ratio": 41.3},
        {"department": "Marketing", "productivity": 115, "engagement": 82, "wellbeing": 79, "neurodiverse_ratio": 19.3}
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
    # ACCOMMODATIONS EXHAUSTIVES
    "workplace_accommodations": [
        # ACCOMMODATIONS PHYSIQUES
        {"category": "Environnement Physique", "condition": "ADHD", "accommodation": "Bureau dans un espace calme", "impact": 9.2, "cost": "Faible", "implementation": "1 semaine", "description": "Bureau éloigné des zones de passage avec réduction du bruit ambiant"},
        {"category": "Environnement Physique", "condition": "ADHD", "accommodation": "Casque antibruit professionnel", "impact": 8.7, "cost": "Faible", "implementation": "Immédiat", "description": "Casque réduction de bruit active pour améliorer la concentration"},
        {"category": "Environnement Physique", "condition": "ADHD", "accommodation": "Éclairage personnalisé", "impact": 7.8, "cost": "Faible", "implementation": "3 jours", "description": "LED douce, éviter néons agressifs"},
        {"category": "Environnement Physique", "condition": "ADHD", "accommodation": "Bureau debout ou ballon stabilité", "impact": 8.1, "cost": "Moyen", "implementation": "1 semaine", "description": "Permet de bouger tout en travaillant"},
        {"category": "Environnement Physique", "condition": "ADHD", "accommodation": "Objets fidget anti-stress", "impact": 7.3, "cost": "Aucun", "implementation": "Immédiat", "description": "Balles anti-stress, cubes fidget, spinners"},
        
        {"category": "Environnement Physique", "condition": "Autism", "accommodation": "Espace de travail personnalisé", "impact": 9.4, "cost": "Faible", "implementation": "1 semaine", "description": "Organisation fixe du bureau avec objets personnels"},
        {"category": "Environnement Physique", "condition": "Autism", "accommodation": "Réduction stimuli sensoriels", "impact": 9.1, "cost": "Moyen", "implementation": "2 semaines", "description": "Contrôle température, éclairage, bruits"},
        {"category": "Environnement Physique", "condition": "Autism", "accommodation": "Espace de pause sensorielle", "impact": 8.9, "cost": "Moyen", "implementation": "1 semaine", "description": "Salle calme pour pauses"},
        
        # ACCOMMODATIONS TEMPORELLES
        {"category": "Gestion du Temps", "condition": "ADHD", "accommodation": "Horaires de travail flexibles", "impact": 8.8, "cost": "Aucun", "implementation": "Immédiat", "description": "Adapter aux pics de concentration"},
        {"category": "Gestion du Temps", "condition": "ADHD", "accommodation": "Pauses fréquentes programmées", "impact": 8.5, "cost": "Aucun", "implementation": "Immédiat", "description": "15min toutes les 2h"},
        {"category": "Gestion du Temps", "condition": "ADHD", "accommodation": "Télétravail partiel", "impact": 9.0, "cost": "Aucun", "implementation": "1 semaine", "description": "Meilleur contrôle environnement"},
        
        {"category": "Gestion du Temps", "condition": "Autism", "accommodation": "Horaires fixes prévisibles", "impact": 9.2, "cost": "Aucun", "implementation": "Immédiat", "description": "Routine quotidienne stable"},
        {"category": "Gestion du Temps", "condition": "Autism", "accommodation": "Préavis changements planning", "impact": 8.7, "cost": "Aucun", "implementation": "Immédiat", "description": "Avertir 24-48h avant"},
        
        # ACCOMMODATIONS ORGANISATIONNELLES  
        {"category": "Organisation", "condition": "ADHD", "accommodation": "Instructions écrites détaillées", "impact": 9.1, "cost": "Faible", "implementation": "3 jours", "description": "Procédures step-by-step avec check-lists"},
        {"category": "Organisation", "condition": "ADHD", "accommodation": "Outils numériques organisation", "impact": 9.3, "cost": "Moyen", "implementation": "1 semaine", "description": "Notion, Trello, Asana, rappels automatiques"},
        {"category": "Organisation", "condition": "ADHD", "accommodation": "Décomposition tâches complexes", "impact": 8.9, "cost": "Aucun", "implementation": "Immédiat", "description": "Diviser en micro-tâches gérables"},
        
        {"category": "Organisation", "condition": "Autism", "accommodation": "Documentation complète", "impact": 9.5, "cost": "Faible", "implementation": "1 semaine", "description": "Manuels exhaustifs avec exemples concrets"},
        {"category": "Organisation", "condition": "Autism", "accommodation": "Templates standardisés", "impact": 9.0, "cost": "Faible", "implementation": "3 jours", "description": "Modèles réutilisables pour tout"},
        
        # ACCOMMODATIONS TECHNOLOGIQUES
        {"category": "Technologie", "condition": "ADHD", "accommodation": "Logiciels anti-distractions", "impact": 8.6, "cost": "Faible", "implementation": "Immédiat", "description": "Cold Turkey, Freedom pour bloquer sites"},
        {"category": "Technologie", "condition": "ADHD", "accommodation": "Applications gestion temps", "impact": 8.8, "cost": "Faible", "implementation": "Immédiat", "description": "Pomodoro Timer, Toggl, RescueTime"},
        {"category": "Technologie", "condition": "ADHD", "accommodation": "Double écran", "impact": 8.1, "cost": "Moyen", "implementation": "3 jours", "description": "Vue d'ensemble des tâches"},
        
        {"category": "Technologie", "condition": "Autism", "accommodation": "Communication asynchrone", "impact": 9.1, "cost": "Aucun", "implementation": "Immédiat", "description": "Slack, Teams plutôt qu'appels"},
        {"category": "Technologie", "condition": "Autism", "accommodation": "Calendrier détaillé", "impact": 8.7, "cost": "Aucun", "implementation": "Immédiat", "description": "Agenda complet avec objectifs"},
        
        # ACCOMMODATIONS MANAGÉRIALES
        {"category": "Management", "condition": "ADHD", "accommodation": "Feedback fréquent", "impact": 9.2, "cost": "Aucun", "implementation": "Immédiat", "description": "Points hebdomadaires constructifs"},
        {"category": "Management", "condition": "ADHD", "accommodation": "Objectifs SMART clairs", "impact": 8.9, "cost": "Aucun", "implementation": "Immédiat", "description": "KPIs précis et deadlines réalistes"},
        
        {"category": "Management", "condition": "Autism", "accommodation": "Communication directe", "impact": 9.4, "cost": "Aucun", "implementation": "Immédiat", "description": "Éviter sous-entendus, être précis"},
        {"category": "Management", "condition": "Autism", "accommodation": "Manager formé autisme", "impact": 9.0, "cost": "Moyen", "implementation": "1 mois", "description": "Formation spécialisée pour manager"},
        
        # ACCOMMODATIONS RH
        {"category": "RH", "condition": "General", "accommodation": "Référent handicap dédié", "impact": 8.8, "cost": "Moyen", "implementation": "1 mois", "description": "Personne formée neurodiversité"},
        {"category": "RH", "condition": "General", "accommodation": "Évaluations adaptées", "impact": 8.5, "cost": "Aucun", "implementation": "Immédiat", "description": "Focus résultats pas méthodes"},
        {"category": "RH", "condition": "General", "accommodation": "Plan carrière personnalisé", "impact": 8.3, "cost": "Faible", "implementation": "1 mois", "description": "Évolution adaptée aux forces"}
    ],
    "recent_activities": [
        {"time": "Il y a 1h", "message": "Screening TDAH complété - Score: 67% - Marie D.", "type": "assessment", "priority": "medium"},
        {"time": "Il y a 3h", "message": "5 nouvelles accommodations implémentées", "type": "accommodation", "priority": "high"},
        {"time": "Il y a 5h", "message": "Formation manager neurodiversité - 12 participants", "type": "training", "priority": "high"},
        {"time": "Il y a 8h", "message": "Rapport mensuel analytics généré", "type": "report", "priority": "low"},
        {"time": "Il y a 1j", "message": "Évaluation autisme - 3 profils traités", "type": "assessment", "priority": "medium"}
    ]
}

# --- THÈME SOMBRE CORRIGÉ ---
def apply_dark_theme_fixed():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Variables CSS */
    :root {
        --bg-primary: #0d1117;
        --bg-secondary: #161b22;
        --bg-tertiary: #21262d;
        --bg-card: #1c2128;
        --accent-gold: #ffd700;
        --accent-blue: #58a6ff;
        --accent-green: #3fb950;
        --accent-orange: #ff8c42;
        --text-primary: #f0f6fc;
        --text-secondary: #8b949e;
        --text-muted: #6e7681;
        --border-color: #30363d;
        --hover-bg: #262c36;
    }

    /* Application du thème sombre global */
    .stApp {
        background-color: var(--bg-primary) !important;
        color: var(--text-primary) !important;
        font-family: 'Inter', sans-serif !important;
    }

    /* Header/Toolbar Streamlit sombre */
    header[data-testid="stHeader"] {
        background-color: var(--bg-secondary) !important;
        border-bottom: 1px solid var(--border-color) !important;
        height: 3.5rem !important;
    }

    .main > div {
        background-color: var(--bg-primary) !important;
        padding-top: 1rem !important;
    }

    /* Container principal */
    .main .block-container {
        background-color: transparent !important;
        padding-top: 2rem !important;
        max-width: 1400px !important;
    }

    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: var(--accent-gold) !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
    }

    h1 { font-size: 2.5rem !important; }
    h2 { font-size: 2rem !important; }
    h3 { font-size: 1.5rem !important; }

    /* Sidebar sombre */
    .css-1d391kg, .css-1cypcdb, .css-17lntkn {
        background-color: var(--bg-secondary) !important;
        border-right: 2px solid var(--accent-gold) !important;
    }
    
    .css-1d391kg .stMarkdown,
    .css-1d391kg .stMarkdown p {
        color: var(--text-primary) !important;
    }

    .css-1d391kg h1, .css-1d391kg h2, .css-1d391kg h3 {
        color: var(--accent-gold) !important;
    }

    /* Métriques */
    [data-testid="metric-container"] {
        background-color: var(--bg-card) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 12px !important;
        padding: 1.5rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
    }

    [data-testid="metric-container"]:hover {
        border-color: var(--accent-gold) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.4) !important;
    }

    [data-testid="metric-container"] [data-testid="metric-label"] {
        color: var(--text-secondary) !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
    }

    [data-testid="metric-container"] [data-testid="metric-value"] {
        color: var(--text-primary) !important;
        font-weight: 800 !important;
        font-size: 2rem !important;
    }

    /* Boutons */
    .stButton > button {
        background: linear-gradient(135deg, var(--accent-gold) 0%, #e6c200 100%) !important;
        color: var(--bg-primary) !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(255, 215, 0, 0.3) !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 20px rgba(255, 215, 0, 0.5) !important;
        background: linear-gradient(135deg, #ffdd33 0%, var(--accent-gold) 100%) !important;
    }

    /* Selectbox */
    .stSelectbox > div > div {
        background-color: var(--bg-card) !important;
        border: 2px solid var(--border-color) !important;
        border-radius: 8px !important;
        color: var(--text-primary) !important;
    }

    .stSelectbox > div > div:focus {
        border-color: var(--accent-gold) !important;
        box-shadow: 0 0 0 2px rgba(255, 215, 0, 0.2) !important;
    }

    /* Text inputs */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background-color: var(--bg-card) !important;
        border: 2px solid var(--border-color) !important;
        border-radius: 8px !important;
        color: var(--text-primary) !important;
        padding: 0.75rem !important;
    }

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--accent-gold) !important;
        box-shadow: 0 0 0 2px rgba(255, 215, 0, 0.2) !important;
    }

    /* Sliders */
    .stSlider > div > div > div > div {
        background-color: var(--accent-gold) !important;
    }

    /* Messages */
    .stSuccess {
        background-color: rgba(63, 185, 80, 0.1) !important;
        border: 1px solid var(--accent-green) !important;
        border-left: 4px solid var(--accent-green) !important;
        border-radius: 8px !important;
        color: var(--text-primary) !important;
    }

    .stWarning {
        background-color: rgba(255, 140, 66, 0.1) !important;
        border: 1px solid var(--accent-orange) !important;
        border-left: 4px solid var(--accent-orange) !important;
        border-radius: 8px !important;
        color: var(--text-primary) !important;
    }

    .stError {
        background-color: rgba(248, 81, 73, 0.1) !important;
        border: 1px solid #f85149 !important;
        border-left: 4px solid #f85149 !important;
        border-radius: 8px !important;
        color: var(--text-primary) !important;
    }

    .stInfo {
        background-color: rgba(88, 166, 255, 0.1) !important;
        border: 1px solid var(--accent-blue) !important;
        border-left: 4px solid var(--accent-blue) !important;
        border-radius: 8px !important;
        color: var(--text-primary) !important;
    }

    /* Expanders */
    .streamlit-expanderHeader {
        background-color: var(--bg-card) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 8px !important;
        color: var(--text-primary) !important;
        font-weight: 600 !important;
    }

    .streamlit-expanderHeader:hover {
        background-color: var(--hover-bg) !important;
        border-color: var(--accent-gold) !important;
    }

    .streamlit-expanderContent {
        background-color: var(--bg-card) !important;
        border: 1px solid var(--border-color) !important;
        border-top: none !important;
        border-radius: 0 0 8px 8px !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background-color: var(--bg-card) !important;
        border-radius: 12px !important;
        padding: 6px !important;
        border: 1px solid var(--border-color) !important;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: transparent !important;
        border-radius: 8px !important;
        color: var(--text-secondary) !important;
        font-weight: 600 !important;
        padding: 0.75rem 1.5rem !important;
        margin: 0 4px !important;
        border: 1px solid transparent !important;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background-color: var(--hover-bg) !important;
        color: var(--text-primary) !important;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, var(--accent-gold) 0%, #e6c200 100%) !important;
        color: var(--bg-primary) !important;
        font-weight: 700 !important;
        box-shadow: 0 2px 8px rgba(255, 215, 0, 0.3) !important;
    }

    /* Progress bars */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, var(--accent-gold) 0%, var(--accent-blue) 100%) !important;
        border-radius: 4px !important;
    }

    /* DataFrames */
    .stDataFrame {
        border-radius: 12px !important;
        overflow: hidden !important;
        border: 1px solid var(--border-color) !important;
        background-color: var(--bg-card) !important;
    }

    .stDataFrame table {
        background-color: var(--bg-card) !important;
        color: var(--text-primary) !important;
    }

    .stDataFrame th {
        background-color: var(--bg-tertiary) !important;
        color: var(--accent-gold) !important;
        font-weight: 700 !important;
        border-bottom: 1px solid var(--border-color) !important;
    }

    .stDataFrame td {
        background-color: var(--bg-card) !important;
        color: var(--text-primary) !important;
        border-bottom: 1px solid var(--border-color) !important;
    }

    /* Sidebar selectbox spécifique */
    .css-1d391kg .stSelectbox > div > div {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        color: var(--text-primary) !important;
    }

    /* Custom classes */
    .metric-card {
        background-color: var(--bg-card) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 16px !important;
        padding: 2rem !important;
        margin: 1rem 0 !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
        transition: all 0.3s ease !important;
    }

    .metric-card:hover {
        transform: translateY(-4px) !important;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.4) !important;
        border-color: var(--accent-gold) !important;
    }

    .activity-card {
        background-color: var(--bg-card) !important;
        border-left: 4px solid var(--accent-gold) !important;
        border-radius: 0 12px 12px 0 !important;
        padding: 1.5rem !important;
        margin: 1rem 0 !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2) !important;
        transition: all 0.3s ease !important;
    }

    .activity-card:hover {
        transform: translateX(8px) !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3) !important;
    }

    .highlight-card {
        background: linear-gradient(135deg, var(--bg-tertiary) 0%, var(--bg-card) 100%) !important;
        border: 1px solid var(--accent-gold) !important;
        border-radius: 16px !important;
        padding: 2rem !important;
        margin: 1.5rem 0 !important;
        box-shadow: 0 4px 16px rgba(255, 215, 0, 0.1) !important;
    }

    /* Text colors */
    .stMarkdown, p, span, div {
        color: var(--text-primary) !important;
    }

    /* Sidebar metrics */
    .sidebar-metric {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid var(--accent-gold) !important;
        border-radius: 12px !important;
        padding: 1rem !important;
        margin: 0.5rem 0 !important;
        backdrop-filter: blur(10px) !important;
    }

    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 12px;
        height: 12px;
    }

    ::-webkit-scrollbar-track {
        background-color: var(--bg-secondary);
        border-radius: 6px;
    }

    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, var(--accent-gold) 0%, #e6c200 100%);
        border-radius: 6px;
        border: 2px solid var(--bg-secondary);
    }

    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #ffdd33 0%, var(--accent-gold) 100%);
    }

    /* Masquer éléments par défaut */
    .css-1rs6os, .css-17ziqus {
        visibility: hidden;
    }

    /* Navigation toolbar sombre */
    .css-14xtw13.e8zbici0 {
        background-color: var(--bg-secondary) !important;
    }

    /* Menu hamburger sombre */
    .css-vk3wp9 {
        background-color: var(--bg-secondary) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER SOMBRE ---
def render_header():
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #161b22 0%, #21262d 100%); 
                border-radius: 16px; padding: 2rem; margin-bottom: 2rem; 
                border: 1px solid #30363d; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div style="display: flex; align-items: center; gap: 1.5rem;">
                <div style="background: linear-gradient(135deg, #ffd700 0%, #ffdd33 100%); 
                            width: 70px; height: 70px; border-radius: 16px; 
                            display: flex; align-items: center; justify-content: center; 
                            font-size: 28px; box-shadow: 0 4px 16px rgba(255, 215, 0, 0.3);">🧠</div>
                <div>
                    <h1 style="margin: 0; font-size: 28px; color: #ffd700; font-weight: 800;">
                        NeuroInsight Hub
                    </h1>
                    <p style="margin: 0; color: #8b949e; font-size: 16px; font-weight: 500;">
                        Workspace RH - Gestion Professionnelle de la Neurodiversité
                    </p>
                </div>
            </div>
            <div style="display: flex; gap: 1.5rem; align-items: center;">
                <div style="text-align: center; padding: 1rem; background: rgba(255, 255, 255, 0.05); 
                            border-radius: 12px; border: 1px solid #30363d;">
                    <div style="font-size: 24px; font-weight: 800; color: #3fb950; margin-bottom: 0.25rem;">
                        {DATA['company_metrics']['neurodiverse_employees']}
                    </div>
                    <div style="font-size: 11px; color: #8b949e; text-transform: uppercase;">
                        Employés Neurodivers
                    </div>
                </div>
                <div style="text-align: center; padding: 1rem; background: rgba(255, 255, 255, 0.05); 
                            border-radius: 12px; border: 1px solid #30363d;">
                    <div style="font-size: 24px; font-weight: 800; color: #58a6ff; margin-bottom: 0.25rem;">
                        {DATA['company_metrics']['roi_percentage']}%
                    </div>
                    <div style="font-size: 11px; color: #8b949e; text-transform: uppercase;">
                        ROI Programme
                    </div>
                </div>
                <img src="https://logos-world.net/wp-content/uploads/2021/01/Ubisoft-Logo.png" 
                     style="height: 50px; opacity: 0.8; filter: brightness(0) invert(1);">
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- SIDEBAR AMÉLIORÉE ---
def render_sidebar():
    with st.sidebar:
        # Header sidebar
        st.markdown("""
        <div style="text-align: center; padding: 2rem 1rem; margin-bottom: 2rem; 
                    border-bottom: 1px solid rgba(255, 215, 0, 0.3);">
            <div style="background: linear-gradient(135deg, #ffd700 0%, #ffdd33 100%); 
                        width: 60px; height: 60px; border-radius: 50%; 
                        display: flex; align-items: center; justify-content: center; 
                        font-size: 24px; margin: 0 auto 1rem; color: #0d1117; font-weight: bold;
                        box-shadow: 0 4px 16px rgba(255, 215, 0, 0.2);">🧠</div>
            <h2 style="color: #ffd700; margin: 0; font-size: 20px; font-weight: 800;">NeuroInsight Hub</h2>
            <p style="color: #8b949e; margin: 0.5rem 0 0 0; font-size: 14px;">
                Plateforme RH Professionnelle
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation
        st.markdown("## 🎯 Navigation")
        
        modules = [
            ("🏠", "Dashboard Principal"),
            ("🧠", "Module TDAH"), 
            ("🎯", "Module Autisme"),
            ("📊", "Observatoire"),
            ("🔬", "NeuroScreen"),
            ("🏢", "Workplace"),
            ("👥", "Recrutement"),
            ("📈", "Analytics")
        ]
        
        page = st.selectbox(
            "Choisir un module",
            options=[f"{icon} {name}" for icon, name in modules]
        )
        
        # Métriques sidebar
        st.markdown("---")
        st.markdown("### 📊 Métriques Temps Réel")
        
        for label, value, delta, color in [
            ("Employés Neurodivers", DATA['company_metrics']['neurodiverse_employees'], "+12", "#3fb950"),
            ("Taux Rétention", f"{DATA['company_metrics']['retention_rate']}%", "+2.3%", "#58a6ff"),
            ("Satisfaction", f"{DATA['company_metrics']['satisfaction_score']}/5", "+0.3", "#ffd700")
        ]:
            st.markdown(f"""
            <div class="sidebar-metric">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                    <div style="color: #f0f6fc; font-size: 18px; font-weight: 700;">{value}</div>
                    <div style="color: {color}; font-size: 12px; font-weight: 600;">↗ {delta}</div>
                </div>
                <div style="color: #8b949e; font-size: 12px;">{label}</div>
            </div>
            """, unsafe_allow_html=True)
        
        return page

# --- DASHBOARD PRINCIPAL ---
def dashboard_principal():
    st.markdown("# 🏠 Dashboard Principal")
    st.markdown("*Vue d'ensemble complète de la neurodiversité en entreprise*")
    
    # KPIs avec design sombre corrigé
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("👥 Total Employés", f"{DATA['company_metrics']['total_employees']:,}", "↗ +3.2%")
    
    with col2:
        st.metric("🧠 Neurodivers", f"{DATA['company_metrics']['neurodiverse_employees']} ({DATA['company_metrics']['neurodiverse_percentage']}%)", "↗ +2.1%")
    
    with col3:
        st.metric("📈 Productivité", f"+{DATA['company_metrics']['productivity_increase']}%", "↗ +5.3%")
    
    with col4:
        st.metric("💰 ROI", f"{DATA['company_metrics']['roi_percentage']}%", "↗ +45%")
    
    st.markdown("---")
    
    # Graphiques avec thème sombre
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Performance par Département")
        
        df_perf = pd.DataFrame(DATA['performance_data'])
        
        fig_perf = go.Figure()
        
        fig_perf.add_trace(go.Bar(
            name='Productivité',
            x=df_perf['department'],
            y=df_perf['productivity'],
            marker_color='#ffd700',
            text=df_perf['productivity'],
            textposition='auto'
        ))
        
        fig_perf.add_trace(go.Scatter(
            name='Engagement',
            x=df_perf['department'],
            y=df_perf['engagement'],
            mode='lines+markers',
            line=dict(color='#58a6ff', width=3),
            marker=dict(size=8),
            yaxis='y2'
        ))
        
        fig_perf.update_layout(
            title='Performance & Engagement',
            paper_bgcolor='#0d1117',
            plot_bgcolor='#0d1117',
            font=dict(color='#f0f6fc'),
            xaxis=dict(gridcolor='#30363d'),
            yaxis=dict(gridcolor='#30363d', title='Productivité (%)'),
            yaxis2=dict(title='Engagement (%)', overlaying='y', side='right'),
            height=400
        )
        
        st.plotly_chart(fig_perf, use_container_width=True)
    
    with col2:
        st.markdown("### 🎯 Répartition Neurodiversité")
        
        labels = ['TDAH', 'Autisme', 'Dyslexie', 'Autres']
        values = [
            DATA['company_metrics']['adhd_employees'],
            DATA['company_metrics']['autism_employees'],
            DATA['company_metrics']['dyslexia_employees'],
            DATA['company_metrics']['neurodiverse_employees'] - 
            sum([DATA['company_metrics']['adhd_employees'], 
                 DATA['company_metrics']['autism_employees'], 
                 DATA['company_metrics']['dyslexia_employees']])
        ]
        
        fig_pie = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=0.5,
            marker=dict(
                colors=['#ffd700', '#58a6ff', '#3fb950', '#ff8c42'],
                line=dict(color='#0d1117', width=2)
            )
        )])
        
        fig_pie.update_layout(
            title='Distribution par Condition',
            paper_bgcolor='#0d1117',
            font=dict(color='#f0f6fc'),
            height=400
        )
        
        st.plotly_chart(fig_pie, use_container_width=True)
    
    # Activités récentes
    st.markdown("### 📋 Activités Récentes")
    
    for activity in DATA['recent_activities']:
        icons = {"assessment": "🔍", "accommodation": "🔧", "report": "📊", "training": "🎓", "recruitment": "👤"}
        colors = {"high": "#f85149", "medium": "#ff8c42", "low": "#3fb950"}
        
        icon = icons.get(activity['type'], '•')
        color = colors.get(activity['priority'], "#8b949e")
        
        st.markdown(f"""
        <div class="activity-card">
            <div style="display: flex; align-items: center; gap: 1rem;">
                <div style="font-size: 24px;">{icon}</div>
                <div style="flex: 1;">
                    <div style="color: #f0f6fc; font-weight: 600; margin-bottom: 0.25rem;">
                        {activity['message']}
                    </div>
                    <div style="display: flex; justify-content: space-between;">
                        <span style="color: #8b949e; font-size: 12px;">{activity['time']}</span>
                        <span style="background: {color}; color: white; padding: 0.25rem 0.75rem; 
                                    border-radius: 12px; font-size: 11px; font-weight: 600;">
                            {activity['priority']}
                        </span>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# --- MODULE TDAH ---
def module_tdah():
    st.markdown("# 🧠 Module TDAH")
    st.markdown("*Trouble du Déficit de l'Attention avec ou sans Hyperactivité*")
    
    # Stats en header
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Prévalence Mondiale", "5.0%")
    with col2:
        st.metric("Adultes France", "3.0%")
    with col3:
        st.metric("Ratio H/F", "2.3:1")
    with col4:
        st.metric("Persistance Adulte", "66%")
    
    st.markdown("---")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Screening", "📊 Statistiques", "🎯 Accommodations", "📈 Analytics"])
    
    with tab1:
        st.markdown("### 🔍 Screening TDAH Professionnel")
        
        st.markdown("""
        <div class="highlight-card">
            <h4 style="color: #ffd700; margin-bottom: 1rem;">🎯 Information Importante</h4>
            <p style="color: #f0f6fc;">
                Outil d'aide au dépistage basé sur les critères cliniques DSM-5. 
                Ne remplace pas un diagnostic médical professionnel.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("🚀 Démarrer l'Évaluation TDAH", expanded=False):
            scores = {"inattention": 0, "hyperactivity": 0, "impulsivity": 0}
            
            for i, item in enumerate(DATA['screening_questions']['adhd']):
                st.markdown(f"**Question {i+1}/8** - Catégorie: {item['category'].title()}")
                st.write(item['q'])
                
                score = st.slider(
                    f"Évaluation question {i+1}",
                    min_value=0, max_value=4, value=0,
                    key=f"adhd_{i}",
                    help="0=Jamais, 1=Parfois, 2=Souvent, 3=Très souvent, 4=Constamment"
                )
                scores[item['category']] += score * item['weight']
                st.markdown("---")
            
            if st.button("🔬 Analyser les Résultats", use_container_width=True):
                total_score = sum(scores.values())
                max_possible = len(DATA['screening_questions']['adhd']) * 4 * 1.2
                percentage = (total_score / max_possible) * 100
                
                st.markdown("### 📊 Résultats de l'Évaluation")
                
                if percentage >= 60:
                    st.error(f"**Score: {percentage:.1f}%** - Probabilité élevée de TDAH")
                    st.markdown("**Recommandation:** Consultation avec un professionnel de santé spécialisé")
                elif percentage >= 40:
                    st.warning(f"**Score: {percentage:.1f}%** - Indicateurs modérés détectés")
                    st.markdown("**Recommandation:** Suivi et accommodations préventives")
                else:
                    st.success(f"**Score: {percentage:.1f}%** - Probabilité faible")
                    st.markdown("**Recommandation:** Aucune action immédiate nécessaire")
                
                # Répartition par catégorie
                col1, col2, col3 = st.columns(3)
                categories = ["inattention", "hyperactivity", "impulsivity"]
                names = ["Inattention", "Hyperactivité", "Impulsivité"]
                
                for i, (cat, name) in enumerate(zip(categories, names)):
                    with [col1, col2, col3][i]:
                        cat_pct = (scores[cat] / total_score * 100) if total_score > 0 else 0
                        st.metric(name, f"{cat_pct:.0f}%")
    
    with tab2:
        st.markdown("### 📊 Statistiques Cliniques TDAH")
        
        challenges = DATA['adhd_statistics']['workplace_challenges']
        
        fig_challenges = go.Figure([go.Bar(
            x=list(challenges.keys()),
            y=list(challenges.values()),
            marker_color=['#f85149', '#ff8c42', '#58a6ff', '#3fb950'],
            text=[f"{v}%" for v in challenges.values()],
            textposition='auto'
        )])
        
        fig_challenges.update_layout(
            title="Défis Principaux en Milieu Professionnel",
            paper_bgcolor='#0d1117',
            plot_bgcolor='#0d1117',
            font=dict(color='#f0f6fc'),
            xaxis=dict(gridcolor='#30363d'),
            yaxis=dict(gridcolor='#30363d'),
            height=400
        )
        
        st.plotly_chart(fig_challenges, use_container_width=True)
    
    with tab3:
        st.markdown("### 🎯 Accommodations Workplace")
        
        # Filtre par catégorie
        categories = list(set(acc['category'] for acc in DATA['workplace_accommodations'] if acc['condition'] == 'ADHD'))
        selected_category = st.selectbox("Filtrer par catégorie", ["Toutes"] + categories)
        
        adhd_accommodations = [acc for acc in DATA['workplace_accommodations'] if acc['condition'] == 'ADHD']
        
        if selected_category != "Toutes":
            adhd_accommodations = [acc for acc in adhd_accommodations if acc['category'] == selected_category]
        
        for acc in adhd_accommodations:
            with st.expander(f"🔧 {acc['accommodation']}", expanded=False):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Impact Score", f"{acc['impact']}/10")
                
                with col2:
                    st.metric("Coût", acc['cost'])
                
                with col3:
                    st.metric("Implémentation", acc['implementation'])
                
                st.markdown(f"**Description:** {acc['description']}")
                st.markdown(f"**Catégorie:** {acc['category']}")
                
                if st.button(f"✅ Recommander", key=f"rec_{acc['accommodation']}"):
                    st.success(f"Accommodation '{acc['accommodation']}' recommandée !")
    
    with tab4:
        st.markdown("### 📈 Analytics et Suivi TDAH")
        
        # Données simulées d'évolution
        dates = pd.date_range(start='2024-01-01', periods=12, freq='M')
        np.random.seed(42)
        
        attention_scores = []
        organisation_scores = []
        productivite_scores = []
        
        for i in range(12):
            improvement = i * 2 + np.random.normal(0, 3)
            attention_scores.append(min(95, max(40, 60 + improvement)))
            organisation_scores.append(min(95, max(35, 55 + improvement)))
            productivite_scores.append(min(95, max(45, 65 + improvement)))
        
        fig_evolution = go.Figure()
        
        fig_evolution.add_trace(go.Scatter(
            x=dates, y=attention_scores,
            mode='lines+markers',
            name='Attention',
            line=dict(color='#58a6ff', width=3)
        ))
        
        fig_evolution.add_trace(go.Scatter(
            x=dates, y=organisation_scores,
            mode='lines+markers',
            name='Organisation', 
            line=dict(color='#3fb950', width=3)
        ))
        
        fig_evolution.add_trace(go.Scatter(
            x=dates, y=productivite_scores,
            mode='lines+markers',
            name='Productivité',
            line=dict(color='#ffd700', width=3)
        ))
        
        fig_evolution.update_layout(
            title="Évolution des Métriques TDAH (N=89 employés)",
            paper_bgcolor='#0d1117',
            plot_bgcolor='#0d1117',
            font=dict(color='#f0f6fc'),
            xaxis=dict(gridcolor='#30363d'),
            yaxis=dict(gridcolor='#30363d', title='Score (%)'),
            height=500
        )
        
        st.plotly_chart(fig_evolution, use_container_width=True)
        
        # KPIs finaux
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Attention Actuelle", f"{attention_scores[-1]:.1f}%", f"+{attention_scores[-1] - attention_scores[0]:.1f}")
        with col2:
            st.metric("Organisation Actuelle", f"{organisation_scores[-1]:.1f}%", f"+{organisation_scores[-1] - organisation_scores[0]:.1f}")
        with col3:
            st.metric("Productivité Actuelle", f"{productivite_scores[-1]:.1f}%", f"+{productivite_scores[-1] - productivite_scores[0]:.1f}")

# --- FONCTION PRINCIPALE ---
def main():
    # Application du thème sombre corrigé
    apply_dark_theme_fixed()
    
    # Header
    render_header()
    
    # Sidebar et navigation
    page = render_sidebar()
    
    # Routing des modules
    if "Dashboard Principal" in page:
        dashboard_principal()
    elif "Module TDAH" in page:
        module_tdah()
    else:
        st.markdown(f"# {page}")
        st.info("🚧 Module en cours de développement avec thème sombre professionnel")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 2rem; background: #161b22; 
                border-radius: 12px; border: 1px solid #30363d; margin-top: 2rem;">
        <div style="color: #ffd700; font-weight: 700; margin-bottom: 0.5rem;">
            © 2025 Ubisoft Entertainment - NeuroInsight Hub Workspace
        </div>
        <div style="color: #8b949e; font-size: 14px;">
            Version 2.6 Dark Professional | Données Sécurisées | Conforme RGPD
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- EXÉCUTION ---
if __name__ == "__main__":
    main()
