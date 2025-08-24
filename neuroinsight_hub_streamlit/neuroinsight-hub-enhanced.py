import os
import streamlit as st
import pandas as pd
import plotly.express as px
import json

# --- CONFIGURATION GÉNÉRALE ---
st.set_page_config(
    page_title="NeuroInsight Hub",
    page_icon=":brain:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- CHEMINS ROBUSTES POUR LE DÉPLOIEMENT ---
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

def asset_path(filename):
    return os.path.join(ASSETS_DIR, filename)

# --- CSS PERSONNALISÉ POUR CONTRASTE ET STYLE RH ---
st.markdown("""
<style>
body, .main, .block-container {
    background: #181C23;
    color: #F3F6FC !important;
}
section[data-testid="stSidebar"] {
    background: #f4f5fa !important;
    color: #223c4c !important;
    border-right: 2px solid #CCC;
}
.sidebar-content {
    margin-top:1em !important;
}
header[data-testid="stHeader"] {
    background: linear-gradient(90deg,#161b22 40%, #1D2836 100%) !important;
    padding: 12px 0;
    color: #FFD700 !important;
    border-bottom: 2px solid #c4bc74;
}
h1, h2, h3, h4, h5 { color: #ffd700 !important; font-family: 'Inter', sans-serif; }
.st-emotion-cache-1d391kg {color: #223c4c!important;}
.metric-value, .metric-label {
    color: #223c4c!important;
}
.metric-card {
    background: #202630 !important;
    border-radius: 1em;
    padding: 1em 2em;
    box-shadow:0 2px 8px #0002;
    display:flex; flex-direction:column; align-items:center; justify-content:center;
    min-width:220px;
}
.module-card {
    background: #23272e;
    border-radius: 1em;
    margin-bottom:2em;
    box-shadow:0 2px 8px #0003;
    padding:2em;
}
input, select, textarea, .stTextInput>div>div>input, .stSelectbox>div>div>div {
    background: #191e23 !important;
    color: #fff !important;
    border: 1px solid #c4bc74 !important;
    border-radius:8px;
}
button, .stButton>button {
    background: linear-gradient(90deg,#223c4c,#c4bc74 90%)!important;
    color:#fff!important;
    border: 0px; border-radius: 9px!important;
    margin:.2em;
    transition:0.2s;
    font-weight: 500;
}
button:hover, .stButton>button:hover { 
    background: #aca45c!important; color: #181C23!important; transform: scale(1.03);
}
.stDataFrame {background:#1d2127!important;}
::-webkit-scrollbar { height:8px; width: 8px; background: #181C23;}
::-webkit-scrollbar-thumb { background:#c4bc74; border-radius:4px;}
footer { color: #888!important; background: #0d1117!important; }
.stAlert {
    background:#21262c!important;
    color:#ffd700!important;
    border:1px solid #c4bc74;
}
</style>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# --- CHARGEMENT DES DONNÉES DEMO ---
try:
    with open(os.path.join(BASE_DIR, "data", "metrics.json"), encoding="utf-8") as f:
        DATA = json.load(f)
except Exception:
    # fallback valeurs pour démo
    DATA = {
        "company_metrics":{
            "neurodiverse_employees": 12,
            "roi_percentage": 312,
            "retention": 89,
            "wellbeing_score": 84
        },
        "performance_data": [
            {"department":"Tech","productivity":85,"engagement":90,"wellbeing":84},
            {"department":"Games","productivity":78,"engagement":88,"wellbeing":80},
            {"department":"Support","productivity":82,"engagement":91,"wellbeing":83},
        ],
        "recent_activities": [
            {"time":"2h","message":"Entretien RH d'onboarding inclusif"},
            {"time":"1j","message":"Implémentation du bureau adapté"},
            {"time":"3j","message":"Feedback positif : manager TDAH"},
        ]
    }

# --- LOGO & HEADER ---
from PIL import Image

def get_logo_path():
    png_asset = asset_path("logo_neuroinsight.png")
    if os.path.exists(png_asset):
        return png_asset
    fallback = asset_path("fallback_brain_icon.png")
    if os.path.exists(fallback):
        return fallback
    return None

st.sidebar.image(get_logo_path(), width=70)
st.sidebar.markdown(
    "<h2 style='color:#223c4c'>NeuroInsight Hub</h2>"
    "<div style='color:#555;font-size:.9em'>Plateforme RH Professionnelle</div>",
    unsafe_allow_html=True
)

# --- SIDEBAR NAVIGATION ---
MODULES = [
    "Dashboard Principal",  "Screening TDAH", "Profil Autisme",  "Observatoire", 
    "Accommodations", "Analytics", "Learning & Development","Settings"
]
selected = st.sidebar.selectbox(
    "Navigation", MODULES, key="module_select", 
    format_func=lambda x: f"🧩 {x}" if x != "Settings" else "⚙️ Paramètres"
)
st.sidebar.markdown("<hr>", unsafe_allow_html=True)
st.sidebar.markdown("<b>Métriques Temps Réel</b>", unsafe_allow_html=True)
st.sidebar.metric("Employés Neurodivers", f"{DATA['company_metrics']['neurodiverse_employees']}")
st.sidebar.metric("ROI Programme", f"{DATA['company_metrics']['roi_percentage']}%")
st.sidebar.metric("Rétention", f"{DATA['company_metrics']['retention']}%")

# --- MAIN CONTENT: MODULES ---

if selected == "Dashboard Principal":
    st.markdown("<h1>Neurolnsight Hub</h1>", unsafe_allow_html=True)
    st.markdown("Workspace RH – Gestion Professionnelle de la Neurodiversité")
    st.markdown("#### Dashboard Principal")
    st.caption("Vue d’ensemble complète de la neurodiversité en entreprise")
    
    # KPI CARDS
    col1, col2, col3, col4 = st.columns(4)
    kpi = DATA['company_metrics'] 
    with col1:
        st.markdown("<div class='metric-card'><span style='font-size:2.6em;'>"
                    f"{kpi['neurodiverse_employees']}</span><br>NEURODIVERS</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='metric-card'><span style='font-size:2.6em;color:#3fb950;'>"
                    f"{kpi['roi_percentage']}%</span><br>ROI PROGRAMME</div>",unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='metric-card'><span style='font-size:2.6em;color:#58a6ff;'>"
                    f"{kpi['retention']}%</span><br>RÉTENTION</div>",unsafe_allow_html=True)
    with col4:
        st.markdown("<div class='metric-card'><span style='font-size:2.6em;color:#FFD700;'>"
                    f"{kpi.get('wellbeing_score',84)}%</span><br>BIEN-ÊTRE</div>",unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # PERFORMANCE PAR DEPT
    dept_df = pd.DataFrame(DATA["performance_data"])
    st.markdown("### Indicateurs Clés de Performance")
    fig = px.bar(
        dept_df, x="department", y=["productivity", "engagement", "wellbeing"],
        barmode="group", color_discrete_map={
            "productivity": "#58a6ff", "engagement": "#FFD700", "wellbeing": "#3fb950"
        }
    )
    fig.update_layout(plot_bgcolor='#202630', paper_bgcolor='#202630', font=dict(color='#F3F6FC'))
    st.plotly_chart(fig, use_container_width=True)
    
    # Activités récentes
    st.markdown("### Activités Récentes")
    for act in DATA["recent_activities"]:
        st.markdown(
            f"<div style='background:#23272e;padding:10px;margin-bottom:4px;border-radius:8px;'>"
            f"<b>{act['time']}</b> – {act['message']}</div>", unsafe_allow_html=True
        )

# --------------- MODULE TDAH SCREENING (WORKPLACE) ---------------
elif selected == "Screening TDAH":
    st.markdown("<h2>🦸‍♂️ Evaluation TDAH en Milieu Professionnel</h2>", unsafe_allow_html=True)
    st.caption("Basé sur l’ASRS v1.1, enrichi pour le contexte entreprise")
    
    questions = [
        ("Vous arrive-t-il souvent d’avoir du mal à organiser une tâche professionnelle longue ou à multiples étapes ?", "Organisation"),
        ("Avez-vous des difficultés à rester concentré dans une réunion ?","Attention"),
        ("Perdez-vous fréquemment des objets nécessaires sur votre lieu de travail ?", "Organisation"),
        ("Vous interrompez-vous ou coupez-vous la parole lors des discussions en équipe ?", "Impulsivité"),
        ("Rencontrez-vous souvent du mal à suivre une procédure écrite complexe ?", "Attention"),
        ("Éprouvez-vous le besoin de bouger ou de manipuler des objets lors des réunions prolongées ?", "Hyperactivité"),
        ("Avez-vous tendance à éviter ou reporter les tâches administratives répétitives ?", "Attention"),
        ("Difficulté à respecter des délais professionnels ?", "Organisation"),
        ("Vous arrive-t-il de finir les phrases des collègues avant eux ?", "Impulsivité"),
        ("Oubliez-vous vos rendez-vous ou deadlines importants ?", "Mémoire de travail"), 
        ("Changez-vous régulièrement d’outil sans finir la tâche en cours ?", "Planification"),
        ("Avez-vous des réactions émotionnelles marquées face à une critique ?", "Régulation émotionnelle"),
        ("Avez-vous fréquemment des pensées envahissantes au travail ?", "Gestion Attentive"),
        ("Faites-vous des erreurs d’inattention dans l’utilisation d’outils numériques ?", "Attention"),
        ("Vous sentez-vous souvent débordé par le nombre de mails/projets ?", "Gestion du temps"),
        ("Avez-vous du mal à traiter plusieurs tâches simultanément ?", "Planification"),
    ]
    st.markdown("**Veuillez indiquer à quelle fréquence vous rencontrez ces situations dans votre quotidien professionnel.**")
    responses = {}
    options = ["Jamais", "Rarement", "Parfois", "Souvent", "Très souvent"]
    score_map = dict(zip(options, range(5)))
    
    for idx, (q,cat) in enumerate(questions):
        key = f"tdah_{idx}"
        responses[key] = st.selectbox(
            f"{q}", options, key=key
        )
    # Calcul du score
    global_score = sum([score_map[resp] for resp in responses.values()])
    st.markdown(f"<br><div class='module-card'><b>Score global :</b> <span style='font-size:1.5em;color:#FFD700'>{global_score} / {5*len(questions)}</span></div>",unsafe_allow_html=True)
    # Interprétation
    if global_score >= 48:
        st.error("Le score révèle une forte probabilité de TDAH impactant sur l’environnement de travail. Une évaluation approfondie et des accommodations sont recommandées.")
    elif global_score >= 30:
        st.warning("Des difficultés typiques du TDAH sont présentes au travail. Des ajustements RH préventifs sont à envisager.")
    else:
        st.success("Peu d’indices de TDAH professionnels détectés.")
    # Affichage par dimension
    st.markdown("#### Carte Profil TDAH Workplace")
    cat_scores = {}
    for idx, (q,cat) in enumerate(questions):
        cat_scores.setdefault(cat, 0)
        cat_scores[cat] += score_map[responses[f"tdah_{idx}"]]
    radar_data = pd.DataFrame([cat_scores])
    fig2 = px.line_polar(radar_data, r=radar_data.T[0], theta=cat_scores.keys(), 
                         line_close=True, color_discrete_sequence=["#ffd700"])
    fig2.update_traces(fill='toself')
    fig2.update_layout(
        polar=dict(bgcolor='#202630'), plot_bgcolor='#23272e', paper_bgcolor='#202630',
        font=dict(color='#FFD700')
    )
    st.plotly_chart(fig2, use_container_width=True)
    st.info("**Pour toutes difficultés détectées, voir suggestions d’accommodations dans l’onglet dédié.**")

# --------------- MODULE AUTISME SCREENING (WORKPLACE) ---------------
elif selected == "Profil Autisme":
    st.markdown("<h2>🌱 Profil Autistique Professionnel</h2>", unsafe_allow_html=True)
    st.caption("Inspiré des questionnaires RAADS et outils professionnels workplace, multi-domaines")
    asd_questions = [
        ("Préférez-vous travailler sur des projets individuels ?", "Sociabilité"),
        ("Avez-vous des routines importantes pour votre équilibre au travail ?", "Flexibilité"),
        ("Avez-vous des intérêts très marqués ou spécialisés ?", "Focalisation"),
        ("Difficulté à décoder l’implicite ou le non-verbal en réunion ?", "Communication"),
        ("Sensibilité accrue au bruit/lumière au travail ?", "Sensoriel"),
        ("Avez-vous du mal à interpréter les normes sociales implicites ?", "Sociabilité"),
        ("Grande faculté à repérer les erreurs/problèmes dans les process ?", "Forces Détail"),
        ("Préférence pour les consignes claires et directives ?", "Structure"),
        ("Fatigue après des interactions sociales prolongées ?", "Sociabilité"),
        ("Grande capacité de concentration sur votre domaine ?", "Focalisation"),
        ("Créativité dans la résolution de problèmes techniques ?", "Compétence"),
        ("Utilisez-vous des objets pour gérer le stress sensoriel ?", "Sensoriel"),
        ("Avez-vous besoin de clarté/routine dans vos tâches quotidiennes ?", "Structure"),
        ("Plus à l’aise à l’écrit qu’à l’oral au travail ?", "Communication"),
        ("Intérêt pour l’approfondissement d’un sujet précis ?", "Focalisation"),
        ("Difficulté à changer d’environnement sans préparation ?", "Flexibilité"),
        ("Hypertolérance ou intolérance à certains environnements sensoriels ?", "Sensoriel"),
        ("Rapidité à remarquer les différences ou incohérences dans les process ?", "Forces Détail"),
    ]
    asd_options = ["Jamais", "Rarement", "Parfois", "Souvent", "Très souvent"]
    asd_score_map = dict(zip(asd_options, range(5)))
    asd_responses = {}
    for idx, (q,cat) in enumerate(asd_questions):
        key = f"asd_{idx}"
        asd_responses[key] = st.selectbox(q, asd_options, key=key)
    score_asd = sum([asd_score_map[asd_responses[k]] for k in asd_responses])
    st.markdown(f"<br><div class='module-card'><b>Score global :</b> <span style='font-size:1.5em;color:#58a6ff'>{score_asd} / {5*len(asd_questions)}</span></div>", unsafe_allow_html=True)
    st.markdown("#### Profil radar compétences et sensibilités")
    asd_cat_scores = {}
    for idx, (q,cat) in enumerate(asd_questions):
        asd_cat_scores.setdefault(cat,0)
        asd_cat_scores[cat] += asd_score_map[asd_responses[f"asd_{idx}"]]
    asd_radar_data = pd.DataFrame([asd_cat_scores])
    fig3 = px.line_polar(asd_radar_data, r=asd_radar_data.T[0], theta=asd_cat_scores.keys(),
                         line_close=True, color_discrete_sequence=["#58a6ff"])
    fig3.update_traces(fill='toself')
    fig3.update_layout(
        polar=dict(bgcolor='#202630'), plot_bgcolor='#23272e', paper_bgcolor='#202630',
        font=dict(color='#58a6ff')
    )
    st.plotly_chart(fig3, use_container_width=True)
    if score_asd > 45:
        st.warning("Le profil montre de nombreuses forces et besoins atypiques en entreprise, il est recommandé d'explorer des accommodations spécifiques et de valoriser la diversité cognitive pour la performance collective.")

# --------------- MODULE OBSERVATOIRE ---------------
elif selected == "Observatoire":
    st.markdown("<h2>📊 Observatoire Neurodiversité</h2>", unsafe_allow_html=True)
    st.caption("Évolution 2020-2025 de la prévalence et de la prise en compte neurodiversité (France & Monde)")
    data_observatoire = pd.DataFrame({
        "Année": [2020, 2021, 2022, 2023, 2024, 2025],
        "TDAH (%)": [4.8, 5, 5.2, 5.3, 5.35, 5.4],
        "Autisme (%)": [1.1, 1.2, 1.3, 1.5, 1.6, 1.8],
        "Dyslexie (%)": [6.0, 6.1, 6.2, 6.25, 6.3, 6.4],
        "Handicap Reconnu (%)": [3, 3.4, 3.7, 4.2, 5.1, 6]
    })
    st.markdown("#### Prévalence en France (%) - Tableau Historique")
    st.dataframe(data_observatoire.style.background_gradient(subset=data_observatoire.columns[1:], cmap='cividis'))
    st.markdown("#### Visualisation Interactive")
    fig4 = px.line(
        data_observatoire.melt(id_vars="Année"), 
        x="Année", y="value", color="variable",
        markers=True, color_discrete_sequence=["#ffd700","#58a6ff","#3fb950","#c4bc74"]
    )
    fig4.update_layout(
        plot_bgcolor='#23272e', paper_bgcolor='#202630',
        legend=dict(font=dict(color="#ffd700")),
        font=dict(color='#f3f6fc')
    )
    st.plotly_chart(fig4, use_container_width=True)
    st.info("Hausse confirmée des diagnostics et des démarches inclusives partout en France et Europe (Insee, 2025).")

# --------------- MODULE ACCOMMODATIONS RH COMPLETES ---------------
elif selected == "Accommodations":
    st.markdown("<h2>🛠️ Accommodations RH Entreprises</h2>", unsafe_allow_html=True)
    st.caption("Liste exhaustive des aménagements et bonnes pratiques déjà mis en place en entreprises.")
    accommodations_db = {
        "Environnement Physique": [
            "Bureau calme ou isolé",
            "Casque antibruit professionnel",
            "Éclairage LED personnalisé",
            "Bureau debout ou ballon ergonomique",
            "Plantes/plantes anti-stress",
            "Objets fidget ou anti-stress",
            "Zone sensorielle de retrait"
        ],
        "Temps & Organisation": [
            "Horaires flexibles ou aménagements de planning",
            "Télétravail adapté (jours fixes, exceptionnel, total)",
            "Pauses fréquentes et prévues",
            "Découpage des tâches en sous-tâches",
            "Process de travail individualisé",
            "Rappels automatiques numériques",
            "Préparation systématique des réunions (ordre du jour, compte-rendu)",
            "Lissage de la charge de travail hebdo"
        ],
        "Technologies & Outils": [
            "Logiciels anti-distraction (Freedom, ColdTurkey)",
            "Gestion du temps (Forest, Todoist, Pomodoro)",
            "Reconnaissance vocale ou synthèse vocale",
            "Double écran ou grand écran",
            "Simplification de l'interface des outils internes",
            "Check-list numérique",
            "Applications d'organisation personnelle"
        ],
        "Management": [
            "Feedback fréquent et constructif personnalisé",
            "Objectifs SMART adaptés",
            "Formations managers (diversité cognitive)",
            "Suivi de mission régulier",
            "Rituel d'accueil dédié",
            "Droit à l'erreur affiché",
            "Réunions d'équipe adaptées"
        ],
        "Relations sociales": [
            "Médiation en cas de conflit par référent",
            "Communication écrite privilégiée",
            "Réduction présence à certains événements",
            "Binôme/buddy system d'intégration",
            "Temps protégé sans sollicitations",
            "Sensibilisation du collectif travail",
            "Support pair-à-pair"
        ],
        "Formation & Sensibilisation": [
            "Sessions courtes et interactives",
            "Supports visuels/multimédia",
            "Mode hybride (en présentiel ou à distance)",
            "Accès facilité à la documentation",
            "Formation individuelle personnalisée",
            "Tutorat dédié"
        ],
        "RH Légal & Parcours de Carrière": [
            "Référent handicap identifié",
            "Confidentialité stricte du dossier médical",
            "Plan d'évolution adapté",
            "Évaluations annuelles accomodées",
            "Parcours promotion interne fléché",
            "Accès aux entretiens sans filtre"
        ],
        "Bien-être & Santé": [
            "Accès facilité à la médecine du travail",
            "Suivi psychologique préventif",
            "Prise en charge ergonomique complète",
            "Ateliers gestion du stress",
            "Accompagnement à la charge mentale",
            "Jours d'absence autorisés pour soins",
            "Tiers de confiance neutre"
        ]
    }
    for cat, lst in accommodations_db.items():
        with st.expander(cat):
            for acc in lst:
                st.markdown(f"- {acc}")

# --------------- MODULE ANALYTICS (KPIs RH) ---------------
elif selected == "Analytics":
    st.markdown("<h2>📈 Analytics RH & Reporting</h2>", unsafe_allow_html=True)
    st.caption("Visualisation détaillée des KPIs de la politique neurodiversité et impact entreprise.")
    analytics_data = pd.DataFrame({
        "Département":["Tech","Games","Support"],
        "Turnover (%)":[5.1, 6.5, 4.2],
        "Intégrations (%)":[17,13,11],
        "ROI Accommodations (%)":[324,295,275]
    })
    st.dataframe(analytics_data.style.background_gradient(cmap='bone'))
    fig5 = px.bar(
        analytics_data, x="Département", y=["Turnover (%)","Intégrations (%)","ROI Accommodations (%)"],
        barmode="group", color_discrete_map={
            "Turnover (%)":"#FFD700","Intégrations (%)":"#58a6ff","ROI Accommodations (%)":"#3fb950"
        }
    )
    fig5.update_layout(plot_bgcolor='#202630',paper_bgcolor='#202630',font=dict(color='#f3f6fc'))
    st.plotly_chart(fig5, use_container_width=True)

# --------------- LEARNING & DEV ---------------
elif selected == "Learning & Development":
    st.markdown("<h2>🎓 Learning & Development</h2>", unsafe_allow_html=True)
    st.caption("Formations, onboarding, documentation et progression des salariés.")
    learn_data = pd.DataFrame([
        {"programme":"Onboarding inclusif","taux_completion":98,"participants":112},
        {"programme":"Formation managers handicap","taux_completion":89,"participants":42},
        {"programme":"Atelier gestion du stress","taux_completion":81,"participants":61},
        {"programme":"Sensibilisation neurodiversité","taux_completion":94,"participants":170}
    ])
    st.dataframe(learn_data.style.background_gradient(subset=["taux_completion"], cmap='summer'))

# --------------- SETTINGS ---------------
elif selected == "Settings":
    st.markdown("<h2>⚙️ Paramètres Utilisateur</h2>",unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("Nom d’utilisateur", value="admin")
        st.selectbox("Thème couleur",["Sombre (par défaut)","Clair"])
    with col2:
        st.radio("Accessibilité visuelle",["Police standard","Police très grande"])
        st.checkbox("Animations CSS", value=True)
    st.info("Pour toute suggestion ou amélioration, contactez l’équipe RH dédiée.")

# --- FOOTER ---
st.markdown(
    "<div style='text-align:center; margin-top:40px; padding:24px 0; background:#161b22; color:#FFD700; font-size:.95em;'>"
    "© 2025 Ubisoft – NeuroInsight Hub &nbsp;&#x2022;&nbsp; Plateforme RH Inclusive"
    "</div>", unsafe_allow_html=True
)
