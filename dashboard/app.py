"""
Smart Predict AI — Dashboard Streamlit (mono-fichier).

Dashboard SaaS moderne avec :
- Page d'accueil splash animee (particules, gradients)
- 6 pages metier (vue d'ensemble, stock, predictions, emplacements, commandes, robot)
- Design inspire de Shine (violet, turquoise, jaune)

Lancer le dashboard depuis la racine du projet :
    streamlit run dashboard/app.py
"""

from __future__ import annotations

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from datetime import date

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from config.settings import settings
from dashboard.styles import (
    get_plotly_theme,
    inject_splash_styles,
    inject_styles,
    render_info_banner,
    render_kpi_card,
    render_page_header,
    render_section_header,
    render_splash_screen,
)
from helpers.data_manager import DataManager
from prediction.prediction_engine import PredictionEngine
from robot_serveur.api_client import RobotClient


# ============================================================
# Initialisation du state pour le splash screen
# ============================================================

if "splash_shown" not in st.session_state:
    st.session_state["splash_shown"] = False


# ============================================================
# Configuration generale de la page
# ============================================================

st.set_page_config(
    page_title=settings.app_name,
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# SPLASH SCREEN (page d'accueil)
# ============================================================

if not st.session_state["splash_shown"]:
    inject_splash_styles()

    SPLASH_CONFIG = {
        "project_name": "Smart Predict AI",
        "subtitle": "Systeme intelligent de gestion d'entrepot",
        "tagline": "IA Predictive · Automatisation · Optimisation",
        "team_members": [
            "Ali EL KOURRI",
            "Ahmed Amine HADRI",
            "Hatim EL GAOUTI",
            "Able SAME",
            "Mariam KRISSE",
        ],
        "supervisor": "M. JEBRANE Aissam",
        "school": "Ecole Centrale Casablanca",
        "project_code": "PLBD 20",
        "logo_emoji": "🌿",
    }

    st.markdown(
        render_splash_screen(**SPLASH_CONFIG),
        unsafe_allow_html=True,
    )

    spacer1, btn_col, spacer2 = st.columns([2, 1, 2])
    with btn_col:
        if st.button("🚀 Commencer", type="primary", use_container_width=True):
            st.session_state["splash_shown"] = True
            st.rerun()

    st.stop()


# ============================================================
# DASHBOARD NORMAL
# ============================================================

inject_styles()

PLOTLY_THEME = get_plotly_theme()


@st.cache_resource
def get_data_manager() -> DataManager:
    return DataManager(data_dir=settings.data_dir)


@st.cache_resource
def get_prediction_engine() -> PredictionEngine:
    return PredictionEngine(models_dir=settings.models_dir)


def format_number(value: float, suffix: str = "") -> str:
    if value >= 1_000_000:
        return f"{value/1_000_000:.1f}M{suffix}"
    if value >= 1_000:
        return f"{value/1_000:.1f}k{suffix}"
    return f"{int(value)}{suffix}"


def apply_plotly_theme(fig: go.Figure) -> go.Figure:
    fig.update_layout(**PLOTLY_THEME["layout"])
    return fig


# ============================================================
# Chargement initial des donnees
# ============================================================

dm = get_data_manager()
engine = get_prediction_engine()

try:
    stock_df = dm.read_stock()
    commandes_df = dm.read_commandes()
    fournisseurs_df = dm.read_fournisseurs()
    historique_df = dm.read_historique()
except Exception as e:
    st.error(f"Erreur de chargement des donnees : {e}")
    st.info(
        "Si les CSV n'existent pas, lance d'abord :\n\n"
        "```\npython -m helpers.generate_data\n```"
    )
    st.stop()

if stock_df.empty:
    st.warning(
        "Aucune donnee disponible. Genere les donnees : `python -m helpers.generate_data`"
    )
    st.stop()


# ============================================================
# Sidebar
# ============================================================

with st.sidebar:
    st.markdown(
        '<div style="text-align:center;padding:1.5rem 0 0.5rem 0;">'
        '<div style="font-size:2.75rem;margin-bottom:0.75rem;">🌿</div>'
        '<h1 style="margin:0 0 0.25rem 0;font-size:1.5rem !important;'
        'color:#6C5CE7 !important;-webkit-text-fill-color:#6C5CE7 !important;">'
        'Smart Predict</h1>'
        '<div style="font-size:0.65rem;color:#B2BEC3 !important;letter-spacing:0.2em;'
        'text-transform:uppercase;font-weight:600;">Entrepot Intelligent</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div style="margin:1rem 0;height:1px;'
        'background:linear-gradient(90deg,transparent,rgba(108,92,231,0.1),transparent);"></div>',
        unsafe_allow_html=True,
    )

    page = st.radio(
        "Navigation",
        options=[
            "🏠 Vue d'ensemble",
            "📦 Stock",
            "📈 Predictions",
            "📍 Emplacements",
            "🚚 Commandes",
            "🤖 Robot",
        ],
        label_visibility="collapsed",
    )

    st.markdown(
        '<div style="margin:1rem 0;height:1px;'
        'background:linear-gradient(90deg,transparent,rgba(108,92,231,0.1),transparent);"></div>',
        unsafe_allow_html=True,
    )

    if st.button("← Retour a l'accueil", use_container_width=True):
        st.session_state["splash_shown"] = False
        st.rerun()

    st.markdown(
        f'<div style="padding:1rem 1.25rem;background:rgba(108,92,231,0.04);'
        f'border-radius:1rem;border:1px solid rgba(108,92,231,0.08);margin-top:1.25rem;">'
        f'<div style="font-size:0.6rem;color:#B2BEC3 !important;letter-spacing:0.2em;'
        f'text-transform:uppercase;font-weight:700;margin-bottom:0.4rem;">VERSION</div>'
        f'<div style="font-weight:800;font-size:1rem;color:#6C5CE7 !important;'
        f'-webkit-text-fill-color:#6C5CE7 !important;">v{settings.app_version}</div>'
        f'<div style="font-size:0.7rem;color:#B2BEC3 !important;margin-top:0.75rem;'
        f'font-weight:600;">PLBD 20 · ECC</div></div>',
        unsafe_allow_html=True,
    )


# ============================================================
# PAGE 1 : Vue d'ensemble
# ============================================================

def render_overview() -> None:
    st.markdown(
        render_page_header("Vue d'ensemble", "Pilotage en temps reel de votre entrepot intelligent"),
        unsafe_allow_html=True,
    )

    low_stock = dm.get_low_stock_products()
    total_units = stock_df["quantity"].sum() if not stock_df.empty else 0
    pending_orders = (
        (commandes_df["status"] == "pending").sum() if not commandes_df.empty else 0
    )

    col1, col2, col3, col4 = st.columns(4, gap="medium")

    with col1:
        st.markdown(
            render_kpi_card("📦", "Produits references", str(len(stock_df)),
                sublabel=f"{stock_df['category'].nunique()} categories", gradient="main"),
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            render_kpi_card("📊", "Unites en stock", format_number(total_units),
                sublabel="Tous produits confondus", gradient="success"),
            unsafe_allow_html=True,
        )
    with col3:
        gradient_alert = "danger" if len(low_stock) > 0 else "success"
        st.markdown(
            render_kpi_card("⚠️", "Alertes stock", str(len(low_stock)),
                sublabel="Produits sous le seuil", gradient=gradient_alert),
            unsafe_allow_html=True,
        )
    with col4:
        st.markdown(
            render_kpi_card("🚚", "Commandes ouvertes", str(int(pending_orders)),
                sublabel="En attente de livraison", gradient="warning"),
            unsafe_allow_html=True,
        )

    st.markdown(
        render_section_header("🚨", "Alertes stock", "Produits necessitant un reapprovisionnement"),
        unsafe_allow_html=True,
    )

    if low_stock.empty:
        st.markdown(
            render_info_banner("✅", "Stock sain",
                "Aucun produit sous le seuil minimum. Tous les niveaux sont nominaux.",
                style="success"),
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            render_info_banner("🔔", f"{len(low_stock)} produit(s) a reapprovisionner",
                "Les produits ci-dessous ont atteint un niveau critique.", style="danger"),
            unsafe_allow_html=True,
        )
        display_df = low_stock[
            ["product_id", "name", "category", "quantity", "min_threshold", "location", "color"]
        ].copy()
        display_df["deficit"] = display_df["min_threshold"] - display_df["quantity"]
        display_df = display_df.sort_values("deficit", ascending=False)
        st.dataframe(display_df, use_container_width=True, hide_index=True)

    st.markdown(
        render_section_header("📊", "Analyse par categorie", "Repartition du stock"),
        unsafe_allow_html=True,
    )

    col_left, col_right = st.columns(2, gap="medium")

    with col_left:
        cat_counts = stock_df.groupby("category").size().reset_index(name="count")
        fig_pie = px.pie(cat_counts, values="count", names="category",
                         title="Nombre de produits", hole=0.6)
        fig_pie.update_traces(textposition="outside", textinfo="percent+label",
                              marker=dict(line=dict(color="white", width=2)),
                              pull=[0.03] * len(cat_counts))
        fig_pie = apply_plotly_theme(fig_pie)
        fig_pie.update_layout(height=420, showlegend=False)
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_right:
        cat_qty = stock_df.groupby("category")["quantity"].sum().reset_index()
        cat_qty = cat_qty.sort_values("quantity", ascending=True)
        fig_bar = px.bar(cat_qty, x="quantity", y="category", orientation="h",
                         title="Volume total par categorie", color="quantity",
                         color_continuous_scale=[[0, "#A29BFE"], [1, "#6C5CE7"]])
        fig_bar = apply_plotly_theme(fig_bar)
        fig_bar.update_layout(height=420, showlegend=False, coloraxis_showscale=False,
                              xaxis_title="Unites", yaxis_title="")
        fig_bar.update_traces(marker_line_width=0, marker_cornerradius=6)
        st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown(
        render_section_header("📈", "Tendance globale", "Evolution de la demande"),
        unsafe_allow_html=True,
    )

    if historique_df.empty:
        st.info("Aucun historique de demande disponible.")
    else:
        daily = historique_df.groupby("date")["quantity"].sum().reset_index().sort_values("date")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=daily["date"], y=daily["quantity"], mode="lines",
            fill="tozeroy", fillcolor="rgba(108,92,231,0.08)",
            line=dict(color="#6C5CE7", width=2.5, shape="spline"), name="Demande"))
        fig = apply_plotly_theme(fig)
        fig.update_layout(title="Demande journaliere totale", xaxis_title="Date",
                          yaxis_title="Unites", height=420, hovermode="x unified", showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

        last_7 = daily.tail(7)
        avg_last = last_7["quantity"].mean()
        avg_total = daily["quantity"].mean()
        delta = avg_last - avg_total
        delta_color = "#10b981" if delta >= 0 else "#FF6B6B"
        delta_icon = "📈" if delta >= 0 else "📉"
        st.markdown(
            render_info_banner(delta_icon, "Performance recente",
                f"Moyenne 7 jours : <strong style='color:#6C5CE7;'>{avg_last:.0f} unites/jour</strong><br>"
                f"Ecart a la moyenne globale : <strong style='color:{delta_color};'>{delta:+.0f}</strong>",
                style="success" if delta >= 0 else "warning"),
            unsafe_allow_html=True,
        )


# ============================================================
# PAGE 2 : Stock
# ============================================================

def render_stock() -> None:
    st.markdown(
        render_page_header("Gestion du stock", "Inventaire en temps reel de l'entrepot"),
        unsafe_allow_html=True,
    )

    with st.expander("🔍 Filtres avances", expanded=True):
        col1, col2, col3 = st.columns(3, gap="medium")
        with col1:
            categories = sorted(stock_df["category"].unique())
            selected_cats = st.multiselect("Categories", categories, default=categories)
        with col2:
            show_low_only = st.checkbox("Seulement produits sous seuil")
        with col3:
            search = st.text_input("Rechercher", placeholder="Nom ou ID...")

    filtered = stock_df[stock_df["category"].isin(selected_cats)].copy()
    if show_low_only:
        filtered = filtered[filtered["quantity"] < filtered["min_threshold"]]
    if search:
        mask = (filtered["name"].str.contains(search, case=False, na=False)
                | filtered["product_id"].str.contains(search, case=False, na=False))
        filtered = filtered[mask]

    col1, col2, col3 = st.columns(3, gap="medium")
    with col1:
        st.markdown(render_kpi_card("📋", "Produits affiches", str(len(filtered)),
                    gradient="main"), unsafe_allow_html=True)
    with col2:
        st.markdown(render_kpi_card("📦", "Unites totales",
                    format_number(int(filtered["quantity"].sum())),
                    gradient="success"), unsafe_allow_html=True)
    with col3:
        n_low = int((filtered["quantity"] < filtered["min_threshold"]).sum())
        st.markdown(render_kpi_card("⚠️", "Sous seuil", str(n_low),
                    gradient="danger" if n_low > 0 else "success"), unsafe_allow_html=True)

    st.markdown(render_section_header("📋", "Liste des produits", f"{len(filtered)} resultats"),
                unsafe_allow_html=True)
    display = filtered.copy()
    display["statut"] = display.apply(
        lambda r: "🔴 Critique" if r["quantity"] < r["min_threshold"]
        else "🟢 OK" if r["quantity"] >= r["min_threshold"] * 2
        else "🟡 Attention", axis=1)
    st.dataframe(
        display[["product_id", "name", "category", "quantity",
                 "min_threshold", "location", "color", "statut"]],
        use_container_width=True, hide_index=True)

    st.markdown(render_section_header("✏️", "Mise a jour du stock", "Ajouter ou retirer des unites"),
                unsafe_allow_html=True)
    with st.form("update_stock_form"):
        col1, col2, col3 = st.columns([2, 1, 1], gap="medium")
        with col1:
            product_id = st.selectbox("Produit", options=stock_df["product_id"].tolist(),
                format_func=lambda pid: f"{pid} - {stock_df.loc[stock_df['product_id'] == pid, 'name'].iloc[0]}")
        with col2:
            delta = st.number_input("Variation", value=0, step=1)
        with col3:
            st.write("")
            st.write("")
            submitted = st.form_submit_button("Appliquer", type="primary")
        if submitted and delta != 0:
            try:
                new_qty = dm.update_stock_quantity(product_id, delta)
                st.success(f"✅ Stock {product_id} mis a jour : {new_qty}")
                st.rerun()
            except ValueError as e:
                st.error(f"❌ {e}")

    st.markdown(render_section_header("📊", "Visualisation", "Explorer la repartition du stock"),
                unsafe_allow_html=True)
    view_mode = st.radio("Type de visualisation",
        ["Quantite par produit", "Quantite par categorie", "Top produits"],
        horizontal=True, label_visibility="collapsed")

    if view_mode == "Quantite par produit":
        fig = px.bar(filtered.sort_values("quantity", ascending=False),
                     x="product_id", y="quantity", color="color", title="Quantite en stock par produit")
    elif view_mode == "Quantite par categorie":
        cat_data = filtered.groupby("category")["quantity"].sum().reset_index()
        fig = px.bar(cat_data, x="category", y="quantity",
                     title="Quantite totale par categorie", color="category")
    else:
        fig = px.bar(filtered.sort_values("quantity", ascending=True),
                     x="quantity", y="name", orientation="h",
                     title="Produits par stock", color="color")
        fig.update_layout(yaxis={"categoryorder": "total ascending"})

    fig = apply_plotly_theme(fig)
    fig.update_traces(marker_line_width=0, marker_cornerradius=5)
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)


# ============================================================
# PAGE 3 : Predictions
# ============================================================

def render_predictions() -> None:
    st.markdown(
        render_page_header("Previsions de demande", "IA predictive avec auto-selection du meilleur modele"),
        unsafe_allow_html=True,
    )

    if historique_df.empty:
        st.warning("Aucun historique de demande disponible.")
        return

    st.markdown(render_section_header("⚙️", "Configuration",
        "Selectionne un produit et un horizon de prediction"), unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1], gap="medium")
    with col1:
        product_id = st.selectbox("Selectionne un produit",
            options=stock_df["product_id"].tolist(),
            format_func=lambda pid: f"{pid} - {stock_df.loc[stock_df['product_id'] == pid, 'name'].iloc[0]} ({stock_df.loc[stock_df['product_id'] == pid, 'color'].iloc[0]})")
    with col2:
        horizon = st.slider("Horizon (jours)", min_value=1, max_value=30,
                             value=settings.default_forecast_horizon)

    if st.button("🚀 Lancer la prediction", type="primary"):
        with st.spinner("🧠 Analyse des patterns historiques..."):
            try:
                predictions = engine.predict(product_id=product_id, n_days=horizon,
                                             history_csv=settings.historique_csv)
                model_info = engine.get_model_info(product_id)
                evaluation = engine.evaluate_model(product_id=product_id,
                    history_csv=settings.historique_csv, test_ratio=0.2)
                st.session_state["last_predictions"] = predictions
                st.session_state["last_product"] = product_id
                st.session_state["last_model_info"] = model_info
                st.session_state["last_evaluation"] = evaluation
                st.success("✅ Prediction terminee avec succes")
            except Exception as e:
                st.error(f"❌ Erreur : {e}")
                return

    if "last_predictions" in st.session_state:
        predictions = st.session_state["last_predictions"]
        last_product = st.session_state["last_product"]
        model_info = st.session_state.get("last_model_info", {})
        evaluation = st.session_state.get("last_evaluation", {})

        if model_info:
            mc = model_info['color']
            st.markdown(
                f'<div style="background:white;border-radius:1.5rem;'
                f'border:1px solid rgba(108,92,231,0.06);'
                f'box-shadow:0 2px 8px rgba(108,92,231,0.04),0 8px 24px rgba(108,92,231,0.03);'
                f'padding:1.75rem;margin-bottom:1.5rem;">'
                f'<div style="display:flex;align-items:center;gap:1.25rem;">'
                f'<div style="font-size:2.5rem;line-height:1;background:rgba(108,92,231,0.06);'
                f'padding:1rem;border-radius:1rem;border:1px solid rgba(108,92,231,0.1);">'
                f'{model_info["icon"]}</div>'
                f'<div style="flex:1;">'
                f'<div style="font-size:0.65rem;color:#B2BEC3;letter-spacing:0.15em;'
                f'text-transform:uppercase;font-weight:700;margin-bottom:0.35rem;">'
                f'Algorithme selectionne automatiquement</div>'
                f'<div style="font-size:1.5rem;font-weight:800;color:{mc};'
                f'margin-bottom:0.4rem;letter-spacing:-0.02em;">{model_info["model_name"]}</div>'
                f'<div style="font-size:0.9rem;color:#636E72;line-height:1.6;">'
                f'{model_info["description"]}</div>'
                f'</div></div></div>',
                unsafe_allow_html=True,
            )

        if evaluation:
            st.markdown(render_section_header("🎯", "Performance du modele",
                f"Evaluation sur {evaluation['n_test']} jours"), unsafe_allow_html=True)

            col1, col2, col3, col4 = st.columns(4, gap="medium")
            with col1:
                score = evaluation["reliability_score"]
                grad = "success" if score >= 80 else "main" if score >= 60 else "warning" if score >= 40 else "danger"
                label_extra = "Excellent" if score >= 80 else "Bon" if score >= 60 else "Moyen" if score >= 40 else "A ameliorer"
                st.markdown(render_kpi_card("🏆", "Score", f"{score:.0f}/100",
                    sublabel=label_extra, gradient=grad), unsafe_allow_html=True)
            with col2:
                st.markdown(render_kpi_card("📊", "MAPE", f"{evaluation['mape']:.1f}%",
                    gradient="purple"), unsafe_allow_html=True)
            with col3:
                st.markdown(render_kpi_card("📏", "MAE", f"{evaluation['mae']:.1f} u.",
                    gradient="main"), unsafe_allow_html=True)
            with col4:
                st.markdown(render_kpi_card("📐", "RMSE", f"{evaluation['rmse']:.1f} u.",
                    gradient="warning"), unsafe_allow_html=True)

            st.markdown(render_section_header("🔬", "Validation : predit vs reel",
                f"Comparaison sur {evaluation['n_test']} jours hors entrainement"),
                unsafe_allow_html=True)

            fig_eval = go.Figure()
            fig_eval.add_trace(go.Scatter(x=evaluation["test_dates"], y=evaluation["actual_values"],
                mode="lines+markers", name="Demande reelle",
                line=dict(color="#54A0FF", width=2.5, shape="spline"), marker=dict(size=7),
                fill="tozeroy", fillcolor="rgba(84,160,255,0.06)"))
            fig_eval.add_trace(go.Scatter(x=evaluation["test_dates"], y=evaluation["predicted_values"],
                mode="lines+markers", name="Prediction",
                line=dict(color="#6C5CE7", width=2.5, dash="dash", shape="spline"),
                marker=dict(size=7, symbol="diamond")))
            fig_eval = apply_plotly_theme(fig_eval)
            fig_eval.update_layout(xaxis_title="Date", yaxis_title="Quantite", height=420,
                hovermode="x unified",
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
            st.plotly_chart(fig_eval, use_container_width=True)

            st.markdown(render_info_banner("📐", "Methodologie",
                f"Entraine sur <strong>{evaluation['n_train']} jours</strong>, "
                f"evalue sur <strong>{evaluation['n_test']} jours</strong> "
                f"({int(evaluation['test_ratio']*100)}%).<br>"
                f"<strong>MAPE</strong> ({evaluation['mape']:.1f}%) · "
                f"<strong>MAE</strong> ({evaluation['mae']:.1f} u.) · "
                f"<strong>RMSE</strong> ({evaluation['rmse']:.1f} u.)",
                style="info"), unsafe_allow_html=True)

        st.markdown(render_section_header("📊", f"Previsions futures pour {last_product}",
            "Projection sur les jours a venir"), unsafe_allow_html=True)

        hist = historique_df[historique_df["product_id"] == last_product].copy()
        hist = hist.groupby("date")["quantity"].sum().reset_index().sort_values("date").tail(60)

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=hist["date"], y=hist["quantity"], mode="lines",
            name="Historique", line=dict(color="#54A0FF", width=2, shape="spline"),
            fill="tozeroy", fillcolor="rgba(84,160,255,0.06)"))
        fig.add_trace(go.Scatter(x=predictions.index, y=predictions.values,
            mode="lines+markers", name="Prediction IA",
            line=dict(color="#6C5CE7", width=3, dash="dash", shape="spline"),
            marker=dict(size=9, line=dict(color="white", width=2))))
        fig = apply_plotly_theme(fig)
        fig.update_layout(title=f"Evolution + prevision sur {len(predictions)} jours",
            xaxis_title="Date", yaxis_title="Quantite", height=480, hovermode="x unified",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
        st.plotly_chart(fig, use_container_width=True)

        total = int(predictions.sum())
        avg = float(predictions.mean())
        max_day = predictions.idxmax().strftime("%Y-%m-%d")
        max_val = int(predictions.max())

        col1, col2, col3 = st.columns(3, gap="medium")
        with col1:
            st.markdown(render_kpi_card("📈", "Demande totale", f"{total} u.",
                gradient="main"), unsafe_allow_html=True)
        with col2:
            st.markdown(render_kpi_card("📊", "Moyenne/jour", f"{avg:.0f} u.",
                gradient="purple"), unsafe_allow_html=True)
        with col3:
            st.markdown(render_kpi_card("🎯", "Pic prevu", f"{max_val} u.",
                sublabel=max_day, gradient="warning"), unsafe_allow_html=True)

        col1, col2 = st.columns(2, gap="medium")
        with col1:
            pred_df = predictions.reset_index()
            pred_df.columns = ["Date", "Demande prevue"]
            pred_df["Demande prevue"] = pred_df["Demande prevue"].round(0).astype(int)
            st.dataframe(pred_df, use_container_width=True, hide_index=True)
        with col2:
            current_stock = int(stock_df.loc[stock_df["product_id"] == last_product, "quantity"].iloc[0])
            if total > current_stock:
                st.markdown(render_info_banner("⚠️", "Reapprovisionnement requis",
                    f"Stock : <strong>{current_stock} u.</strong><br>"
                    f"Demande : <strong>{total} u.</strong><br>"
                    f"Deficit : <strong>{total - current_stock} u.</strong>",
                    style="danger"), unsafe_allow_html=True)
            else:
                st.markdown(render_info_banner("✅", "Stock suffisant",
                    f"Stock : <strong>{current_stock} u.</strong><br>"
                    f"Demande : <strong>{total} u.</strong><br>"
                    f"Marge : <strong>{current_stock - total} u.</strong>",
                    style="success"), unsafe_allow_html=True)

    st.markdown(render_section_header("🔬", "Comparaison multi-produits",
        "Compare jusqu'a 4 produits"), unsafe_allow_html=True)
    selected_products = st.multiselect("Selectionne des produits",
        options=stock_df["product_id"].tolist(), max_selections=4)

    if selected_products and st.button("Comparer", key="compare_btn"):
        with st.spinner("Calcul..."):
            fig_compare = go.Figure()
            for pid in selected_products:
                try:
                    preds = engine.predict(product_id=pid, n_days=horizon,
                                           history_csv=settings.historique_csv)
                    fig_compare.add_trace(go.Scatter(x=preds.index, y=preds.values,
                        mode="lines+markers", name=pid,
                        line=dict(width=2.5, shape="spline"), marker=dict(size=7)))
                except Exception as e:
                    st.warning(f"Echec {pid} : {e}")
            fig_compare = apply_plotly_theme(fig_compare)
            fig_compare.update_layout(title="Comparaison", xaxis_title="Date",
                yaxis_title="Demande prevue", height=500, hovermode="x unified")
            st.plotly_chart(fig_compare, use_container_width=True)


# ============================================================
# PAGE 4 : Commandes
# ============================================================

def render_commandes() -> None:
    st.markdown(render_page_header("Commandes fournisseurs", "Suivi et gestion des commandes"),
                unsafe_allow_html=True)

    if commandes_df.empty:
        st.warning("Aucune commande a afficher.")
        return

    cmd_df = commandes_df.copy()
    cmd_df["order_date"] = pd.to_datetime(cmd_df["order_date"])

    col1, col2, col3, col4 = st.columns(4, gap="medium")
    with col1:
        st.markdown(render_kpi_card("📋", "Total", str(len(cmd_df)), gradient="main"),
                    unsafe_allow_html=True)
    with col2:
        st.markdown(render_kpi_card("⏳", "En attente",
            str(int((cmd_df["status"] == "pending").sum())), gradient="warning"),
            unsafe_allow_html=True)
    with col3:
        st.markdown(render_kpi_card("🚚", "En livraison",
            str(int((cmd_df["status"] == "shipped").sum())), gradient="blue"),
            unsafe_allow_html=True)
    with col4:
        st.markdown(render_kpi_card("✅", "Livrees",
            str(int((cmd_df["status"] == "delivered").sum())), gradient="success"),
            unsafe_allow_html=True)

    st.markdown(render_section_header("📋", "Liste des commandes",
        f"{len(cmd_df)} resultats"), unsafe_allow_html=True)
    display = cmd_df.merge(
        fournisseurs_df[["supplier_id", "name"]].rename(columns={"name": "fournisseur"}),
        on="supplier_id", how="left",
    ).merge(
        stock_df[["product_id", "name", "color"]].rename(columns={"name": "produit"}),
        on="product_id", how="left",
    )
    st.dataframe(
        display[["commande_id", "order_date", "product_id", "produit", "color",
                 "quantity", "supplier_id", "fournisseur", "status"]]
        .sort_values("order_date", ascending=False),
        use_container_width=True, hide_index=True)

    st.markdown(render_section_header("➕", "Nouvelle commande",
        "Passer une commande chez un fournisseur"), unsafe_allow_html=True)
    with st.form("new_commande_form"):
        col1, col2 = st.columns(2, gap="medium")
        with col1:
            new_product = st.selectbox("Produit", options=stock_df["product_id"].tolist(),
                format_func=lambda pid: f"{pid} - {stock_df.loc[stock_df['product_id'] == pid, 'name'].iloc[0]}")
            new_quantity = st.number_input("Quantite", min_value=1, value=50, step=1)
        with col2:
            new_supplier = st.selectbox("Fournisseur", options=fournisseurs_df["supplier_id"].tolist(),
                format_func=lambda sid: f"{sid} - {fournisseurs_df.loc[fournisseurs_df['supplier_id'] == sid, 'name'].iloc[0]}")
            new_status = st.selectbox("Statut initial", ["pending", "shipped"])
        submit = st.form_submit_button("Creer la commande", type="primary")
        if submit:
            try:
                cmd_id = dm.add_commande(product_id=new_product, quantity=int(new_quantity),
                    supplier_id=new_supplier, status=new_status)
                st.success(f"✅ Commande {cmd_id} creee")
                st.rerun()
            except Exception as e:
                st.error(f"❌ {e}")


# ============================================================
# PAGE 5 : Robot
# ============================================================

@st.cache_resource
def get_robot_client() -> RobotClient:
    return RobotClient(host=settings.pi_host, port=settings.pi_port)


def render_robot() -> None:
    st.markdown(render_page_header("Robot d'entrepot", "Pilotage du robot autonome"),
                unsafe_allow_html=True)

    robot = get_robot_client()
    connected = robot.is_connected()

    if connected:
        st.markdown(render_info_banner("🟢", "Robot connecte",
            f"Connecte a <strong>{settings.pi_host}:{settings.pi_port}</strong>",
            style="success"), unsafe_allow_html=True)
    else:
        st.markdown(render_info_banner("🔴", "Robot hors ligne",
            f"Impossible de joindre <strong>{settings.pi_host}:{settings.pi_port}</strong>.<br>"
            "Verifie que le serveur API tourne sur le Raspberry Pi :<br>"
            "<code>python api_server.py</code>",
            style="danger"), unsafe_allow_html=True)

    st.markdown(render_section_header("📡", "Etat du robot", "Donnees temps reel"),
                unsafe_allow_html=True)

    status = robot.status() if connected else {
        "status": "offline", "battery": "--", "position": "--",
        "mission_active": False, "distance_cm": "--",
        "last_color_detected": "--", "arm_state": "--",
        "line_sensors": {"left": 0, "center": 0, "right": 0},
    }

    stat_label = status.get("status", "offline")
    stat_map = {
        "idle": ("Inactif", "success"), "moving": ("En mouvement", "teal"),
        "turning": ("Rotation", "blue"), "mission": ("Mission active", "main"),
        "offline": ("Hors ligne", "danger"),
    }
    stat_text, stat_grad = stat_map.get(stat_label, ("Inconnu", "warning"))

    col1, col2, col3, col4 = st.columns(4, gap="medium")
    with col1:
        st.markdown(render_kpi_card("⚡", "Etat", stat_text, gradient=stat_grad),
                    unsafe_allow_html=True)
    with col2:
        dist = status.get("distance_cm", "--")
        st.markdown(render_kpi_card("📏", "Distance",
            f"{dist} cm" if isinstance(dist, (int, float)) else "--",
            sublabel="Capteur ultrason", gradient="blue"), unsafe_allow_html=True)
    with col3:
        st.markdown(render_kpi_card("🎨", "Couleur",
            status.get("last_color_detected", "--") or "--",
            sublabel="Camera", gradient="purple"), unsafe_allow_html=True)
    with col4:
        arm = status.get("arm_state", "--")
        st.markdown(render_kpi_card("🦾", "Bras",
            {"repos": "Libre", "charge": "Charge"}.get(arm, arm),
            sublabel="Etat pince", gradient="teal"), unsafe_allow_html=True)

    sensors = status.get("line_sensors", {})
    sl, sc, sr = sensors.get("left", 0), sensors.get("center", 0), sensors.get("right", 0)
    st.markdown(
        f'<div style="display:flex;gap:1rem;justify-content:center;margin:1rem 0;">'
        f'<div style="text-align:center;padding:0.75rem 1.5rem;border-radius:1rem;'
        f'background:{"#10b981" if sl else "#FF6B6B"};color:white;font-weight:700;">G {"ON" if sl else "OFF"}</div>'
        f'<div style="text-align:center;padding:0.75rem 1.5rem;border-radius:1rem;'
        f'background:{"#10b981" if sc else "#FF6B6B"};color:white;font-weight:700;">C {"ON" if sc else "OFF"}</div>'
        f'<div style="text-align:center;padding:0.75rem 1.5rem;border-radius:1rem;'
        f'background:{"#10b981" if sr else "#FF6B6B"};color:white;font-weight:700;">D {"ON" if sr else "OFF"}</div>'
        f'</div>', unsafe_allow_html=True)

    st.markdown(render_section_header("🎮", "Controle manuel", "Pilotage direct"),
                unsafe_allow_html=True)

    _, col_center, _ = st.columns([1, 2, 1], gap="medium")
    with col_center:
        _, c2, _ = st.columns(3)
        with c2:
            if st.button("⬆️ Avancer", use_container_width=True, disabled=not connected):
                robot.forward(); st.toast("Avance")
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("⬅️ Gauche", use_container_width=True, disabled=not connected):
                robot.left(); st.toast("Gauche")
        with c2:
            if st.button("⏹️ Stop", type="primary", use_container_width=True, disabled=not connected):
                robot.stop(); st.toast("Stop")
        with c3:
            if st.button("➡️ Droite", use_container_width=True, disabled=not connected):
                robot.right(); st.toast("Droite")
        _, c2, _ = st.columns(3)
        with c2:
            if st.button("⬇️ Reculer", use_container_width=True, disabled=not connected):
                robot.backward(); st.toast("Recule")

    st.markdown(render_section_header("🦾", "Bras robotique", "Controle de la pince"),
                unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4, gap="medium")
    with col1:
        if st.button("📦 Prendre", use_container_width=True, disabled=not connected):
            with st.spinner("Prise..."): robot.pick()
            st.toast("Objet saisi")
    with col2:
        if st.button("📤 Deposer", use_container_width=True, disabled=not connected):
            with st.spinner("Depot..."): robot.drop()
            st.toast("Objet depose")
    with col3:
        if st.button("💡 LED ON", use_container_width=True, disabled=not connected):
            robot.led_on()
    with col4:
        if st.button("🔇 LED OFF", use_container_width=True, disabled=not connected):
            robot.led_off()

    with st.expander("⚙️ Servo manuel"):
        sc1, sc2, sc3 = st.columns([1, 2, 1])
        with sc1:
            servo_ch = st.selectbox("Canal", options=[0, 1, 2, 3, 4], index=0)
        with sc2:
            servo_angle = st.slider("Angle", 0, 180, 90)
        with sc3:
            st.write(""); st.write("")
            if st.button("Appliquer", disabled=not connected):
                robot.servo(servo_ch, servo_angle)

    st.markdown(render_section_header("🚀", "Mission autonome",
        "Lancer une mission de pick & drop par couleur"), unsafe_allow_html=True)

    couleurs = sorted(stock_df["color"].dropna().unique().tolist())
    mission_active = status.get("mission_active", False)

    col1, col2 = st.columns(2, gap="medium")
    with col1:
        pick_color = st.selectbox("Couleur a PRENDRE", couleurs, index=0,
                                  disabled=mission_active or not connected)
    with col2:
        drop_color = st.selectbox("Couleur de DEPOT", couleurs,
                                  index=min(1, len(couleurs)-1),
                                  disabled=mission_active or not connected)

    col1, col2 = st.columns(2, gap="medium")
    with col1:
        if not mission_active:
            if st.button("🚀 Lancer la mission", type="primary",
                         use_container_width=True, disabled=not connected):
                result = robot.start_mission(pick_color, drop_color)
                if result.get("ok"):
                    st.toast(f"Mission : {pick_color} → {drop_color}")
                    st.rerun()
                else:
                    st.error(result.get("error", "Erreur"))
        else:
            st.markdown(render_info_banner("🟢", "Mission en cours",
                f"Prendre : <strong>{status.get('mission_color_pick', '?')}</strong> · "
                f"Deposer : <strong>{status.get('mission_color_drop', '?')}</strong>",
                style="success"), unsafe_allow_html=True)
    with col2:
        if mission_active:
            if st.button("🛑 Arreter la mission", type="primary", use_container_width=True):
                robot.stop_mission(); st.toast("Mission arretee"); st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 Rafraichir l'etat", use_container_width=True):
        st.rerun()


# ============================================================
# PAGE 6 : Emplacements optimises
# ============================================================

def render_emplacements() -> None:
    st.markdown(render_page_header("Emplacements optimises",
        "Proposition de placement basee sur la demande prevue"), unsafe_allow_html=True)

    st.markdown(render_info_banner("💡", "Principe",
        "Les produits les plus demandes sont places <strong>au plus proche du point "
        "d'expedition (A1-R1)</strong>. Cela reduit le temps de picking et les deplacements du robot.",
        style="info"), unsafe_allow_html=True)

    st.markdown(render_section_header("⚙️", "Configuration", "Parametres"), unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="medium")
    with col1:
        horizon_empl = st.slider("Horizon de prediction (jours)", 1, 30, 7, key="horizon_empl")
    with col2:
        nb_allees = st.number_input("Nombre d'allees", 1, 10, 5)
        nb_rangees = st.number_input("Nombre de rangees", 1, 10, 6)

    if st.button("🚀 Generer les emplacements optimises", type="primary"):
        with st.spinner("Calcul des previsions pour tous les produits..."):
            demandes = {}
            for pid in stock_df["product_id"].tolist():
                try:
                    preds = engine.predict(product_id=pid, n_days=horizon_empl,
                                           history_csv=settings.historique_csv)
                    demandes[pid] = int(preds.sum())
                except Exception:
                    demandes[pid] = 0

            produits_tries = sorted(demandes.items(), key=lambda x: x[1], reverse=True)
            emplacements = [f"A{a}-R{r}" for a in range(1, nb_allees+1) for r in range(1, nb_rangees+1)]

            resultats = []
            for i, (pid, dem_tot) in enumerate(produits_tries):
                row = stock_df.loc[stock_df["product_id"] == pid].iloc[0]
                nouveau = emplacements[i] if i < len(emplacements) else "Extension"
                ancien = row["location"]
                resultats.append({
                    "Rang": i + 1, "Produit": pid, "Nom": row["name"],
                    "Couleur": row.get("color", ""), "Stock": int(row["quantity"]),
                    "Demande prevue": dem_tot, "Ancien empl.": ancien,
                    "Nouvel empl.": nouveau,
                    "Statut": "✅ Inchange" if ancien == nouveau else f"🔄 {ancien} → {nouveau}",
                })

            st.session_state["emplacements_resultats"] = resultats
            st.success(f"✅ Emplacements calcules pour {len(resultats)} produits")

    if "emplacements_resultats" in st.session_state:
        resultats = st.session_state["emplacements_resultats"]
        nb_changes = sum(1 for r in resultats if "🔄" in r["Statut"])

        col1, col2, col3 = st.columns(3, gap="medium")
        with col1:
            st.markdown(render_kpi_card("📦", "Produits", str(len(resultats)),
                gradient="main"), unsafe_allow_html=True)
        with col2:
            st.markdown(render_kpi_card("🔄", "Deplacements", str(nb_changes),
                sublabel=f"{len(resultats) - nb_changes} inchanges", gradient="warning"),
                unsafe_allow_html=True)
        with col3:
            if resultats:
                st.markdown(render_kpi_card("🏆", "Plus demande", resultats[0]["Nom"],
                    sublabel=f"{resultats[0]['Demande prevue']} u.",
                    gradient="purple"), unsafe_allow_html=True)

        st.markdown(render_section_header("📋", "Plan d'emplacement",
            "Classe par demande decroissante"), unsafe_allow_html=True)
        st.dataframe(pd.DataFrame(resultats), use_container_width=True, hide_index=True)

        st.markdown(render_section_header("📊", "Demande prevue par produit", ""),
                    unsafe_allow_html=True)
        chart_df = pd.DataFrame([{"Nom": r["Nom"], "Demande": r["Demande prevue"],
            "Couleur": r["Couleur"]} for r in resultats]).sort_values("Demande", ascending=True)
        fig = px.bar(chart_df, x="Demande", y="Nom", orientation="h", color="Couleur",
                     title="Demande prevue par produit")
        fig = apply_plotly_theme(fig)
        fig.update_traces(marker_line_width=0, marker_cornerradius=5)
        fig.update_layout(height=400, xaxis_title="Demande totale (unites)", yaxis_title="")
        st.plotly_chart(fig, use_container_width=True)

        st.markdown(render_info_banner("📐", "Methodologie",
            "L'emplacement <strong>A1-R1</strong> (le plus proche de l'expedition) est "
            "attribue au produit le plus demande, etc.", style="info"), unsafe_allow_html=True)


# ============================================================
# Routeur
# ============================================================

if page == "🏠 Vue d'ensemble":
    render_overview()
elif page == "📦 Stock":
    render_stock()
elif page == "📈 Predictions":
    render_predictions()
elif page == "📍 Emplacements":
    render_emplacements()
elif page == "🚚 Commandes":
    render_commandes()
elif page == "🤖 Robot":
    render_robot()
    