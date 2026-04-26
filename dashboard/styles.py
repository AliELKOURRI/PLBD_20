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
/* ============ Import de la police Inter ============ */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

/* ============ Variables globales ============ */
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

/* ============ Police globale ============ */
html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

/* ============ Layout général ============ */
.main .block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1400px;
}

/* Cache le menu hamburger et le footer Streamlit */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* ============ Titres ============ */
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

/* ============ Sidebar ============ */
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

/* Boutons radio sidebar — style premium */
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

/* ============ KPI Metrics — cards modernes ============ */
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

/* ============ Boutons ============ */
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

/* ============ Inputs ============ */
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

/* ============ Tableaux (DataFrame) ============ */
[data-testid="stDataFrame"] {
    border-radius: 1rem !important;
    overflow: hidden;
    box-shadow: var(--shadow-md);
    border: 1px solid var(--border-soft);
}

/* ============ Expanders ============ */
.streamlit-expanderHeader {
    background: var(--bg-soft) !important;
    border-radius: 0.75rem !important;
    font-weight: 600 !important;
    transition: all 0.2s ease !important;
}

.streamlit-expanderHeader:hover {
    background: #e0f2fe !important;
}

/* ============ Alertes (success/warning/error/info) ============ */
.stAlert {
    border-radius: 1rem !important;
    border: none !important;
    padding: 1rem 1.25rem !important;
    box-shadow: var(--shadow-sm);
}

/* ============ Plotly charts — fond cohérent ============ */
.stPlotlyChart {
    background: var(--bg-card);
    border-radius: 1rem;
    padding: 1rem;
    box-shadow: var(--shadow-md);
    border: 1px solid var(--border-soft);
}

/* ============ Forms ============ */
[data-testid="stForm"] {
    background: var(--bg-card);
    padding: 1.5rem !important;
    border-radius: 1rem !important;
    border: 1px solid var(--border-soft);
    box-shadow: var(--shadow-sm);
}

/* ============ Animations ============ */
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

/* ============ Markdown séparateurs ============ */
hr {
    margin: 2rem 0 !important;
    border: none !important;
    height: 1px !important;
    background: linear-gradient(90deg, transparent, var(--border-soft), transparent) !important;
}

/* ============ Tabs ============ */
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

/* ============ Spinner ============ */
.stSpinner > div {
    border-top-color: var(--primary) !important;
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
    """
    Génère le HTML d'une KPI card custom avec gradient, icône, et hover.

    Args:
        icon: Emoji ou icône (ex: "📦", "💰")
        label: Texte du label (ex: "Produits en stock")
        value: Valeur principale (ex: "30")
        sublabel: Sous-texte optionnel (ex: "+5% ce mois")
        gradient: Type de gradient ('main', 'success', 'warning', 'danger',
                  'purple', 'pink')

    Returns:
        HTML string à injecter via st.markdown(..., unsafe_allow_html=True).
    """
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