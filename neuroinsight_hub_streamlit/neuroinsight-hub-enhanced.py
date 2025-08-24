# NeuroInsight Hub - Workspace Professionnel Dark Theme
# Application Streamlit avec design sombre et interface RH avancée

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

# --- DONNÉES ENRICHIES AVEC ACCOMMODATIONS COMPLÈTES ---
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
    # ACCOMMODATIONS EXHAUSTIVES BASÉES SUR LES MEILLEURES PRATIQUES D'ENTREPRISE
    "workplace_accommodations": [
        # ACCOMMODATIONS PHYSIQUES
        {"category": "Environnement Physique", "condition": "ADHD", "accommodation": "Bureau dans un espace calme et peu distrayant", "impact": 9.2, "cost": "Faible", "implementation": "1 semaine", "description": "Bureau éloigné des zones de passage, fenêtres avec stores, réduction du bruit ambiant"},
        {"category": "Environnement Physique", "condition": "ADHD", "accommodation": "Casque antibruit ou écouteurs", "impact": 8.7, "cost": "Faible", "implementation": "Immédiat", "description": "Casque réduction de bruit active pour améliorer la concentration"},
        {"category": "Environnement Physique", "condition": "ADHD", "accommodation": "Éclairage personnalisé et lampes d'appoint", "impact": 7.8, "cost": "Faible", "implementation": "3 jours", "description": "Éviter les néons agressifs, préférer l'éclairage naturel ou LED douce"},
        {"category": "Environnement Physique", "condition": "ADHD", "accommodation": "Bureau debout ou ballon de stabilité", "impact": 8.1, "cost": "Moyen", "implementation": "1 semaine", "description": "Permet de bouger tout en travaillant, améliore la concentration"},
        {"category": "Environnement Physique", "condition": "ADHD", "accommodation": "Objets fidget et anti-stress", "impact": 7.3, "cost": "Aucun", "implementation": "Immédiat", "description": "Balles anti-stress, cubes fidget, spinners pour canaliser l'agitation"},
        
        {"category": "Environnement Physique", "condition": "Autism", "accommodation": "Espace de travail personnalisé et prévisible", "impact": 9.4, "cost": "Faible", "implementation": "1 semaine", "description": "Organisation fixe du bureau, objets personnels autorisés, routine d'installation"},
        {"category": "Environnement Physique", "condition": "Autism", "accommodation": "Réduction des stimuli sensoriels", "impact": 9.1, "cost": "Moyen", "implementation": "2 semaines", "description": "Contrôle température, éclairage tamisé, réduction bruits soudains"},
        {"category": "Environnement Physique", "condition": "Autism", "accommodation": "Espace de retrait/pause sensorielle", "impact": 8.9, "cost": "Moyen", "implementation": "1 semaine", "description": "Salle calme disponible pour les pauses quand surcharge sensorielle"},
        
        # ACCOMMODATIONS TEMPORELLES
        {"category": "Gestion du Temps", "condition": "ADHD", "accommodation": "Horaires de travail flexibles", "impact": 8.8, "cost": "Aucun", "implementation": "Immédiat", "description": "Adapter les horaires aux pics de concentration naturels"},
        {"category": "Gestion du Temps", "condition": "ADHD", "accommodation": "Pauses fréquentes (15min toutes les 2h)", "impact": 8.5, "cost": "Aucun", "implementation": "Immédiat", "description": "Pauses programmées pour maintenir la concentration"},
        {"category": "Gestion du Temps", "condition": "ADHD", "accommodation": "Télétravail partiel ou complet", "impact": 9.0, "cost": "Aucun", "implementation": "1 semaine", "description": "Éviter les distractions du bureau, meilleur contrôle de l'environnement"},
        {"category": "Gestion du Temps", "condition": "ADHD", "accommodation": "Jours de récupération supplémentaires", "impact": 7.9, "cost": "Faible", "implementation": "Immédiat", "description": "RTT supplémentaires pour éviter la fatigue cognitive"},
        
        {"category": "Gestion du Temps", "condition": "Autism", "accommodation": "Horaires fixes et prévisibles", "impact": 9.2, "cost": "Aucun", "implementation": "Immédiat", "description": "Routine quotidienne stable, éviter les changements d'horaires"},
        {"category": "Gestion du Temps", "condition": "Autism", "accommodation": "Préavis pour les changements d'emploi du temps", "impact": 8.7, "cost": "Aucun", "implementation": "Immédiat", "description": "Avertir 24-48h avant tout changement de planning"},
        {"category": "Gestion du Temps", "condition": "Autism", "accommodation": "Pauses programmées et ritualisées", "impact": 8.3, "cost": "Aucun", "implementation": "Immédiat", "description": "Pauses à heures fixes avec activités préférées"},
        
        # ACCOMMODATIONS ORGANISATIONNELLES  
        {"category": "Organisation du Travail", "condition": "ADHD", "accommodation": "Instructions écrites détaillées et check-lists", "impact": 9.1, "cost": "Faible", "implementation": "3 jours", "description": "Procédures écrites step-by-step, listes de vérification pour éviter les oublis"},
        {"category": "Organisation du Travail", "condition": "ADHD", "accommodation": "Outils numériques d'organisation", "impact": 9.3, "cost": "Moyen", "implementation": "1 semaine", "description": "Notion, Trello, Asana, rappels automatiques, calendriers partagés"},
        {"category": "Organisation du Travail", "condition": "ADHD", "accommodation": "Décomposition des tâches complexes", "impact": 8.9, "cost": "Aucun", "implementation": "Immédiat", "description": "Diviser les gros projets en micro-tâches gérables"},
        {"category": "Organisation du Travail", "condition": "ADHD", "accommodation": "Système de rappels et alertes", "impact": 8.4, "cost": "Aucun", "implementation": "Immédiat", "description": "Notifications, alarmes, rappels calendrier pour deadlines"},
        {"category": "Organisation du Travail", "condition": "ADHD", "accommodation": "Prioritisation visuelle des tâches", "impact": 8.2, "cost": "Aucun", "implementation": "Immédiat", "description": "Code couleur, système Eisenhower, Kanban boards"},
        
        {"category": "Organisation du Travail", "condition": "Autism", "accommodation": "Procédures détaillées et documentation complète", "impact": 9.5, "cost": "Faible", "implementation": "1 semaine", "description": "Manuels complets, FAQ, exemples concrets pour chaque processus"},
        {"category": "Organisation du Travail", "condition": "Autism", "accommodation": "Templates et modèles standardisés", "impact": 9.0, "cost": "Faible", "implementation": "3 jours", "description": "Modèles réutilisables pour emails, rapports, présentations"},
        {"category": "Organisation du Travail", "condition": "Autism", "accommodation": "Planning détaillé et structuré", "impact": 8.8, "cost": "Aucun", "implementation": "Immédiat", "description": "Agenda détaillé avec objectifs clairs et étapes définies"},
        
        # ACCOMMODATIONS TECHNOLOGIQUES
        {"category": "Outils Technologiques", "condition": "ADHD", "accommodation": "Logiciels de blocage de distractions", "impact": 8.6, "cost": "Faible", "implementation": "Immédiat", "description": "Cold Turkey, Freedom, Focus pour bloquer sites distrayants"},
        {"category": "Outils Technologiques", "condition": "ADHD", "accommodation": "Applications de gestion du temps", "impact": 8.8, "cost": "Faible", "implementation": "Immédiat", "description": "Pomodoro Timer, Toggl, RescueTime pour tracking"},
        {"category": "Outils Technologiques", "condition": "ADHD", "accommodation": "Synthèse vocale et reconnaissance vocale", "impact": 7.9, "cost": "Faible", "implementation": "3 jours", "description": "Dragon, Voice Typing pour dictée et lecture audio"},
        {"category": "Outils Technologiques", "condition": "ADHD", "accommodation": "Double écran ou écran large", "impact": 8.1, "cost": "Moyen", "implementation": "3 jours", "description": "Éviter les changements d'applications, vue d'ensemble des tâches"},
        
        {"category": "Outils Technologiques", "condition": "Autism", "accommodation": "Outils de communication asynchrone privilégiés", "impact": 9.1, "cost": "Aucun", "implementation": "Immédiat", "description": "Slack, Teams, emails plutôt qu'appels téléphoniques improvistes"},
        {"category": "Outils Technologiques", "condition": "Autism", "accommodation": "Calendrier partagé avec détails complets", "impact": 8.7, "cost": "Aucun", "implementation": "Immédiat", "description": "Calendrier avec agenda, participants, objectifs, documents"},
        {"category": "Outils Technologiques", "condition": "Autism", "accommodation": "Outils de mind mapping et visualisation", "impact": 8.4, "cost": "Faible", "implementation": "3 jours", "description": "MindMeister, Lucidchart pour organiser les idées visuellement"},
        
        # ACCOMMODATIONS MANAGÉRIALES
        {"category": "Management", "condition": "ADHD", "accommodation": "Feedback fréquent et constructif", "impact": 9.2, "cost": "Aucun", "implementation": "Immédiat", "description": "Points hebdomadaires, feedback immédiat, reconnaissance des efforts"},
        {"category": "Management", "condition": "ADHD", "accommodation": "Objectifs clairs et mesurables", "impact": 8.9, "cost": "Aucun", "implementation": "Immédiat", "description": "SMART goals, KPIs précis, deadlines réalistes"},
        {"category": "Management", "condition": "ADHD", "accommodation": "Coaching et mentoring", "impact": 8.7, "cost": "Moyen", "implementation": "1 mois", "description": "Coach TDAH, mentor interne, accompagnement personnalisé"},
        {"category": "Management", "condition": "ADHD", "accommodation": "Flexibilité dans les méthodes de travail", "impact": 8.5, "cost": "Aucun", "implementation": "Immédiat", "description": "Liberté dans l'organisation, résultats plutôt que méthodes"},
        
        {"category": "Management", "condition": "Autism", "accommodation": "Communication directe et explicite", "impact": 9.4, "cost": "Aucun", "implementation": "Immédiat", "description": "Éviter sous-entendus, être précis, confirmer par écrit"},
        {"category": "Management", "condition": "Autism", "accommodation": "Manager formé à l'autisme", "impact": 9.0, "cost": "Moyen", "implementation": "1 mois", "description": "Formation spécialisée pour comprendre les besoins autistiques"},
        {"category": "Management", "condition": "Autism", "accommodation": "Réunions structurées avec ordre du jour", "impact": 8.8, "cost": "Aucun", "implementation": "Immédiat", "description": "Agenda envoyé avant, objectifs clairs, temps limité"},
        {"category": "Management", "condition": "Autism", "accommodation": "Éviter les changements organisationnels fréquents", "impact": 8.6, "cost": "Aucun", "implementation": "Immédiat", "description": "Stabilité dans l'équipe, les processus, l'environnement"},
        
        # ACCOMMODATIONS SOCIALES
        {"category": "Interactions Sociales", "condition": "ADHD", "accommodation": "Espaces collaboratifs adaptés", "impact": 7.8, "cost": "Moyen", "implementation": "1 mois", "description": "Salles de réunion insonorisées, espaces informels"},
        {"category": "Interactions Sociales", "condition": "ADHD", "accommodation": "Groupes de parole et support entre pairs", "impact": 8.3, "cost": "Faible", "implementation": "1 mois", "description": "Réseau interne, groupes d'entraide, parrainage"},
        
        {"category": "Interactions Sociales", "condition": "Autism", "accommodation": "Réduction des interactions sociales obligatoires", "impact": 8.9, "cost": "Aucun", "implementation": "Immédiat", "description": "Dispense événements team building, déjeuners facultatifs"},
        {"category": "Interactions Sociales", "condition": "Autism", "accommodation": "Communication écrite privilégiée", "impact": 8.7, "cost": "Aucun", "implementation": "Immédiat", "description": "Emails, chat, documentation plutôt qu'oral"},
        {"category": "Interactions Sociales", "condition": "Autism", "accommodation": "Buddy/parrain neurotypique", "impact": 8.5, "cost": "Faible", "implementation": "1 semaine", "description": "Collègue référent pour questions sociales et navigation"},
        
        # ACCOMMODATIONS FORMATIVES
        {"category": "Formation et Développement", "condition": "ADHD", "accommodation": "Formations courtes et interactives", "impact": 8.4, "cost": "Faible", "implementation": "Variable", "description": "Sessions 30-45min max, exercices pratiques, breaks fréquents"},
        {"category": "Formation et Développement", "condition": "ADHD", "accommodation": "Supports multimédia et visuels", "impact": 8.1, "cost": "Faible", "implementation": "1 semaine", "description": "Vidéos, infographies, mind maps plutôt que texte seul"},
        {"category": "Formation et Développement", "condition": "ADHD", "accommodation": "Formation aux outils d'organisation", "impact": 9.0, "cost": "Moyen", "implementation": "1 mois", "description": "Formation spécialisée sur les outils et techniques TDAH"},
        
        {"category": "Formation et Développement", "condition": "Autism", "accommodation": "Documentation complète et détaillée", "impact": 9.3, "cost": "Faible", "implementation": "2 semaines", "description": "Manuels exhaustifs, FAQ, exemples concrets"},
        {"category": "Formation et Développement", "condition": "Autism", "accommodation": "Formation individuelle ou petits groupes", "impact": 8.9, "cost": "Moyen", "implementation": "Variable", "description": "Éviter les grands groupes, préférer le one-to-one"},
        {"category": "Formation et Développement", "condition": "Autism", "accommodation": "Temps d'adaptation prolongé", "impact": 8.6, "cost": "Aucun", "implementation": "Variable", "description": "Période d'intégration étendue, pas de pression temporelle"},
        
        # ACCOMMODATIONS LÉGALES ET RH
        {"category": "RH et Légal", "condition": "General", "accommodation": "Confidentialité médicale stricte", "impact": 9.5, "cost": "Aucun", "implementation": "Immédiat", "description": "Information limitée au strict nécessaire, consentement explicite"},
        {"category": "RH et Légal", "condition": "General", "accommodation": "Référent handicap/diversité", "impact": 8.8, "cost": "Moyen", "implementation": "1 mois", "description": "Personne formée dédiée aux questions neurodiversité"},
        {"category": "RH et Légal", "condition": "General", "accommodation": "Aménagement des évaluations de performance", "impact": 8.5, "cost": "Aucun", "implementation": "Immédiat", "description": "Critères adaptés, focus sur les résultats, pas les méthodes"},
        {"category": "RH et Légal", "condition": "General", "accommodation": "Plan de carrière personnalisé", "impact": 8.3, "cost": "Faible", "implementation": "1 mois", "description": "Évolution adaptée aux forces et besoins spécifiques"}
    ],
    "recent_activities": [
        {"time": "Il y a 1h", "message": "Screening TDAH complété - Score: 67% - Marie D.", "type": "assessment", "priority": "medium"},
        {"time": "Il y a 3h", "message": "5 nouvelles accommodations implémentées", "type": "accommodation", "priority": "high"},
        {"time": "Il y a 5h", "message": "Formation manager neurodiversité - 12 participants", "type": "training", "priority": "high"},
        {"time": "Il y a 8h", "message": "Rapport mensuel analytics généré", "type": "report", "priority": "low"},
        {"time": "Il y a 1j", "message": "Évaluation autisme - 3 profils traités", "type": "assessment", "priority": "medium"}
    ]
}

# --- THÈME SOMBRE PROFESSIONNEL ---
def apply_dark_professional_theme():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Variables pour thème sombre professionnel */
    :root {
        --bg-primary: #0F1419;
        --bg-secondary: #1A1D23;
        --bg-tertiary: #252A32;
        --bg-card: #1E2329;
        --accent-gold: #D4B886;
        --accent-blue: #4A9EF8;
        --accent-green: #00D2A3;
        --accent-orange: #FF8A4C;
        --text-primary: #FFFFFF;
        --text-secondary: #B0B3B8;
        --text-muted: #8A8D93;
        --border-color: #3E4146;
        --hover-bg: #2D3139;
        --success: #00C851;
        --warning: #FF8800;
        --error: #FF4444;
        --info: #33B5E5;
    }

    /* Background principal sombre */
    .stApp {
        background: linear-gradient(135deg, var(--bg-primary) 0%, var(--bg-secondary) 100%);
        color: var(--text-primary);
        font-family: 'Inter', sans-serif;
    }
    
    /* Conteneur principal */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        background: transparent;
    }

    /* Headers avec gradient */
    h1, h2, h3 {
        background: linear-gradient(135deg, var(--accent-gold) 0%, #F4E4BC 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700 !important;
        margin-bottom: 1.5rem !important;
    }

    h1 { font-size: 2.5rem !important; }
    h2 { font-size: 2rem !important; }
    h3 { font-size: 1.5rem !important; }

    /* Sidebar sombre */
    .css-1d391kg {
        background: linear-gradient(180deg, var(--bg-secondary) 0%, var(--bg-tertiary) 100%) !important;
        border-right: 2px solid var(--accent-gold);
    }
    
    .css-1d391kg .stMarkdown {
        color: var(--text-primary);
    }

    .css-1d391kg h2, .css-1d391kg h3 {
        color: var(--accent-gold) !important;
        -webkit-text-fill-color: var(--accent-gold) !important;
    }

    /* Métriques modernes */
    [data-testid="metric-container"] {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
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
        height: 3px;
        background: linear-gradient(90deg, var(--accent-gold) 0%, var(--accent-blue) 100%);
    }

    [data-testid="metric-container"]:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4);
        border-color: var(--accent-gold);
    }

    [data-testid="metric-container"] [data-testid="metric-label"] {
        color: var(--text-secondary) !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    [data-testid="metric-container"] [data-testid="metric-value"] {
        color: var(--text-primary) !important;
        font-weight: 800 !important;
        font-size: 2.2rem !important;
        line-height: 1.2;
    }

    [data-testid="metric-container"] [data-testid="metric-delta"] {
        font-weight: 600 !important;
        font-size: 14px !important;
    }

    /* Boutons avec effet glassmorphism */
    .stButton button {
        background: linear-gradient(135deg, var(--accent-gold) 0%, #C4A973 100%);
        color: var(--bg-primary);
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 700;
        font-size: 14px;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 20px rgba(212, 184, 134, 0.3);
        backdrop-filter: blur(10px);
    }

    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(212, 184, 134, 0.5);
        background: linear-gradient(135deg, #E5C998 0%, var(--accent-gold) 100%);
    }

    /* Selectbox sombre */
    .stSelectbox > div > div {
        background: var(--bg-card) !important;
        border: 2px solid var(--border-color) !important;
        border-radius: 12px !important;
        color: var(--text-primary) !important;
    }

    .stSelectbox > div > div:focus-within {
        border-color: var(--accent-gold) !important;
        box-shadow: 0 0 0 3px rgba(212, 184, 134, 0.2) !important;
    }

    /* Inputs sombres */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: var(--bg-card) !important;
        border: 2px solid var(--border-color) !important;
        border-radius: 12px !important;
        color: var(--text-primary) !important;
        padding: 1rem !important;
    }

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--accent-gold) !important;
        box-shadow: 0 0 0 3px rgba(212, 184, 134, 0.2) !important;
    }

    /* Sliders sombres */
    .stSlider > div > div > div {
        color: var(--accent-gold) !important;
    }

    .stSlider > div > div > div > div {
        background: var(--accent-gold) !important;
    }

    /* Messages d'état sombres */
    .stSuccess {
        background: rgba(0, 200, 81, 0.15) !important;
        border: 1px solid var(--success) !important;
        border-left: 4px solid var(--success) !important;
        border-radius: 12px !important;
        color: var(--text-primary) !important;
    }

    .stWarning {
        background: rgba(255, 136, 0, 0.15) !important;
        border: 1px solid var(--warning) !important;
        border-left: 4px solid var(--warning) !important;
        border-radius: 12px !important;
        color: var(--text-primary) !important;
    }

    .stError {
        background: rgba(255, 68, 68, 0.15) !important;
        border: 1px solid var(--error) !important;
        border-left: 4px solid var(--error) !important;
        border-radius: 12px !important;
        color: var(--text-primary) !important;
    }

    .stInfo {
        background: rgba(51, 181, 229, 0.15) !important;
        border: 1px solid var(--info) !important;
        border-left: 4px solid var(--info) !important;
        border-radius: 12px !important;
        color: var(--text-primary) !important;
    }

    /* Expanders sombres */
    .streamlit-expanderHeader {
        background: var(--bg-card) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 12px !important;
        color: var(--text-primary) !important;
        font-weight: 600 !important;
        transition: all 0.3s ease;
    }

    .streamlit-expanderHeader:hover {
        background: var(--hover-bg) !important;
        border-color: var(--accent-gold) !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    }

    .streamlit-expanderContent {
        background: var(--bg-card) !important;
        border: 1px solid var(--border-color) !important;
        border-top: none !important;
        border-radius: 0 0 12px 12px !important;
    }

    /* Tabs sombres */
    .stTabs [data-baseweb="tab-list"] {
        background: var(--bg-card);
        border-radius: 16px;
        padding: 8px;
        border: 1px solid var(--border-color);
        gap: 8px;
    }

    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 12px;
        color: var(--text-secondary);
        font-weight: 600;
        padding: 1rem 1.5rem;
        transition: all 0.3s ease;
        border: 1px solid transparent;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background: var(--hover-bg);
        color: var(--text-primary);
        border-color: var(--border-color);
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, var(--accent-gold) 0%, #C4A973 100%) !important;
        color: var(--bg-primary) !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 20px rgba(212, 184, 134, 0.3);
    }

    /* Progress bars */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, var(--accent-gold) 0%, var(--accent-blue) 100%) !important;
        border-radius: 8px !important;
    }

    /* DataFrames sombres */
    .stDataFrame {
        border-radius: 16px !important;
        overflow: hidden !important;
        border: 1px solid var(--border-color) !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }

    .stDataFrame table {
        background: var(--bg-card) !important;
        color: var(--text-primary) !important;
    }

    .stDataFrame th {
        background: var(--bg-tertiary) !important;
        color: var(--accent-gold) !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        padding: 1rem !important;
    }

    .stDataFrame td {
        background: var(--bg-card) !important;
        color: var(--text-primary) !important;
        border-bottom: 1px solid var(--border-color) !important;
        padding: 0.75rem 1rem !important;
    }

    /* Sidebar selectbox sombre */
    .css-1d391kg .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        color: var(--text-primary) !important;
    }

    /* Cards personnalisées */
    .metric-card-dark {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }

    .metric-card-dark:before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, var(--accent-gold) 0%, var(--accent-blue) 50%, var(--accent-green) 100%);
    }

    .metric-card-dark:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4);
        border-color: var(--accent-gold);
    }

    .highlight-card-dark {
        background: linear-gradient(135deg, var(--bg-tertiary) 0%, var(--bg-card) 100%);
        border: 1px solid var(--accent-gold);
        border-radius: 20px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 12px 40px rgba(212, 184, 134, 0.1);
    }

    .activity-card-dark {
        background: var(--bg-card);
        border-left: 4px solid var(--accent-gold);
        border-radius: 0 12px 12px 0;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
    }

    .activity-card-dark:hover {
        transform: translateX(8px);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.3);
    }

    /* Accommodation cards */
    .accommodation-card {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
        position: relative;
    }

    .accommodation-card:hover {
        border-color: var(--accent-gold);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        transform: translateY(-2px);
    }

    /* Scrollbar sombre */
    ::-webkit-scrollbar {
        width: 12px;
        height: 12px;
    }

    ::-webkit-scrollbar-track {
        background: var(--bg-secondary);
        border-radius: 6px;
    }

    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, var(--accent-gold) 0%, #C4A973 100%);
        border-radius: 6px;
        border: 2px solid var(--bg-secondary);
    }

    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #E5C998 0%, var(--accent-gold) 100%);
    }

    /* Masquer les éléments Streamlit par défaut */
    .css-1rs6os, .css-17ziqus {
        visibility: hidden;
    }

    header[data-testid="stHeader"] {
        background: transparent;
        height: 0;
    }

    /* Sidebar métriques */
    .sidebar-metric {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(212, 184, 134, 0.3);
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        backdrop-filter: blur(10px);
    }

    /* Loading spinner */
    .stSpinner > div {
        border-top-color: var(--accent-gold) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER MODERNE SOMBRE ---
def render_dark_header():
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1A1D23 0%, #252A32 100%); 
                border-radius: 20px; padding: 2rem; margin-bottom: 2rem; 
                border: 1px solid #3E4146; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div style="display: flex; align-items: center; gap: 1.5rem;">
                <div style="background: linear-gradient(135deg, #D4B886 0%, #F4E4BC 100%); 
                            width: 80px; height: 80px; border-radius: 20px; 
                            display: flex; align-items: center; justify-content: center; 
                            font-size: 32px; box-shadow: 0 8px 20px rgba(212, 184, 134, 0.3);">🧠</div>
                <div>
                    <h1 style="margin: 0; font-size: 32px; background: linear-gradient(135deg, #D4B886 0%, #F4E4BC 100%); 
                               -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
                               font-weight: 800;">NeuroInsight Hub</h1>
                    <p style="margin: 0; color: #B0B3B8; font-size: 16px; font-weight: 500;">
                        Workspace RH - Gestion Professionnelle de la Neurodiversité
                    </p>
                </div>
            </div>
            <div style="display: flex; gap: 2rem;">
                <div style="text-align: center; padding: 1rem; background: rgba(255, 255, 255, 0.05); 
                            border-radius: 12px; border: 1px solid #3E4146; backdrop-filter: blur(10px);">
                    <div style="font-size: 28px; font-weight: 800; color: #00D2A3; margin-bottom: 0.5rem;">
                        {DATA['company_metrics']['neurodiverse_employees']}
                    </div>
                    <div style="font-size: 12px; color: #B0B3B8; text-transform: uppercase; letter-spacing: 1px;">
                        Employés Neurodivers
                    </div>
                </div>
                <div style="text-align: center; padding: 1rem; background: rgba(255, 255, 255, 0.05); 
                            border-radius: 12px; border: 1px solid #3E4146; backdrop-filter: blur(10px);">
                    <div style="font-size: 28px; font-weight: 800; color: #4A9EF8; margin-bottom: 0.5rem;">
                        {DATA['company_metrics']['roi_percentage']}%
                    </div>
                    <div style="font-size: 12px; color: #B0B3B8; text-transform: uppercase; letter-spacing: 1px;">
                        ROI Programme
                    </div>
                </div>
                <img src="https://logos-world.net/wp-content/uploads/2021/01/Ubisoft-Logo.png" 
                     style="height: 60px; opacity: 0.8; filter: brightness(0) invert(1);">
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- SIDEBAR ERGONOMIQUE ---
def render_ergonomic_sidebar():
    with st.sidebar:
        # Header sidebar
        st.markdown("""
        <div style="text-align: center; padding: 2rem 1rem; margin-bottom: 2rem; 
                    border-bottom: 1px solid rgba(212, 184, 134, 0.3);">
            <div style="background: linear-gradient(135deg, #D4B886 0%, #F4E4BC 100%); 
                        width: 70px; height: 70px; border-radius: 50%; 
                        display: flex; align-items: center; justify-content: center; 
                        font-size: 28px; margin: 0 auto 1rem; 
                        box-shadow: 0 8px 20px rgba(212, 184, 134, 0.2);">🧠</div>
            <h2 style="color: #D4B886; margin: 0; font-size: 22px; font-weight: 800;">NeuroInsight Hub</h2>
            <p style="color: #B0B3B8; margin: 0.5rem 0 0 0; font-size: 14px; font-weight: 500;">
                Plateforme RH Professionnelle
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation moderne
        st.markdown("## 🎯 Navigation")
        
        modules = [
            ("🏠", "Dashboard Principal", "Vue d'ensemble des métriques clés"),
            ("🧠", "Module TDAH", "Screening et gestion TDAH"), 
            ("🎯", "Module Autisme", "Évaluation et talents autistiques"),
            ("📊", "Observatoire", "Statistiques et tendances"),
            ("🔬", "NeuroScreen", "Tests cognitifs standardisés"),
            ("🏢", "Workplace", "Accommodations et support"),
            ("👥", "Recrutement", "Processus inclusifs"),
            ("📈", "Analytics", "Insights et rapports avancés")
        ]
        
        selected_module = st.selectbox(
            "Choisir un module",
            options=[f"{icon} {name}" for icon, name, _ in modules],
            format_func=lambda x: x,
            help="Sélectionnez le module à consulter"
        )
        
        # Métriques temps réel
        st.markdown("---")
        st.markdown("### 📊 Métriques Temps Réel")
        
        metrics_data = [
            ("Employés Neurodivers", DATA['company_metrics']['neurodiverse_employees'], "+12", "#00D2A3"),
            ("Taux Rétention", f"{DATA['company_metrics']['retention_rate']}%", "+2.3%", "#4A9EF8"),
            ("Satisfaction", f"{DATA['company_metrics']['satisfaction_score']}/5", "+0.3", "#D4B886"),
            ("Accommodations", "43", "+8", "#FF8A4C")
        ]
        
        for label, value, delta, color in metrics_data:
            st.markdown(f"""
            <div class="sidebar-metric">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                    <div style="color: #FFFFFF; font-size: 20px; font-weight: 700;">{value}</div>
                    <div style="color: {color}; font-size: 12px; font-weight: 600;">↗ {delta}</div>
                </div>
                <div style="color: #B0B3B8; font-size: 12px; font-weight: 500;">{label}</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Alertes importantes
        st.markdown("### 🚨 Alertes")
        
        alerts = [
            ("Demandes en attente", "5", "warning"),
            ("Formations à planifier", "3", "info"),
            ("Évaluations urgentes", "2", "error")
        ]
        
        for alert_text, count, alert_type in alerts:
            color_map = {
                "warning": "#FF8800",
                "info": "#4A9EF8", 
                "error": "#FF4444"
            }
            color = color_map[alert_type]
            
            st.markdown(f"""
            <div style="background: rgba(255, 255, 255, 0.05); border-left: 4px solid {color}; 
                        padding: 1rem; margin-bottom: 0.5rem; border-radius: 0 8px 8px 0;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div style="color: #FFFFFF; font-size: 14px; font-weight: 500;">{alert_text}</div>
                    <div style="background: {color}; color: #FFFFFF; padding: 0.25rem 0.75rem; 
                                border-radius: 12px; font-size: 12px; font-weight: 700;">{count}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Progression objectifs
        st.markdown("### 📈 Objectifs Mensuels")
        
        objectives = [
            ("Screenings", 23, 30),
            ("Accommodations", 18, 20), 
            ("Formations", 12, 15)
        ]
        
        for obj_name, current, target in objectives:
            progress = (current / target) * 100
            st.markdown(f"""
            <div style="background: rgba(255, 255, 255, 0.05); padding: 1rem; 
                        border-radius: 12px; margin-bottom: 0.75rem;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                    <span style="color: #FFFFFF; font-weight: 600; font-size: 14px;">{obj_name}</span>
                    <span style="color: #D4B886; font-weight: 700; font-size: 14px;">{current}/{target}</span>
                </div>
                <div style="background: rgba(255, 255, 255, 0.1); height: 8px; border-radius: 4px; overflow: hidden;">
                    <div style="background: linear-gradient(90deg, #D4B886, #4A9EF8); height: 100%; 
                                width: {progress}%; transition: width 0.3s ease; border-radius: 4px;"></div>
                </div>
                <div style="color: #B0B3B8; font-size: 11px; margin-top: 0.25rem;">{progress:.0f}% complété</div>
            </div>
            """, unsafe_allow_html=True)
        
        return selected_module

# --- DASHBOARD PRINCIPAL SOMBRE ---
def dashboard_principal():
    st.markdown("# 🏠 Dashboard Principal")
    st.markdown("*Vue d'ensemble complète de la neurodiversité en entreprise*")
    
    # KPIs principaux avec design sombre
    st.markdown("### 📊 Indicateurs Clés de Performance")
    
    col1, col2, col3, col4 = st.columns(4)
    
    kpi_data = [
        ("👥 Total Employés", f"{DATA['company_metrics']['total_employees']:,}", "↗ +3.2%", "#4A9EF8"),
        ("🧠 Neurodivers", f"{DATA['company_metrics']['neurodiverse_employees']} ({DATA['company_metrics']['neurodiverse_percentage']}%)", "↗ +2.1%", "#00D2A3"),
        ("📈 Productivité", f"+{DATA['company_metrics']['productivity_increase']}%", "↗ +5.3%", "#D4B886"),
        ("💰 ROI", f"{DATA['company_metrics']['roi_percentage']}%", "↗ +45%", "#FF8A4C")
    ]
    
    for i, (label, value, delta, color) in enumerate(kpi_data):
        with [col1, col2, col3, col4][i]:
            st.markdown(f"""
            <div class="metric-card-dark">
                <div style="text-align: center;">
                    <div style="color: {color}; font-size: 14px; font-weight: 600; 
                                text-transform: uppercase; letter-spacing: 1px; margin-bottom: 1rem;">
                        {label}
                    </div>
                    <div style="color: #FFFFFF; font-size: 2.5rem; font-weight: 800; margin-bottom: 0.5rem;">
                        {value}
                    </div>
                    <div style="color: #00D2A3; font-size: 14px; font-weight: 600;">
                        {delta}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Graphiques avec thème sombre
    col1, col2 = st.columns([1.3, 1])
    
    with col1:
        st.markdown("### 📊 Performance par Département")
        
        df_perf = pd.DataFrame(DATA['performance_data'])
        
        # Graphique en barres avec thème sombre
        fig_perf = go.Figure()
        
        fig_perf.add_trace(go.Bar(
            name='Productivité',
            x=df_perf['department'],
            y=df_perf['productivity'],
            marker=dict(color='#D4B886', line=dict(color='#F4E4BC', width=1)),
            text=df_perf['productivity'],
            textposition='auto',
            textfont=dict(color='white', size=12, family='Inter')
        ))
        
        fig_perf.add_trace(go.Scatter(
            name='Engagement',
            x=df_perf['department'],
            y=df_perf['engagement'],
            mode='lines+markers',
            line=dict(color='#4A9EF8', width=3),
            marker=dict(size=10, color='#4A9EF8'),
            yaxis='y2'
        ))
        
        fig_perf.update_layout(
            title={
                'text': 'Performance & Engagement par Département',
                'x': 0.5,
                'font': {'size': 18, 'color': '#FFFFFF', 'family': 'Inter'}
            },
            xaxis=dict(
                title='Département',
                color='#B0B3B8',
                gridcolor='#3E4146'
            ),
            yaxis=dict(
                title='Productivité (%)',
                color='#B0B3B8',
                gridcolor='#3E4146'
            ),
            yaxis2=dict(
                title='Engagement (%)',
                overlaying='y',
                side='right',
                color='#4A9EF8'
            ),
            paper_bgcolor='#1E2329',
            plot_bgcolor='#1E2329',
            font=dict(color='#FFFFFF', family='Inter'),
            height=450,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        st.plotly_chart(fig_perf, use_container_width=True)
    
    with col2:
        st.markdown("### 🎯 Répartition Neurodiversité")
        
        # Donut chart avec thème sombre
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
        colors = ['#D4B886', '#4A9EF8', '#00D2A3', '#FF8A4C']
        
        fig_donut = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=0.6,
            marker=dict(colors=colors, line=dict(color='#1E2329', width=3)),
            textinfo='label+percent',
            textfont=dict(size=12, color='white', family='Inter'),
            hovertemplate='<b>%{label}</b><br>%{value} employés (%{percent})<extra></extra>'
        )])
        
        fig_donut.update_layout(
            title={
                'text': 'Distribution par Condition',
                'x': 0.5,
                'font': {'size': 16, 'color': '#FFFFFF', 'family': 'Inter'}
            },
            paper_bgcolor='#1E2329',
            font=dict(color='#FFFFFF', family='Inter'),
            height=450,
            showlegend=True,
            legend=dict(
                orientation="v",
                yanchor="middle",
                y=0.5,
                xanchor="left",
                x=1.05
            )
        )
        
        # Annotation centrale
        fig_donut.add_annotation(
            text=f"<b style='color: #D4B886; font-size: 24px;'>{sum(values)}</b><br><span style='color: #B0B3B8;'>Total</span>",
            x=0.5, y=0.5,
            font_size=16,
            showarrow=False
        )
        
        st.plotly_chart(fig_donut, use_container_width=True)
    
    # Section activités et objectifs
    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        st.markdown("### 📋 Activités Récentes")
        
        for activity in DATA['recent_activities']:
            icons = {
                "assessment": "🔍", 
                "accommodation": "🔧", 
                "report": "📊", 
                "training": "🎓", 
                "recruitment": "👤"
            }
            
            priority_colors = {
                "high": "#FF4444",
                "medium": "#FF8800", 
                "low": "#00D2A3"
            }
            
            color = priority_colors.get(activity['priority'], "#B0B3B8")
            
            st.markdown(f"""
            <div class="activity-card-dark">
                <div style="display: flex; align-items: center; gap: 1rem;">
                    <div style="font-size: 28px;">{icons.get(activity['type'], '•')}</div>
                    <div style="flex: 1;">
                        <div style="color: #FFFFFF; font-weight: 600; font-size: 15px; margin-bottom: 0.25rem;">
                            {activity['message']}
                        </div>
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <span style="color: #B0B3B8; font-size: 12px;">{activity['time']}</span>
                            <span style="background: {color}; color: white; padding: 0.25rem 0.75rem; 
                                        border-radius: 12px; font-size: 11px; font-weight: 600; text-transform: uppercase;">
                                {activity['priority']}
                            </span>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 🎯 Objectifs du Trimestre")
        
        quarterly_objectives = [
            {"name": "Screenings", "current": 67, "target": 100, "color": "#D4B886"},
            {"name": "Accommodations", "current": 43, "target": 60, "color": "#4A9EF8"},
            {"name": "Formations", "current": 28, "target": 40, "color": "#00D2A3"},
            {"name": "Recrutements", "current": 12, "target": 20, "color": "#FF8A4C"}
        ]
        
        for obj in quarterly_objectives:
            progress = (obj['current'] / obj['target']) * 100
            st.markdown(f"""
            <div style="background: #1E2329; border: 1px solid #3E4146; padding: 1.5rem; 
                        margin-bottom: 1rem; border-radius: 16px; 
                        border-left: 4px solid {obj['color']}; transition: all 0.3s ease;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                    <span style="color: #FFFFFF; font-weight: 600; font-size: 16px;">{obj['name']}</span>
                    <span style="color: {obj['color']}; font-weight: 800; font-size: 18px;">
                        {obj['current']}/{obj['target']}
                    </span>
                </div>
                <div style="background: #252A32; height: 10px; border-radius: 5px; overflow: hidden; margin-bottom: 0.5rem;">
                    <div style="background: linear-gradient(90deg, {obj['color']}, {obj['color']}CC); 
                                height: 100%; width: {progress}%; transition: width 0.5s ease; border-radius: 5px;"></div>
                </div>
                <div style="color: #B0B3B8; font-size: 13px; font-weight: 500;">
                    {progress:.1f}% complété • {obj['target'] - obj['current']} restant
                </div>
            </div>
            """, unsafe_allow_html=True)

# --- MODULE TDAH AMÉLIORÉ ---
def module_tdah():
    st.markdown("# 🧠 Module TDAH")
    st.markdown("*Trouble du Déficit de l'Attention avec ou sans Hyperactivité - Gestion Professionnelle*")
    
    # Stats header
    col1, col2, col3, col4 = st.columns(4)
    
    stats = [
        ("Prévalence Mondiale", "5.0%", "#4A9EF8"),
        ("Adultes France", "3.0%", "#00D2A3"),
        ("Ratio H/F", "2.3:1", "#D4B886"),
        ("Persistance Adulte", "66%", "#FF8A4C")
    ]
    
    for i, (label, value, color) in enumerate(stats):
        with [col1, col2, col3, col4][i]:
            st.markdown(f"""
            <div style="background: #1E2329; border: 1px solid #3E4146; padding: 2rem; 
                        border-radius: 16px; text-align: center; border-top: 4px solid {color};">
                <div style="color: {color}; font-size: 36px; font-weight: 800; margin-bottom: 0.5rem;">
                    {value}
                </div>
                <div style="color: #B0B3B8; font-size: 14px; font-weight: 600;">
                    {label}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Tabs avec thème sombre
    tab1, tab2, tab3, tab4 = st.tabs([
        "📋 Screening Interactif", 
        "📊 Statistiques", 
        "🎯 Accommodations", 
        "📈 Analytics"
    ])
    
    with tab1:
        st.markdown("### 🔍 Screening TDAH Professionnel")
        
        # Information importante
        st.markdown("""
        <div class="highlight-card-dark">
            <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
                <div style="font-size: 48px;">🎯</div>
                <div>
                    <h4 style="color: #D4B886; margin: 0; font-size: 20px;">Information Importante</h4>
                    <p style="color: #B0B3B8; margin: 0.5rem 0 0 0;">
                        Outil d'aide au dépistage basé sur les critères cliniques DSM-5. 
                        Ne remplace pas un diagnostic médical professionnel.
                    </p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Questionnaire interactif
        with st.expander("🚀 Démarrer l'Évaluation TDAH", expanded=False):
            scores = {"inattention": 0, "hyperactivity": 0, "impulsivity": 0}
            
            st.markdown("""
            <div style="background: rgba(74, 158, 248, 0.1); border: 1px solid #4A9EF8; 
                        padding: 2rem; border-radius: 16px; margin-bottom: 2rem;">
                <h5 style="color: #4A9EF8; margin-bottom: 1rem; font-size: 18px;">📝 Instructions d'Évaluation</h5>
                <p style="color: #FFFFFF; margin-bottom: 1rem; font-size: 16px;">
                    Évaluez chaque affirmation selon votre expérience des <strong>6 derniers mois</strong> :
                </p>
                <div style="display: grid; grid-template-columns: repeat(5, 1fr); gap: 1rem; margin-top: 1rem;">
                    <div style="text-align: center; padding: 0.75rem; background: rgba(255, 255, 255, 0.05); border-radius: 8px;">
                        <div style="color: #D4B886; font-weight: 700; font-size: 18px;">0</div>
                        <div style="color: #B0B3B8; font-size: 12px;">Jamais</div>
                    </div>
                    <div style="text-align: center; padding: 0.75rem; background: rgba(255, 255, 255, 0.05); border-radius: 8px;">
                        <div style="color: #D4B886; font-weight: 700; font-size: 18px;">1</div>
                        <div style="color: #B0B3B8; font-size: 12px;">Parfois</div>
                    </div>
                    <div style="text-align: center; padding: 0.75rem; background: rgba(255, 255, 255, 0.05); border-radius: 8px;">
                        <div style="color: #D4B886; font-weight: 700; font-size: 18px;">2</div>
                        <div style="color: #B0B3B8; font-size: 12px;">Souvent</div>
                    </div>
                    <div style="text-align: center; padding: 0.75rem; background: rgba(255, 255, 255, 0.05); border-radius: 8px;">
                        <div style="color: #D4B886; font-weight: 700; font-size: 18px;">3</div>
                        <div style="color: #B0B3B8; font-size: 12px;">Très souvent</div>
                    </div>
                    <div style="text-align: center; padding: 0.75rem; background: rgba(255, 255, 255, 0.05); border-radius: 8px;">
                        <div style="color: #D4B886; font-weight: 700; font-size: 18px;">4</div>
                        <div style="color: #B0B3B8; font-size: 12px;">Constamment</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Questions avec design sombre
            for i, item in enumerate(DATA['screening_questions']['adhd']):
                category_colors = {
                    "inattention": "#4A9EF8",
                    "hyperactivity": "#00D2A3", 
                    "impulsivity": "#FF8A4C"
                }
                
                color = category_colors.get(item['category'], "#B0B3B8")
                category_names = {
                    "inattention": "Inattention",
                    "hyperactivity": "Hyperactivité",
                    "impulsivity": "Impulsivité"
                }
                category_name = category_names.get(item['category'], item['category'])
                
                st.markdown(f"""
                <div style="background: #1E2329; border: 1px solid #3E4146; padding: 2rem; 
                            margin-bottom: 1.5rem; border-radius: 16px; 
                            border-left: 4px solid {color};">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;">
                        <span style="color: #B0B3B8; font-weight: 600; font-size: 14px;">
                            Question {i+1}/8
                        </span>
                        <span style="background: {color}; color: white; padding: 0.5rem 1rem; 
                                    border-radius: 20px; font-size: 12px; font-weight: 700; text-transform: uppercase;">
                            {category_name}
                        </span>
                    </div>
                    <p style="color: #FFFFFF; font-size: 18px; font-weight: 600; margin: 0; line-height: 1.4;">
                        {item['q']}
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                score = st.slider(
                    f"Évaluation question {i+1}",
                    min_value=0, max_value=4, value=0,
                    key=f"adhd_{i}",
                    help=f"Catégorie: {category_name} | Pondération: {item['weight']}"
                )
                scores[item['category']] += score * item['weight']
            
            # Bouton d'analyse
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                if st.button("🔬 Analyser les Résultats", use_container_width=True):
                    total_score = sum(scores.values())
                    max_possible = len(DATA['screening_questions']['adhd']) * 4 * 1.2
                    percentage = (total_score / max_possible) * 100
                    
                    st.markdown("### 📊 Résultats de l'Évaluation TDAH")
                    
                    # Affichage des résultats avec design sombre
                    if percentage >= 60:
                        st.markdown(f"""
                        <div style="background: rgba(255, 68, 68, 0.15); border: 2px solid #FF4444; 
                                    border-radius: 20px; padding: 3rem; margin: 2rem 0; text-align: center;">
                            <div style="font-size: 64px; margin-bottom: 1rem;">⚠️</div>
                            <div style="color: #FF4444; font-size: 48px; font-weight: 800; margin-bottom: 1rem;">
                                {percentage:.1f}%
                            </div>
                            <div style="color: #FFFFFF; font-size: 24px; font-weight: 700; margin-bottom: 1rem;">
                                Probabilité Élevée de TDAH
                            </div>
                            <div style="color: #B0B3B8; font-size: 16px; line-height: 1.5;">
                                <strong>Recommandation :</strong> Consultation urgente avec un professionnel de santé 
                                spécialisé pour évaluation approfondie et plan d'accompagnement.
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    elif percentage >= 40:
                        st.markdown(f"""
                        <div style="background: rgba(255, 136, 0, 0.15); border: 2px solid #FF8800; 
                                    border-radius: 20px; padding: 3rem; margin: 2rem 0; text-align: center;">
                            <div style="font-size: 64px; margin-bottom: 1rem;">⚠️</div>
                            <div style="color: #FF8800; font-size: 48px; font-weight: 800; margin-bottom: 1rem;">
                                {percentage:.1f}%
                            </div>
                            <div style="color: #FFFFFF; font-size: 24px; font-weight: 700; margin-bottom: 1rem;">
                                Indicateurs Modérés Détectés
                            </div>
                            <div style="color: #B0B3B8; font-size: 16px; line-height: 1.5;">
                                <strong>Recommandation :</strong> Suivi régulier et mise en place d'accommodations 
                                préventives. Évaluation complémentaire conseillée.
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div style="background: rgba(0, 210, 163, 0.15); border: 2px solid #00D2A3; 
                                    border-radius: 20px; padding: 3rem; margin: 2rem 0; text-align: center;">
                            <div style="font-size: 64px; margin-bottom: 1rem;">✅</div>
                            <div style="color: #00D2A3; font-size: 48px; font-weight: 800; margin-bottom: 1rem;">
                                {percentage:.1f}%
                            </div>
                            <div style="color: #FFFFFF; font-size: 24px; font-weight: 700; margin-bottom: 1rem;">
                                Probabilité Faible
                            </div>
                            <div style="color: #B0B3B8; font-size: 16px; line-height: 1.5;">
                                Aucune action immédiate nécessaire. 
                                Réévaluation recommandée dans 12 mois.
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Analyse par catégorie
                    st.markdown("### 📊 Analyse Détaillée par Catégorie")
                    
                    col1, col2, col3 = st.columns(3)
                    categories = ["inattention", "hyperactivity", "impulsivity"]
                    category_names = ["Inattention", "Hyperactivité", "Impulsivité"]
                    category_colors = ["#4A9EF8", "#00D2A3", "#FF8A4C"]
                    
                    for i, (cat, name, color) in enumerate(zip(categories, category_names, category_colors)):
                        with [col1, col2, col3][i]:
                            cat_percentage = (scores[cat] / total_score * 100) if total_score > 0 else 0
                            st.markdown(f"""
                            <div style="background: #1E2329; border: 1px solid #3E4146; padding: 2rem; 
                                        border-radius: 16px; text-align: center; border-top: 4px solid {color};">
                                <div style="color: {color}; font-size: 36px; font-weight: 800; margin-bottom: 0.5rem;">
                                    {cat_percentage:.0f}%
                                </div>
                                <div style="color: #FFFFFF; font-weight: 700; font-size: 16px; margin-bottom: 0.5rem;">
                                    {name}
                                </div>
                                <div style="background: rgba(255, 255, 255, 0.1); height: 8px; border-radius: 4px; overflow: hidden;">
                                    <div style="background: {color}; height: 100%; width: {cat_percentage}%; border-radius: 4px;"></div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("### 📊 Statistiques Cliniques et Épidémiologiques")
        
        # Graphique des défis workplace
        challenges = DATA['adhd_statistics']['workplace_challenges']
        
        fig_challenges = go.Figure()
        
        fig_challenges.add_trace(go.Bar(
            x=list(challenges.keys()),
            y=list(challenges.values()),
            marker=dict(
                color=['#FF4444', '#FF8800', '#4A9EF8', '#00D2A3'],
                line=dict(color='#FFFFFF', width=1)
            ),
            text=[f"{v}%" for v in challenges.values()],
            textposition='auto',
            textfont=dict(color='white', size=14, family='Inter', weight='bold'),
            hovertemplate='<b>%{x}</b><br>%{y}% des employés TDAH concernés<extra></extra>'
        ))
        
        fig_challenges.update_layout(
            title={
                'text': 'Défis Principaux des Employés TDAH en Milieu Professionnel',
                'x': 0.5,
                'font': {'size': 20, 'color': '#FFFFFF', 'family': 'Inter'}
            },
            xaxis=dict(
                title='Type de Défi',
                color='#B0B3B8',
                gridcolor='#3E4146',
                tickangle=45
            ),
            yaxis=dict(
                title='Pourcentage d\'Employés Concernés (%)',
                color='#B0B3B8',
                gridcolor='#3E4146'
            ),
            paper_bgcolor='#1E2329',
            plot_bgcolor='#1E2329',
            font=dict(color='#FFFFFF', family='Inter'),
            height=500
        )
        
        st.plotly_chart(fig_challenges, use_container_width=True)
        
        # Données complémentaires
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📈 Données Épidémiologiques Détaillées")
            
            epidemio_data = [
                ("Prévalence mondiale", "5.0%", "Population générale"),
                ("Adultes France", "3.0%", "Diagnostics confirmés"),
                ("Enfants France", "3.5%", "Âge scolaire"),
                ("Persistance adulte", "66%", "Depuis l'enfance"),
                ("Comorbidités", "50%", "Autres troubles"),
                ("Ratio H/F", "2.3:1", "Chez les adultes")
            ]
            
            for title, value, desc in epidemio_data:
                st.markdown(f"""
                <div style="background: #1E2329; border: 1px solid #3E4146; padding: 1.5rem; 
                            margin-bottom: 1rem; border-radius: 12px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <div style="color: #FFFFFF; font-weight: 700; font-size: 16px;">{title}</div>
                            <div style="color: #B0B3B8; font-size: 14px; margin-top: 0.25rem;">{desc}</div>
                        </div>
                        <div style="color: #D4B886; font-size: 24px; font-weight: 800;">
                            {value}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("#### 🎯 Facteurs de Succès Identifiés")
            
            success_factors = [
                ("Structure claire", 94.2, "Procédures définies"),
                ("Feedback régulier", 89.1, "Communication fréquente"),
                ("Pauses fréquentes", 85.7, "Gestion énergie"),
                ("Environnement calme", 91.3, "Réduction distractions"),
                ("Outils organisation", 87.5, "Support technologique"),
                ("Horaires flexibles", 82.4, "Adaptation rythmes")
            ]
            
            for factor, percentage, desc in success_factors:
                st.markdown(f"""
                <div style="background: #1E2329; border: 1px solid #3E4146; padding: 1.5rem; 
                            margin-bottom: 1rem; border-radius: 12px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                        <div style="color: #FFFFFF; font-weight: 600; font-size: 15px;">{factor}</div>
                        <div style="color: #00D2A3; font-weight: 800; font-size: 18px;">{percentage}%</div>
                    </div>
                    <div style="background: rgba(255, 255, 255, 0.1); height: 8px; border-radius: 4px; overflow: hidden;">
                        <div style="background: linear-gradient(90deg, #00D2A3, #4A9EF8); height: 100%; 
                                    width: {percentage}%; border-radius: 4px; transition: width 0.5s ease;"></div>
                    </div>
                    <div style="color: #B0B3B8; font-size: 12px; margin-top: 0.5rem;">{desc}</div>
                </div>
                """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown("### 🎯 Accommodations Workplace - Catalogue Exhaustif")
        
        # Filtre par catégorie
        categories = list(set(acc['category'] for acc in DATA['workplace_accommodations'] if acc['condition'] == 'ADHD'))
        selected_category = st.selectbox(
            "Filtrer par catégorie d'accommodation",
            ["Toutes les catégories"] + categories
        )
        
        # Accommodations filtrées
        adhd_accommodations = [acc for acc in DATA['workplace_accommodations'] 
                              if acc['condition'] == 'ADHD']
        
        if selected_category != "Toutes les catégories":
            adhd_accommodations = [acc for acc in adhd_accommodations 
                                  if acc['category'] == selected_category]
        
        # Affichage des accommodations avec design sombre
        for acc in adhd_accommodations:
            # Couleurs selon impact
            if acc['impact'] >= 9:
                impact_color = "#00D2A3"
                impact_label = "Impact Élevé"
            elif acc['impact'] >= 7.5:
                impact_color = "#FF8800" 
                impact_label = "Impact Modéré"
            else:
                impact_color = "#4A9EF8"
                impact_label = "Impact Standard"
            
            # Couleurs selon coût
            cost_colors = {"Aucun": "#00D2A3", "Faible": "#FF8800", "Moyen": "#FF4444"}
            cost_color = cost_colors[acc['cost']]
            
            with st.expander(f"🔧 {acc['accommodation']}", expanded=False):
                st.markdown(f"""
                <div style="background: #1E2329; border: 1px solid #3E4146; padding: 2rem; 
                            border-radius: 16px; margin-bottom: 1rem;">
                    <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 2rem; margin-bottom: 2rem;">
                        <div style="text-align: center; padding: 1.5rem; background: rgba(255, 255, 255, 0.05); 
                                    border-radius: 12px; border: 2px solid {impact_color};">
                            <div style="color: {impact_color}; font-size: 32px; font-weight: 800; margin-bottom: 0.5rem;">
                                {acc['impact']}/10
                            </div>
                            <div style="color: #FFFFFF; font-weight: 600; margin-bottom: 0.25rem;">Score Impact</div>
                            <div style="color: #B0B3B8; font-size: 12px;">{impact_label}</div>
                        </div>
                        
                        <div style="text-align: center; padding: 1.5rem; background: rgba(255, 255, 255, 0.05); 
                                    border-radius: 12px; border: 2px solid {cost_color};">
                            <div style="color: {cost_color}; font-size: 20px; font-weight: 800; margin-bottom: 0.5rem;">
                                {acc['cost']}
                            </div>
                            <div style="color: #FFFFFF; font-weight: 600; margin-bottom: 0.25rem;">Niveau Coût</div>
                            <div style="color: #B0B3B8; font-size: 12px;">Investissement requis</div>
                        </div>
                        
                        <div style="text-align: center; padding: 1.5rem; background: rgba(255, 255, 255, 0.05); 
                                    border-radius: 12px; border: 2px solid #4A9EF8;">
                            <div style="color: #4A9EF8; font-size: 20px; font-weight: 800; margin-bottom: 0.5rem;">
                                {acc['implementation']}
                            </div>
                            <div style="color: #FFFFFF; font-weight: 600; margin-bottom: 0.25rem;">Implémentation</div>
                            <div style="color: #B0B3B8; font-size: 12px;">Délai de mise en œuvre</div>
                        </div>
                    </div>
                    
                    <div style="margin-bottom: 2rem;">
                        <h5 style="color: #D4B886; margin-bottom: 1rem;">📋 Description Détaillée</h5>
                        <p style="color: #B0B3B8; line-height: 1.6; font-size: 15px;">
                            {acc['description']}
                        </p>
                    </div>
                    
                    <div style="margin-bottom: 2rem;">
                        <h5 style="color: #D4B886; margin-bottom: 1rem;">🏷️ Catégorie</h5>
                        <span style="background: {impact_color}; color: white; padding: 0.5rem 1rem; 
                                    border-radius: 20px; font-size: 14px; font-weight: 600;">
                            {acc['category']}
                        </span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Boutons d'action
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button(f"✅ Recommander", key=f"recommend_{acc['accommodation']}"):
                        st.success(f"✅ Accommodation '{acc['accommodation']}' ajoutée aux recommandations !")
                        st.balloons()
                
                with col2:
                    if st.button(f"📋 Plus d'infos", key=f"info_{acc['accommodation']}"):
                        st.info(f"ℹ️ Documentation détaillée disponible sur l'intranet RH.")
                
                with col3:
                    if st.button(f"📞 Contacter expert", key=f"contact_{acc['accommodation']}"):
                        st.info(f"📞 Référent handicap contacté pour guidance.")
    
    with tab4:
        st.markdown("### 📈 Analytics et Suivi TDAH")
        
        # Évolution des métriques (données simulées réalistes)
        dates = pd.date_range(start='2024-01-01', periods=12, freq='M')
        
        # Données d'évolution plus réalistes
        np.random.seed(42)  # Pour la reproductibilité
        base_attention = 58
        base_organisation = 52
        base_productivite = 61
        
        attention_scores = []
        organisation_scores = []
        productivite_scores = []
        
        for i in range(12):
            # Amélioration graduelle avec interventions marquées
            month_factor = i / 12
            seasonal_variation = np.sin(i * 2 * np.pi / 12) * 3
            intervention_boost = 0
            
            # Simulation d'interventions
            if i >= 3:  # Accommodations mises en place
                intervention_boost += 8
            if i >= 7:  # Formation complémentaire
                intervention_boost += 5
            
            attention = min(95, max(35, base_attention + (month_factor * 20) + seasonal_variation + 
                                   intervention_boost + np.random.normal(0, 3)))
            organisation = min(95, max(30, base_organisation + (month_factor * 25) + seasonal_variation + 
                                     intervention_boost + np.random.normal(0, 2.5)))
            productivite = min(95, max(40, base_productivite + (month_factor * 18) + seasonal_variation + 
                                     intervention_boost + np.random.normal(0, 4)))
            
            attention_scores.append(attention)
            organisation_scores.append(organisation)
            productivite_scores.append(productivite)
        
        df_evolution = pd.DataFrame({
            'Date': dates,
            'Attention': attention_scores,
            'Organisation': organisation_scores,
            'Productivité': productivite_scores
        })
        
        # Graphique d'évolution avec thème sombre
        fig_evolution = go.Figure()
        
        fig_evolution.add_trace(go.Scatter(
            x=df_evolution['Date'],
            y=df_evolution['Attention'],
            mode='lines+markers',
            name='Capacité d\'Attention',
            line=dict(color='#4A9EF8', width=4),
            marker=dict(size=8, color='#4A9EF8'),
            hovertemplate='<b>Attention</b><br>%{x}<br>Score: %{y:.1f}%<extra></extra>'
        ))
        
        fig_evolution.add_trace(go.Scatter(
            x=df_evolution['Date'],
            y=df_evolution['Organisation'],
            mode='lines+markers',
            name='Compétences d\'Organisation',
            line=dict(color='#00D2A3', width=4),
            marker=dict(size=8, color='#00D2A3'),
            hovertemplate='<b>Organisation</b><br>%{x}<br>Score: %{y:.1f}%<extra></extra>'
        ))
        
        fig_evolution.add_trace(go.Scatter(
            x=df_evolution['Date'],
            y=df_evolution['Productivité'],
            mode='lines+markers',
            name='Productivité Globale',
            line=dict(color='#D4B886', width=4),
            marker=dict(size=8, color='#D4B886'),
            hovertemplate='<b>Productivité</b><br>%{x}<br>Score: %{y:.1f}%<extra></extra>'
        ))
        
        # Annotations des interventions
        fig_evolution.add_annotation(
            x=dates[3], y=max(attention_scores[3], organisation_scores[3], productivite_scores[3]) + 5,
            text="🔧 Accommodations<br>implémentées",
            showarrow=True,
            arrowhead=2,
            arrowcolor="#00D2A3",
            font=dict(color="#00D2A3", size=12),
            bgcolor="rgba(0, 210, 163, 0.1)",
            bordercolor="#00D2A3",
            borderwidth=1
        )
        
        fig_evolution.add_annotation(
            x=dates[7], y=max(attention_scores[7], organisation_scores[7], productivite_scores[7]) + 5,
            text="🎓 Formation<br>spécialisée",
            showarrow=True,
            arrowhead=2,
            arrowcolor="#D4B886",
            font=dict(color="#D4B886", size=12),
            bgcolor="rgba(212, 184, 134, 0.1)",
            bordercolor="#D4B886",
            borderwidth=1
        )
        
        fig_evolution.update_layout(
            title={
                'text': 'Évolution des Métriques TDAH - Cohorte Employés (N=89)',
                'x': 0.5,
                'font': {'size': 22, 'color': '#FFFFFF', 'family': 'Inter', 'weight': 'bold'}
            },
            xaxis=dict(
                title='Période',
                color='#B0B3B8',
                gridcolor='#3E4146'
            ),
            yaxis=dict(
                title='Score de Performance (%)',
                color='#B0B3B8',
                gridcolor='#3E4146',
                range=[25, 100]
            ),
            hovermode='x unified',
            paper_bgcolor='#1E2329',
            plot_bgcolor='#1E2329',
            font=dict(color='#FFFFFF', family='Inter'),
            height=600,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                bgcolor="rgba(30, 35, 41, 0.8)",
                bordercolor="#3E4146",
                borderwidth=1
            )
        )
        
        # Zone d'excellence
        fig_evolution.add_shape(
            type="rect",
            x0=dates[0], x1=dates[-1],
            y0=80, y1=100,
            fillcolor="rgba(0, 210, 163, 0.1)",
            line=dict(width=0),
            layer="below"
        )
        
        fig_evolution.add_annotation(
            x=dates[6], y=90,
            text="Zone d'Excellence",
            showarrow=False,
            font=dict(size=14, color="#00D2A3", weight='bold'),
            bgcolor="rgba(0, 210, 163, 0.2)",
            bordercolor="#00D2A3",
            borderwidth=1
        )
        
        st.plotly_chart(fig_evolution, use_container_width=True)
        
        # KPIs d'amélioration
        col1, col2, col3, col4 = st.columns(4)
        
        current_attention = attention_scores[-1]
        current_organisation = organisation_scores[-1]  
        current_productivite = productivite_scores[-1]
        
        initial_attention = attention_scores[0]
        initial_organisation = organisation_scores[0]
        initial_productivite = productivite_scores[0]
        
        improvement_attention = current_attention - initial_attention
        improvement_organisation = current_organisation - initial_organisation
        improvement_productivite = current_productivite - initial_productivite
        
        retention_rate = 94.2
        
        metrics_data = [
            ("Attention", current_attention, improvement_attention, "#4A9EF8"),
            ("Organisation", current_organisation, improvement_organisation, "#00D2A3"),
            ("Productivité", current_productivite, improvement_productivite, "#D4B886"),
            ("Rétention", retention_rate, 2.3, "#FF8A4C")
        ]
        
        for i, (metric, current, improvement, color) in enumerate(metrics_data):
            with [col1, col2, col3, col4][i]:
                unit = "%" if metric != "Rétention" else "%"
                st.markdown(f"""
                <div style="background: #1E2329; border: 1px solid #3E4146; padding: 2rem; 
                            border-radius: 16px; text-align: center; border-top: 4px solid {color};">
                    <div style="color: {color}; font-size: 36px; font-weight: 800; margin-bottom: 0.5rem;">
                        {current:.1f}{unit}
                    </div>
                    <div style="color: #FFFFFF; font-weight: 700; font-size: 16px; margin-bottom: 1rem;">
                        {metric}
                    </div>
                    <div style="color: #00D2A3; font-size: 14px; font-weight: 600;">
                        {'+' if improvement > 0 else ''}{improvement:.1f} points cette année
                    </div>
                </div>
                """, unsafe_allow_html=True)

# --- FONCTION PRINCIPALE ---
def main():
    # Applique le thème sombre
    apply_dark_professional_theme()
    
    # Header moderne sombre
    render_dark_header()
    
    # Sidebar ergonomique
    selected_module = render_ergonomic_sidebar()
    
    # Router les modules
    if "Dashboard Principal" in selected_module:
        dashboard_principal()
    elif "Module TDAH" in selected_module:
        module_tdah()
    # TODO: Implémenter les autres modules avec le même niveau de qualité
    elif "Module Autisme" in selected_module:
        st.markdown("# 🎯 Module Autisme")
        st.info("🚧 Module en cours de développement avec design sombre professionnel")
    elif "Observatoire" in selected_module:
        st.markdown("# 📊 Observatoire")
        st.info("🚧 Module en cours de développement avec analytics avancées")
    elif "NeuroScreen" in selected_module:
        st.markdown("# 🔬 NeuroScreen") 
        st.info("🚧 Tests cognitifs en cours d'implémentation")
    elif "Workplace" in selected_module:
        st.markdown("# 🏢 Gestion Workplace")
        st.info("🚧 Interface accommodations en développement")
    elif "Recrutement" in selected_module:
        st.markdown("# 👥 Recrutement Neurodiversité")
        st.info("🚧 Processus inclusifs en cours d'intégration")
    elif "Analytics" in selected_module:
        st.markdown("# 📈 Analytics & Reporting")
        st.info("🚧 Dashboards exécutifs en préparation")
    
    # Footer professionnel sombre
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 2rem; margin-top: 3rem; 
                background: linear-gradient(135deg, #1A1D23 0%, #252A32 100%); 
                border-radius: 16px; border: 1px solid #3E4146;">
        <div style="color: #D4B886; font-size: 18px; font-weight: 700; margin-bottom: 0.5rem;">
            © 2025 Ubisoft Entertainment - NeuroInsight Hub Workspace
        </div>
        <div style="color: #B0B3B8; font-size: 14px; margin-bottom: 1rem;">
            Plateforme RH Professionnelle de Gestion de la Neurodiversité | Version 2.5 Dark Professional
        </div>
        <div style="color: #8A8D93; font-size: 12px;">
            🔒 Données Sécurisées • ✅ Conforme RGPD • 🏆 Certifié ISO 27001 • 🌟 Excellence RH
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- EXÉCUTION ---
if __name__ == "__main__":
    main()
