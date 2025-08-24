
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, date

# Configuration Ubisoft-inspired
st.set_page_config(
    page_title="NeuroInsight Hub - Workspace",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Styles CSS inspirés d'Ubisoft - modernes et professionnels
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Variables de couleurs inspirées Ubisoft */
    :root {
        --primary-blue: #003f7f;
        --accent-blue: #0066cc;
        --dark-blue: #001f3f;
        --light-blue: #e6f2ff;
        --gradient-bg: linear-gradient(135deg, #003f7f 0%, #0066cc 100%);
        --card-shadow: 0 8px 32px rgba(0, 63, 127, 0.1);
        --border-radius: 12px;
    }

    /* Styles généraux */
    .main {
        padding: 2rem 3rem;
        background: linear-gradient(135deg, #f8fbff 0%, #ffffff 100%);
        font-family: 'Inter', sans-serif;
    }

    /* Header principal */
    .main-header {
        background: var(--gradient-bg);
        padding: 2rem 3rem;
        border-radius: var(--border-radius);
        color: white;
        margin-bottom: 2rem;
        box-shadow: var(--card-shadow);
        position: relative;
        overflow: hidden;
    }

    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: 200px;
        height: 100%;
        background: linear-gradient(45deg, rgba(255,255,255,0.1) 0%, transparent 100%);
        transform: skewX(-15deg);
    }

    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }

    .main-header .subtitle {
        font-size: 1.2rem;
        opacity: 0.9;
        margin-top: 0.5rem;
        font-weight: 400;
    }

    /* Cards modernes */
    .metric-card {
        background: white;
        padding: 1.8rem;
        border-radius: var(--border-radius);
        box-shadow: var(--card-shadow);
        border-left: 4px solid var(--accent-blue);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        height: 100%;
    }

    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(0, 63, 127, 0.15);
    }

    .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        color: var(--primary-blue);
        margin: 0;
    }

    .metric-label {
        font-size: 0.95rem;
        color: #666;
        margin-top: 0.5rem;
        font-weight: 500;
    }

    .metric-change {
        font-size: 0.85rem;
        margin-top: 0.3rem;
        padding: 0.2rem 0.6rem;
        border-radius: 20px;
        font-weight: 600;
    }

    .positive-change {
        color: #22c55e;
        background: #f0fdf4;
    }

    /* Navigation sidebar */
    .sidebar .sidebar-content {
        background: var(--gradient-bg);
        padding: 2rem 1rem;
    }

    /* Boutons d'action */
    .action-button {
        background: var(--gradient-bg);
        color: white;
        padding: 0.8rem 1.5rem;
        border-radius: var(--border-radius);
        border: none;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(0, 63, 127, 0.3);
    }

    .action-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0, 63, 127, 0.4);
    }

    /* Accommodation cards */
    .accommodation-card {
        background: white;
        padding: 1.5rem;
        border-radius: var(--border-radius);
        box-shadow: var(--card-shadow);
        margin-bottom: 1rem;
        border-left: 4px solid var(--accent-blue);
        transition: all 0.3s ease;
    }

    .accommodation-card:hover {
        transform: translateX(4px);
        box-shadow: 0 8px 24px rgba(0, 63, 127, 0.12);
    }

    .accommodation-title {
        font-weight: 600;
        color: var(--primary-blue);
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
    }

    .impact-score {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        background: var(--light-blue);
        color: var(--primary-blue);
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-top: 0.5rem;
    }

    /* Profile cards pour les résultats de tests */
    .profile-card {
        background: linear-gradient(135deg, #f8fbff 0%, #ffffff 100%);
        padding: 2rem;
        border-radius: var(--border-radius);
        box-shadow: var(--card-shadow);
        border: 2px solid var(--accent-blue);
        margin: 1.5rem 0;
    }

    .profile-title {
        color: var(--primary-blue);
        font-size: 1.4rem;
        font-weight: 700;
        margin-bottom: 1rem;
        text-align: center;
    }

    .profile-section {
        margin-bottom: 1.5rem;
    }

    .profile-section h4 {
        color: var(--primary-blue);
        font-weight: 600;
        margin-bottom: 0.8rem;
        border-bottom: 2px solid var(--light-blue);
        padding-bottom: 0.3rem;
    }

    /* Footer moderne */
    .footer {
        margin-top: 3rem;
        padding: 2rem;
        text-align: center;
        color: #666;
        border-top: 1px solid #e5e5e5;
        font-size: 0.9rem;
    }

    /* Animations et transitions */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .animate-fade-in {
        animation: fadeInUp 0.6s ease-out;
    }

    /* Responsive */
    @media (max-width: 768px) {
        .main {
            padding: 1rem;
        }

        .main-header {
            padding: 1.5rem;
        }

        .main-header h1 {
            font-size: 2rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Navigation sidebar
st.sidebar.markdown("""
<div style="text-align: center; padding: 1rem 0; background: linear-gradient(135deg, #003f7f 0%, #0066cc 100%); margin: -1rem -1rem 2rem -1rem; border-radius: 0 0 12px 12px;">
    <h2 style="color: white; margin: 0; font-weight: 700;">🎯 Navigation</h2>
</div>
""", unsafe_allow_html=True)

# Menu de navigation
page = st.sidebar.selectbox(
    "",
    ["🏠 Dashboard Principal", "🧠 Module TDAH", "🎯 Module Autisme", 
     "📊 Observatoire Données", "🔬 NeuroScreen Évaluations", 
     "🏢 Gestion Workplace", "👥 Recrutement Neurodiversité", 
     "📈 Analytics & Reporting"]
)

# Métriques rapides en sidebar
st.sidebar.markdown("### 📊 Métriques Rapides")
col1, col2, col3 = st.sidebar.columns(3)
with col1:
    st.metric("Employés Neurodivers", "187")
with col2:
    st.metric("Taux de Rétention", "92.3%")
with col3:
    st.metric("Score Satisfaction", "4.2/5")

# Header principal
st.markdown("""
<div class="main-header animate-fade-in">
    <h1>🧠 NeuroInsight Hub - Workspace</h1>
    <div class="subtitle">Plateforme complète de gestion de la neurodiversité</div>
</div>
""", unsafe_allow_html=True)

# DASHBOARD PRINCIPAL
if page == "🏠 Dashboard Principal":
    st.markdown('<div class="animate-fade-in">', unsafe_allow_html=True)

    # Métriques principales
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">1,247</div>
            <div class="metric-label">👥 Total Employés</div>
            <div class="metric-change positive-change">↗ +3.2%</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">187 <span style="font-size: 1rem;">(15.0%)</span></div>
            <div class="metric-label">🧠 Employés Neurodivers</div>
            <div class="metric-change positive-change">↗ +2.1%</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">18.5%</div>
            <div class="metric-label">📈 Augmentation Productivité</div>
            <div class="metric-change positive-change">↗ +5.3%</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">4.2/5</div>
            <div class="metric-label">⭐ Score Bien-être</div>
            <div class="metric-change positive-change">↗ +0.3</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # Graphiques
    col1, col2 = st.columns(2)

    with col1:
        # Répartition des conditions
        conditions = ["TDAH", "Autisme", "Dyslexie", "Autres"]
        values = [47.6, 27.8, 24.6, 0]

        fig_pie = px.pie(
            values=values, 
            names=conditions,
            title="Répartition des Conditions Neurodivergentes",
            color_discrete_sequence=['#003f7f', '#0066cc', '#4d94ff', '#b3d9ff']
        )
        fig_pie.update_layout(
            title_font_size=16,
            title_font_color='#003f7f',
            font_family="Inter"
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        # Performance par département
        departments = ["IT", "Design", "Finance", "Marketing", "Support"]
        productivity = [85, 78, 82, 75, 80]
        engagement = [88, 85, 79, 77, 83]
        wellbeing = [86, 82, 80, 76, 81]

        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(name='Productivité', x=departments, y=productivity, marker_color='#003f7f'))
        fig_bar.add_trace(go.Bar(name='Engagement', x=departments, y=engagement, marker_color='#0066cc'))
        fig_bar.add_trace(go.Bar(name='Bien-être', x=departments, y=wellbeing, marker_color='#4d94ff'))

        fig_bar.update_layout(
            title='Performance par Département',
            xaxis_title='Département',
            yaxis_title='Score',
            barmode='group',
            title_font_size=16,
            title_font_color='#003f7f',
            font_family="Inter"
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    # Activités récentes
    st.markdown("### 📋 Activités Récentes")
    activities = [
        ("Il y a 2h", "🔍 Nouveau screening TDAH complété"),
        ("Il y a 4h", "🔧 Accommodations mises en place pour 3 employés"),
        ("Il y a 6h", "📊 Rapport mensuel généré"),
        ("Il y a 1j", "🎓 Formation managers neurodiversité"),
        ("Il y a 2j", "👤 5 nouveaux candidats évalués")
    ]

    for time, activity in activities:
        st.markdown(f"**{time}** - {activity}")

# MODULE TDAH
elif page == "🧠 Module TDAH":
    st.markdown("## 🧠 Module TDAH - Trouble du Déficit de l'Attention/Hyperactivité")

    # Informations générales
    st.markdown("**Prévalence**: 5% population mondiale • 3% adultes France • Ratio M/F: 2.3:1")

    tab1, tab2, tab3, tab4 = st.tabs(["🔍 Screening", "📊 Statistiques", "🎯 Accommodations", "📈 Suivi"])

    with tab1:
        st.markdown("### 🔍 Screening TDAH")

        with st.expander("🔴 Démarrer le Screening TDAH", expanded=False):
            st.markdown("**Répondez aux questions suivantes (0=Jamais, 4=Très souvent):**")

            questions = [
                "Difficulté à terminer les détails d'un projet",
                "Difficulté à organiser les tâches et activités", 
                "Éviter les tâches nécessitant un effort mental soutenu",
                "Perdre des objets nécessaires aux tâches",
                "Être facilement distrait par des stimuli externes",
                "Oublier les activités quotidiennes",
                "Remuer les mains/pieds quand assis",
                "Se lever dans des situations où il faut rester assis",
                "Se sentir agité",
                "Difficulté à se détendre lors d'activités de loisir",
                "Parler excessivement",
                "Répondre avant que les questions soient terminées"
            ]

            scores = []
            for i, question in enumerate(questions):
                score = st.slider(f"{i+1}. {question}", 0, 4, 0, key=f"q_{i}")
                scores.append(score)

            if st.button("Calculer le score TDAH", key="calc_adhd"):
                total_score = sum(scores)
                inattention_score = sum(scores[:6])
                hyperactivity_score = sum(scores[6:])

                st.markdown("### 📊 Résultats du Screening TDAH")

                # Profil détaillé
                st.markdown(f"""
                <div class="profile-card">
                    <div class="profile-title">📋 Votre Profil TDAH Détaillé</div>

                    <div class="profile-section">
                        <h4>🎯 Scores Obtenus</h4>
                        <p><strong>Score Total:</strong> {total_score}/48</p>
                        <p><strong>Inattention:</strong> {inattention_score}/24</p>
                        <p><strong>Hyperactivité/Impulsivité:</strong> {hyperactivity_score}/24</p>
                    </div>

                    <div class="profile-section">
                        <h4>📈 Interprétation</h4>
                        {"<p><strong style='color: #dc2626;'>Risque Élevé:</strong> Vos scores suggèrent des symptômes significatifs de TDAH. Une évaluation professionnelle est recommandée.</p>" if total_score >= 24 else 
                         "<p><strong style='color: #ea580c;'>Risque Modéré:</strong> Certains symptômes sont présents. Un suivi peut être bénéfique.</p>" if total_score >= 12 else
                         "<p><strong style='color: #16a34a;'>Risque Faible:</strong> Peu de symptômes détectés. Continuez à surveiller votre bien-être au travail.</p>"}
                    </div>

                    <div class="profile-section">
                        <h4>💡 Recommandations Personnalisées</h4>
                        {"<ul><li>Consultez un professionnel de santé spécialisé en TDAH</li><li>Mettez en place des accommodations workplace immédiates</li><li>Utilisez des outils de gestion du temps et d'organisation</li><li>Demandez un environnement de travail calme</li></ul>" if total_score >= 24 else
                         "<ul><li>Explorez des stratégies d'organisation</li><li>Utilisez des techniques de gestion du temps</li><li>Demandez des pauses régulières</li><li>Considérez un coaching en productivité</li></ul>" if total_score >= 12 else
                         "<ul><li>Maintenez vos bonnes pratiques actuelles</li><li>Restez attentif à votre bien-être</li><li>Explorez des outils de productivité</li><li>Participez aux formations neurodiversité</li></ul>"}
                    </div>

                    <div class="profile-section">
                        <h4>🎯 Prochaines Étapes</h4>
                        {"<ol><li>Prenez rendez-vous avec votre médecin traitant</li><li>Contactez les RH pour discuter d'accommodations</li><li>Explorez le catalogue d'accommodations de cette plateforme</li><li>Rejoignez notre groupe de support TDAH</li></ol>" if total_score >= 24 else
                         "<ol><li>Discutez avec votre manager de vos besoins</li><li>Explorez les outils d'organisation disponibles</li><li>Participez aux ateliers sur la gestion du temps</li><li>Effectuez un nouveau screening dans 3 mois</li></ol>"}
                    </div>
                </div>
                """, unsafe_allow_html=True)

    with tab2:
        st.markdown("### 📊 Statistiques TDAH")

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Prévalence Mondiale", "5.0%")
        with col2:
            st.metric("Adultes France", "3.0%")
        with col3:
            st.metric("Persistance Adulte", "66.0%")
        with col4:
            st.metric("Comorbidités", "50.0%")

        # Graphique des défis
        challenges = ["Difficultés d'attention", "Gestion du temps", "Organisation", "Impulsivité"]
        percentages = [75, 68, 72, 55]

        fig = px.bar(x=challenges, y=percentages, title="Défis Principaux en Milieu Professionnel (%)")
        fig.update_layout(title_font_color='#003f7f', font_family="Inter")
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        st.markdown("### 🎯 Accommodations Recommandées")

        # Catalogue étendu d'accommodations TDAH
        accommodations_tdah = {
            "Environnement de Travail": [
                {"nom": "🔇 Environnement calme et sans distraction", "impact": 8.5, "coût": "Faible", "description": "Espace de travail isolé des bruits et distractions visuelles"},
                {"nom": "🎧 Casque antibruit ou musique de concentration", "impact": 7.8, "coût": "Faible", "description": "Permet de bloquer les distractions auditives"},
                {"nom": "💡 Éclairage personnalisé et contrôle luminosité", "impact": 7.2, "coût": "Moyen", "description": "Réduction de la fatigue oculaire et amélioration de la concentration"},
                {"nom": "🪑 Mobilier ergonomique et espaces flexibles", "impact": 7.0, "coût": "Moyen", "description": "Bureau debout, ballon de yoga, espaces variés pour s'adapter aux besoins"}
            ],
            "Gestion du Temps": [
                {"nom": "⏰ Pauses régulières et fréquentes", "impact": 8.2, "coût": "Aucun", "description": "Pauses de 5-10 min toutes les heures pour maintenir l'attention"},
                {"nom": "📅 Horaires flexibles et pic de performance", "impact": 8.7, "coût": "Faible", "description": "Adapter les horaires aux moments de meilleure concentration"},
                {"nom": "⏱️ Techniques Pomodoro et gestion par blocs", "impact": 8.0, "coût": "Aucun", "description": "Structuration du travail en périodes courtes et focalisées"},
                {"nom": "🔔 Rappels et alarmes personnalisés", "impact": 7.5, "coût": "Aucun", "description": "Notifications pour les tâches, réunions et deadlines"}
            ],
            "Outils Numériques": [
                {"nom": "📱 Applications de gestion des tâches", "impact": 9.1, "coût": "Faible", "description": "Todoist, Notion, Asana pour organiser et prioriser"},
                {"nom": "🧠 Mind mapping et visualisation", "impact": 8.3, "coût": "Faible", "description": "MindMeister, XMind pour structurer les idées"},
                {"nom": "📝 Outils de prise de notes collaboratives", "impact": 7.9, "coût": "Faible", "description": "OneNote, Obsidian pour capturer et organiser l'information"},
                {"nom": "🤖 Assistants IA et automatisation", "impact": 8.6, "coût": "Moyen", "description": "Calendly, Zapier pour automatiser les tâches répétitives"}
            ],
            "Support et Formation": [
                {"nom": "👨‍🏫 Coaching TDAH spécialisé", "impact": 9.2, "coût": "Élevé", "description": "Accompagnement personnalisé par un professionnel formé"},
                {"nom": "👥 Groupes de support et mentorat", "impact": 8.1, "coût": "Faible", "description": "Partage d'expériences avec d'autres employés neurodivers"},
                {"nom": "📚 Formation managers sur le TDAH", "impact": 8.8, "coût": "Moyen", "description": "Sensibilisation et outils pour mieux accompagner"},
                {"nom": "🎯 Plans de développement personnalisés", "impact": 8.4, "coût": "Moyen", "description": "Objectifs adaptés et progression sur mesure"}
            ]
        }

        for category, items in accommodations_tdah.items():
            st.markdown(f"#### {category}")
            for item in items:
                with st.expander(f"🔧 {item['nom']}"):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"**Description**: {item['description']}")
                        st.progress(item['impact']/10)
                        st.markdown(f"**Impact Score**: {item['impact']}/10")
                    with col2:
                        st.markdown(f"**Coût**: {item['coût']}")
                        cost_color = {"Aucun": "#22c55e", "Faible": "#eab308", "Moyen": "#ea580c", "Élevé": "#dc2626"}
                        st.markdown(f"<span style='color: {cost_color.get(item['coût'], '#666')};'>● Niveau de coût</span>", unsafe_allow_html=True)

    with tab4:
        st.markdown("### 📈 Suivi et Évolution")

        # Graphique d'évolution
        dates = pd.date_range('2024-03-01', '2024-11-01', freq='M')
        attention_scores = [65, 68, 72, 75, 78, 82, 85, 87, 90]
        organization_scores = [60, 63, 67, 71, 75, 79, 83, 86, 88]
        productivity_scores = [70, 73, 76, 80, 83, 87, 90, 92, 94]

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dates, y=attention_scores, mode='lines+markers', name='Attention', line=dict(color='#003f7f')))
        fig.add_trace(go.Scatter(x=dates, y=organization_scores, mode='lines+markers', name='Organisation', line=dict(color='#0066cc')))
        fig.add_trace(go.Scatter(x=dates, y=productivity_scores, mode='lines+markers', name='Productivité', line=dict(color='#4d94ff')))

        fig.update_layout(
            title='Évolution des Métriques TDAH (Moyenne des employés)',
            xaxis_title='Date',
            yaxis_title='Score',
            title_font_color='#003f7f',
            font_family="Inter"
        )
        st.plotly_chart(fig, use_container_width=True)

# MODULE AUTISME
elif page == "🎯 Module Autisme":
    st.markdown("## 🎯 Module Autisme - Troubles du Spectre Autistique")

    st.markdown("**Emploi**: 22% taux d'emploi • 85% chômage • 7M personnes en Europe")

    tab1, tab2, tab3, tab4 = st.tabs(["🔍 Évaluation", "💪 Forces", "🛠️ Accommodations", "📊 Analytics"])

    with tab1:
        st.markdown("### 🔍 Évaluation Autisme")

        with st.expander("🟢 Démarrer l'Évaluation Autisme", expanded=False):
            st.markdown("**Questionnaire d'auto-évaluation des traits autistiques au travail:**")

            questions_autisme = [
                "Je préfère les routines prévisibles au travail",
                "Les changements soudains de planning me perturbent",
                "Je remarque des détails que d'autres ne voient pas",
                "Les environnements bruyants me fatiguent rapidement",
                "Je préfère les instructions écrites aux explications verbales",
                "Les interactions sociales informelles me demandent beaucoup d'énergie",
                "J'ai des intérêts très spécialisés dans mon domaine",
                "Je suis très précis dans mon travail",
                "Les réunions improvisées me stressent",
                "Je communique mieux par écrit qu'à l'oral"
            ]

            scores_autisme = []
            for i, question in enumerate(questions_autisme):
                score = st.slider(f"{i+1}. {question}", 1, 5, 3, key=f"autism_q_{i}", 
                                help="1=Pas du tout d'accord, 5=Tout à fait d'accord")
                scores_autisme.append(score)

            if st.button("Analyser le profil autistique", key="calc_autism"):
                total_score = sum(scores_autisme)

                st.markdown("### 📊 Résultats de l'Évaluation Autisme")

                # Profil détaillé pour l'autisme
                st.markdown(f"""
                <div class="profile-card">
                    <div class="profile-title">🎯 Votre Profil Autistique Détaillé</div>

                    <div class="profile-section">
                        <h4>📊 Score Global</h4>
                        <p><strong>Score Total:</strong> {total_score}/50</p>
                        <p><strong>Pourcentage:</strong> {(total_score/50)*100:.1f}%</p>
                    </div>

                    <div class="profile-section">
                        <h4>🎭 Profil et Besoins</h4>
                        {"<p><strong style='color: #dc2626;'>Profil Fortement Autistique:</strong> Vous présentez de nombreux traits autistiques. Des accommodations significatives pourraient grandement améliorer votre bien-être au travail.</p>" if total_score >= 40 else 
                         "<p><strong style='color: #ea580c;'>Profil Modérément Autistique:</strong> Vous présentez plusieurs traits autistiques. Certaines accommodations seraient bénéfiques.</p>" if total_score >= 30 else
                         "<p><strong style='color: #16a34a;'>Profil Légèrement Autistique:</strong> Vous présentez quelques traits autistiques. Des ajustements mineurs peuvent suffire.</p>"}
                    </div>

                    <div class="profile-section">
                        <h4>💎 Vos Forces Identifiées</h4>
                        <ul>
                            <li><strong>Attention aux détails:</strong> Capacité à détecter des erreurs et inconsistances</li>
                            <li><strong>Pensée systémique:</strong> Compréhension approfondie des processus complexes</li>
                            <li><strong>Expertise spécialisée:</strong> Connaissances approfondies dans vos domaines d'intérêt</li>
                            <li><strong>Fiabilité:</strong> Consistance et précision dans l'exécution des tâches</li>
                            <li><strong>Objectivité:</strong> Prise de décision basée sur les faits plutôt que les émotions</li>
                        </ul>
                    </div>

                    <div class="profile-section">
                        <h4>🛠️ Accommodations Recommandées</h4>
                        {"<ul><li>Espace de travail calme et prévisible</li><li>Instructions écrites détaillées</li><li>Horaires fixes et prévisibles</li><li>Réduction des stimuli sensoriels</li><li>Communication directe et claire</li><li>Temps de préparation pour les changements</li></ul>" if total_score >= 40 else
                         "<ul><li>Environnement de travail structuré</li><li>Préavis pour les changements</li><li>Instructions claires et précises</li><li>Espace personnel respecté</li><li>Meetings organisés et cadrés</li></ul>" if total_score >= 30 else
                         "<ul><li>Routines de travail claires</li><li>Communication transparente</li><li>Objectifs explicites</li><li>Feedback régulier et constructif</li></ul>"}
                    </div>

                    <div class="profile-section">
                        <h4>📈 Plan de Développement</h4>
                        <ol>
                            <li><strong>Immediate:</strong> Discutez de vos besoins avec votre manager</li>
                            <li><strong>Court terme:</strong> Mettez en place les accommodations prioritaires</li>
                            <li><strong>Moyen terme:</strong> Explorez les opportunités utilisant vos forces</li>
                            <li><strong>Long terme:</strong> Développez un plan de carrière adapté</li>
                        </ol>
                    </div>

                    <div class="profile-section">
                        <h4>🤝 Ressources et Support</h4>
                        <ul>
                            <li>Consultation avec notre spécialiste neurodiversité</li>
                            <li>Accès au groupe de support autisme</li>
                            <li>Formation manager sur l'accompagnement autisme</li>
                            <li>Ressources en ligne sur l'autisme au travail</li>
                        </ul>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    with tab2:
        st.markdown("### 💪 Forces et Talents Autistiques")

        col1, col2 = st.columns(2)

        with col1:
            forces = ["Attention aux Détails", "Reconnaissance Motifs", "Raisonnement Logique", "Fiabilité"]
            percentages = [94.2, 89.7, 91.3, 88.9]

            fig = px.bar(x=forces, y=percentages, title="Pourcentage d'Employés Autistes Excellant dans Chaque Domaine")
            fig.update_layout(title_font_color='#003f7f', font_family="Inter")
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("""
            #### 🎯 Opportunités de Carrière

            **Rôles Idéaux:**
            - 🔍 **Analyse de données** - Détection de patterns complexes
            - 🧪 **Contrôle qualité** - Précision et attention aux détails  
            - 💻 **Développement** - Logique et résolution de problèmes
            - 📊 **Recherche** - Analyse approfondie et méthodique
            - 🔐 **Audit** - Vérification systématique et rigoureuse
            - 🎨 **Design UX** - Attention aux détails d'interaction
            - 📚 **Documentation** - Organisation et clarté
            - 🔬 **Testing** - Identification d'anomalies
            """)

    with tab3:
        st.markdown("### 🛠️ Accommodations Workplace")

        # Catalogue étendu d'accommodations Autisme
        accommodations_autisme = {
            "Communication et Instructions": [
                {"nom": "📝 Instructions écrites détaillées", "impact": 9.2, "coût": "Faible", "description": "Documentation complète des processus et procédures"},
                {"nom": "🗣️ Communication directe et littérale", "impact": 8.7, "coût": "Aucun", "description": "Éviter les métaphores, être précis et explicite"},
                {"nom": "📧 Préférence communication écrite", "impact": 8.3, "coût": "Aucun", "description": "Email, chat plutôt que téléphone ou face-à-face"},
                {"nom": "⏰ Préavis pour les changements", "impact": 9.0, "coût": "Aucun", "description": "Information à l'avance des modifications de routine"}
            ],
            "Environnement Sensoriel": [
                {"nom": "🔇 Réduction stimuli sensoriels", "impact": 8.9, "coût": "Moyen", "description": "Contrôle bruit, éclairage, température"},
                {"nom": "🎧 Casque antibruit personnalisé", "impact": 8.5, "coût": "Faible", "description": "Réduction des distractions auditives"},
                {"nom": "💡 Éclairage adapté (éviter fluorescent)", "impact": 7.8, "coût": "Moyen", "description": "LED doux ou éclairage naturel"},
                {"nom": "🏠 Option télétravail régulier", "impact": 9.3, "coût": "Faible", "description": "Environnement contrôlé et familier"}
            ],
            "Organisation et Routine": [
                {"nom": "📅 Horaires fixes et prévisibles", "impact": 8.7, "coût": "Faible", "description": "Routine stable, éviter les changements fréquents"},
                {"nom": "🗂️ Organisation workspace personnalisée", "impact": 8.1, "coût": "Faible", "description": "Arrangement personnel de l'espace de travail"},
                {"nom": "📋 Checklists et processus structurés", "impact": 8.8, "coût": "Aucun", "description": "Étapes claires pour chaque tâche"},
                {"nom": "🎯 Objectifs SMART détaillés", "impact": 8.4, "coût": "Aucun", "description": "Spécifiques, mesurables, atteignables, réalistes, temporels"}
            ],
            "Social et Meetings": [
                {"nom": "📊 Agenda meetings détaillé à l'avance", "impact": 8.6, "coût": "Aucun", "description": "Ordre du jour précis et préparation possible"},
                {"nom": "👤 Réunions en petit comité", "impact": 8.2, "coût": "Aucun", "description": "Éviter les grandes assemblées"},
                {"nom": "🚫 Exemption événements sociaux obligatoires", "impact": 7.9, "coût": "Aucun", "description": "Participation volontaire aux activités sociales"},
                {"nom": "🤝 Buddy system/mentor dédié", "impact": 8.7, "coût": "Faible", "description": "Personne référente pour questions et support"}
            ]
        }

        for category, items in accommodations_autisme.items():
            st.markdown(f"#### {category}")
            for item in items:
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.markdown(f"**{item['nom']}**")
                    st.markdown(f"{item['description']}")
                    st.progress(item['impact']/10)
                with col2:
                    st.markdown(f"Impact: {item['impact']}/10")
                    st.markdown(f"Coût: {item['coût']}")
                st.markdown("---")

    with tab4:
        st.markdown("### 📊 Analytics Autisme")

        # Comparaison performance par département
        departments = ["IT", "Design", "Finance", "Support"]
        autistic_performance = [95, 87, 91, 83]
        neurotypical_performance = [82, 84, 86, 88]

        fig = go.Figure()
        fig.add_trace(go.Bar(name='Employés Autistes', x=departments, y=autistic_performance, marker_color='#003f7f'))
        fig.add_trace(go.Bar(name='Employés Neurotypiques', x=departments, y=neurotypical_performance, marker_color='#4d94ff'))

        fig.update_layout(
            title='Comparaison Performance par Département (%)',
            xaxis_title='Département',
            yaxis_title='Score Performance',
            barmode='group',
            title_font_color='#003f7f',
            font_family="Inter"
        )
        st.plotly_chart(fig, use_container_width=True)

# GESTION WORKPLACE
elif page == "🏢 Gestion Workplace":
    st.markdown("## 🏢 Gestion Workplace - Accommodations & Support")

    tab1, tab2, tab3 = st.tabs(["🔧 Catalogue Accommodations", "📝 Demandes", "📊 Statistiques"])

    with tab1:
        st.markdown("### 🔧 Catalogue d'Accommodations")

        filter_condition = st.selectbox("Filtrer par condition", ["Toutes", "TDAH", "Autisme", "Dyslexie", "Dyspraxie", "Troubles Exécutifs"])

        # Catalogue massif d'accommodations
        all_accommodations = {
            "TDAH": [
                {"nom": "🔇 Environnement calme sans distraction", "impact": 8.5, "coût": "Faible"},
                {"nom": "⏰ Pauses régulières (toutes les heures)", "impact": 7.8, "coût": "Aucun"},
                {"nom": "📱 Outils numériques d'organisation", "impact": 9.1, "coût": "Moyen"},
                {"nom": "🎧 Casque antibruit et musique focus", "impact": 8.2, "coût": "Faible"},
                {"nom": "📅 Horaires flexibles selon pic d'énergie", "impact": 8.7, "coût": "Faible"},
                {"nom": "⏱️ Techniques Pomodoro structurées", "impact": 8.0, "coût": "Aucun"},
                {"nom": "🧠 Coaching TDAH spécialisé", "impact": 9.2, "coût": "Élevé"},
                {"nom": "📝 Prise de notes collaborative", "impact": 7.5, "coût": "Faible"}
            ],
            "Autisme": [
                {"nom": "📝 Instructions écrites détaillées", "impact": 9.2, "coût": "Faible"},
                {"nom": "📅 Horaires fixes et prévisibles", "impact": 8.7, "coût": "Faible"},
                {"nom": "🔇 Réduction stimuli sensoriels", "impact": 8.9, "coût": "Moyen"},
                {"nom": "🗣️ Communication directe et claire", "impact": 8.5, "coût": "Aucun"},
                {"nom": "📧 Préférence communication écrite", "impact": 8.3, "coût": "Aucun"},
                {"nom": "🏠 Télétravail régulier", "impact": 9.3, "coût": "Faible"},
                {"nom": "📊 Agenda meetings détaillé", "impact": 8.6, "coût": "Aucun"},
                {"nom": "🤝 Buddy system dédié", "impact": 8.7, "coût": "Faible"}
            ],
            "Dyslexie": [
                {"nom": "🎤 Outils de reconnaissance vocale", "impact": 9.0, "coût": "Moyen"},
                {"nom": "📖 Logiciels de lecture d'écran", "impact": 8.8, "coût": "Faible"},
                {"nom": "🎨 Fond coloré et polices adaptées", "impact": 7.9, "coût": "Aucun"},
                {"nom": "⏰ Temps supplémentaire pour lecture/écriture", "impact": 8.4, "coût": "Aucun"},
                {"nom": "📱 Apps d'aide à l'orthographe avancées", "impact": 8.1, "coût": "Faible"},
                {"nom": "🗣️ Instructions verbales prioritaires", "impact": 7.8, "coût": "Aucun"},
                {"nom": "📹 Enregistrement meetings autorisé", "impact": 8.3, "coût": "Aucun"},
                {"nom": "🧠 Mind mapping pour organisation", "impact": 8.6, "coût": "Faible"}
            ],
            "Dyspraxie": [
                {"nom": "⌨️ Clavier ergonomique adapté", "impact": 8.2, "coût": "Moyen"},
                {"nom": "🖱️ Souris alternative (trackball/verticale)", "impact": 7.8, "coût": "Moyen"},
                {"nom": "📝 Réduction tâches manuscrites", "impact": 8.5, "coût": "Aucun"},
                {"nom": "⏰ Temps supplémentaire tâches manuelles", "impact": 8.0, "coût": "Aucun"},
                {"nom": "🏢 Éviter hot-desking (bureau fixe)", "impact": 7.9, "coût": "Faible"},
                {"nom": "🔧 Adaptation outils de travail", "impact": 8.3, "coût": "Moyen"},
                {"nom": "🗺️ Plans et signalisation claire", "impact": 7.5, "coût": "Faible"},
                {"nom": "👥 Assistance pour tâches complexes", "impact": 8.1, "coût": "Faible"}
            ],
            "Troubles Exécutifs": [
                {"nom": "📋 Checklists détaillées pour chaque tâche", "impact": 8.8, "coût": "Aucun"},
                {"nom": "🎯 Objectifs SMART décomposés", "impact": 8.6, "coût": "Aucun"},
                {"nom": "📅 Outils de planification avancés", "impact": 9.0, "coût": "Faible"},
                {"nom": "🔔 Rappels automatisés multiples", "impact": 8.4, "coût": "Faible"},
                {"nom": "👨‍🏫 Coaching en organisation", "impact": 9.1, "coût": "Élevé"},
                {"nom": "📊 Templates et modèles standardisés", "impact": 8.2, "coût": "Aucun"},
                {"nom": "⏰ Blocs de temps dédiés par type de tâche", "impact": 8.7, "coût": "Aucun"},
                {"nom": "🤖 Automatisation tâches répétitives", "impact": 8.9, "coût": "Moyen"}
            ]
        }

        # Accommodations universelles bénéficiant à tous
        universal_accommodations = [
            {"nom": "💡 Éclairage naturel optimisé", "impact": 7.8, "coût": "Moyen"},
            {"nom": "🌿 Plantes et espaces verts", "impact": 7.5, "coût": "Faible"},
            {"nom": "🪑 Mobilier ergonomique varié", "impact": 8.0, "coût": "Moyen"},
            {"nom": "🔇 Zones de silence désignées", "impact": 8.3, "coût": "Faible"},
            {"nom": "☕ Espaces détente accessibles", "impact": 7.7, "coût": "Faible"},
            {"nom": "🚶 Zones de mouvement/marche", "impact": 7.6, "coût": "Faible"},
            {"nom": "📞 Cabines téléphoniques privées", "impact": 7.9, "coût": "Moyen"},
            {"nom": "🎨 Espaces créatifs flexibles", "impact": 8.1, "coût": "Moyen"}
        ]

        accommodations_to_show = []
        if filter_condition == "Toutes":
            for condition, items in all_accommodations.items():
                accommodations_to_show.extend([(f"{condition}: {item['nom']}", item['impact'], item['coût']) for item in items])
            accommodations_to_show.extend([(f"Universel: {item['nom']}", item['impact'], item['coût']) for item in universal_accommodations])
        elif filter_condition in all_accommodations:
            accommodations_to_show = [(item['nom'], item['impact'], item['coût']) for item in all_accommodations[filter_condition]]

        for name, impact, cost in accommodations_to_show:
            with st.expander(f"🛠️ {name}"):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.progress(impact/10)
                    st.markdown(f"**Impact Score**: {impact}/10")
                with col2:
                    st.markdown(f"**Coût**: {cost}")
                    cost_colors = {"Aucun": "#22c55e", "Faible": "#eab308", "Moyen": "#ea580c", "Élevé": "#dc2626"}
                    st.markdown(f"<span style='color: {cost_colors.get(cost, '#666')};'>● Niveau de coût</span>", unsafe_allow_html=True)

    with tab2:
        st.markdown("### 📝 Nouvelles Demandes d'Accommodation")

        col1, col2, col3 = st.columns(3)
        with col1:
            condition = st.selectbox("Condition", ["TDAH", "Autisme", "Dyslexie", "Dyspraxie", "Autre"])
        with col2:
            department = st.selectbox("Département", ["IT", "Design", "Finance", "Marketing", "Support", "RH"])
        with col3:
            priority = st.selectbox("Priorité", ["Normale", "Élevée", "Urgente"])

        accommodation_request = st.text_area("Accommodation demandée")
        justification = st.text_area("Justification")

        if st.button("Soumettre la demande"):
            st.success("✅ Demande soumise avec succès ! Vous recevrez une réponse sous 48h.")

    with tab3:
        st.markdown("### 📊 Statistiques des Accommodations")

        col1, col2 = st.columns(2)

        with col1:
            # Accommodations par type
            types = ["Technologiques", "Environnementales", "Organisationnelles", "Support Humain"]
            counts = [45, 38, 52, 28]

            fig_pie = px.pie(values=counts, names=types, title="Répartition des Accommodations par Type")
            fig_pie.update_layout(title_font_color='#003f7f', font_family="Inter")
            st.plotly_chart(fig_pie, use_container_width=True)

        with col2:
            # Satisfaction par accommodation
            satisfaction_data = pd.DataFrame({
                'Accommodation': ['Environnement calme', 'Horaires flexibles', 'Outils numériques', 'Formation managers'],
                'Satisfaction': [4.6, 4.4, 4.7, 4.2],
                'Utilisation': [89, 76, 82, 67]
            })

            fig_bar = px.bar(satisfaction_data, x='Accommodation', y='Satisfaction', 
                           title="Satisfaction par Type d'Accommodation")
            fig_bar.update_layout(title_font_color='#003f7f', font_family="Inter")
            st.plotly_chart(fig_bar, use_container_width=True)

# RECRUTEMENT NEURODIVERSITÉ
elif page == "👥 Recrutement Neurodiversité":
    st.markdown("## 👥 Recrutement Neurodiversité - Processus Inclusifs")

    tab1, tab2, tab3 = st.tabs(["📋 Guide Inclusif", "✍️ Rédaction Offres", "🎤 Entretiens Adaptés"])

    with tab1:
        st.markdown("### 🎯 Guide de Recrutement Inclusif")

        st.markdown("#### ✅ Checklist Processus Inclusif")
        checklist_items = [
            "Description de poste claire et spécifique",
            "Canaux de diffusion diversifiés", 
            "Processus de candidature flexible",
            "Entretiens adaptés (questions concrètes)",
            "Évaluation basée sur les compétences",
            "Feedback constructif systématique",
            "Accompagnement lors de l'intégration"
        ]

        for item in checklist_items:
            st.checkbox(item, value=True)

        with st.expander("📝 Rédaction d'Offres Inclusives"):
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**À faire:**")
                st.markdown("""
                - Utiliser un langage clair et direct
                - Lister les compétences essentielles uniquement  
                - Mentionner l'engagement diversité
                - Proposer des accommodations
                """)

            with col2:
                st.markdown("**À éviter:**")
                st.markdown("""
                - Jargon et métaphores
                - Listes interminables de qualifications
                - Références à la "culture fit"
                - Exigences non essentielles
                """)

    with tab2:
        st.markdown("### ✍️ Générateur d'Offres Inclusives")

        st.markdown("**Créez une offre d'emploi neurodiversité-friendly:**")

        col1, col2 = st.columns(2)

        with col1:
            job_title = st.text_input("Titre du poste")
            department = st.selectbox("Département", ["IT", "Design", "Finance", "Marketing", "Support"])
            level = st.selectbox("Niveau", ["Junior", "Intermédiaire", "Senior"])

        with col2:
            contract_type = st.selectbox("Type de contrat", ["CDI", "CDD", "Stage", "Freelance"])
            location = st.selectbox("Localisation", ["Paris", "Lyon", "Remote", "Hybride"])

        st.markdown("**Compétences essentielles (maximum 5):**")
        skills = []
        for i in range(5):
            skill = st.text_input(f"Compétence {i+1}", key=f"skill_{i}")
            if skill:
                skills.append(skill)

        if st.button("Générer l'offre inclusive"):
            st.markdown("### 📄 Offre d'Emploi Générée")

            offer_text = f"""
            # {job_title} - {department}

            ## À propos du poste
            Nous recherchons un(e) {job_title} {level.lower()} pour rejoindre notre équipe {department}. 
            Ce poste en {contract_type} est basé à {location}.

            ## Compétences requises
            """ + ''.join([f"- {skill}" for skill in skills]) + f"""

            ## Notre engagement neurodiversité
            Nous valorisons la diversité cognitive et nous nous engageons à créer un environnement 
            de travail inclusif pour tous. Des accommodations raisonnables peuvent être mises en 
            place selon vos besoins.

            ## Processus de candidature
            - Candidatures acceptées par CV, portfolio ou vidéo
            - Possibilité de recevoir les questions d'entretien à l'avance
            - Accommodations disponibles pendant le processus
            - Feedback constructif fourni à tous les candidats

            ## Contact
            Pour toute question sur les accommodations ou le processus, contactez-nous à 
            inclusion@entreprise.com
            """

            st.markdown(offer_text)

    with tab3:
        st.markdown("### 🎤 Guide des Entretiens Adaptés")

        st.markdown("#### Préparation de l'Entretien")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            **Avant l'entretien:**
            - Envoyer les questions à l'avance (optionnel)
            - Proposer différents formats (présentiel, visio, téléphone)
            - Expliquer le déroulement détaillé
            - Offrir une visite des locaux au préalable
            - Permettre d'amener un support (notes, portfolio)
            """)

        with col2:
            st.markdown("""
            **Pendant l'entretien:**
            - Utiliser des questions concrètes et directes
            - Éviter les questions hypothétiques complexes
            - Laisser du temps de réflexion
            - Accepter les réponses écrites si nécessaire
            - Se concentrer sur les compétences techniques
            """)

        st.markdown("#### 🗣️ Exemples de Questions Adaptées")

        questions_categories = {
            "Questions Techniques": [
                "Décrivez votre expérience avec [technologie spécifique]",
                "Montrez-nous un exemple de projet que vous avez réalisé",
                "Comment procédez-vous pour résoudre un bug ?",
                "Quels outils utilisez-vous pour [tâche spécifique] ?"
            ],
            "Questions sur l'Expérience": [
                "Parlez-nous d'un projet dont vous êtes fier",
                "Décrivez votre méthode de travail habituelle",
                "Quelles sont vos préférences en matière d'environnement de travail ?",
                "Comment préférez-vous recevoir les instructions ?"
            ],
            "Questions sur les Besoins": [
                "Avez-vous besoin d'accommodations particulières ?",
                "Quel environnement de travail vous permet d'être le plus productif ?",
                "Comment préférez-vous communiquer avec votre équipe ?",
                "Y a-t-il des aspects du poste qui pourraient nécessiter des ajustements ?"
            ]
        }

        for category, questions in questions_categories.items():
            st.markdown(f"**{category}**")
            for question in questions:
                st.markdown(f"- {question}")

# ANALYTICS & REPORTING  
elif page == "📈 Analytics & Reporting":
    st.markdown("## 📈 Analytics & Reporting - Insights Avancés")

    tab1, tab2, tab3 = st.tabs(["📊 Dashboard Exécutif", "📋 Rapports", "📈 Prédictions"])

    with tab1:
        st.markdown("### 📊 Dashboard Exécutif")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("ROI Programme", "312%", "+45%")
        with col2:
            st.metric("Coût par Accommodation", "€1,620", "-€230")
        with col3:
            st.metric("Temps Implémentation", "12 jours", "-3 jours")
        with col4:
            st.metric("Score Maturité", "8.2/10", "+1.1")

        col1, col2 = st.columns(2)

        with col1:
            # Évolution ROI
            months = ["Jan", "Fév", "Mar", "Avr", "Mai", "Juin"]
            roi_values = [150, 180, 220, 265, 290, 312]

            fig_roi = px.line(x=months, y=roi_values, title="Évolution ROI Programme (%)")
            fig_roi.update_layout(title_font_color='#003f7f', font_family="Inter")
            st.plotly_chart(fig_roi, use_container_width=True)

        with col2:
            # Répartition investissements
            categories = ["Accommodations", "Formation", "Outils Tech", "Évaluations"]
            investments = [45.4, 23.5, 18.8, 12.3]

            fig_invest = px.pie(values=investments, names=categories, 
                              title="Répartition des Investissements (€)")
            fig_invest.update_layout(title_font_color='#003f7f', font_family="Inter")
            st.plotly_chart(fig_invest, use_container_width=True)

    with tab2:
        st.markdown("### 📋 Génération de Rapports")

        col1, col2, col3 = st.columns(3)

        with col1:
            report_type = st.selectbox("Type de rapport", 
                                     ["Rapport Mensuel Complet", "Analyse ROI", "Suivi Accommodations", 
                                      "Performance Employés", "Indicateurs Diversité"])
        with col2:
            period = st.selectbox("Période", ["Dernier Mois", "Trimestre", "Année", "Personnalisée"])

        with col3:
            format_type = st.selectbox("Format", ["PDF", "Excel", "PowerPoint"])

        if st.button("Générer le Rapport"):
            st.success("📊 Rapport généré avec succès ! Téléchargement en cours...")

            # Exemple de contenu de rapport
            st.markdown("### Aperçu du Rapport")

            sample_data = pd.DataFrame({
                'Métrique': ['Employés Neurodivers', 'Taux Satisfaction', 'Accommodations Actives', 
                           'ROI Programme', 'Temps Moyen Implémentation'],
                'Valeur Actuelle': ['187 (15%)', '4.2/5', '156', '312%', '12 jours'],
                'Évolution': ['+2.1%', '+0.3', '+23', '+45%', '-3 jours'],
                'Statut': ['✅ Cible atteinte', '✅ Cible atteinte', '🟡 En progression', 
                          '✅ Dépasse cible', '✅ Amélioration']
            })

            st.dataframe(sample_data, use_container_width=True)

    with tab3:
        st.markdown("### 📈 Modèles Prédictifs")

        st.markdown("#### 🔮 Prédictions Basées sur l'IA")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            **Prévisions 6 mois:**
            - 📈 Croissance employés neurodivers: **+18%**
            - 🎯 Taux de rétention prévu: **94.5%**
            - 💰 ROI attendu: **385%**
            - ⏱️ Réduction temps d'adaptation: **-25%**
            """)

        with col2:
            st.markdown("""
            **Recommandations IA:**
            - 🔧 Augmenter accommodations tech (+15%)
            - 👨‍🏫 Former 12 managers supplémentaires  
            - 🏢 Étendre programme à 2 nouveaux départements
            - 📊 Implémenter suivi temps réel
            """)

        # Graphique prédictif
        future_months = ["Jul", "Août", "Sep", "Oct", "Nov", "Déc"]
        current_values = [187, 189, 192, 195, 198, 201]
        predicted_values = [204, 208, 213, 218, 224, 230]

        fig_pred = go.Figure()
        fig_pred.add_trace(go.Scatter(x=future_months, y=current_values, 
                                    mode='lines+markers', name='Tendance Actuelle',
                                    line=dict(color='#003f7f')))
        fig_pred.add_trace(go.Scatter(x=future_months, y=predicted_values,
                                    mode='lines+markers', name='Prédiction IA',
                                    line=dict(color='#0066cc', dash='dash')))

        fig_pred.update_layout(
            title='Prédiction Évolution Employés Neurodivers',
            xaxis_title='Mois',
            yaxis_title="Nombre d'Employés",
            title_font_color='#003f7f',
            font_family="Inter"
        )
        st.plotly_chart(fig_pred, use_container_width=True)

# OBSERVATOIRE DONNÉES et NEUROSCREEN ÉVALUATIONS (gardés simples pour l'espace)
elif page == "📊 Observatoire Données":
    import streamlit as st
    import pandas as pd
    import plotly.express as px
    
    st.markdown("## 📊 Observatoire des Données Neurodiversité")
    
    # 1. Évolution de la Prévalence (2020–2024)
    prevalence = pd.DataFrame({
        "Année": [2020, 2021, 2022, 2023, 2024],
        "TDAH (%)": [2.8, 3.0, 3.2, 3.5, 3.7],
        "Autisme (%)": [0.8, 0.9, 1.0, 1.05, 1.1],
        "Total (%)": [3.6, 3.9, 4.2, 4.55, 4.8]
    })
    fig_prev = px.line(prevalence, x="Année", y=["TDAH (%)","Autisme (%)","Total (%)"],
                       markers=True,
                       title="Évolution de la Prévalence Neurodiversité en France (2020–2024)",
                       labels={"value":"Prévalence (%)","variable":"Condition"})
    fig_prev.update_layout(legend_title_text=None, font_family="Inter")
    st.plotly_chart(fig_prev, use_container_width=True)
    
    # 2. Données Régionales détaillées
    st.markdown("### 🗺️ Prévalence par Région (France)")
    regions = pd.DataFrame({
        "Région": ["Île-de-France","PACA","Nouvelle-Aquitaine","Occitanie","Auvergne-Rhône-Alpes"],
        "Population": [12000000, 5000000, 6000000, 5800000, 8000000],
        "TDAH (%)": [3.2, 3.4, 3.1, 3.3, 3.5],
        "Autisme (%)": [1.2, 0.9, 1.0, 0.8, 1.1]
    })
    regions["Est. TDAH"] = (regions["Population"] * regions["TDAH (%)"] / 100).astype(int)
    regions["Est. Autisme"] = (regions["Population"] * regions["Autisme (%)"] / 100).astype(int)
    
    # Carte choroplèthe simplifiée
    fig_map = px.choropleth(
        regions,
        geojson="https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/regions-version-simplifiee.geojson",
        featureidkey="properties.nom",
        locations="Région",
        color="Total (%)",
        hover_data=["TDAH (%)","Autisme (%)"],
        title="Cartographie de la Prévalence par Région",
        color_continuous_scale="Blues"
    )
    fig_map.update_geos(fitbounds="locations", visible=False)
    st.plotly_chart(fig_map, use_container_width=True)
    
    # Tableau détaillé
    st.markdown("#### 📋 Tableau de Données Régionales")
    st.dataframe(regions.set_index("Région"), use_container_width=True)
    
    # 3. Comparaisons Internationales
    st.markdown("### 🌍 Comparaisons Internationales")
    intl = pd.DataFrame({
        "Pays": ["France","Allemagne","Royaume-Uni","Suède","Espagne","Italie"],
        "TDAH (%)": [3.7, 4.0, 5.0, 4.5, 3.2, 2.8],
        "Autisme (%)": [1.1, 1.2, 1.3, 1.4, 1.0, 0.9]
    })
    fig_intl = px.scatter(intl, x="TDAH (%)", y="Autisme (%)", size="TDAH (%)",
                          text="Pays", title="TDAH vs Autisme par Pays (taille = TDAH%)",
                          labels={"x":"TDAH (%)","y":"Autisme (%)"})
    fig_intl.update_traces(textposition="top center")
    st.plotly_chart(fig_intl, use_container_width=True)


elif page == "🔬 NeuroScreen Évaluations":
    import streamlit as st
    import pandas as pd
    import plotly.express as px
    import numpy as np
    
    st.markdown("## 🔬 NeuroScreen - Évaluations Neuroscientifiques")
    
    # 1. Présentation de la batterie de tests
    st.markdown("""
    **NeuroScreen** utilise une batterie de tests cognitifs standardisés afin d’évaluer différentes fonctions neuropsychologiques, avec reporting automatisé.
    """)
    
    tests = [
        {"nom": "Attention Soutenue", "durée": "15 min", 
         "description": "Maintenir l’attention sur une tâche répétitive."},
        {"nom": "Mémoire de Travail", "durée": "10 min", 
         "description": "Manipulation d’informations en mémoire à court terme."},
        {"nom": "Flexibilité Cognitive", "durée": "12 min", 
         "description": "Passage rapide d’une règle ou stratégie à une autre."},
        {"nom": "Vitesse de Traitement", "durée": "8 min", 
         "description": "Réactivité et rapidité de traitement de l’information."},
        {"nom": "Inhibition", "durée": "10 min", 
         "description": "Capacité à supprimer une réponse inappropriée."}
    ]
    
    for test in tests:
        with st.expander(f"🧪 {test['nom']} ({test['durée']})"):
            st.markdown(f"**Description**: {test['description']}")
            if st.button(f"Lancer {test['nom']}"):
                st.info(f"Test « {test['nom']} » en cours...")  # placeholder
                # Ici, appeler la fonction d’exécution du test
                # puis collecter le score
    
    # 2. Simulation de résultats et profil détaillé
    st.markdown("### 📊 Résultats et Profil Cognitif")
    
    # Simulation de données de scores pour l'exemple
    np.random.seed(42)
    scores = {
        "Attention Soutenue": np.random.normal(75, 10),
        "Mémoire de Travail": np.random.normal(70, 12),
        "Flexibilité Cognitive": np.random.normal(65, 15),
        "Vitesse de Traitement": np.random.normal(80, 8),
        "Inhibition": np.random.normal(60, 12),
    }
    df_scores = pd.DataFrame.from_dict(scores, orient='index', columns=['Score'])
    df_scores['Score'] = df_scores['Score'].clip(0, 100).round(1)
    
    # Radar chart des fonctions cognitives
    fig_radar = px.line_polar(
        df_scores.reset_index(),
        r='Score', theta='index', line_close=True,
        title="Profil Cognitif - Score par Domaine",
        color_discrete_sequence=["#0066cc"]
    )
    fig_radar.update_traces(fill='toself')
    st.plotly_chart(fig_radar, use_container_width=True)
    
    # 3. Interprétation et recommandations
    st.markdown("#### 🔍 Interprétation des Scores")
    for domaine, row in df_scores.iterrows():
        score = row['Score']
        if score >= 80:
            niveau = "🔝 Excellente performance"
        elif score >= 60:
            niveau = "✅ Compétence satisfaisante"
        else:
            niveau = "⚠️ À renforcer"
        st.markdown(f"- **{domaine}**: {score}/100 — {niveau}")
    
    # Recommandations génériques
    st.markdown("#### 💡 Recommandations Personnalisées")
    if df_scores.min().values[0] < 60:
        st.markdown("""
    - Entraînez la fonction cognitive faible via des exercices ciblés (apps, jeux cérébraux).
    - Planifiez des pauses régulières pendant les tâches exigeantes.
    - Utilisez des supports visuels (mind mapping, checklists).
    - Envisagez un suivi neuropsychologique pour approfondir.
    """)
    else:
        st.markdown("""
    - Continuez à pratiquer des activités stimulant ces fonctions (lecture rapide, puzzles).
    - Maintenez un environnement de travail adapté (calme, organisation).
    - Participez aux modules de formation cognitifs de NeuroScreen.
    """)
    
    # 4. Suivi longitudinal
    st.markdown("### 📈 Suivi Longitudinal")
    
    # Exemple de données historiques
    dates = pd.date_range(end=pd.Timestamp.today(), periods=6, freq='M')
    historic = pd.DataFrame({
        "Date": dates,
        "Attention": np.linspace(65, scores["Attention Soutenue"], 6),
        "Mémoire": np.linspace(60, scores["Mémoire de Travail"], 6),
        "Flexibilité": np.linspace(55, scores["Flexibilité Cognitive"], 6)
    })
    fig_line = px.line(
        historic.melt(id_vars='Date', var_name='Domaine', value_name='Score'),
        x='Date', y='Score', color='Domaine',
        title="Évolution des Scores Cognitifs",
        markers=True
    )
    fig_line.update_layout(legend_title=None, font_family="Inter")
    st.plotly_chart(fig_line, use_container_width=True)

# Footer moderne (sans mention Ubisoft inappropriée)
st.markdown("---")
st.markdown("""
<div class="footer">
    <p>© 2025 NeuroInsight Hub Workspace | Version 2.0</p>
    <p style="font-size: 0.8rem; margin-top: 0.5rem;">
        Hosted with Streamlit • Created by remichenouri
    </p>
</div>
""", unsafe_allow_html=True)
