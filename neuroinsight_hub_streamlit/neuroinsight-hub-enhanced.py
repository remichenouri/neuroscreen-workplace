
# NeuroInsight Hub - Enterprise HR Tool
# Application Streamlit avec thème Ubisoft et fonctionnalités avancées

import os
import json
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
from fpdf import FPDF
import base64
from io import BytesIO
import hashlib

# --- CONFIGURATION AVANCÉE ---
st.set_page_config(
    page_title="NeuroInsight Hub - Enterprise HR Tool",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.ubisoft.com/hr-support',
        'Report a bug': "https://www.ubisoft.com/hr-bug-report",
        'About': "# NeuroInsight Hub Enterprise\nPlateforme RH Professionnelle - Neurodiversité & Inclusion\n\n© 2025 Ubisoft Entertainment"
    }
)

# --- DONNÉES ENTERPRISE COMPLÈTES ---
ENTERPRISE_DATA = {
    "company_metrics": {
        "total_employees": 1847,
        "neurodiverse_employees": 287,
        "neurodiverse_percentage": 15.5,
        "adhd_employees": 139,
        "autism_employees": 78,
        "dyslexia_employees": 70,
        "retention_rate": 94.8,
        "satisfaction_score": 4.4,
        "productivity_increase": 22.3,
        "roi_percentage": 415,
        "cost_savings": 285000,
        "training_completion": 97.2,
        "accommodation_success_rate": 91.7,
        "manager_confidence": 88.9,
        "compliance_score": 99.2
    },

    "team_metrics": [
        {"team_id": "T001", "manager": "Sarah L.", "team_size": 12, "neurodiverse_count": 4, "productivity_score": 127, "satisfaction": 4.6, "accommodations": 8, "roi": 380},
        {"team_id": "T002", "manager": "Marcus D.", "team_size": 8, "neurodiverse_count": 2, "productivity_score": 118, "satisfaction": 4.2, "accommodations": 3, "roi": 295},
        {"team_id": "T003", "manager": "Elena M.", "team_size": 15, "neurodiverse_count": 6, "productivity_score": 134, "satisfaction": 4.7, "accommodations": 12, "roi": 445},
        {"team_id": "T004", "manager": "James K.", "team_size": 10, "neurodiverse_count": 3, "productivity_score": 122, "satisfaction": 4.4, "accommodations": 5, "roi": 325},
        {"team_id": "T005", "manager": "Aisha P.", "team_size": 20, "neurodiverse_count": 8, "productivity_score": 141, "satisfaction": 4.8, "accommodations": 18, "roi": 492}
    ],

    "accommodation_database": [
        # Environnement Physique
        {"id": "ENV001", "category": "Environnement Physique", "accommodation": "Bureau isolé acoustique", "condition": "ADHD", "cost": 850, "implementation_days": 3, "success_rate": 94.2, "roi": 312, "description": "Bureau avec cloisons phoniques et contrôle sonore avancé"},
        {"id": "ENV002", "category": "Environnement Physique", "accommodation": "Éclairage LED personnalisé", "condition": "Autism", "cost": 320, "implementation_days": 1, "success_rate": 89.7, "roi": 245, "description": "Système d'éclairage adaptable avec contrôle de température de couleur"},
        {"id": "ENV003", "category": "Environnement Physique", "accommodation": "Espace sensoriel de décompression", "condition": "Autism", "cost": 2500, "implementation_days": 7, "success_rate": 91.8, "roi": 425, "description": "Salle équipée pour la régulation sensorielle et la pause cognitive"},

        # Technologies & Outils
        {"id": "TECH001", "category": "Technologie", "accommodation": "Suite logiciels attention", "condition": "ADHD", "cost": 180, "implementation_days": 1, "success_rate": 87.3, "roi": 198, "description": "Cold Turkey Pro, Forest, Focus - suite complète de gestion attention"},
        {"id": "TECH002", "category": "Technologie", "accommodation": "Interface adaptée dyslexie", "condition": "Dyslexia", "cost": 95, "implementation_days": 1, "success_rate": 92.1, "roi": 167, "description": "OpenDyslexic, Bionic Reading, ajustements typographiques"},
        {"id": "TECH003", "category": "Technologie", "accommodation": "Communication asynchrone renforcée", "condition": "Autism", "cost": 0, "implementation_days": 0, "success_rate": 96.4, "roi": 289, "description": "Protocoles Slack/Teams optimisés, templates de communication"},

        # Management & Organisation
        {"id": "MGT001", "category": "Management", "accommodation": "Feedback structuré hebdomadaire", "condition": "General", "cost": 0, "implementation_days": 0, "success_rate": 89.2, "roi": 156, "description": "Sessions 1:1 avec framework SMART et suivi personnalisé"},
        {"id": "MGT002", "category": "Management", "accommodation": "Décomposition tâches complexes", "condition": "ADHD", "cost": 0, "implementation_days": 0, "success_rate": 93.7, "roi": 278, "description": "Micro-tâches avec deadlines intermédiaires et validation"},

        # Temps & Planning
        {"id": "TIME001", "category": "Temps & Planning", "accommodation": "Horaires flexibles core-time", "condition": "General", "cost": 0, "implementation_days": 1, "success_rate": 91.5, "roi": 201, "description": "Plages libres 6h-10h et 15h-19h, core-time 10h-15h"},
        {"id": "TIME002", "category": "Temps & Planning", "accommodation": "Télétravail hybride adapté", "condition": "General", "cost": 0, "implementation_days": 0, "success_rate": 88.9, "roi": 234, "description": "2-3 jours/semaine selon besoins, espaces dédiés domicile"}
    ],

    "compliance_metrics": {
        "gdpr_score": 99.2,
        "ai_act_compliance": 97.8,
        "accessibility_score": 94.5,
        "audit_last_date": "2025-08-15",
        "certification_status": "Certifié ISO 27001",
        "data_breaches": 0,
        "privacy_requests_handled": 23,
        "training_compliance": 98.1
    },

    "roi_calculator_data": {
        "base_salary": 55000,
        "productivity_gain_percent": 18.5,
        "retention_improvement": 12.3,
        "recruitment_cost_saved": 15000,
        "training_efficiency": 25.4,
        "absence_reduction": 8.7
    }
}

# --- THÈME UBISOFT ENTERPRISE ---
def apply_ubisoft_enterprise_theme():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

    /* Variables Ubisoft Enterprise */
    :root {
        --ubisoft-primary: #0a0e27;
        --ubisoft-secondary: #1a1f3a;
        --ubisoft-tertiary: #2a2f4a;
        --ubisoft-accent: #0095ff;
        --ubisoft-gold: #ffb800;
        --ubisoft-success: #00d084;
        --ubisoft-warning: #ff6b35;
        --ubisoft-error: #ff3366;
        --ubisoft-text: #ffffff;
        --ubisoft-text-muted: #a0a5ba;
        --ubisoft-border: #3a3f5a;
        --ubisoft-hover: #3a4158;
    }

    /* Application globale */
    .stApp {
        background: linear-gradient(135deg, var(--ubisoft-primary) 0%, var(--ubisoft-secondary) 100%);
        color: var(--ubisoft-text);
        font-family: 'Inter', sans-serif;
    }

    /* Header personnalisé */
    header[data-testid="stHeader"] {
        background: linear-gradient(90deg, var(--ubisoft-primary) 0%, var(--ubisoft-tertiary) 100%);
        border-bottom: 2px solid var(--ubisoft-accent);
        height: 4rem;
    }

    /* Sidebar Ubisoft */
    .css-1d391kg, .css-1cypcdb, .css-17lntkn {
        background: linear-gradient(180deg, var(--ubisoft-secondary) 0%, var(--ubisoft-tertiary) 100%);
        border-right: 3px solid var(--ubisoft-gold);
    }

    /* Titres avec style Ubisoft */
    h1, h2, h3, h4, h5, h6 {
        color: var(--ubisoft-gold);
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }

    h1 {
        font-size: 2.8rem;
        background: linear-gradient(135deg, var(--ubisoft-gold), var(--ubisoft-accent));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Métriques Enterprise */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, var(--ubisoft-tertiary), var(--ubisoft-secondary));
        border: 1px solid var(--ubisoft-border);
        border-left: 4px solid var(--ubisoft-accent);
        border-radius: 16px;
        padding: 2rem;
        transition: all 0.3s ease;
        box-shadow: 0 8px 32px rgba(0, 149, 255, 0.1);
    }

    [data-testid="metric-container"]:hover {
        border-left-color: var(--ubisoft-gold);
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(255, 184, 0, 0.2);
    }

    [data-testid="metric-container"] [data-testid="metric-label"] {
        color: var(--ubisoft-text-muted);
        font-weight: 600;
        font-size: 13px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    [data-testid="metric-container"] [data-testid="metric-value"] {
        color: var(--ubisoft-text);
        font-weight: 800;
        font-size: 2.2rem;
    }

    /* Boutons Enterprise */
    .stButton > button {
        background: linear-gradient(135deg, var(--ubisoft-accent) 0%, var(--ubisoft-gold) 100%);
        color: var(--ubisoft-primary);
        border: none;
        border-radius: 12px;
        padding: 0.8rem 2rem;
        font-weight: 700;
        font-size: 14px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
        box-shadow: 0 6px 20px rgba(0, 149, 255, 0.3);
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 30px rgba(255, 184, 0, 0.4);
        background: linear-gradient(135deg, var(--ubisoft-gold) 0%, var(--ubisoft-accent) 100%);
    }

    /* Cards Enterprise */
    .enterprise-card {
        background: linear-gradient(135deg, var(--ubisoft-tertiary), var(--ubisoft-secondary));
        border: 1px solid var(--ubisoft-border);
        border-radius: 20px;
        padding: 2.5rem;
        margin: 1.5rem 0;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
    }

    .enterprise-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 15px 40px rgba(0, 149, 255, 0.15);
        border-color: var(--ubisoft-accent);
    }

    .manager-card {
        background: linear-gradient(45deg, var(--ubisoft-secondary), var(--ubisoft-tertiary));
        border: 2px solid var(--ubisoft-gold);
        border-radius: 16px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(255, 184, 0, 0.1);
    }

    /* Tabs Ubisoft Style */
    .stTabs [data-baseweb="tab-list"] {
        background: var(--ubisoft-tertiary);
        border-radius: 16px;
        padding: 8px;
        border: 1px solid var(--ubisoft-border);
        box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.2);
    }

    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 12px;
        color: var(--ubisoft-text-muted);
        font-weight: 600;
        padding: 1rem 2rem;
        margin: 0 6px;
        transition: all 0.3s ease;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background: var(--ubisoft-hover);
        color: var(--ubisoft-text);
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, var(--ubisoft-accent), var(--ubisoft-gold));
        color: var(--ubisoft-primary);
        font-weight: 800;
        box-shadow: 0 4px 15px rgba(0, 149, 255, 0.3);
    }

    /* Inputs et contrôles */
    .stSelectbox > div > div, .stTextInput > div > div > input {
        background: var(--ubisoft-tertiary);
        border: 2px solid var(--ubisoft-border);
        border-radius: 12px;
        color: var(--ubisoft-text);
        padding: 0.8rem;
    }

    .stSelectbox > div > div:focus, .stTextInput > div > div > input:focus {
        border-color: var(--ubisoft-accent);
        box-shadow: 0 0 0 3px rgba(0, 149, 255, 0.2);
    }

    /* Messages et alertes */
    .stSuccess {
        background: rgba(0, 208, 132, 0.1);
        border: 1px solid var(--ubisoft-success);
        border-left: 4px solid var(--ubisoft-success);
        border-radius: 12px;
        color: var(--ubisoft-text);
    }

    .stWarning {
        background: rgba(255, 107, 53, 0.1);
        border: 1px solid var(--ubisoft-warning);
        border-left: 4px solid var(--ubisoft-warning);
        border-radius: 12px;
        color: var(--ubisoft-text);
    }

    .stError {
        background: rgba(255, 51, 102, 0.1);
        border: 1px solid var(--ubisoft-error);
        border-left: 4px solid var(--ubisoft-error);
        border-radius: 12px;
        color: var(--ubisoft-text);
    }

    .stInfo {
        background: rgba(0, 149, 255, 0.1);
        border: 1px solid var(--ubisoft-accent);
        border-left: 4px solid var(--ubisoft-accent);
        border-radius: 12px;
        color: var(--ubisoft-text);
    }

    /* Progress bars */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, var(--ubisoft-accent), var(--ubisoft-gold));
        border-radius: 8px;
    }

    /* DataFrames */
    .stDataFrame {
        border-radius: 16px;
        overflow: hidden;
        border: 1px solid var(--ubisoft-border);
        background: var(--ubisoft-tertiary);
    }

    .stDataFrame table {
        background: var(--ubisoft-tertiary);
        color: var(--ubisoft-text);
    }

    .stDataFrame th {
        background: var(--ubisoft-secondary);
        color: var(--ubisoft-gold);
        font-weight: 700;
        border-bottom: 2px solid var(--ubisoft-accent);
    }

    /* Custom classes */
    .roi-calculator {
        background: linear-gradient(135deg, rgba(0, 149, 255, 0.1), rgba(255, 184, 0, 0.1));
        border: 2px solid var(--ubisoft-accent);
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem 0;
    }

    .compliance-dashboard {
        background: linear-gradient(45deg, var(--ubisoft-secondary), rgba(0, 208, 132, 0.05));
        border: 1px solid var(--ubisoft-success);
        border-radius: 16px;
        padding: 2rem;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ENTERPRISE UBISOFT ---
def render_enterprise_header():
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #0a0e27 0%, #2a2f4a 100%); 
                border-radius: 20px; padding: 2.5rem; margin-bottom: 2rem; 
                border: 1px solid #3a3f5a; box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4);
                position: relative; overflow: hidden;">

        <!-- Effet de spiral Ubisoft en arrière-plan -->
        <div style="position: absolute; top: -50px; right: -50px; width: 200px; height: 200px; 
                    opacity: 0.1; background: radial-gradient(circle, #0095ff 0%, transparent 70%);
                    border-radius: 50%; animation: rotate 20s linear infinite;"></div>

        <div style="display: flex; justify-content: space-between; align-items: center; position: relative; z-index: 1;">
            <div style="display: flex; align-items: center; gap: 2rem;">
                <div style="background: linear-gradient(135deg, #0095ff 0%, #ffb800 100%); 
                            width: 80px; height: 80px; border-radius: 20px; 
                            display: flex; align-items: center; justify-content: center; 
                            font-size: 32px; box-shadow: 0 6px 20px rgba(0, 149, 255, 0.3);
                            position: relative;">
                    🧠
                    <div style="position: absolute; inset: -2px; background: linear-gradient(135deg, #0095ff, #ffb800); 
                                border-radius: 22px; z-index: -1; opacity: 0.5; filter: blur(4px);"></div>
                </div>
                <div>
                    <h1 style="margin: 0; font-size: 32px; background: linear-gradient(135deg, #ffb800, #0095ff); 
                               -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
                               font-weight: 900; text-shadow: none;">
                        NeuroInsight Hub Enterprise
                    </h1>
                    <p style="margin: 0; color: #a0a5ba; font-size: 18px; font-weight: 500;">
                        🏢 Enterprise HR Tool - Neurodiversité & Intelligence d'Affaires
                    </p>
                </div>
            </div>

            <div style="display: flex; gap: 2rem; align-items: center;">
                <div style="text-align: center; padding: 1.5rem; 
                            background: rgba(0, 149, 255, 0.1); border-radius: 16px; 
                            border: 1px solid #0095ff; backdrop-filter: blur(10px);">
                    <div style="font-size: 28px; font-weight: 900; color: #00d084; margin-bottom: 0.5rem;">
                        {ENTERPRISE_DATA['company_metrics']['neurodiverse_employees']}
                    </div>
                    <div style="font-size: 12px; color: #a0a5ba; text-transform: uppercase; letter-spacing: 1px;">
                        Employés Neurodivers
                    </div>
                </div>

                <div style="text-align: center; padding: 1.5rem; 
                            background: rgba(255, 184, 0, 0.1); border-radius: 16px; 
                            border: 1px solid #ffb800; backdrop-filter: blur(10px);">
                    <div style="font-size: 28px; font-weight: 900; color: #ffb800; margin-bottom: 0.5rem;">
                        {ENTERPRISE_DATA['company_metrics']['roi_percentage']}%
                    </div>
                    <div style="font-size: 12px; color: #a0a5ba; text-transform: uppercase; letter-spacing: 1px;">
                        ROI Programme
                    </div>
                </div>

                <div style="display: flex; align-items: center; gap: 1rem;">
                    <img src="https://logos-world.net/wp-content/uploads/2021/01/Ubisoft-Logo.png" 
                         style="height: 60px; opacity: 0.9; filter: brightness(0) invert(1);">
                    <div style="font-size: 12px; color: #a0a5ba; text-align: right;">
                        <div style="font-weight: 600;">© 2025 Ubisoft</div>
                        <div>Enterprise Edition</div>
                    </div>
                </div>
            </div>
        </div>

        <style>
        @keyframes rotate {{
            from {{ transform: rotate(0deg); }}
            to {{ transform: rotate(360deg); }}
        }}
        </style>
    </div>
    """, unsafe_allow_html=True)

# --- SIDEBAR ENTERPRISE ---
def render_enterprise_sidebar():
    with st.sidebar:
        # Header sidebar avec design Ubisoft
        st.markdown("""
        <div style="text-align: center; padding: 2rem 1rem; margin-bottom: 2rem; 
                    border-bottom: 2px solid rgba(0, 149, 255, 0.3); position: relative;">

            <div style="background: linear-gradient(135deg, #0095ff 0%, #ffb800 100%); 
                        width: 70px; height: 70px; border-radius: 50%; 
                        display: flex; align-items: center; justify-content: center; 
                        font-size: 28px; margin: 0 auto 1.5rem; color: #0a0e27; font-weight: bold;
                        box-shadow: 0 8px 25px rgba(0, 149, 255, 0.3); position: relative;">
                🧠
                <div style="position: absolute; inset: -3px; background: linear-gradient(135deg, #0095ff, #ffb800); 
                            border-radius: 50%; z-index: -1; opacity: 0.3; filter: blur(6px);"></div>
            </div>

            <h2 style="color: #ffb800; margin: 0; font-size: 22px; font-weight: 900;">
                NeuroInsight Hub
            </h2>
            <p style="color: #a0a5ba; margin: 0.5rem 0 0 0; font-size: 14px; font-weight: 500;">
                Enterprise HR Tool
            </p>
            <div style="background: linear-gradient(90deg, #0095ff, #ffb800); height: 2px; 
                        width: 50px; margin: 1rem auto; border-radius: 1px;"></div>
        </div>
        """, unsafe_allow_html=True)

        # Navigation Enterprise
        st.markdown("## 🎯 Navigation Enterprise")

        modules = [
            ("🏠", "Dashboard Principal"),
            ("🏢", "Manager Dashboard"),
            ("🧠", "Module TDAH"), 
            ("🎯", "Module Autisme"),
            ("📊", "Observatoire Analytics"),
            ("🔬", "NeuroScreen Pro"),
            ("🏢", "Workplace Solutions"),
            ("💼", "Recrutement Inclusif"),
            ("📈", "Business Intelligence"),
            ("💰", "ROI Calculator"),
            ("📋", "Compliance GDPR"),
            ("⚙️", "Enterprise Settings")
        ]

        page = st.selectbox(
            "Choisir un module",
            options=[f"{icon} {name}" for icon, name in modules],
            index=0
        )

        # Métriques temps réel avec design amélioré
        st.markdown("---")
        st.markdown("### 📊 Métriques Temps Réel")

        metrics_data = [
            ("Employés Neurodivers", ENTERPRISE_DATA['company_metrics']['neurodiverse_employees'], "+15", "#00d084"),
            ("Taux Rétention", f"{ENTERPRISE_DATA['company_metrics']['retention_rate']}%", "+2.8%", "#0095ff"),
            ("Score Satisfaction", f"{ENTERPRISE_DATA['company_metrics']['satisfaction_score']}/5", "+0.4", "#ffb800"),
            ("ROI Programme", f"{ENTERPRISE_DATA['company_metrics']['roi_percentage']}%", "+85%", "#ff6b35"),
            ("Compliance GDPR", f"{ENTERPRISE_DATA['compliance_metrics']['gdpr_score']}%", "✓", "#00d084")
        ]

        for label, value, delta, color in metrics_data:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(42, 47, 74, 0.8), rgba(26, 31, 58, 0.8)); 
                        border: 1px solid {color}; border-radius: 12px; padding: 1rem; margin-bottom: 0.8rem;
                        backdrop-filter: blur(10px); transition: all 0.3s ease;"
                 onmouseover="this.style.transform='translateX(4px)'; this.style.boxShadow='0 4px 20px {color}40';"
                 onmouseout="this.style.transform='translateX(0)'; this.style.boxShadow='none';">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                    <div style="color: #ffffff; font-size: 20px; font-weight: 800;">{value}</div>
                    <div style="color: {color}; font-size: 13px; font-weight: 700;">↗ {delta}</div>
                </div>
                <div style="color: #a0a5ba; font-size: 11px; font-weight: 500;">{label}</div>
            </div>
            """, unsafe_allow_html=True)

        # Status système
        st.markdown("---")
        st.markdown("### 🔧 Status Système")

        status_items = [
            ("API Status", "🟢 Opérationnel", "#00d084"),
            ("Base de Données", "🟢 Connectée", "#00d084"),
            ("Sécurité", "🟡 Monitoring", "#ffb800"),
            ("Backup", "🟢 Synchronisé", "#00d084")
        ]

        for item, status, color in status_items:
            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; align-items: center; 
                        padding: 0.5rem; margin-bottom: 0.3rem;">
                <span style="color: #a0a5ba; font-size: 12px;">{item}</span>
                <span style="color: {color}; font-size: 11px; font-weight: 600;">{status}</span>
            </div>
            """, unsafe_allow_html=True)

        return page

# --- FUNCTIONS UTILITAIRES ---
def generate_pdf_report(title, content, filename):
    """Génère un rapport PDF professionnel"""
    buffer = BytesIO()
    pdf = FPDF()
    pdf.add_page()

    # Header
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, title.encode('latin1', 'replace').decode('latin1'), 0, 1, 'C')
    pdf.ln(10)

    # Content
    pdf.set_font('Arial', '', 12)
    for line in content.split('\n'):
        if line.strip():
            pdf.cell(0, 8, line.encode('latin1', 'replace').decode('latin1'), 0, 1, 'L')

    # Save to buffer
    pdf_string = pdf.output(dest='S').encode('latin1')
    buffer.write(pdf_string)
    buffer.seek(0)

    return buffer

def calculate_accommodation_roi(base_salary, accommodation_cost, productivity_gain, retention_improvement):
    """Calcule le ROI d'une accommodation"""
    annual_productivity_value = base_salary * (productivity_gain / 100)
    retention_value = 15000 * (retention_improvement / 100)  # Coût évité de recrutement
    total_benefit = annual_productivity_value + retention_value
    roi = ((total_benefit - accommodation_cost) / accommodation_cost) * 100
    return {
        'annual_benefit': total_benefit,
        'roi_percentage': roi,
        'payback_months': (accommodation_cost / total_benefit * 12) if total_benefit > 0 else float('inf')
    }

# --- DASHBOARD PRINCIPAL ENTERPRISE ---
def dashboard_principal_enterprise():
    st.markdown("# 🏠 Dashboard Principal Enterprise")
    st.markdown("*Vue d'ensemble complète avec analytics avancés et intelligence d'affaires*")

    # KPIs Enterprise avec design amélioré
    col1, col2, col3, col4, col5 = st.columns(5)

    metrics = ENTERPRISE_DATA['company_metrics']

    with col1:
        st.metric("👥 Employés Total", f"{metrics['total_employees']:,}", "↗ +5.2%")

    with col2:
        st.metric("🧠 Neurodivers", f"{metrics['neurodiverse_employees']} ({metrics['neurodiverse_percentage']:.1f}%)", "↗ +3.8%")

    with col3:
        st.metric("📈 Productivité", f"+{metrics['productivity_increase']:.1f}%", "↗ +7.2%")

    with col4:
        st.metric("💰 ROI Programme", f"{metrics['roi_percentage']:,}%", "↗ +85%")

    with col5:
        st.metric("🎯 Satisfaction", f"{metrics['satisfaction_score']:.1f}/5.0", "↗ +0.4")

    st.markdown("---")

    # Graphiques Enterprise
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📊 Performance Équipes par Manager")

        team_df = pd.DataFrame(ENTERPRISE_DATA['team_metrics'])

        fig_teams = go.Figure()

        # Barres pour la productivité
        fig_teams.add_trace(go.Bar(
            name='Score Productivité',
            x=team_df['manager'],
            y=team_df['productivity_score'],
            marker_color='#0095ff',
            text=team_df['productivity_score'],
            textposition='auto',
            hovertemplate='<b>%{x}</b><br>Productivité: %{y}<br>Équipe: %{customdata[0]} membres<br>Neurodivers: %{customdata[1]}<extra></extra>',
            customdata=list(zip(team_df['team_size'], team_df['neurodiverse_count']))
        ))

        # Ligne pour la satisfaction
        fig_teams.add_trace(go.Scatter(
            name='Satisfaction',
            x=team_df['manager'],
            y=team_df['satisfaction'] * 30,  # Scale for visibility
            mode='lines+markers',
            line=dict(color='#ffb800', width=3),
            marker=dict(size=8, color='#ffb800'),
            yaxis='y2'
        ))

        fig_teams.update_layout(
            title='Performance & Satisfaction par Manager',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#ffffff'),
            xaxis=dict(gridcolor='#3a3f5a', tickangle=45),
            yaxis=dict(gridcolor='#3a3f5a', title='Score Productivité'),
            yaxis2=dict(title='Satisfaction (×30)', overlaying='y', side='right', gridcolor='#3a3f5a'),
            height=400
        )

        st.plotly_chart(fig_teams, use_container_width=True)

    with col2:
        st.markdown("### 🎯 Distribution Conditions Neurodivergentes")

        conditions_data = {
            'TDAH': metrics['adhd_employees'],
            'Autisme': metrics['autism_employees'], 
            'Dyslexie': metrics['dyslexia_employees'],
            'Autres': metrics['neurodiverse_employees'] - (metrics['adhd_employees'] + metrics['autism_employees'] + metrics['dyslexia_employees'])
        }

        fig_donut = go.Figure(data=[go.Pie(
            labels=list(conditions_data.keys()),
            values=list(conditions_data.values()),
            hole=0.6,
            marker=dict(
                colors=['#0095ff', '#ffb800', '#00d084', '#ff6b35'],
                line=dict(color='#0a0e27', width=3)
            ),
            textinfo='label+percent',
            textfont=dict(color='#ffffff', size=12),
            hovertemplate='<b>%{label}</b><br>Employés: %{value}<br>Pourcentage: %{percent}<extra></extra>'
        )])

        fig_donut.update_layout(
            title='Répartition par Condition',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#ffffff'),
            height=400,
            annotations=[dict(text=f'{metrics["neurodiverse_employees"]}<br>Total', x=0.5, y=0.5, 
                             font_size=20, font_color='#ffb800', showarrow=False)]
        )

        st.plotly_chart(fig_donut, use_container_width=True)

    # Section Insights Enterprise
    st.markdown("### 🔍 Insights & Recommandations Enterprise")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="enterprise-card">
            <h4 style="color: #00d084; margin-bottom: 1rem;">✅ Points Forts</h4>
            <ul style="color: #ffffff; line-height: 1.6;">
                <li>ROI programme exceptionnel: <strong>415%</strong></li>
                <li>Taux de rétention élevé: <strong>94.8%</strong></li>
                <li>Satisfaction employés: <strong>4.4/5.0</strong></li>
                <li>Conformité GDPR: <strong>99.2%</strong></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="enterprise-card">
            <h4 style="color: #ffb800; margin-bottom: 1rem;">⚠️ Points d'Attention</h4>
            <ul style="color: #ffffff; line-height: 1.6;">
                <li>Variabilité performance inter-équipes</li>
                <li>Besoins formation managers</li>
                <li>Optimisation processus screening</li>
                <li>Harmonisation accommodations</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="enterprise-card">
            <h4 style="color: #0095ff; margin-bottom: 1rem;">🎯 Recommandations</h4>
            <ul style="color: #ffffff; line-height: 1.6;">
                <li>Déployer formation managers</li>
                <li>Standardiser best practices</li>
                <li>Élargir programme inclusion</li>
                <li>Benchmark industrie</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# --- MANAGER DASHBOARD ENTERPRISE ---
def manager_dashboard_enterprise():
    st.markdown("# 🏢 Manager Dashboard Enterprise")
    st.markdown("*Outils avancés pour managers - Insights équipe et recommandations personnalisées*")

    # Sélection manager
    managers = [team['manager'] for team in ENTERPRISE_DATA['team_metrics']]
    selected_manager = st.selectbox("👨‍💼 Sélectionner un Manager", managers)

    # Données équipe sélectionnée
    team_data = next(team for team in ENTERPRISE_DATA['team_metrics'] if team['manager'] == selected_manager)

    # KPIs Manager
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("👥 Taille Équipe", team_data['team_size'], delta=None)
    with col2:
        st.metric("🧠 Neurodivers", f"{team_data['neurodiverse_count']}/{team_data['team_size']}", 
                 delta=f"{(team_data['neurodiverse_count']/team_data['team_size']*100):.1f}%")
    with col3:
        st.metric("📈 Productivité", team_data['productivity_score'], delta="+12 pts")
    with col4:
        st.metric("😊 Satisfaction", f"{team_data['satisfaction']:.1f}/5", delta="+0.3")
    with col5:
        st.metric("💰 ROI Équipe", f"{team_data['roi']}%", delta="+45%")

    st.markdown("---")

    # Tabs Manager Dashboard
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Vue d'Ensemble Équipe", 
        "🎯 Recommandations", 
        "💼 Guidelines Manager", 
        "📈 ROI Calculator", 
        "📋 Compliance"
    ])

    with tab1:
        st.markdown("### 📊 Team Neurodiversity Overview (Anonymisé)")

        col1, col2 = st.columns(2)

        with col1:
            # Graphique radar des compétences équipe
            categories = ['Créativité', 'Attention Détails', 'Résolution Problèmes', 
                         'Innovation', 'Collaboration', 'Efficacité']

            # Données simulées basées sur composition neurodivergente
            neuro_ratio = team_data['neurodiverse_count'] / team_data['team_size']
            base_scores = [75, 80, 78, 85, 82, 88]
            neuro_boost = [25, 20, 22, 15, 5, 12]  # Boost lié à la neurodiversité

            team_scores = [base + (boost * neuro_ratio) for base, boost in zip(base_scores, neuro_boost)]

            fig_radar = go.Figure()

            fig_radar.add_trace(go.Scatterpolar(
                r=team_scores,
                theta=categories,
                fill='toself',
                name=f'Équipe {selected_manager}',
                line_color='#0095ff',
                fillcolor='rgba(0, 149, 255, 0.2)'
            ))

            # Moyenne entreprise pour comparaison
            company_avg = [82, 75, 80, 78, 85, 83]
            fig_radar.add_trace(go.Scatterpolar(
                r=company_avg,
                theta=categories,
                fill='toself',
                name='Moyenne Entreprise',
                line_color='#ffb800',
                fillcolor='rgba(255, 184, 0, 0.1)',
                line_dash='dash'
            ))

            fig_radar.update_layout(
                polar=dict(
                    bgcolor='rgba(0,0,0,0)',
                    radialaxis=dict(
                        visible=True,
                        range=[0, 120],
                        gridcolor='#3a3f5a',
                        tickfont=dict(color='#a0a5ba')
                    ),
                    angularaxis=dict(
                        gridcolor='#3a3f5a',
                        tickfont=dict(color='#ffffff')
                    )
                ),
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#ffffff'),
                title='Profil Compétences Équipe vs Moyenne Entreprise'
            )

            st.plotly_chart(fig_radar, use_container_width=True)

        with col2:
            # Métriques détaillées équipe
            st.markdown("#### 📈 Métriques Détaillées")

            # Données simulées pour l'équipe
            metrics_detail = {
                "Projets Complétés": {"value": 23, "vs_avg": "+18%", "color": "#00d084"},
                "Délais Respectés": {"value": "94%", "vs_avg": "+12%", "color": "#0095ff"}, 
                "Innovation Score": {"value": 8.7, "vs_avg": "+23%", "color": "#ffb800"},
                "Collaboration": {"value": "92%", "vs_avg": "+8%", "color": "#00d084"},
                "Absentéisme": {"value": "2.1%", "vs_avg": "-35%", "color": "#00d084"},
                "Turnover": {"value": "0%", "vs_avg": "-100%", "color": "#00d084"}
            }

            for metric, data in metrics_detail.items():
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, rgba(42, 47, 74, 0.8), rgba(26, 31, 58, 0.8)); 
                            border-left: 4px solid {data['color']}; border-radius: 8px; 
                            padding: 1rem; margin-bottom: 0.8rem;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <div style="color: #a0a5ba; font-size: 12px; margin-bottom: 0.2rem;">{metric}</div>
                            <div style="color: #ffffff; font-size: 18px; font-weight: 700;">{data['value']}</div>
                        </div>
                        <div style="color: {data['color']}; font-size: 14px; font-weight: 600;">
                            {data['vs_avg']}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    with tab2:
        st.markdown("### 🎯 Accommodation Recommendations Generator")

        # Générateur de recommandations personnalisées
        st.markdown("#### Configuration Équipe")

        col1, col2 = st.columns(2)

        with col1:
            team_composition = st.multiselect(
                "Composition Neurodivergente Équipe",
                ["ADHD", "Autism", "Dyslexia", "General"],
                default=["ADHD", "Autism"]
            )

            priority_areas = st.multiselect(
                "Domaines Prioritaires",
                ["Productivité", "Collaboration", "Innovation", "Bien-être", "Communication"],
                default=["Productivité", "Bien-être"]
            )

        with col2:
            budget_range = st.select_slider(
                "Budget Accommodations (€/employé/an)",
                options=[500, 1000, 2000, 5000, 10000],
                value=2000
            )

            urgency = st.radio(
                "Urgence Implementation",
                ["Immédiate (1-7 jours)", "Court terme (1-4 semaines)", "Moyen terme (1-3 mois)"]
            )

        if st.button("🎯 Générer Recommandations Personnalisées", key="recommendations"):
            st.markdown("#### 📋 Recommandations Générées")

            # Filtrer accommodations basées sur la configuration
            filtered_accommodations = [
                acc for acc in ENTERPRISE_DATA['accommodation_database'] 
                if any(condition in team_composition for condition in [acc['condition']] + ['General']) 
                and acc['cost'] <= budget_range
            ]

            # Trier par ROI
            filtered_accommodations.sort(key=lambda x: x['roi'], reverse=True)

            # Afficher top 5 recommandations
            for i, acc in enumerate(filtered_accommodations[:5]):
                priority_badge = "🔥 HAUTE" if i < 2 else "⭐ MOYENNE" if i < 4 else "💡 FAIBLE"

                st.markdown(f"""
                <div class="manager-card">
                    <div style="display: flex; justify-content: between; align-items: start; margin-bottom: 1rem;">
                        <h4 style="color: #ffb800; margin: 0; flex: 1;">{acc['accommodation']}</h4>
                        <span style="background: #0095ff; color: #ffffff; padding: 0.3rem 0.8rem; 
                                    border-radius: 12px; font-size: 11px; font-weight: 600;">{priority_badge}</span>
                    </div>

                    <p style="color: #a0a5ba; margin-bottom: 1.5rem; line-height: 1.5;">
                        {acc['description']}
                    </p>

                    <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem;">
                        <div>
                            <div style="color: #a0a5ba; font-size: 11px; margin-bottom: 0.3rem;">COÛT</div>
                            <div style="color: #ffffff; font-weight: 600;">{acc['cost']}€</div>
                        </div>
                        <div>
                            <div style="color: #a0a5ba; font-size: 11px; margin-bottom: 0.3rem;">IMPLÉMENTATION</div>
                            <div style="color: #ffffff; font-weight: 600;">{acc['implementation_days']} jours</div>
                        </div>
                        <div>
                            <div style="color: #a0a5ba; font-size: 11px; margin-bottom: 0.3rem;">SUCCÈS</div>
                            <div style="color: #00d084; font-weight: 600;">{acc['success_rate']}%</div>
                        </div>
                        <div>
                            <div style="color: #a0a5ba; font-size: 11px; margin-bottom: 0.3rem;">ROI</div>
                            <div style="color: #ffb800; font-weight: 600;">{acc['roi']}%</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    with tab3:
        st.markdown("### 💼 Manager Guidelines Personnalisées")

        # Guidelines basées sur la composition de l'équipe
        neuro_ratio = team_data['neurodiverse_count'] / team_data['team_size']

        guidelines_sections = [
            {
                "title": "🗣️ Communication Efficace",
                "tips": [
                    "Privilégier les instructions écrites et détaillées",
                    "Éviter les consignes implicites ou sous-entendues", 
                    "Confirmer la compréhension par reformulation",
                    "Utiliser des canaux asynchrones (Slack/Teams)"
                ]
            },
            {
                "title": "📅 Organisation & Planning",
                "tips": [
                    "Décomposer les projets complexes en micro-tâches",
                    "Définir des deadlines intermédiaires claires",
                    "Prévoir des temps de buffer pour adaptation",
                    "Maintenir des routines prévisibles"
                ]
            },
            {
                "title": "🎯 Feedback & Évaluation", 
                "tips": [
                    "Fournir un feedback fréquent et constructif",
                    "Se concentrer sur les résultats, pas les méthodes",
                    "Célébrer les réussites et forces uniques",
                    "Adapter les critères d'évaluation"
                ]
            },
            {
                "title": "🤝 Gestion d'Équipe Inclusive",
                "tips": [
                    "Sensibiliser l'équipe à la neurodiversité",
                    "Favoriser l'entraide et la complémentarité",
                    "Adapter l'assignation des tâches aux profils",
                    "Créer un environnement psychologique sécurisant"
                ]
            }
        ]

        for section in guidelines_sections:
            with st.expander(f"**{section['title']}**", expanded=True):
                for tip in section['tips']:
                    st.markdown(f"• {tip}")

        # Ressources additionnelles
        st.markdown("#### 📚 Ressources Complémentaires")

        resources = [
            {"title": "Guide Complet Manager Neurodiversité", "type": "PDF", "size": "2.3 MB"},
            {"title": "Checklist Onboarding Inclusif", "type": "Excel", "size": "156 KB"},
            {"title": "Templates Communication Adaptée", "type": "Word", "size": "892 KB"},
            {"title": "Formation Interactive Neurodiversité", "type": "Lien", "size": "45 min"}
        ]

        for resource in resources:
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.markdown(f"📄 **{resource['title']}**")
            with col2:
                st.markdown(f"`{resource['type']}`")
            with col3:
                st.button("📥 Télécharger", key=f"dl_{resource['title'][:10]}")

    with tab4:
        st.markdown("### 📈 ROI Impact Calculator")

        st.markdown("""
        <div class="roi-calculator">
            <h4 style="color: #ffb800; margin-bottom: 1.5rem;">💰 Calculateur ROI Accommodations</h4>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### 📊 Paramètres Équipe")

            avg_salary = st.number_input(
                "Salaire Moyen Équipe (€/an)",
                min_value=30000,
                max_value=120000,
                value=55000,
                step=5000
            )

            accommodation_budget = st.number_input(
                "Budget Accommodations (€/an)",
                min_value=500,
                max_value=20000,
                value=3500,
                step=500
            )

            expected_productivity_gain = st.slider(
                "Gain Productivité Attendu (%)",
                min_value=5,
                max_value=40,
                value=18,
                step=1
            )

            retention_improvement = st.slider(
                "Amélioration Rétention (%)",
                min_value=5,
                max_value=30,
                value=12,
                step=1
            )

        with col2:
            st.markdown("#### 📈 Calculs ROI")

            # Calculs
            productivity_value = avg_salary * (expected_productivity_gain / 100) * team_data['team_size']
            retention_value = 15000 * (retention_improvement / 100) * team_data['neurodiverse_count']
            total_annual_benefit = productivity_value + retention_value
            total_cost = accommodation_budget * team_data['team_size']
            roi_percent = ((total_annual_benefit - total_cost) / total_cost) * 100 if total_cost > 0 else 0
            payback_months = (total_cost / total_annual_benefit * 12) if total_annual_benefit > 0 else 0

            # Affichage résultats
            results = [
                ("💰 Bénéfice Annuel Total", f"{total_annual_benefit:,.0f}€", "#00d084"),
                ("💸 Coût Total Accommodations", f"{total_cost:,.0f}€", "#ff6b35"),
                ("📈 ROI Calculé", f"{roi_percent:.0f}%", "#ffb800"),
                ("⏱️ Retour sur Investissement", f"{payback_months:.1f} mois", "#0095ff"),
                ("💎 Valeur Nette", f"{total_annual_benefit - total_cost:,.0f}€", "#00d084")
            ]

            for label, value, color in results:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, rgba(42, 47, 74, 0.8), rgba(26, 31, 58, 0.8)); 
                            border-left: 4px solid {color}; border-radius: 8px; 
                            padding: 1rem; margin-bottom: 0.8rem;">
                    <div style="color: #a0a5ba; font-size: 12px; margin-bottom: 0.3rem;">{label}</div>
                    <div style="color: {color}; font-size: 22px; font-weight: 800;">{value}</div>
                </div>
                """, unsafe_allow_html=True)

        # Bouton génération rapport
        if st.button("📊 Générer Rapport ROI Détaillé", key="roi_report"):
            report_content = f"""
RAPPORT ROI - ÉQUIPE {selected_manager.upper()}
=====================================

PARAMÈTRES:
- Taille équipe: {team_data['team_size']} employés
- Employés neurodivers: {team_data['neurodiverse_count']}
- Salaire moyen: {avg_salary:,}€
- Budget accommodations: {accommodation_budget:,}€/employé

RÉSULTATS:
- Bénéfice annuel: {total_annual_benefit:,.0f}€
- Coût total: {total_cost:,.0f}€
- ROI: {roi_percent:.0f}%
- Retour sur investissement: {payback_months:.1f} mois

RECOMMANDATIONS:
- Programme fortement rentable
- Déploiement recommandé
- Suivi trimestriel des métriques
            """

            pdf_buffer = generate_pdf_report(
                f"Rapport ROI - Équipe {selected_manager}",
                report_content,
                f"roi_report_{selected_manager.lower().replace(' ', '_')}"
            )

            st.download_button(
                label="📥 Télécharger Rapport PDF",
                data=pdf_buffer,
                file_name=f"roi_report_{selected_manager.lower().replace(' ', '_')}.pdf",
                mime="application/pdf"
            )

        st.markdown("</div>", unsafe_allow_html=True)

    with tab5:
        st.markdown("### 📋 Compliance Reports (GDPR/AI Act)")

        st.markdown("""
        <div class="compliance-dashboard">
            <h4 style="color: #00d084; margin-bottom: 1.5rem;">✅ Tableau de Bord Conformité</h4>
        """, unsafe_allow_html=True)

        compliance_data = ENTERPRISE_DATA['compliance_metrics']

        # Métriques conformité
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("GDPR Score", f"{compliance_data['gdpr_score']:.1f}%", "↗ +0.3%")
        with col2:
            st.metric("AI Act Compliance", f"{compliance_data['ai_act_compliance']:.1f}%", "↗ +2.1%")
        with col3:
            st.metric("Accessibilité", f"{compliance_data['accessibility_score']:.1f}%", "↗ +1.8%")
        with col4:
            st.metric("Formation", f"{compliance_data['training_compliance']:.1f}%", "↗ +0.5%")

        # Détails conformité
        st.markdown("#### 📊 Détails Conformité par Domaine")

        compliance_areas = [
            {"area": "Protection Données Personnelles", "score": 99.5, "status": "✅ Conforme", "last_audit": "2025-08-15"},
            {"area": "Consentement & Transparence", "score": 98.8, "status": "✅ Conforme", "last_audit": "2025-08-12"},
            {"area": "Droits Employés (GDPR)", "score": 99.1, "status": "✅ Conforme", "last_audit": "2025-08-10"},
            {"area": "IA Éthique & Non-Discrimination", "score": 97.5, "status": "⚠️ Surveillance", "last_audit": "2025-08-08"},
            {"area": "Accessibilité Numérique", "score": 94.2, "status": "✅ Conforme", "last_audit": "2025-08-05"},
            {"area": "Sécurité Système", "score": 99.8, "status": "✅ Excellent", "last_audit": "2025-08-18"}
        ]

        for area in compliance_areas:
            col1, col2, col3, col4 = st.columns([3, 1, 2, 2])

            with col1:
                st.markdown(f"**{area['area']}**")
            with col2:
                color = "#00d084" if area['score'] >= 95 else "#ffb800" if area['score'] >= 90 else "#ff6b35"
                st.markdown(f"<span style='color: {color}; font-weight: 700;'>{area['score']:.1f}%</span>", 
                           unsafe_allow_html=True)
            with col3:
                st.markdown(area['status'])
            with col4:
                st.markdown(f"`{area['last_audit']}`")

        # Actions conformité
        st.markdown("#### ⚡ Actions Rapides")

        action_col1, action_col2, action_col3 = st.columns(3)

        with action_col1:
            if st.button("📊 Générer Audit Report", key="audit_report"):
                st.success("✅ Rapport d'audit généré et envoyé au DPO")

        with action_col2:
            if st.button("🔒 Vérifier Consentements", key="check_consent"):
                st.info("🔍 Vérification en cours... 23/23 consentements valides")

        with action_col3:
            if st.button("📋 Export Conformité", key="export_compliance"):
                compliance_report = f"""
RAPPORT CONFORMITÉ - {datetime.now().strftime('%Y-%m-%d')}
==========================================

SCORES GLOBAUX:
- GDPR: {compliance_data['gdpr_score']:.1f}%
- AI Act: {compliance_data['ai_act_compliance']:.1f}%
- Accessibilité: {compliance_data['accessibility_score']:.1f}%

STATUS: {"✅ CONFORME" if compliance_data['gdpr_score'] >= 95 else "⚠️ ATTENTION"}

DERNIERS AUDITS:
- Audit général: {compliance_data['audit_last_date']}
- Certification: {compliance_data['certification_status']}
- Incidents: {compliance_data['data_breaches']} breach(es)

RECOMMANDATIONS:
- Maintenir niveau excellent
- Suivi continu IA Act
- Formation équipes
                """

                pdf_buffer = generate_pdf_report(
                    "Rapport Conformité Enterprise",
                    compliance_report,
                    "compliance_report"
                )

                st.download_button(
                    label="📥 Télécharger PDF",
                    data=pdf_buffer,
                    file_name=f"compliance_report_{datetime.now().strftime('%Y%m%d')}.pdf",
                    mime="application/pdf"
                )

        st.markdown("</div>", unsafe_allow_html=True)

        # Alertes conformité
        st.markdown("#### 🚨 Alertes & Notifications")

        alerts = [
            {"type": "info", "message": "Mise à jour GDPR disponible - Formation équipe recommandée", "date": "2025-08-20"},
            {"type": "success", "message": "Audit sécurité passé avec succès (99.8%)", "date": "2025-08-18"},
            {"type": "warning", "message": "AI Act - Nouvelles guidelines à implémenter d'ici fin septembre", "date": "2025-08-15"}
        ]

        for alert in alerts:
            alert_color = {"info": "#0095ff", "success": "#00d084", "warning": "#ffb800", "error": "#ff6b35"}[alert['type']]
            alert_icon = {"info": "ℹ️", "success": "✅", "warning": "⚠️", "error": "🚨"}[alert['type']]

            st.markdown(f"""
            <div style="background: rgba{tuple(list(bytes.fromhex(alert_color[1:])) + [26])}; 
                        border: 1px solid {alert_color}; border-left: 4px solid {alert_color};
                        border-radius: 8px; padding: 1rem; margin-bottom: 0.8rem;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div style="display: flex; align-items: center; gap: 0.5rem;">
                        <span style="font-size: 16px;">{alert_icon}</span>
                        <span style="color: #ffffff;">{alert['message']}</span>
                    </div>
                    <span style="color: #a0a5ba; font-size: 12px;">{alert['date']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

# --- MODULE ROI CALCULATOR STANDALONE ---
def roi_calculator_enterprise():
    st.markdown("# 💰 ROI Calculator Enterprise")
    st.markdown("*Calculateur avancé de retour sur investissement pour programmes neurodiversité*")

    st.markdown("""
    <div class="roi-calculator">
        <h3 style="color: #ffb800; margin-bottom: 2rem;">🎯 Calculateur ROI Complet</h3>
    """, unsafe_allow_html=True)

    # Configuration entreprise
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 🏢 Paramètres Entreprise")

        company_size = st.number_input(
            "Nombre d'employés total",
            min_value=50,
            max_value=10000,
            value=1847,
            step=50
        )

        neurodiverse_percentage = st.slider(
            "Pourcentage employés neurodivers (%)",
            min_value=5.0,
            max_value=30.0,
            value=15.5,
            step=0.5
        )

        average_salary = st.number_input(
            "Salaire annuel moyen (€)",
            min_value=30000,
            max_value=120000,
            value=55000,
            step=2500
        )

        program_duration = st.selectbox(
            "Durée programme (années)",
            options=[1, 2, 3, 5],
            index=2
        )

    with col2:
        st.markdown("#### 📈 Impacts Attendus")

        productivity_gain = st.slider(
            "Gain productivité (%)",
            min_value=5,
            max_value=40,
            value=22,
            step=1
        )

        retention_improvement = st.slider(
            "Amélioration rétention (%)",
            min_value=5,
            max_value=30,
            value=12,
            step=1
        )

        innovation_boost = st.slider(
            "Boost innovation (%)",
            min_value=10,
            max_value=50,
            value=25,
            step=5
        )

        absence_reduction = st.slider(
            "Réduction absentéisme (%)",
            min_value=5,
            max_value=25,
            value=8,
            step=1
        )

    # Coûts programme
    st.markdown("#### 💸 Coûts Programme")

    cost_col1, cost_col2, cost_col3 = st.columns(3)

    with cost_col1:
        accommodation_cost = st.number_input(
            "Coût accommodations/employé/an (€)",
            min_value=500,
            max_value=15000,
            value=2500,
            step=250
        )

    with cost_col2:
        training_cost = st.number_input(
            "Formation managers/RH (€)",
            min_value=5000,
            max_value=100000,
            value=25000,
            step=2500
        )

    with cost_col3:
        system_cost = st.number_input(
            "Systèmes/Outils (€/an)",
            min_value=2000,
            max_value=50000,
            value=15000,
            step=1000
        )

    # Calculs ROI
    if st.button("🚀 Calculer ROI Complet", key="full_roi_calc"):

        # Nombre employés neurodivers
        neurodiverse_count = int(company_size * neurodiverse_percentage / 100)

        # Bénéfices annuels
        productivity_value = neurodiverse_count * average_salary * (productivity_gain / 100)
        retention_value = neurodiverse_count * 15000 * (retention_improvement / 100)  # Coût évité recrutement
        innovation_value = company_size * 2000 * (innovation_boost / 100)  # Valeur innovation
        absence_value = neurodiverse_count * 1500 * (absence_reduction / 100)  # Économies absences

        total_annual_benefits = productivity_value + retention_value + innovation_value + absence_value

        # Coûts annuels
        total_accommodation_cost = neurodiverse_count * accommodation_cost
        annual_training_cost = training_cost / program_duration  # Amortissement formation
        total_annual_costs = total_accommodation_cost + annual_training_cost + system_cost

        # ROI
        net_annual_benefit = total_annual_benefits - total_annual_costs
        roi_percentage = (net_annual_benefit / total_annual_costs) * 100 if total_annual_costs > 0 else 0
        payback_period = total_annual_costs / total_annual_benefits if total_annual_benefits > 0 else 0

        # Bénéfices cumulés sur période
        cumulative_benefits = total_annual_benefits * program_duration
        cumulative_costs = (total_accommodation_cost * program_duration) + training_cost + (system_cost * program_duration)
        total_roi = ((cumulative_benefits - cumulative_costs) / cumulative_costs) * 100

        # Affichage résultats
        st.markdown("## 📊 Résultats ROI Détaillés")

        # Métriques principales
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("🎯 ROI Annuel", f"{roi_percentage:.0f}%", delta=f"+{roi_percentage-100:.0f} pts")
        with col2:
            st.metric("💰 Bénéfice Net/An", f"{net_annual_benefit:,.0f}€", delta="Positif")
        with col3:
            st.metric("⏱️ Retour Investiss.", f"{payback_period:.1f} ans", delta="Court terme")
        with col4:
            st.metric("🚀 ROI Total", f"{total_roi:.0f}%", delta=f"{program_duration} ans")

        # Breakdown détaillé
        st.markdown("### 📈 Décomposition Bénéfices Annuels")

        benefits_data = {
            'Source': ['Productivité', 'Rétention', 'Innovation', 'Absentéisme'],
            'Montant (€)': [productivity_value, retention_value, innovation_value, absence_value],
            'Pourcentage': [
                (productivity_value / total_annual_benefits * 100),
                (retention_value / total_annual_benefits * 100), 
                (innovation_value / total_annual_benefits * 100),
                (absence_value / total_annual_benefits * 100)
            ]
        }

        benefits_df = pd.DataFrame(benefits_data)

        # Graphique bénéfices
        fig_benefits = go.Figure(data=[
            go.Bar(
                x=benefits_df['Source'],
                y=benefits_df['Montant (€)'],
                marker_color=['#0095ff', '#ffb800', '#00d084', '#ff6b35'],
                text=[f"{val:,.0f}€" for val in benefits_df['Montant (€)']],
                textposition='auto'
            )
        ])

        fig_benefits.update_layout(
            title='Répartition Bénéfices Annuels par Source',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#ffffff'),
            xaxis=dict(gridcolor='#3a3f5a'),
            yaxis=dict(gridcolor='#3a3f5a', title='Montant (€)'),
            height=400
        )

        st.plotly_chart(fig_benefits, use_container_width=True)

        # Évolution ROI sur période
        st.markdown("### 📅 Évolution ROI sur Période")

        years = list(range(1, program_duration + 1))
        cumulative_roi = []
        for year in years:
            year_benefits = total_annual_benefits * year
            year_costs = (total_accommodation_cost * year) + training_cost + (system_cost * year)
            year_roi = ((year_benefits - year_costs) / year_costs) * 100 if year_costs > 0 else 0
            cumulative_roi.append(year_roi)

        fig_evolution = go.Figure()

        fig_evolution.add_trace(go.Scatter(
            x=years,
            y=cumulative_roi,
            mode='lines+markers',
            name='ROI Cumulé',
            line=dict(color='#0095ff', width=4),
            marker=dict(size=10, color='#ffb800'),
            fill='tonexty'
        ))

        fig_evolution.update_layout(
            title='Évolution ROI Cumulé par Année',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#ffffff'),
            xaxis=dict(gridcolor='#3a3f5a', title='Années'),
            yaxis=dict(gridcolor='#3a3f5a', title='ROI (%)'),
            height=400
        )

        st.plotly_chart(fig_evolution, use_container_width=True)

        # Rapport détaillé
        if st.button("📋 Générer Rapport ROI Complet", key="complete_roi_report"):
            detailed_report = f"""
RAPPORT ROI PROGRAMME NEURODIVERSITÉ - ANALYSE COMPLÈTE
======================================================

DATE: {datetime.now().strftime('%d/%m/%Y')}
ENTREPRISE: {company_size:,} employés

PARAMÈTRES:
- Employés neurodivers: {neurodiverse_count:,} ({neurodiverse_percentage:.1f}%)
- Salaire moyen: {average_salary:,}€
- Durée programme: {program_duration} ans

BÉNÉFICES ANNUELS:
- Productivité: {productivity_value:,.0f}€
- Rétention: {retention_value:,.0f}€  
- Innovation: {innovation_value:,.0f}€
- Absentéisme: {absence_value:,.0f}€
TOTAL: {total_annual_benefits:,.0f}€

COÛTS ANNUELS:
- Accommodations: {total_accommodation_cost:,.0f}€
- Formation: {annual_training_cost:,.0f}€
- Systèmes: {system_cost:,.0f}€
TOTAL: {total_annual_costs:,.0f}€

RÉSULTATS:
- ROI Annuel: {roi_percentage:.0f}%
- Bénéfice Net: {net_annual_benefit:,.0f}€/an
- ROI Total ({program_duration} ans): {total_roi:.0f}%
- Payback: {payback_period:.1f} années

RECOMMANDATIONS:
{"✅ Programme hautement rentable - Déploiement immédiat recommandé" if roi_percentage > 200 else "⚠️ Programme modérément rentable - Optimisation recommandée" if roi_percentage > 50 else "❌ Programme peu rentable - Révision nécessaire"}

PROCHAINES ÉTAPES:
1. Validation budgétaire direction
2. Plan déploiement par phases
3. KPIs suivi et mesure impact
4. Formation équipes RH/Management
            """

            pdf_buffer = generate_pdf_report(
                "Rapport ROI Programme Neurodiversité - Analyse Complète",
                detailed_report,
                "roi_complete_analysis"
            )

            st.download_button(
                label="📥 Télécharger Rapport PDF Complet",
                data=pdf_buffer,
                file_name=f"roi_analysis_complete_{datetime.now().strftime('%Y%m%d')}.pdf",
                mime="application/pdf"
            )

    st.markdown("</div>", unsafe_allow_html=True)

# --- COMPLIANCE GDPR STANDALONE ---
def compliance_gdpr_enterprise():
    st.markdown("# 📋 Compliance GDPR Enterprise")
    st.markdown("*Dashboard conformité avancé avec monitoring temps réel*")

    compliance_data = ENTERPRISE_DATA['compliance_metrics']

    # Header conformité
    st.markdown("""
    <div class="compliance-dashboard">
        <h3 style="color: #00d084; margin-bottom: 2rem;">🛡️ Dashboard Conformité GDPR & AI Act</h3>
    """, unsafe_allow_html=True)

    # Scores globaux
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("🛡️ GDPR Global", f"{compliance_data['gdpr_score']:.1f}%", "↗ +0.3%")
    with col2:
        st.metric("🤖 AI Act", f"{compliance_data['ai_act_compliance']:.1f}%", "↗ +2.1%")
    with col3:
        st.metric("♿ Accessibilité", f"{compliance_data['accessibility_score']:.1f}%", "↗ +1.8%")
    with col4:
        st.metric("🎓 Formation", f"{compliance_data['training_compliance']:.1f}%", "↗ +0.5%")

    # Tabs conformité
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Vue d'Ensemble", 
        "🛡️ GDPR Détails", 
        "🤖 AI Act Monitoring",
        "📋 Audits & Rapports",
        "⚡ Actions Rapides"
    ])

    with tab1:
        st.markdown("### 📈 Score Conformité par Domaine")

        # Données conformité détaillées
        compliance_areas = {
            'Protection Données': 99.5,
            'Consentement': 98.8,
            'Droits Employés': 99.1,
            'Sécurité Système': 99.8,
            'Transparence': 97.2,
            'Formation Équipes': 98.1,
            'Documentation': 96.8,
            'Incidents': 100.0
        }

        # Graphique radar conformité
        fig_compliance = go.Figure()

        fig_compliance.add_trace(go.Scatterpolar(
            r=list(compliance_areas.values()),
            theta=list(compliance_areas.keys()),
            fill='toself',
            name='Scores Actuels',
            line_color='#00d084',
            fillcolor='rgba(0, 208, 132, 0.2)'
        ))

        # Target compliance (100%)
        target_scores = [100] * len(compliance_areas)
        fig_compliance.add_trace(go.Scatterpolar(
            r=target_scores,
            theta=list(compliance_areas.keys()),
            fill='toself',
            name='Cible (100%)',
            line_color='#ffb800',
            fillcolor='rgba(255, 184, 0, 0.1)',
            line_dash='dash'
        ))

        fig_compliance.update_layout(
            polar=dict(
                bgcolor='rgba(0,0,0,0)',
                radialaxis=dict(
                    visible=True,
                    range=[80, 100],
                    gridcolor='#3a3f5a',
                    tickfont=dict(color='#a0a5ba')
                ),
                angularaxis=dict(
                    gridcolor='#3a3f5a',
                    tickfont=dict(color='#ffffff', size=10)
                )
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#ffffff'),
            title='Profil Conformité Détaillé',
            height=500
        )

        st.plotly_chart(fig_compliance, use_container_width=True)

        # Timeline conformité
        st.markdown("### 📅 Timeline Conformité Récente")

        timeline_events = [
            {"date": "2025-08-18", "event": "Audit sécurité réussi", "score": 99.8, "type": "success"},
            {"date": "2025-08-15", "event": "Mise à jour politique GDPR", "score": 99.2, "type": "info"},
            {"date": "2025-08-12", "event": "Formation équipe RH", "score": 98.1, "type": "success"},
            {"date": "2025-08-10", "event": "Révision droits employés", "score": 99.1, "type": "success"},
            {"date": "2025-08-08", "event": "AI Act - Nouvelle directive", "score": 97.8, "type": "warning"}
        ]

        for event in timeline_events:
            color_map = {"success": "#00d084", "info": "#0095ff", "warning": "#ffb800", "error": "#ff6b35"}
            icon_map = {"success": "✅", "info": "ℹ️", "warning": "⚠️", "error": "🚨"}

            st.markdown(f"""
            <div style="display: flex; align-items: center; gap: 1rem; padding: 1rem; 
                        background: rgba{tuple(list(bytes.fromhex(color_map[event['type']][1:])) + [26])};
                        border-left: 4px solid {color_map[event['type']]}; border-radius: 8px; margin-bottom: 0.8rem;">
                <div style="font-size: 20px;">{icon_map[event['type']]}</div>
                <div style="flex: 1;">
                    <div style="color: #ffffff; font-weight: 600;">{event['event']}</div>
                    <div style="color: #a0a5ba; font-size: 12px;">{event['date']}</div>
                </div>
                <div style="color: {color_map[event['type']]}; font-weight: 700; font-size: 16px;">
                    {event['score']:.1f}%
                </div>
            </div>
            """, unsafe_allow_html=True)

    with tab2:
        st.markdown("### 🛡️ GDPR - Analyse Détaillée")

        # Métriques GDPR spécifiques
        gdpr_metrics = [
            {"metric": "Demandes d'accès traitées", "value": compliance_data['privacy_requests_handled'], "target": 25, "unit": "demandes"},
            {"metric": "Violations de données", "value": compliance_data['data_breaches'], "target": 0, "unit": "incidents"},
            {"metric": "Temps réponse moyen", "value": 8.5, "target": 30, "unit": "jours"},
            {"metric": "Consentements valides", "value": 99.8, "target": 100, "unit": "%"},
            {"metric": "Données anonymisées", "value": 94.2, "target": 95, "unit": "%"},
            {"metric": "Politiques à jour", "value": 100, "target": 100, "unit": "%"}
        ]

        for metric in gdpr_metrics:
            col1, col2, col3 = st.columns([2, 1, 1])

            with col1:
                st.markdown(f"**{metric['metric']}**")
            with col2:
                color = "#00d084" if metric['value'] <= metric['target'] else "#ffb800"
                st.markdown(f"<span style='color: {color}; font-weight: 700;'>{metric['value']} {metric['unit']}</span>", 
                           unsafe_allow_html=True)
            with col3:
                st.markdown(f"Cible: {metric['target']} {metric['unit']}")

        # Checklist GDPR
        st.markdown("### ✅ Checklist Conformité GDPR")

        gdpr_checklist = [
            {"item": "Registre des traitements à jour", "status": True},
            {"item": "Analyse d'impact (DPIA) effectuée", "status": True},
            {"item": "Procédures notification violations", "status": True},
            {"item": "Formation DPO et équipes", "status": True},
            {"item": "Contrats sous-traitants conformes", "status": True},
            {"item": "Procédure exercice droits", "status": True},
            {"item": "Privacy by design implémenté", "status": False},
            {"item": "Audit externe réalisé", "status": True}
        ]

        col1, col2 = st.columns(2)

        for i, item in enumerate(gdpr_checklist):
            with col1 if i % 2 == 0 else col2:
                icon = "✅" if item['status'] else "❌"
                color = "#00d084" if item['status'] else "#ff6b35"
                st.markdown(f"""
                <div style="display: flex; align-items: center; gap: 0.8rem; padding: 0.8rem; 
                            background: rgba{tuple(list(bytes.fromhex(color[1:])) + [13])}; 
                            border-radius: 8px; margin-bottom: 0.5rem;">
                    <span style="font-size: 16px;">{icon}</span>
                    <span style="color: #ffffff; font-size: 14px;">{item['item']}</span>
                </div>
                """, unsafe_allow_html=True)

    with tab3:
        st.markdown("### 🤖 AI Act - Monitoring Continu")

        st.info("🆕 **AI Act European** - Nouvelles réglementations en vigueur depuis 2025")

        # Systèmes IA utilisés
        ai_systems = [
            {"system": "Screening Neurodiversité", "risk_level": "Limité", "compliance": 98.5, "status": "✅ Conforme"},
            {"system": "Recommandations Accommodations", "risk_level": "Minimal", "compliance": 99.2, "status": "✅ Conforme"},
            {"system": "Analytics Prédictifs RH", "risk_level": "Haut", "compliance": 95.8, "status": "⚠️ Surveillance"},
            {"system": "Chatbot Support Employés", "risk_level": "Minimal", "compliance": 100.0, "status": "✅ Conforme"}
        ]

        for system in ai_systems:
            risk_colors = {"Minimal": "#00d084", "Limité": "#ffb800", "Haut": "#ff6b35"}
            risk_color = risk_colors.get(system['risk_level'], "#a0a5ba")

            st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(42, 47, 74, 0.8), rgba(26, 31, 58, 0.8)); 
                        border: 1px solid #3a3f5a; border-left: 4px solid {risk_color}; 
                        border-radius: 12px; padding: 1.5rem; margin-bottom: 1rem;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                    <h4 style="color: #ffffff; margin: 0;">{system['system']}</h4>
                    <span style="background: {risk_color}; color: #ffffff; padding: 0.3rem 0.8rem; 
                                border-radius: 12px; font-size: 11px; font-weight: 600;">
                        {system['risk_level']}
                    </span>
                </div>

                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                    <div>
                        <div style="color: #a0a5ba; font-size: 12px; margin-bottom: 0.3rem;">CONFORMITÉ</div>
                        <div style="color: #ffffff; font-weight: 700;">{system['compliance']:.1f}%</div>
                    </div>
                    <div>
                        <div style="color: #a0a5ba; font-size: 12px; margin-bottom: 0.3rem;">STATUS</div>
                        <div style="color: #ffffff; font-weight: 600;">{system['status']}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Exigences AI Act
        st.markdown("### 📋 Exigences AI Act par Système")

        ai_requirements = {
            "Documentation technique": 95,
            "Transparence algorithmes": 92,
            "Supervision humaine": 98,
            "Gestion des biais": 89,
            "Logs et auditabilité": 97,
            "Tests de sécurité": 94
        }

        # Graphique bar chart exigences
        fig_ai_req = go.Figure(data=[
            go.Bar(
                x=list(ai_requirements.keys()),
                y=list(ai_requirements.values()),
                marker_color=['#00d084' if v >= 95 else '#ffb800' if v >= 90 else '#ff6b35' for v in ai_requirements.values()],
                text=[f"{v}%" for v in ai_requirements.values()],
                textposition='auto'
            )
        ])

        fig_ai_req.update_layout(
            title='Conformité AI Act par Exigence',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#ffffff'),
            xaxis=dict(gridcolor='#3a3f5a', tickangle=45),
            yaxis=dict(gridcolor='#3a3f5a', title='Score Conformité (%)'),
            height=400
        )

        st.plotly_chart(fig_ai_req, use_container_width=True)

    with tab4:
        st.markdown("### 📋 Audits & Rapports de Conformité")

        # Calendrier audits
        st.markdown("#### 📅 Calendrier Audits 2025")

        audits_2025 = [
            {"date": "2025-09-15", "type": "GDPR Complet", "auditeur": "Cabinet Ernst & Young", "status": "Planifié"},
            {"date": "2025-10-20", "type": "AI Act Spécialisé", "auditeur": "Deloitte AI Center", "status": "Planifié"},
            {"date": "2025-11-10", "type": "Sécurité Systèmes", "auditeur": "Internal IT", "status": "Planifié"},
            {"date": "2025-08-18", "type": "Sécurité Trimestriel", "auditeur": "Internal IT", "status": "✅ Complété"},
            {"date": "2025-08-15", "type": "GDPR Trimestriel", "auditeur": "DPO Internal", "status": "✅ Complété"}
        ]

        for audit in audits_2025:
            status_color = "#00d084" if "Complété" in audit['status'] else "#0095ff"

            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; align-items: center; 
                        padding: 1rem; background: rgba(42, 47, 74, 0.3); 
                        border-radius: 8px; margin-bottom: 0.8rem;">
                <div>
                    <div style="color: #ffffff; font-weight: 600;">{audit['type']}</div>
                    <div style="color: #a0a5ba; font-size: 12px;">{audit['auditeur']}</div>
                </div>
                <div style="text-align: right;">
                    <div style="color: #ffffff; font-weight: 600;">{audit['date']}</div>
                    <div style="color: {status_color}; font-size: 12px; font-weight: 600;">{audit['status']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Génération rapports
        st.markdown("#### 📄 Génération Rapports")

        report_col1, report_col2, report_col3 = st.columns(3)

        with report_col1:
            if st.button("📊 Rapport GDPR Mensuel", key="gdpr_monthly"):
                gdpr_report = f"""
RAPPORT CONFORMITÉ GDPR - {datetime.now().strftime('%B %Y').upper()}
===========================================================

SCORES GLOBAUX:
- Score GDPR: {compliance_data['gdpr_score']:.1f}%
- Demandes traitées: {compliance_data['privacy_requests_handled']}
- Violations: {compliance_data['data_breaches']}

DOMAINES D'EXCELLENCE:
- Sécurité système: 99.8%
- Protection données: 99.5%
- Droits employés: 99.1%

POINTS D'AMÉLIORATION:
- Privacy by design: 96.8%
- Transparence: 97.2%

ACTIONS RECOMMANDÉES:
1. Finaliser implémentation privacy by design
2. Améliorer documentation transparence
3. Maintenir formations régulières
4. Préparer audit externe septembre

STATUS: ✅ PLEINEMENT CONFORME
PROCHAINE RÉVISION: {(datetime.now() + timedelta(days=30)).strftime('%d/%m/%Y')}
                """

                pdf_buffer = generate_pdf_report(
                    f"Rapport GDPR - {datetime.now().strftime('%B %Y')}",
                    gdpr_report,
                    f"gdpr_report_{datetime.now().strftime('%Y%m')}"
                )

                st.download_button(
                    label="📥 Télécharger PDF",
                    data=pdf_buffer,
                    file_name=f"gdpr_report_{datetime.now().strftime('%Y%m')}.pdf",
                    mime="application/pdf",
                    key="dl_gdpr_monthly"
                )

        with report_col2:
            if st.button("🤖 Rapport AI Act", key="ai_act_report"):
                ai_report = f"""
RAPPORT AI ACT COMPLIANCE - {datetime.now().strftime('%B %Y').upper()}
=========================================================

SCORE GLOBAL AI ACT: {compliance_data['ai_act_compliance']:.1f}%

SYSTÈMES IA DÉPLOYÉS: 4
- Screening Neurodiversité (Risque Limité)
- Recommandations (Risque Minimal) 
- Analytics RH (Risque Haut)
- Chatbot Support (Risque Minimal)

CONFORMITÉ PAR EXIGENCE:
- Supervision humaine: 98%
- Logs et auditabilité: 97%
- Documentation technique: 95%
- Tests sécurité: 94%

ACTIONS EN COURS:
- Amélioration gestion biais (89% → 95%)
- Renforcement transparence algorithmes
- Audit externe spécialisé prévu octobre 2025

STATUS: ⚠️ SURVEILLANCE RENFORCÉE
OBJECTIF: 99%+ d'ici fin 2025
                """

                pdf_buffer = generate_pdf_report(
                    f"Rapport AI Act - {datetime.now().strftime('%B %Y')}",
                    ai_report,
                    f"ai_act_report_{datetime.now().strftime('%Y%m')}"
                )

                st.download_button(
                    label="📥 Télécharger PDF",
                    data=pdf_buffer,
                    file_name=f"ai_act_report_{datetime.now().strftime('%Y%m')}.pdf",
                    mime="application/pdf",
                    key="dl_ai_monthly"
                )

        with report_col3:
            if st.button("📈 Rapport Consolidé", key="consolidated_report"):
                consolidated_report = f"""
RAPPORT CONFORMITÉ CONSOLIDÉ - {datetime.now().strftime('%B %Y').upper()}
================================================================

VUE D'ENSEMBLE:
- Score GDPR: {compliance_data['gdpr_score']:.1f}%
- Score AI Act: {compliance_data['ai_act_compliance']:.1f}%
- Score Accessibilité: {compliance_data['accessibility_score']:.1f}%
- Formation équipes: {compliance_data['training_compliance']:.1f}%

CERTIFICATION:
- {compliance_data['certification_status']}
- Dernier audit: {compliance_data['audit_last_date']}

INDICATEURS CLÉS:
- Zéro violation données en 2025
- {compliance_data['privacy_requests_handled']} demandes traitées
- Temps réponse moyen: 8.5 jours

TENDANCES:
- ✅ Amélioration continue tous domaines
- 🎯 Objectif 99%+ maintenu
- 📈 ROI conformité: positif

PROCHAINES ÉTAPES:
1. Audit GDPR externe (septembre)
2. Audit AI Act spécialisé (octobre)
3. Formation continue équipes
4. Monitoring automatisé renforcé

CONCLUSION: 🏆 EXCELLENCE CONFORMITÉ
Ubisoft maintient des standards exceptionnels
de conformité réglementaire et d'éthique AI.
                """

                pdf_buffer = generate_pdf_report(
                    f"Rapport Conformité Consolidé - {datetime.now().strftime('%B %Y')}",
                    consolidated_report,
                    f"compliance_consolidated_{datetime.now().strftime('%Y%m')}"
                )

                st.download_button(
                    label="📥 Télécharger PDF",
                    data=pdf_buffer,
                    file_name=f"compliance_consolidated_{datetime.now().strftime('%Y%m')}.pdf",
                    mime="application/pdf",
                    key="dl_consolidated"
                )

    with tab5:
        st.markdown("### ⚡ Actions Rapides & Outils")

        # Actions urgentes
        st.markdown("#### 🚨 Actions Urgentes")

        urgent_actions = [
            {"action": "Révision politique confidentialité", "deadline": "2025-09-01", "priority": "Haute"},
            {"action": "Formation AI Act équipe RH", "deadline": "2025-09-15", "priority": "Moyenne"},
            {"action": "Audit logs systèmes IA", "deadline": "2025-08-30", "priority": "Haute"}
        ]

        for action in urgent_actions:
            priority_color = {"Haute": "#ff6b35", "Moyenne": "#ffb800", "Faible": "#00d084"}[action['priority']]

            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.markdown(f"**{action['action']}**")
            with col2:
                st.markdown(f"📅 {action['deadline']}")
            with col3:
                st.markdown(f"<span style='color: {priority_color}; font-weight: 600;'>{action['priority']}</span>", 
                           unsafe_allow_html=True)

        # Outils rapides
        st.markdown("#### 🛠️ Outils de Conformité")

        tool_col1, tool_col2, tool_col3 = st.columns(3)

        with tool_col1:
            if st.button("🔍 Vérification GDPR Rapide", key="quick_gdpr_check"):
                st.success("✅ Vérification complétée - Aucun problème détecté")
                st.info("Dernière vérification: " + datetime.now().strftime('%H:%M:%S'))

        with tool_col2:
            if st.button("🤖 Scan Systèmes IA", key="ai_systems_scan"):
                st.warning("⚠️ 1 système nécessite attention (Analytics RH)")
                st.info("Scan complété: " + datetime.now().strftime('%H:%M:%S'))

        with tool_col3:
            if st.button("📊 Génération Metrics", key="generate_metrics"):
                st.success("✅ Métriques générées et exportées")
                st.info("Export: " + datetime.now().strftime('%H:%M:%S'))

        # Monitoring temps réel
        st.markdown("#### 📡 Monitoring Temps Réel")

        monitoring_data = {
            "API Calls": {"current": 1247, "limit": 5000, "status": "Normal"},
            "Data Processing": {"current": 78, "limit": 100, "status": "Normal"}, 
            "User Sessions": {"current": 156, "limit": 500, "status": "Normal"},
            "Storage Usage": {"current": 2.3, "limit": 10.0, "status": "Normal"}
        }

        for metric, data in monitoring_data.items():
            percentage = (data['current'] / data['limit']) * 100
            color = "#00d084" if percentage < 70 else "#ffb800" if percentage < 90 else "#ff6b35"

            st.markdown(f"""
            <div style="background: rgba(42, 47, 74, 0.3); border-radius: 8px; 
                        padding: 1rem; margin-bottom: 0.8rem;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                    <span style="color: #ffffff; font-weight: 600;">{metric}</span>
                    <span style="color: {color}; font-weight: 600;">{data['status']}</span>
                </div>
                <div style="background: rgba(0,0,0,0.3); border-radius: 4px; height: 8px; margin-bottom: 0.5rem;">
                    <div style="background: {color}; height: 100%; border-radius: 4px; width: {percentage:.1f}%;"></div>
                </div>
                <div style="color: #a0a5ba; font-size: 12px;">
                    {data['current']}/{data['limit']} ({percentage:.1f}%)
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# --- FONCTION MAIN ENTERPRISE ---
def main_enterprise():
    # Application du thème Ubisoft Enterprise
    apply_ubisoft_enterprise_theme()

    # Header Enterprise
    render_enterprise_header()

    # Sidebar et navigation
    page = render_enterprise_sidebar()

    # Routing des modules Enterprise
    if "Dashboard Principal" in page:
        dashboard_principal_enterprise()
    elif "Manager Dashboard" in page:
        manager_dashboard_enterprise()
    elif "Module TDAH" in page:
        # Réutiliser le module existant avec les nouvelles données
        st.markdown("# 🧠 Module TDAH Enterprise")
        st.info("🚧 Module en cours de mise à niveau avec fonctionnalités Enterprise...")
    elif "Module Autisme" in page:
        st.markdown("# 🎯 Module Autisme Enterprise") 
        st.info("🚧 Module en cours de mise à niveau avec fonctionnalités Enterprise...")
    elif "ROI Calculator" in page:
        roi_calculator_enterprise()
    elif "Compliance GDPR" in page:
        compliance_gdpr_enterprise()
    else:
        module_name = page.split(" ", 1)[1] if " " in page else page
        st.markdown(f"# {page}")
        st.info(f"🚧 Module **{module_name}** en cours de développement avec nouvelles fonctionnalités Enterprise")

    # Footer Enterprise
    st.markdown("---")
    st.markdown(f"""
    <div style="text-align: center; padding: 2.5rem; 
                background: linear-gradient(135deg, #0a0e27 0%, #2a2f4a 100%); 
                border-radius: 16px; border: 1px solid #3a3f5a; margin-top: 2rem;
                position: relative; overflow: hidden;">

        <!-- Effet spiral Ubisoft -->
        <div style="position: absolute; top: -30px; right: -30px; width: 120px; height: 120px; 
                    opacity: 0.05; background: radial-gradient(circle, #0095ff 0%, transparent 70%);
                    border-radius: 50%; animation: rotate 25s linear infinite;"></div>

        <div style="position: relative; z-index: 1;">
            <div style="display: flex; justify-content: center; align-items: center; gap: 1rem; margin-bottom: 1rem;">
                <img src="https://logos-world.net/wp-content/uploads/2021/01/Ubisoft-Logo.png" 
                     style="height: 40px; opacity: 0.9; filter: brightness(0) invert(1);">
                <div style="color: #ffb800; font-weight: 800; font-size: 18px;">
                    NeuroInsight Hub Enterprise
                </div>
            </div>

            <div style="color: #a0a5ba; font-size: 14px; margin-bottom: 1rem;">
                © 2025 Ubisoft Entertainment - Enterprise HR Tool v3.0
            </div>

            <div style="display: flex; justify-content: center; gap: 2rem; font-size: 12px; color: #6a7081;">
                <div>🛡️ GDPR Compliant</div>
                <div>🔒 ISO 27001 Certified</div>
                <div>♿ Accessible</div>
                <div>🌍 Global Ready</div>
            </div>

            <div style="margin-top: 1.5rem; padding-top: 1.5rem; 
                        border-top: 1px solid rgba(160, 165, 186, 0.2);">
                <div style="color: #0095ff; font-size: 13px; font-weight: 600;">
                    "Creating Worlds, Embracing Minds" 🧠✨
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- EXÉCUTION ---
if __name__ == "__main__":
    main_enterprise()
