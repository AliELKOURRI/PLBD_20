"""
Styles CSS custom pour le dashboard Smart Predict AI.

Design system inspire de Shine :
- Fond clair lumineux avec blobs organiques colores
- Sidebar blanche epuree
- Accent indigo/violet pour les CTA
- Coins tres arrondis, ombres douces
- Typographie Inter bold et aérée
"""

from __future__ import annotations

import streamlit as st


CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

:root {
    --primary: #6C5CE7;
    --primary-dark: #5A4BD1;
    --primary-light: #A29BFE;
    --accent-teal: #00D2D3;
    --accent-yellow: #FECA57;
    --accent-blue: #54A0FF;
    --accent-green: #10b981;
    --gradient-primary: linear-gradient(135deg, #6C5CE7 0%, #A29BFE 100%);
    --gradient-teal: linear-gradient(135deg, #00D2D3 0%, #55E6C1 100%);
    --gradient-success: linear-gradient(135deg, #10b981 0%, #34d399 100%);
    --gradient-warning: linear-gradient(135deg, #FECA57 0%, #F39C12 100%);
    --gradient-danger: linear-gradient(135deg, #FF6B6B 0%, #EE5A24 100%);
    --gradient-blue: linear-gradient(135deg, #54A0FF 0%, #2E86DE 100%);
    --bg-page: #F5F7FF;
    --bg-card: #ffffff;
    --bg-soft: #F0F3FF;
    --border-soft: rgba(108, 92, 231, 0.08);
    --text-primary: #2D3436;
    --text-secondary: #636E72;
    --text-muted: #B2BEC3;
    --shadow-card: 0 2px 8px rgba(108, 92, 231, 0.06), 0 8px 24px rgba(108, 92, 231, 0.04);
    --shadow-card-hover: 0 8px 32px rgba(108, 92, 231, 0.12), 0 2px 8px rgba(108, 92, 231, 0.06);
    --shadow-button: 0 4px 16px rgba(108, 92, 231, 0.3);
    --radius-sm: 0.75rem;
    --radius-md: 1rem;
    --radius-lg: 1.5rem;
    --radius-xl: 2rem;
    --radius-full: 999px;
    --transition: 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    --transition-spring: 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    -webkit-font-smoothing: antialiased !important;
}

/* ============================================================
   PAGE BACKGROUND — Light with colorful blobs
   ============================================================ */

[data-testid="stAppViewContainer"] {
    background: var(--bg-page);
    position: relative;
}

[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    top: -120px;
    left: -120px;
    width: 500px;
    height: 500px;
    background: radial-gradient(circle, rgba(0, 210, 211, 0.18) 0%, transparent 70%);
    border-radius: 50%;
    pointer-events: none;
    z-index: 0;
    animation: blobFloat1 18s ease-in-out infinite;
}

[data-testid="stAppViewContainer"]::after {
    content: '';
    position: fixed;
    bottom: -100px;
    right: -100px;
    width: 450px;
    height: 450px;
    background: radial-gradient(circle, rgba(254, 202, 87, 0.2) 0%, transparent 70%);
    border-radius: 50%;
    pointer-events: none;
    z-index: 0;
    animation: blobFloat2 20s ease-in-out infinite;
}

@keyframes blobFloat1 {
    0%, 100% { transform: translate(0, 0) scale(1); }
    33% { transform: translate(40px, 30px) scale(1.05); }
    66% { transform: translate(-20px, 50px) scale(0.95); }
}

@keyframes blobFloat2 {
    0%, 100% { transform: translate(0, 0) scale(1); }
    33% { transform: translate(-30px, -40px) scale(1.08); }
    66% { transform: translate(20px, -20px) scale(0.92); }
}

.main .block-container {
    padding-top: 2.5rem;
    padding-bottom: 4rem;
    max-width: 1400px;
    position: relative;
    z-index: 1;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

/* ============================================================
   TYPOGRAPHY
   ============================================================ */

h1 {
    font-weight: 800 !important;
    letter-spacing: -0.035em !important;
    color: var(--text-primary) !important;
    -webkit-text-fill-color: var(--text-primary) !important;
    background: none !important;
    margin-bottom: 0.5rem !important;
    line-height: 1.1 !important;
}

h2 {
    font-weight: 700 !important;
    color: var(--text-primary) !important;
    letter-spacing: -0.025em !important;
}

h3 {
    font-weight: 600 !important;
    color: var(--text-primary) !important;
}

/* ============================================================
   SIDEBAR — Clean white
   ============================================================ */

section[data-testid="stSidebar"] {
    background: #ffffff !important;
    border-right: 1px solid rgba(108, 92, 231, 0.06) !important;
    box-shadow: 4px 0 20px rgba(0, 0, 0, 0.03);
}

section[data-testid="stSidebar"] * {
    color: var(--text-primary) !important;
}

section[data-testid="stSidebar"] h1 {
    color: var(--primary) !important;
    -webkit-text-fill-color: var(--primary) !important;
    font-size: 1.6rem !important;
    margin-bottom: 0 !important;
}

section[data-testid="stSidebar"] hr {
    border-color: rgba(108, 92, 231, 0.06) !important;
    margin: 1.25rem 0 !important;
}

section[data-testid="stSidebar"] .stRadio > div {
    gap: 0.375rem !important;
}

section[data-testid="stSidebar"] label[data-baseweb="radio"] {
    padding: 0.75rem 1rem !important;
    border-radius: var(--radius-md) !important;
    transition: all var(--transition) !important;
    cursor: pointer !important;
    border: 1px solid transparent !important;
}

section[data-testid="stSidebar"] label[data-baseweb="radio"]:hover {
    background: var(--bg-soft) !important;
    border-color: rgba(108, 92, 231, 0.1) !important;
    transform: translateX(4px) !important;
}

/* ============================================================
   BUTTONS — Indigo/violet like Shine
   ============================================================ */

.stButton > button {
    border-radius: var(--radius-full) !important;
    font-weight: 700 !important;
    padding: 0.7rem 2rem !important;
    transition: all var(--transition-spring) !important;
    border: none !important;
    letter-spacing: 0.01em !important;
    font-size: 0.95rem !important;
}

.stButton > button[kind="primary"] {
    background: var(--gradient-primary) !important;
    color: white !important;
    box-shadow: var(--shadow-button) !important;
}

.stButton > button[kind="primary"]:hover {
    transform: translateY(-3px) scale(1.02) !important;
    box-shadow: 0 8px 28px rgba(108, 92, 231, 0.4) !important;
}

.stButton > button[kind="secondary"] {
    background: white !important;
    color: var(--primary) !important;
    border: 2px solid rgba(108, 92, 231, 0.2) !important;
    box-shadow: none !important;
}

.stButton > button[kind="secondary"]:hover {
    border-color: var(--primary) !important;
    background: var(--bg-soft) !important;
    box-shadow: 0 4px 12px rgba(108, 92, 231, 0.1) !important;
}

/* ============================================================
   FORM INPUTS
   ============================================================ */

.stSelectbox > div > div,
.stMultiSelect > div > div,
.stTextInput > div > div,
.stNumberInput > div > div {
    border-radius: var(--radius-md) !important;
    border: 2px solid rgba(108, 92, 231, 0.08) !important;
    transition: all var(--transition) !important;
    background: white !important;
}

.stSelectbox > div > div:focus-within,
.stTextInput > div > div:focus-within,
.stNumberInput > div > div:focus-within {
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 4px rgba(108, 92, 231, 0.08) !important;
}

/* ============================================================
   METRIC CARDS
   ============================================================ */

[data-testid="stMetric"] {
    background: white;
    padding: 1.5rem !important;
    border-radius: var(--radius-lg) !important;
    border: 1px solid rgba(108, 92, 231, 0.06);
    box-shadow: var(--shadow-card);
    transition: all var(--transition-spring);
}

[data-testid="stMetric"]::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 4px;
    background: var(--gradient-primary);
    border-radius: var(--radius-lg) var(--radius-lg) 0 0;
}

[data-testid="stMetric"]:hover {
    transform: translateY(-4px);
    box-shadow: var(--shadow-card-hover);
}

[data-testid="stMetric"] label {
    color: var(--text-secondary) !important;
    font-weight: 600 !important;
    font-size: 0.8rem !important;
    letter-spacing: 0.04em !important;
    text-transform: uppercase;
}

[data-testid="stMetric"] [data-testid="stMetricValue"] {
    font-size: 2rem !important;
    font-weight: 800 !important;
    color: var(--text-primary) !important;
}

/* ============================================================
   DATA FRAMES
   ============================================================ */

[data-testid="stDataFrame"] {
    border-radius: var(--radius-lg) !important;
    overflow: hidden;
    box-shadow: var(--shadow-card);
    border: 1px solid rgba(108, 92, 231, 0.06);
    background: white;
}

/* ============================================================
   EXPANDERS
   ============================================================ */

.streamlit-expanderHeader {
    background: var(--bg-soft) !important;
    border-radius: var(--radius-md) !important;
    font-weight: 600 !important;
    transition: all var(--transition) !important;
    border: 1px solid rgba(108, 92, 231, 0.06) !important;
}

.streamlit-expanderHeader:hover {
    background: rgba(108, 92, 231, 0.06) !important;
    border-color: rgba(108, 92, 231, 0.12) !important;
}

/* ============================================================
   ALERTS
   ============================================================ */

.stAlert {
    border-radius: var(--radius-lg) !important;
    border: none !important;
    padding: 1rem 1.25rem !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}

/* ============================================================
   PLOTLY CHARTS
   ============================================================ */

.stPlotlyChart {
    background: white;
    border-radius: var(--radius-xl);
    padding: 1.25rem;
    box-shadow: var(--shadow-card);
    border: 1px solid rgba(108, 92, 231, 0.06);
    transition: all var(--transition);
}

.stPlotlyChart:hover {
    box-shadow: var(--shadow-card-hover);
}

/* ============================================================
   FORMS
   ============================================================ */

[data-testid="stForm"] {
    background: white;
    padding: 1.75rem !important;
    border-radius: var(--radius-xl) !important;
    border: 1px solid rgba(108, 92, 231, 0.06);
    box-shadow: var(--shadow-card);
}

/* ============================================================
   TABS
   ============================================================ */

.stTabs [data-baseweb="tab-list"] {
    gap: 0.375rem;
    background: var(--bg-soft);
    padding: 0.3rem;
    border-radius: var(--radius-full);
}

.stTabs [data-baseweb="tab"] {
    border-radius: var(--radius-full) !important;
    padding: 0.5rem 1.25rem !important;
    font-weight: 600 !important;
    transition: all var(--transition) !important;
}

.stTabs [aria-selected="true"] {
    background: var(--gradient-primary) !important;
    color: white !important;
    box-shadow: 0 2px 8px rgba(108, 92, 231, 0.3) !important;
}

/* ============================================================
   SCROLLBAR
   ============================================================ */

::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(108, 92, 231, 0.15); border-radius: 999px; }
::-webkit-scrollbar-thumb:hover { background: rgba(108, 92, 231, 0.3); }

/* ============================================================
   DIVIDERS / SPINNER / ANIMATIONS
   ============================================================ */

hr {
    margin: 2rem 0 !important;
    border: none !important;
    height: 1px !important;
    background: linear-gradient(90deg, transparent, rgba(108, 92, 231, 0.1), transparent) !important;
}

.stSpinner > div { border-top-color: var(--primary) !important; }

@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(16px); }
    to { opacity: 1; transform: translateY(0); }
}

.main .block-container > div {
    animation: fadeInUp 0.4s ease-out;
}

.stRadio > div[role="radiogroup"] > label {
    border-radius: var(--radius-full) !important;
    padding: 0.5rem 1rem !important;
    transition: all var(--transition) !important;
}

.stRadio > div[role="radiogroup"] > label:hover {
    background: var(--bg-soft);
}
</style>
"""


SPLASH_CSS = """
<style>
section[data-testid="stSidebar"] { display: none !important; }

.main .block-container {
    max-width: 100% !important;
    padding: 0 !important;
    position: relative !important;
    z-index: 100 !important;
}

[data-testid="stAppViewContainer"] {
    position: relative !important;
    background: transparent !important;
}

[data-testid="stAppViewContainer"]::before,
[data-testid="stAppViewContainer"]::after { display: none !important; }

.splash-container {
    position: fixed;
    top: 0; left: 0;
    width: 100vw; height: 100vh;
    background: linear-gradient(160deg, #F5F7FF 0%, #EDE8FF 40%, #F5F7FF 100%);
    overflow: hidden;
    z-index: 1;
    pointer-events: none;
}

/* Blob turquoise */
.splash-container::before {
    content: '';
    position: absolute;
    top: -15%; left: -10%;
    width: 600px; height: 600px;
    background: radial-gradient(circle, rgba(0, 210, 211, 0.25) 0%, transparent 70%);
    border-radius: 50%;
    animation: blobFloat1 18s ease-in-out infinite;
    z-index: 1;
}

/* Blob jaune */
.splash-container::after {
    content: '';
    position: absolute;
    bottom: -15%; right: -10%;
    width: 550px; height: 550px;
    background: radial-gradient(circle, rgba(254, 202, 87, 0.3) 0%, transparent 70%);
    border-radius: 50%;
    animation: blobFloat2 20s ease-in-out infinite;
    z-index: 1;
}

.particles {
    position: absolute;
    width: 100%; height: 100%;
    overflow: hidden;
    z-index: 2;
}

.particle {
    position: absolute;
    border-radius: 50%;
    animation: float 18s infinite ease-in-out;
}

.particle:nth-child(1) { width: 14px; height: 14px; top: 20%; left: 15%; background: #00D2D3; animation-delay: 0s; }
.particle:nth-child(2) { width: 10px; height: 10px; top: 55%; left: 80%; background: #6C5CE7; animation-delay: -3s; }
.particle:nth-child(3) { width: 18px; height: 18px; top: 30%; left: 65%; background: #FECA57; animation-delay: -5s; }
.particle:nth-child(4) { width: 8px; height: 8px; top: 70%; left: 25%; background: #54A0FF; animation-delay: -7s; }
.particle:nth-child(5) { width: 12px; height: 12px; top: 15%; left: 50%; background: #FF6B6B; animation-delay: -9s; }
.particle:nth-child(6) { width: 16px; height: 16px; top: 75%; left: 60%; background: #00D2D3; animation-delay: -11s; }
.particle:nth-child(7) { width: 10px; height: 10px; top: 45%; left: 8%; background: #FECA57; animation-delay: -13s; }
.particle:nth-child(8) { width: 14px; height: 14px; top: 35%; left: 88%; background: #6C5CE7; animation-delay: -15s; }

@keyframes float {
    0%, 100% { transform: translate(0, 0) scale(1); opacity: 0.7; }
    25% { transform: translate(30px, -40px) scale(1.2); opacity: 1; }
    50% { transform: translate(-20px, -70px) scale(0.8); opacity: 0.5; }
    75% { transform: translate(-40px, -30px) scale(1.1); opacity: 0.9; }
}

.geo-decor { display: none; }
.geo-line { display: none; }

.splash-content {
    position: relative;
    z-index: 10;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100vh;
    padding: 2rem;
    padding-bottom: 8rem;
    text-align: center;
    animation: fadeInScale 0.8s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes fadeInScale {
    from { opacity: 0; transform: scale(0.96) translateY(8px); }
    to { opacity: 1; transform: scale(1) translateY(0); }
}

.splash-logo-wrapper {
    position: relative;
    width: 140px; height: 140px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 2rem;
    animation: floatLogo 4s infinite ease-in-out;
}

@keyframes floatLogo {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-12px); }
}

.splash-logo-aura {
    position: absolute;
    width: 100%; height: 100%;
    background: radial-gradient(circle, rgba(108, 92, 231, 0.15) 0%, transparent 70%);
    border-radius: 50%;
    animation: pulse-aura 3s infinite ease-in-out;
}

@keyframes pulse-aura {
    0%, 100% { transform: scale(1); opacity: 0.4; }
    50% { transform: scale(1.3); opacity: 0.7; }
}

.splash-logo-ring {
    position: absolute;
    width: 130%; height: 130%;
    border: 2px solid rgba(108, 92, 231, 0.15);
    border-radius: 50%;
    animation: rotate 12s linear infinite;
}

.splash-logo-ring::before {
    content: '';
    position: absolute;
    top: -4px; left: 50%;
    width: 8px; height: 8px;
    background: #6C5CE7;
    border-radius: 50%;
    box-shadow: 0 0 10px rgba(108, 92, 231, 0.6);
}

@keyframes rotate {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}

.splash-logo-emoji {
    position: relative;
    font-size: 4.5rem;
    filter: drop-shadow(0 4px 20px rgba(108, 92, 231, 0.3));
    z-index: 2;
}

.splash-title {
    font-size: 4rem;
    font-weight: 900;
    letter-spacing: -0.04em;
    margin: 0 0 0.75rem 0;
    color: #2D3436;
    line-height: 1.05;
}

.splash-subtitle {
    font-size: 1.3rem;
    font-weight: 400;
    color: #636E72;
    margin: 0 0 0.5rem 0;
    letter-spacing: 0.01em;
}

.splash-tagline {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.8rem;
    color: #6C5CE7;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin: 0 0 2.5rem 0;
    padding: 0.5rem 1.75rem;
    border: 2px solid rgba(108, 92, 231, 0.15);
    border-radius: 999px;
    background: rgba(108, 92, 231, 0.04);
}

.splash-team {
    margin: 1.5rem 0;
    padding: 2.5rem 3rem;
    background: white;
    border: 1px solid rgba(108, 92, 231, 0.08);
    border-radius: 2rem;
    max-width: 700px;
    width: 90%;
    box-shadow: 0 4px 24px rgba(108, 92, 231, 0.06);
}

.splash-team-label {
    font-size: 0.7rem;
    color: #B2BEC3;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    font-weight: 700;
    margin-bottom: 1.25rem;
}

.splash-team-list {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 0.625rem;
    margin-bottom: 1.75rem;
}

.splash-team-member {
    background: var(--bg-soft);
    border: 1px solid rgba(108, 92, 231, 0.08);
    color: #2D3436;
    padding: 0.5rem 1.25rem;
    border-radius: 999px;
    font-size: 0.9rem;
    font-weight: 600;
    transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.splash-team-member:hover {
    background: rgba(108, 92, 231, 0.08);
    border-color: rgba(108, 92, 231, 0.2);
    transform: translateY(-3px);
    box-shadow: 0 4px 12px rgba(108, 92, 231, 0.1);
}

.splash-supervisor {
    margin-top: 1.25rem;
    padding-top: 1.25rem;
    border-top: 1px solid rgba(108, 92, 231, 0.06);
}

.splash-supervisor-label {
    font-size: 0.7rem;
    color: #B2BEC3;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    font-weight: 700;
    margin-bottom: 0.5rem;
}

.splash-supervisor-name {
    font-size: 1.1rem;
    color: #6C5CE7;
    font-weight: 700;
}

.splash-school {
    margin-top: 0.5rem;
    font-size: 0.8rem;
    color: #B2BEC3;
    letter-spacing: 0.03em;
}

/* CTA Button */
.main .block-container {
    display: flex !important;
    flex-direction: column !important;
    justify-content: flex-end !important;
    min-height: 100vh !important;
    padding-bottom: 60px !important;
}

.stButton {
    display: flex !important;
    justify-content: center !important;
    z-index: 999 !important;
    position: relative !important;
}

.stButton > button {
    background: linear-gradient(135deg, #6C5CE7 0%, #A29BFE 100%) !important;
    color: white !important;
    font-size: 1.05rem !important;
    font-weight: 700 !important;
    padding: 1rem 3rem !important;
    border-radius: 999px !important;
    border: none !important;
    box-shadow: 0 8px 28px rgba(108, 92, 231, 0.35) !important;
    letter-spacing: 0.06em !important;
    transition: all 0.35s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
    text-transform: uppercase !important;
    cursor: pointer !important;
    min-width: 260px !important;
}

.stButton > button:hover {
    transform: translateY(-3px) scale(1.03) !important;
    box-shadow: 0 14px 40px rgba(108, 92, 231, 0.45) !important;
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
    gradients = {
        "main": ("linear-gradient(135deg, #6C5CE7 0%, #A29BFE 100%)",
                 "rgba(108, 92, 231, 0.3)"),
        "success": ("linear-gradient(135deg, #10b981 0%, #34d399 100%)",
                    "rgba(16, 185, 129, 0.3)"),
        "warning": ("linear-gradient(135deg, #FECA57 0%, #F39C12 100%)",
                    "rgba(254, 202, 87, 0.3)"),
        "danger": ("linear-gradient(135deg, #FF6B6B 0%, #EE5A24 100%)",
                   "rgba(255, 107, 107, 0.3)"),
        "purple": ("linear-gradient(135deg, #6C5CE7 0%, #8B5CF6 100%)",
                   "rgba(108, 92, 231, 0.3)"),
        "pink": ("linear-gradient(135deg, #FD79A8 0%, #E84393 100%)",
                 "rgba(253, 121, 168, 0.3)"),
        "teal": ("linear-gradient(135deg, #00D2D3 0%, #55E6C1 100%)",
                 "rgba(0, 210, 211, 0.3)"),
        "blue": ("linear-gradient(135deg, #54A0FF 0%, #2E86DE 100%)",
                 "rgba(84, 160, 255, 0.3)"),
    }
    bg, glow = gradients.get(gradient, gradients["main"])

    sublabel_html = (
        f'<div style="font-size:0.8rem;opacity:0.85;margin-top:0.5rem;'
        f'font-weight:500;">{sublabel}</div>'
    ) if sublabel else ''

    return (
        f'<div style="background:{bg};padding:1.75rem;border-radius:1.5rem;color:white;'
        f'box-shadow:0 8px 24px -4px {glow};position:relative;overflow:hidden;'
        f'transition:all 0.35s cubic-bezier(0.34,1.56,0.64,1);cursor:default;"'
        f' onmouseover="this.style.transform=\'translateY(-6px) scale(1.02)\';'
        f'this.style.boxShadow=\'0 16px 40px -8px {glow}\'"'
        f' onmouseout="this.style.transform=\'translateY(0) scale(1)\';'
        f'this.style.boxShadow=\'0 8px 24px -4px {glow}\'">'
        f'<div style="position:absolute;top:-30px;right:-30px;width:120px;height:120px;'
        f'background:rgba(255,255,255,0.1);border-radius:50%;"></div>'
        f'<div style="position:absolute;bottom:-20px;left:-20px;width:80px;height:80px;'
        f'background:rgba(255,255,255,0.06);border-radius:50%;"></div>'
        f'<div style="position:relative;z-index:1;">'
        f'<div style="font-size:2rem;margin-bottom:0.75rem;">{icon}</div>'
        f'<div style="font-size:0.75rem;font-weight:700;opacity:0.85;margin-bottom:0.5rem;'
        f'letter-spacing:0.06em;text-transform:uppercase;">{label}</div>'
        f'<div style="font-size:2.25rem;font-weight:800;line-height:1.1;'
        f'letter-spacing:-0.025em;">{value}</div>'
        f'{sublabel_html}'
        f'</div></div>'
    )


def render_section_header(icon: str, title: str, subtitle: str = "") -> str:
    subtitle_html = (
        f'<div style="font-size:0.825rem;color:#B2BEC3;margin-top:0.2rem;'
        f'font-weight:400;">{subtitle}</div>'
    ) if subtitle else ''
    return (
        f'<div style="margin:2.5rem 0 1.5rem 0;">'
        f'<div style="display:flex;align-items:center;gap:0.875rem;">'
        f'<div style="font-size:1.5rem;width:3rem;height:3rem;display:flex;'
        f'align-items:center;justify-content:center;background:rgba(108,92,231,0.06);'
        f'border-radius:1rem;border:1px solid rgba(108,92,231,0.1);">{icon}</div>'
        f'<div>'
        f'<div style="font-size:1.375rem;font-weight:700;color:#2D3436;'
        f'line-height:1.2;letter-spacing:-0.02em;">{title}</div>'
        f'{subtitle_html}'
        f'</div></div></div>'
    )


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
    members_html = "".join(
        f'<div class="splash-team-member">{member}</div>'
        for member in team_members
    )

    return (
        f'<div class="splash-container">'
        f'<div class="particles">'
        f'<div class="particle"></div><div class="particle"></div>'
        f'<div class="particle"></div><div class="particle"></div>'
        f'<div class="particle"></div><div class="particle"></div>'
        f'<div class="particle"></div><div class="particle"></div>'
        f'</div>'
        f'<div class="splash-content">'
        f'<div class="splash-logo-wrapper">'
        f'<div class="splash-logo-aura"></div>'
        f'<div class="splash-logo-ring"></div>'
        f'<div class="splash-logo-emoji">{logo_emoji}</div>'
        f'</div>'
        f'<h1 class="splash-title">{project_name}</h1>'
        f'<p class="splash-subtitle">{subtitle}</p>'
        f'<div class="splash-tagline">{tagline}</div>'
        f'<div class="splash-team">'
        f'<div class="splash-team-label">Equipe projet</div>'
        f'<div class="splash-team-list">{members_html}</div>'
        f'<div class="splash-supervisor">'
        f'<div class="splash-supervisor-label">Encadre par</div>'
        f'<div class="splash-supervisor-name">{supervisor}</div>'
        f'<div class="splash-school">{school} &middot; {project_code}</div>'
        f'</div></div></div></div>'
    )


def render_page_header(title: str, subtitle: str, icon: str = "") -> str:
    icon_html = f'<span style="font-size:2rem;margin-right:0.5rem;">{icon}</span>' if icon else ''
    return (
        f'<div style="margin-bottom:2.5rem;padding:2rem 2.5rem;background:white;'
        f'border-radius:2rem;border:1px solid rgba(108,92,231,0.06);'
        f'box-shadow:0 2px 8px rgba(108,92,231,0.04),0 8px 24px rgba(108,92,231,0.03);'
        f'position:relative;overflow:hidden;">'
        f'<div style="position:absolute;top:0;left:0;right:0;height:4px;'
        f'background:linear-gradient(90deg,#00D2D3,#6C5CE7,#FECA57);"></div>'
        f'<div style="display:flex;align-items:center;gap:0.5rem;">'
        f'{icon_html}'
        f'<div>'
        f'<h1 style="font-size:2.5rem;margin:0 !important;padding:0;line-height:1.15;'
        f'color:#2D3436 !important;-webkit-text-fill-color:#2D3436 !important;">{title}</h1>'
        f'<p style="font-size:1.05rem;color:#636E72;margin:0.4rem 0 0 0;'
        f'font-weight:400;">{subtitle}</p>'
        f'</div></div></div>'
    )


def render_glass_container(content: str, padding: str = "1.75rem") -> str:
    return (
        f'<div style="background:white;border-radius:1.5rem;'
        f'border:1px solid rgba(108,92,231,0.06);'
        f'box-shadow:0 2px 8px rgba(108,92,231,0.04),0 8px 24px rgba(108,92,231,0.03);'
        f'padding:{padding};margin-bottom:1.5rem;">'
        f'{content}</div>'
    )


def render_info_banner(
    icon: str,
    title: str,
    body: str,
    style: str = "info",
) -> str:
    styles = {
        "info": {
            "bg": "rgba(84,160,255,0.06)",
            "border": "#54A0FF",
            "border_light": "rgba(84,160,255,0.12)",
            "title_color": "#2E86DE",
            "text_color": "#2D3436",
        },
        "success": {
            "bg": "rgba(16,185,129,0.06)",
            "border": "#10b981",
            "border_light": "rgba(16,185,129,0.12)",
            "title_color": "#059669",
            "text_color": "#2D3436",
        },
        "warning": {
            "bg": "rgba(254,202,87,0.08)",
            "border": "#F39C12",
            "border_light": "rgba(243,156,18,0.12)",
            "title_color": "#E67E22",
            "text_color": "#2D3436",
        },
        "danger": {
            "bg": "rgba(255,107,107,0.06)",
            "border": "#FF6B6B",
            "border_light": "rgba(255,107,107,0.12)",
            "title_color": "#EE5A24",
            "text_color": "#2D3436",
        },
    }
    s = styles.get(style, styles["info"])
    return (
        f'<div style="background:{s["bg"]};padding:1.5rem 1.75rem;'
        f'border-radius:1.5rem;border:1px solid {s["border_light"]};'
        f'border-left:4px solid {s["border"]};'
        f'box-shadow:0 2px 8px rgba(0,0,0,0.02);margin:1rem 0;">'
        f'<div style="display:flex;align-items:flex-start;gap:0.75rem;">'
        f'<div style="font-size:1.5rem;flex-shrink:0;margin-top:0.1rem;">{icon}</div>'
        f'<div>'
        f'<div style="font-size:1.05rem;font-weight:700;color:{s["title_color"]};'
        f'margin-bottom:0.4rem;">{title}</div>'
        f'<div style="color:{s["text_color"]};line-height:1.65;font-size:0.9rem;">'
        f'{body}</div>'
        f'</div></div></div>'
    )


def render_status_badge(text: str, color: str = "green") -> str:
    colors = {
        "green": ("#059669", "rgba(16,185,129,0.1)", "rgba(16,185,129,0.2)"),
        "red": ("#EE5A24", "rgba(255,107,107,0.1)", "rgba(255,107,107,0.2)"),
        "yellow": ("#E67E22", "rgba(254,202,87,0.1)", "rgba(254,202,87,0.2)"),
        "blue": ("#2E86DE", "rgba(84,160,255,0.1)", "rgba(84,160,255,0.2)"),
        "purple": ("#6C5CE7", "rgba(108,92,231,0.1)", "rgba(108,92,231,0.2)"),
    }
    text_c, bg_c, border_c = colors.get(color, colors["green"])
    return (
        f'<span style="display:inline-block;padding:0.25rem 0.75rem;border-radius:999px;'
        f'font-size:0.75rem;font-weight:700;color:{text_c};background:{bg_c};'
        f'border:1px solid {border_c};">{text}</span>'
    )


def get_plotly_theme() -> dict:
    return {
        "layout": {
            "font": {
                "family": "Inter, -apple-system, sans-serif",
                "color": "#2D3436",
                "size": 12,
            },
            "paper_bgcolor": "rgba(0,0,0,0)",
            "plot_bgcolor": "rgba(245,247,255,0.5)",
            "colorway": [
                "#6C5CE7", "#00D2D3", "#FECA57", "#54A0FF",
                "#FF6B6B", "#FD79A8", "#10b981", "#A29BFE",
            ],
            "xaxis": {
                "gridcolor": "rgba(108,92,231,0.06)",
                "zerolinecolor": "rgba(108,92,231,0.1)",
                "gridwidth": 1,
            },
            "yaxis": {
                "gridcolor": "rgba(108,92,231,0.06)",
                "zerolinecolor": "rgba(108,92,231,0.1)",
                "gridwidth": 1,
            },
            "title": {
                "font": {"size": 15, "weight": 700, "color": "#2D3436"},
            },
            "margin": {"t": 48, "b": 40, "l": 48, "r": 24},
            "hoverlabel": {
                "bgcolor": "#2D3436",
                "font_color": "#F5F7FF",
                "font_size": 12,
                "font_family": "Inter, sans-serif",
                "bordercolor": "rgba(255,255,255,0.1)",
            },
        }
    }


def inject_styles() -> None:
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def inject_splash_styles() -> None:
    st.markdown(SPLASH_CSS, unsafe_allow_html=True)
