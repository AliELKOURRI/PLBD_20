"""
Styles CSS custom pour le dashboard Smart Predict AI.

Injecte des styles modernes via st.markdown(unsafe_allow_html=True) pour
transformer l'apparence par défaut de Streamlit en un dashboard SaaS pro.

Palette : teal/vert (industriel, durable, moderne).
Police : Inter (Google Font).
"""

from __future__ import annotations

import streamlit as st


CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

:root {
    --primary: #10b981;
    --primary-dark: #059669;
    --primary-light: #34d399;
    --teal: #0ea5e9;
    --gradient-main: linear-gradient(135deg, #0ea5e9 0%, #10b981 100%);
    --gradient-success: linear-gradient(135deg, #10b981 0%, #059669 100%);
    --gradient-warning: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
    --gradient-danger: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
    --gradient-purple: linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%);
    --gradient-pink: linear-gradient(135deg, #ec4899 0%, #db2777 100%);
    --bg-card: #ffffff;
    --bg-soft: #f1f5f9;
    --border-soft: #e2e8f0;
    --text-primary: #0f172a;
    --text-secondary: #64748b;
    --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
    --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
    --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
    --shadow-xl: 0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1);
}

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

.main .block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1400px;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

h1 {
    font-weight: 800 !important;
    letter-spacing: -0.025em !important;
    background: var(--gradient-main);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.5rem !important;
}

h2 {
    font-weight: 700 !important;
    color: var(--text-primary) !important;
    letter-spacing: -0.02em !important;
}

h3 {
    font-weight: 600 !important;
    color: var(--text-primary) !important;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
    border-right: 1px solid #334155;
}

section[data-testid="stSidebar"] * {
    color: #e2e8f0 !important;
}

section[data-testid="stSidebar"] h1 {
    background: linear-gradient(135deg, #10b981 0%, #34d399 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-size: 1.75rem !important;
    margin-bottom: 0 !important;
}

section[data-testid="stSidebar"] hr {
    border-color: #334155 !important;
    margin: 1rem 0 !important;
}

section[data-testid="stSidebar"] .stRadio > div {
    gap: 0.5rem !important;
}

section[data-testid="stSidebar"] label[data-baseweb="radio"] {
    padding: 0.75rem 1rem !important;
    border-radius: 0.75rem !important;
    transition: all 0.2s ease !important;
    cursor: pointer !important;
}

section[data-testid="stSidebar"] label[data-baseweb="radio"]:hover {
    background: rgba(16, 185, 129, 0.1) !important;
    transform: translateX(4px) !important;
}

[data-testid="stMetric"] {
    background: var(--bg-card);
    padding: 1.5rem !important;
    border-radius: 1rem !important;
    border: 1px solid var(--border-soft);
    box-shadow: var(--shadow-md);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}

[data-testid="stMetric"]::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: var(--gradient-main);
}

[data-testid="stMetric"]:hover {
    transform: translateY(-4px);
    box-shadow: var(--shadow-xl);
    border-color: var(--primary);
}

[data-testid="stMetric"] label {
    color: var(--text-secondary) !important;
    font-weight: 500 !important;
    font-size: 0.875rem !important;
    letter-spacing: 0.025em !important;
}

[data-testid="stMetric"] [data-testid="stMetricValue"] {
    font-size: 2.25rem !important;
    font-weight: 800 !important;
    color: var(--text-primary) !important;
    background: var(--gradient-main);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

[data-testid="stMetric"] [data-testid="stMetricDelta"] {
    font-weight: 600 !important;
    font-size: 0.875rem !important;
}

.stButton > button {
    border-radius: 0.75rem !important;
    font-weight: 600 !important;
    padding: 0.625rem 1.25rem !important;
    transition: all 0.2s ease !important;
    border: none !important;
    box-shadow: var(--shadow-sm);
}

.stButton > button[kind="primary"] {
    background: var(--gradient-main) !important;
    color: white !important;
}

.stButton > button[kind="primary"]:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 20px -5px rgba(16, 185, 129, 0.5) !important;
}

.stButton > button[kind="secondary"] {
    background: white !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border-soft) !important;
}

.stButton > button[kind="secondary"]:hover {
    border-color: var(--primary) !important;
    color: var(--primary) !important;
}

.stSelectbox > div > div,
.stMultiSelect > div > div,
.stTextInput > div > div,
.stNumberInput > div > div {
    border-radius: 0.75rem !important;
    border: 1px solid var(--border-soft) !important;
    transition: all 0.2s ease !important;
}

.stSelectbox > div > div:focus-within,
.stTextInput > div > div:focus-within,
.stNumberInput > div > div:focus-within {
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1) !important;
}

[data-testid="stDataFrame"] {
    border-radius: 1rem !important;
    overflow: hidden;
    box-shadow: var(--shadow-md);
    border: 1px solid var(--border-soft);
}

.streamlit-expanderHeader {
    background: var(--bg-soft) !important;
    border-radius: 0.75rem !important;
    font-weight: 600 !important;
    transition: all 0.2s ease !important;
}

.streamlit-expanderHeader:hover {
    background: #e0f2fe !important;
}

.stAlert {
    border-radius: 1rem !important;
    border: none !important;
    padding: 1rem 1.25rem !important;
    box-shadow: var(--shadow-sm);
}

.stPlotlyChart {
    background: var(--bg-card);
    border-radius: 1rem;
    padding: 1rem;
    box-shadow: var(--shadow-md);
    border: 1px solid var(--border-soft);
}

[data-testid="stForm"] {
    background: var(--bg-card);
    padding: 1.5rem !important;
    border-radius: 1rem !important;
    border: 1px solid var(--border-soft);
    box-shadow: var(--shadow-sm);
}

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

.main .block-container > div {
    animation: fadeInUp 0.5s ease-out;
}

hr {
    margin: 2rem 0 !important;
    border: none !important;
    height: 1px !important;
    background: linear-gradient(90deg, transparent, var(--border-soft), transparent) !important;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 0.5rem;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 0.75rem !important;
    padding: 0.5rem 1.25rem !important;
    font-weight: 500 !important;
}

.stTabs [aria-selected="true"] {
    background: var(--gradient-main) !important;
    color: white !important;
}

.stSpinner > div {
    border-top-color: var(--primary) !important;
}
</style>
"""


SPLASH_CSS = """
<style>
/* Cache la sidebar pendant le splash */
section[data-testid="stSidebar"] {
    display: none !important;
}

.main .block-container {
    max-width: 100% !important;
    padding: 0 !important;
}

.splash-container {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: linear-gradient(135deg, #0f172a 0%, #064e3b 50%, #0f172a 100%);
    overflow: hidden;
    z-index: 1;
}

.particles {
    position: absolute;
    width: 100%;
    height: 100%;
    overflow: hidden;
    z-index: 1;
}

.particle {
    position: absolute;
    background: radial-gradient(circle, rgba(16, 185, 129, 0.6) 0%, rgba(16, 185, 129, 0) 70%);
    border-radius: 50%;
    animation: float 15s infinite ease-in-out;
}

.particle:nth-child(1) { width: 200px; height: 200px; top: 10%; left: 10%; animation-delay: 0s; }
.particle:nth-child(2) { width: 150px; height: 150px; top: 60%; left: 80%; animation-delay: -2s; }
.particle:nth-child(3) { width: 100px; height: 100px; top: 30%; left: 70%; animation-delay: -4s; }
.particle:nth-child(4) { width: 250px; height: 250px; top: 70%; left: 20%; animation-delay: -6s; }
.particle:nth-child(5) { width: 180px; height: 180px; top: 20%; left: 50%; animation-delay: -8s; }
.particle:nth-child(6) { width: 120px; height: 120px; top: 80%; left: 60%; animation-delay: -10s; }
.particle:nth-child(7) { width: 90px; height: 90px; top: 50%; left: 5%; animation-delay: -12s; }
.particle:nth-child(8) { width: 160px; height: 160px; top: 40%; left: 90%; animation-delay: -14s; }

@keyframes float {
    0%, 100% { transform: translate(0, 0) scale(1); opacity: 0.4; }
    25% { transform: translate(50px, -80px) scale(1.1); opacity: 0.6; }
    50% { transform: translate(-30px, -120px) scale(0.9); opacity: 0.3; }
    75% { transform: translate(-80px, -50px) scale(1.05); opacity: 0.5; }
}

.geo-decor {
    position: absolute;
    border: 2px solid rgba(16, 185, 129, 0.3);
    border-radius: 50%;
}

.geo-decor.circle-1 {
    width: 600px;
    height: 600px;
    top: -200px;
    right: -200px;
    border-style: dashed;
    animation: rotate 30s linear infinite;
}

.geo-decor.circle-2 {
    width: 400px;
    height: 400px;
    bottom: -150px;
    left: -150px;
    border-color: rgba(14, 165, 233, 0.3);
    animation: rotate 25s linear infinite reverse;
}

.geo-decor.circle-3 {
    width: 300px;
    height: 300px;
    top: 50%;
    left: 50%;
    border-color: rgba(52, 211, 153, 0.15);
    animation: rotate-center 40s linear infinite;
}

@keyframes rotate {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}

@keyframes rotate-center {
    from { transform: translate(-50%, -50%) rotate(0deg); }
    to { transform: translate(-50%, -50%) rotate(360deg); }
}

.geo-line {
    position: absolute;
    background: linear-gradient(90deg, transparent, rgba(16, 185, 129, 0.4), transparent);
    height: 2px;
    animation: pulse-line 4s infinite ease-in-out;
}

.geo-line.line-1 {
    width: 300px;
    top: 25%;
    left: 0;
    animation-delay: 0s;
}

.geo-line.line-2 {
    width: 250px;
    bottom: 30%;
    right: 0;
    animation-delay: -2s;
}

@keyframes pulse-line {
    0%, 100% { opacity: 0.2; transform: scaleX(1); }
    50% { opacity: 0.7; transform: scaleX(1.2); }
}

.splash-content {
    position: relative;
    z-index: 10;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100vh;
    padding: 2rem;
    text-align: center;
    color: white;
    animation: fadeInScale 1s ease-out;
}

@keyframes fadeInScale {
    from { opacity: 0; transform: scale(0.95); }
    to { opacity: 1; transform: scale(1); }
}

.splash-logo-wrapper {
    position: relative;
    width: 180px;
    height: 180px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 2rem;
    animation: floatLogo 3s infinite ease-in-out;
}

@keyframes floatLogo {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-15px); }
}

.splash-logo-aura {
    position: absolute;
    width: 100%;
    height: 100%;
    background: radial-gradient(circle, rgba(16, 185, 129, 0.5) 0%, transparent 70%);
    border-radius: 50%;
    animation: pulse-aura 2s infinite ease-in-out;
}

@keyframes pulse-aura {
    0%, 100% { transform: scale(1); opacity: 0.5; }
    50% { transform: scale(1.3); opacity: 0.8; }
}

.splash-logo-emoji {
    position: relative;
    font-size: 6rem;
    filter: drop-shadow(0 0 30px rgba(16, 185, 129, 0.6));
    z-index: 2;
}

.splash-title {
    font-size: 4rem;
    font-weight: 900;
    letter-spacing: -0.03em;
    margin: 0 0 1rem 0;
    background: linear-gradient(135deg, #34d399 0%, #0ea5e9 50%, #34d399 100%);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: shimmer 3s linear infinite;
}

@keyframes shimmer {
    to { background-position: 200% center; }
}

.splash-subtitle {
    font-size: 1.5rem;
    font-weight: 400;
    color: #cbd5e1;
    margin: 0 0 0.5rem 0;
    letter-spacing: -0.01em;
}

.splash-tagline {
    display: inline-block;
    font-size: 0.9rem;
    color: #10b981;
    font-weight: 600;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    margin: 0 0 3rem 0;
    padding: 0.5rem 1.5rem;
    border: 1px solid rgba(16, 185, 129, 0.3);
    border-radius: 999px;
    background: rgba(16, 185, 129, 0.05);
    backdrop-filter: blur(10px);
}

.splash-team {
    margin: 2rem 0;
    padding: 2rem 3rem;
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 1.5rem;
    max-width: 700px;
    width: 90%;
}

.splash-team-label {
    font-size: 0.75rem;
    color: #94a3b8;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    font-weight: 600;
    margin-bottom: 1rem;
}

.splash-team-list {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 0.75rem;
    margin-bottom: 1.5rem;
}

.splash-team-member {
    background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(14, 165, 233, 0.15) 100%);
    border: 1px solid rgba(16, 185, 129, 0.3);
    color: #e2e8f0;
    padding: 0.5rem 1.25rem;
    border-radius: 999px;
    font-size: 0.95rem;
    font-weight: 500;
    transition: all 0.3s ease;
}

.splash-team-member:hover {
    background: linear-gradient(135deg, rgba(16, 185, 129, 0.3) 0%, rgba(14, 165, 233, 0.3) 100%);
    transform: translateY(-2px);
}

.splash-supervisor {
    margin-top: 1rem;
    padding-top: 1rem;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.splash-supervisor-label {
    font-size: 0.75rem;
    color: #94a3b8;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    font-weight: 600;
    margin-bottom: 0.5rem;
}

.splash-supervisor-name {
    font-size: 1.125rem;
    color: #34d399;
    font-weight: 600;
}

.splash-school {
    margin-top: 0.75rem;
    font-size: 0.875rem;
    color: #94a3b8;
}

/* Bouton commencer (mode splash) */
.stButton > button {
    background: linear-gradient(135deg, #10b981 0%, #0ea5e9 100%) !important;
    color: white !important;
    font-size: 1.125rem !important;
    font-weight: 700 !important;
    padding: 1rem 3rem !important;
    border-radius: 999px !important;
    border: none !important;
    box-shadow: 0 10px 40px -10px rgba(16, 185, 129, 0.6) !important;
    letter-spacing: 0.05em !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    text-transform: uppercase !important;
}

.stButton > button:hover {
    transform: translateY(-3px) scale(1.05) !important;
    box-shadow: 0 20px 50px -10px rgba(16, 185, 129, 0.8) !important;
}
</style>
"""


def render_kpi_card(
    icon: str,
    label: str,
    value: str,
    sublabel: str = "",
    gradient: str = "main",
) -> str:
    """Génère le HTML d'une KPI card custom avec gradient, icône, et hover."""
    gradients = {
        "main": "linear-gradient(135deg, #0ea5e9 0%, #10b981 100%)",
        "success": "linear-gradient(135deg, #10b981 0%, #059669 100%)",
        "warning": "linear-gradient(135deg, #f59e0b 0%, #d97706 100%)",
        "danger": "linear-gradient(135deg, #ef4444 0%, #dc2626 100%)",
        "purple": "linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%)",
        "pink": "linear-gradient(135deg, #ec4899 0%, #db2777 100%)",
    }
    bg = gradients.get(gradient, gradients["main"])

    return f"""
    <div style="
        background: {bg};
        padding: 1.75rem;
        border-radius: 1.25rem;
        color: white;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.15);
        position: relative;
        overflow: hidden;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: default;
    " onmouseover="this.style.transform='translateY(-6px)'; this.style.boxShadow='0 20px 40px -10px rgba(0,0,0,0.3)'"
       onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 10px 25px -5px rgba(0,0,0,0.15)'">
        <div style="
            position: absolute;
            top: -20px;
            right: -20px;
            width: 100px;
            height: 100px;
            background: rgba(255,255,255,0.1);
            border-radius: 50%;
        "></div>
        <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">{icon}</div>
        <div style="
            font-size: 0.875rem;
            font-weight: 500;
            opacity: 0.9;
            margin-bottom: 0.25rem;
            letter-spacing: 0.025em;
            text-transform: uppercase;
        ">{label}</div>
        <div style="
            font-size: 2.5rem;
            font-weight: 800;
            line-height: 1.1;
            letter-spacing: -0.025em;
        ">{value}</div>
        {f'<div style="font-size: 0.875rem; opacity: 0.85; margin-top: 0.5rem; font-weight: 500;">{sublabel}</div>' if sublabel else ''}
    </div>
    """


def render_section_header(icon: str, title: str, subtitle: str = "") -> str:
    """Header de section moderne avec icône."""
    return f"""
    <div style="margin: 2rem 0 1.5rem 0;">
        <div style="display: flex; align-items: center; gap: 0.75rem;">
            <div style="
                font-size: 1.75rem;
                width: 3rem;
                height: 3rem;
                display: flex;
                align-items: center;
                justify-content: center;
                background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
                border-radius: 0.75rem;
                border: 1px solid #a7f3d0;
            ">{icon}</div>
            <div>
                <div style="
                    font-size: 1.5rem;
                    font-weight: 700;
                    color: #0f172a;
                    line-height: 1.2;
                ">{title}</div>
                {f'<div style="font-size: 0.875rem; color: #64748b; margin-top: 0.25rem;">{subtitle}</div>' if subtitle else ''}
            </div>
        </div>
    </div>
    """


def render_splash_screen(
    project_name: str,
    subtitle: str,
    tagline: str,
    team_members: list[str],
    supervisor: str,
    school: str,
    project_code: str,
    logo_emoji: str = "🌿",
) -> str:
    """Génère le HTML complet de la page d'accueil splash screen."""
    members_html = "".join(
        f'<div class="splash-team-member">{member}</div>'
        for member in team_members
    )

    return f"""<div class="splash-container"><div class="geo-decor circle-1"></div><div class="geo-decor circle-2"></div><div class="geo-decor circle-3"></div><div class="geo-line line-1"></div><div class="geo-line line-2"></div><div class="particles"><div class="particle"></div><div class="particle"></div><div class="particle"></div><div class="particle"></div><div class="particle"></div><div class="particle"></div><div class="particle"></div><div class="particle"></div></div><div class="splash-content"><div class="splash-logo-wrapper"><div class="splash-logo-aura"></div><div class="splash-logo-emoji">{logo_emoji}</div></div><h1 class="splash-title">{project_name}</h1><p class="splash-subtitle">{subtitle}</p><div class="splash-tagline">{tagline}</div><div class="splash-team"><div class="splash-team-label">Équipe projet</div><div class="splash-team-list">{members_html}</div><div class="splash-supervisor"><div class="splash-supervisor-label">Encadré par</div><div class="splash-supervisor-name">{supervisor}</div><div class="splash-school">{school} · {project_code}</div></div></div></div></div>"""


def get_plotly_theme() -> dict:
    """Configuration Plotly cohérente avec le design teal/vert."""
    return {
        "layout": {
            "font": {
                "family": "Inter, sans-serif",
                "color": "#0f172a",
                "size": 13,
            },
            "paper_bgcolor": "rgba(0,0,0,0)",
            "plot_bgcolor": "#f8fafc",
            "colorway": [
                "#10b981", "#0ea5e9", "#8b5cf6", "#f59e0b",
                "#ef4444", "#ec4899", "#14b8a6", "#6366f1",
            ],
            "xaxis": {
                "gridcolor": "#e2e8f0",
                "zerolinecolor": "#cbd5e1",
            },
            "yaxis": {
                "gridcolor": "#e2e8f0",
                "zerolinecolor": "#cbd5e1",
            },
            "title": {
                "font": {"size": 16, "weight": 700, "color": "#0f172a"},
            },
        }
    }


def inject_styles() -> None:
    """Injecte tous les styles CSS dans la page Streamlit."""
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def inject_splash_styles() -> None:
    """Injecte les styles spécifiques au splash screen."""
    st.markdown(SPLASH_CSS, unsafe_allow_html=True)