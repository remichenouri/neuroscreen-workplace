import json
import streamlit as st
import pandas as pd
import plotly.express as px

# --- CONFIGURATION ---
st.set_page_config(
    page_title="NeuroInsight Hub",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

import os, json

# 1. Récupère le dossier où se trouve ce script (app.py)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 2. Construit le chemin vers data/metrics.json
metrics_path = os.path.join(BASE_DIR, "data", "metrics.json")

# 3. Charge le fichier
with open(metrics_path, "r", encoding="utf-8") as f:
    data = json.load(f)


well = data["wellness_metrics"]
perf = pd.DataFrame(data["performance_data"])
neuro = pd.DataFrame(data["neuro_insights"])
learn = pd.DataFrame(data["learning_programs"])
activities = pd.DataFrame(data["recent_activities"])

# --- SIDEBAR ---
st.sidebar.image("assets/ubisoft_swirl.png", width=64)
st.sidebar.title("NeuroInsight Hub")
st.sidebar.caption("Ubisoft HR Platform")
page = st.sidebar.radio("Navigation", [
    "Dashboard", "Employee Wellness", "Performance Analytics",
    "Team Collaboration", "Learning & Development", "Settings"
])

# --- STYLE CSS ---
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --- FONTS & COULEURS ---
PRIMARY = "#000000"
ACCENT = "#c4bc74"
DARK_BG = "#041e28"

# --- PAGES ---
if page == "Dashboard":
    st.markdown("## Dashboard Principal")
    col1, col2, col3 = st.columns(3)
    col1.metric("Score Bien-Être", f"{well['overall_score']}%", delta=None)
    col2.metric("Engagement", f"{well['engagement_level']}%", delta=None)
    col3.metric("Stress", f"{well['stress_level']}%", delta=None)
    st.markdown("---")
    fig = px.bar(
        perf,
        x="department", y=["productivity","engagement","wellbeing"],
        barmode="group", title="KPIs par département",
        color_discrete_sequence=["#223c4c","#c4bc74","#aca45c"]
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("### Activités récentes")
    st.table(activities[["time","message"]].rename(columns={"time":"Depuis","message":"Activité"}))

elif page == "Employee Wellness":
    st.markdown("## Employee Wellness & NeuroInsights")
    cols = st.columns(4)
    for idx, metric in neuro.iterrows():
        cols[idx].metric(
            metric["metric"],
            f"{metric['value']}%",
            delta="↑" if metric["trend"]=="up" else "↓" if metric["trend"]=="down" else "–"
        )
    st.markdown("---")
    st.write("Insights détaillés :")
    st.dataframe(neuro[["metric","description"]])

elif page == "Performance Analytics":
    st.markdown("## Performance Analytics")
    fig2 = px.line(
        perf.melt(id_vars="department", value_vars=["productivity","engagement","wellbeing"]),
        x="department", y="value", color="variable",
        title="Tendances de performance",
        color_discrete_map={
            "productivity":"#223c4c",
            "engagement":"#c4bc74",
            "wellbeing":"#aca45c"
        }
    )
    st.plotly_chart(fig2, use_container_width=True)

elif page == "Team Collaboration":
    st.markdown("## Team Collaboration")
    st.write("Module à implémenter : chat interne, feedback, mentoring…")

elif page == "Learning & Development":
    st.markdown("## Learning & Development")
    st.table(
        learn.rename(columns={
            "name":"Programme","completion":"Taux de complétion (%)",
            "participants":"Participants"
        })
    )

elif page == "Settings":
    st.markdown("## Paramètres Utilisateur")
    st.text_input("Nom d’utilisateur", value="admin")
    st.selectbox("Thème", ["Light","Dark"], index=0)

# Footer
st.markdown(
    "<div style='text-align:center; margin-top:50px; color:#888;'>"
    "© 2025 Ubisoft – NeuroInsight Hub"
    "</div>",
    unsafe_allow_html=True
)

