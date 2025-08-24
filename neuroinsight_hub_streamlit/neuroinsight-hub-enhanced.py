def apply_ubisoft_enterprise_theme():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

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

    .stApp {
        background: linear-gradient(135deg, var(--ubisoft-primary) 0%, var(--ubisoft-secondary) 100%);
        color: var(--ubisoft-text);
        font-family: 'Inter', sans-serif;
    }

    header[data-testid="stHeader"] {
        background: linear-gradient(90deg, var(--ubisoft-primary) 0%, var(--ubisoft-tertiary) 100%);
        border-bottom: 2px solid var(--ubisoft-accent);
        height: 4rem;
    }

    .stSidebar, .css-1d391kg, .css-1cypcdb, .css-17lntkn {
        background: linear-gradient(180deg, var(--ubisoft-secondary) 0%, var(--ubisoft-tertiary) 100%);
        border-right: 3px solid var(--ubisoft-gold);
    }

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

    [data-testid="metric-container"] {
        background: linear-gradient(135deg, var(--ubisoft-tertiary), var(--ubisoft-secondary));
        border: 1px solid var(--ubisoft-border);
        border-left: 4px solid var(--ubisoft-accent);
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(0, 149, 255, 0.1);
        transition: all 0.3s ease;
    }
    [data-testid="metric-container"]:hover {
        border-left-color: var(--ubisoft-gold);
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(255, 184, 0, 0.2);
    }
    [data-testid="metric-container"] [data-testid="metric-label"] { color: var(--ubisoft-text-muted); }
    [data-testid="metric-container"] [data-testid="metric-value"] { color: var(--ubisoft-text); }

    .stButton > button {
        background: linear-gradient(135deg, var(--ubisoft-accent) 0%, var(--ubisoft-gold) 100%);
        color: var(--ubisoft-primary);
        border: none;
        border-radius: 12px;
        padding: 0.8rem 2rem;
        font-weight: 700;
        text-transform: uppercase;
        box-shadow: 0 6px 20px rgba(0,149,255,0.3);
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 30px rgba(255,184,0,0.4);
        background: linear-gradient(135deg, var(--ubisoft-gold) 0%, var(--ubisoft-accent) 100%);
    }

    .enterprise-card, .manager-card { /* règles inchangées */ }

    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ENTERPRISE UBISOFT ---
def render_enterprise_header():
    st.markdown(f"""
    <div style="background: linear-gradient(135deg,#0a0e27 0%,#2a2f4a 100%);border-radius:20px;
                padding:2.5rem;margin-bottom:2rem;position:relative;overflow:hidden;
                box-shadow:0 12px 40px rgba(0,0,0,0.4);border:1px solid #3a3f5a;">
      <div style="position:absolute;top:-50px;right:-50px;width:200px;height:200px;
                  background:radial-gradient(circle,#0095ff 0%,transparent 70%);
                  opacity:0.1;border-radius:50%;animation:rotate 20s linear infinite;"></div>
      <div style="display:flex;justify-content:space-between;align-items:center;position:relative;z-index:1;">
        <div style="display:flex;align-items:center;gap:2rem;">
          <div style="width:80px;height:80px;border-radius:20px;
                      background:linear-gradient(135deg,#0095ff 0%,#ffb800 100%);
                      display:flex;align-items:center;justify-content:center;
                      font-size:32px;box-shadow:0 6px 20px rgba(0,149,255,0.3);position:relative;">
            🧠
          </div>
          <div>
            <h1 style="margin:0;font-size:32px;
                       background:linear-gradient(135deg,#ffb800,#0095ff);
                       -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                       font-weight:900;text-shadow:none;">
              NeuroInsight Hub Enterprise
            </h1>
            <p style="margin:0;color:#a0a5ba;font-size:18px;font-weight:500;">
              🏢 Enterprise HR Tool - Neurodiversité & Intelligence d'Affaires
            </p>
          </div>
        </div>
        <div style="display:flex;gap:2rem;align-items:center;">
          <div style="text-align:center;padding:1.5rem;
                      background:rgba(0,149,255,0.1);border-radius:16px;
                      border:1px solid #0095ff;backdrop-filter:blur(10px);">
            <div style="font-size:28px;font-weight:900;color:#00d084;margin-bottom:0.5rem;">
              {ENTERPRISE_DATA['company_metrics']['neurodiverse_employees']}
            </div>
            <div style="font-size:12px;color:#a0a5ba;text-transform:uppercase;letter-spacing:1px;">
              Employés Neurodivers
            </div>
          </div>
          <div style="text-align:center;padding:1.5rem;
                      background:rgba(255,184,0,0.1);border-radius:16px;
                      border:1px solid #ffb800;backdrop-filter:blur(10px);">
            <div style="font-size:28px;font-weight:900;color:#ffb800;margin-bottom:0.5rem;">
              {ENTERPRISE_DATA['company_metrics']['roi_percentage']}%
            </div>
            <div style="font-size:12px;color:#a0a5ba;text-transform:uppercase;letter-spacing:1px;">
              ROI Programme
            </div>
          </div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

# --- SIDEBAR ENTERPRISE ---
def render_enterprise_sidebar():
    with st.sidebar:
        st.markdown("""
        <div style="text-align:center;padding:2rem 1rem;margin-bottom:2rem;
                    border-bottom:2px solid rgba(0,149,255,0.3);position:relative;">
          <div style="width:70px;height:70px;border-radius:50%;
                      background:linear-gradient(135deg,#0095ff 0%,#ffb800 100%);
                      display:flex;align-items:center;justify-content:center;
                      font-size:28px;color:#0a0e27;font-weight:bold;
                      box-shadow:0 8px 25px rgba(0,149,255,0.3);margin:0 auto 1.5rem;">
            🧠
          </div>
          <h2 style="color:#ffb800;margin:0;font-size:22px;font-weight:900;">
            NeuroInsight Hub
          </h2>
          <p style="color:#a0a5ba;margin:0.5rem 0 0;font-size:14px;font-weight:500;">
            Enterprise HR Tool
          </p>
          <div style="width:50px;height:2px;margin:1rem auto;border-radius:1px;
                      background:linear-gradient(90deg,#0095ff,#ffb800);"></div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("## 🎯 Navigation Enterprise")
        modules = [
            ("🏠", "Dashboard Principal"), ("🏢", "Manager Dashboard"), ("🧠", "Module TDAH"),
            ("🎯", "Module Autisme"), ("📊", "Observatoire Analytics"), ("🔬", "NeuroScreen Pro"),
            ("💼", "Recrutement Inclusif"), ("📈", "Business Intelligence"),
            ("💰", "ROI Calculator"), ("📋", "Compliance GDPR"), ("⚙️", "Enterprise Settings")
        ]
        page = st.selectbox("Choisir un module", [f"{i} {n}" for i,n in modules])
        return page

# --- UTILITAIRES PDF ---
def generate_pdf_report(title, content, filename):
    buffer = BytesIO()
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, title, 0, 1, 'C')
    pdf.ln(10)
    pdf.set_font('Arial', '', 12)
    for line in content.split('\n'):
        if line:
            pdf.cell(0, 8, line, 0, 1)
    buffer.write(pdf.output(dest='S').encode('latin1'))
    buffer.seek(0)
    return buffer

# --- DASHBOARD PRINCIPAL ENTERPRISE ---
def dashboard_principal_enterprise():
    st.markdown("# 🏠 Dashboard Principal Enterprise")
    st.markdown("*Vue d'ensemble complète avec analytics avancés et intelligence d'affaires*")
    metrics = ENTERPRISE_DATA['company_metrics']
    cols = st.columns(5)
    labels = ["👥 Employés Total", "🧠 Neurodivers", "📈 Productivité", "💰 ROI Programme", "🎯 Satisfaction"]
    values = [
        f"{metrics['total_employees']:,}",
        f"{metrics['neurodiverse_employees']} ({metrics['neurodiverse_percentage']:.1f}%)",
        f"+{metrics['productivity_increase']:.1f}%",
        f"{metrics['roi_percentage']}%",
        f"{metrics['satisfaction_score']:.1f}/5"
    ]
    deltas = ["↗ +5.2%", "↗ +3.8%", "↗ +7.2%", "↗ +85%", "↗ +0.4"]
    for col, l, v, d in zip(cols, labels, values, deltas):
        with col:
            st.metric(l, v, d)
    st.markdown("---")

    # Graphiques
    team_df = pd.DataFrame(ENTERPRISE_DATA['team_metrics'])
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=team_df['manager'],
        y=team_df['productivity_score'],
        marker_color='#0095ff', name='Productivité',
        text=team_df['productivity_score'], textposition='auto'
    ))
    fig.add_trace(go.Scatter(
        x=team_df['manager'],
        y=team_df['satisfaction'] * 30,
        mode='lines+markers', name='Satisfaction',
        line=dict(color='#ffb800', width=3), yaxis='y2'
    ))
    fig.update_layout(
        title="Performance & Satisfaction par Manager",
        yaxis=dict(title="Score Productivité"),
        yaxis2=dict(title="Satisfaction ×30", overlaying='y', side='right'),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig, use_container_width=True)

    cond = {
        'TDAH': metrics['adhd_employees'],
        'Autisme': metrics['autism_employees'],
        'Dyslexie': metrics['dyslexia_employees'],
        'Autres': metrics['neurodiverse_employees'] - sum([
            metrics['adhd_employees'], metrics['autism_employees'], metrics['dyslexia_employees']
        ])
    }
    fig2 = go.Figure(go.Pie(labels=list(cond.keys()), values=list(cond.values()), hole=0.6))
    fig2.update_layout(title="Répartition par Condition", paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig2, use_container_width=True)
