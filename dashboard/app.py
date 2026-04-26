"""
Smart Predict AI — Dashboard Streamlit (mono-fichier).

Dashboard SaaS moderne avec :
- Page d'accueil splash animée (particules, gradients, glassmorphism)
- 5 pages métier (vue d'ensemble, stock, prédictions, commandes, robot)
- Design teal/vert avec animations subtiles

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
    render_kpi_card,
    render_section_header,
    render_splash_screen,
)
from helpers.data_manager import DataManager
from prediction.prediction_engine import PredictionEngine


# ============================================================
# Initialisation du state pour le splash screen
# ============================================================

if "splash_shown" not in st.session_state:
    st.session_state["splash_shown"] = False


# ============================================================
# Configuration générale de la page
# ============================================================

st.set_page_config(
    page_title=settings.app_name,
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded" if st.session_state.get("splash_shown") else "collapsed",
)


# ============================================================
# SPLASH SCREEN (page d'accueil)
# ============================================================

if not st.session_state["splash_shown"]:
    inject_splash_styles()

    # Indique le mode splash via une classe CSS au body
    st.markdown(
        '<script>document.body.classList.add("splash-mode");</script>',
        unsafe_allow_html=True,
    )

    # Configuration du splash
    SPLASH_CONFIG = {
        "project_name": "Smart Predict AI",
        "subtitle": "Système intelligent de gestion d'entrepôt",
        "tagline": "IA Prédictive · Automatisation · Optimisation",
        "team_members": [
            "Ali EL KOURRI",
            "Ahmed Amine HADRI",
            "Hatim EL GAOUTI",
            "Able SAME",
            "Mariam KRISSE",
        ],
        "supervisor": "M. JEBRANE Aissam",
        "school": "École Centrale Casablanca",
        "project_code": "PLBD 20",
        "logo_emoji": "🌿",
    }

    # Affiche le splash screen
    st.markdown(
        render_splash_screen(**SPLASH_CONFIG),
        unsafe_allow_html=True,
    )

    # Bouton "Commencer" centré
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown(
            '<div style="display: flex; justify-content: center; margin-top: -100px; position: relative; z-index: 100;">',
            unsafe_allow_html=True,
        )
        if st.button("🚀 Commencer", type="primary", use_container_width=True):
            st.session_state["splash_shown"] = True
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # Stoppe l'exécution du reste du fichier
    st.stop()


# ============================================================
# DASHBOARD NORMAL (uniquement si splash_shown == True)
# ============================================================

# Injection des styles custom
inject_styles()

PLOTLY_THEME = get_plotly_theme()


# ============================================================
# Helpers
# ============================================================

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
# Chargement initial des données
# ============================================================

dm = get_data_manager()
engine = get_prediction_engine()

try:
    stock_df = dm.read_stock()
    commandes_df = dm.read_commandes()
    fournisseurs_df = dm.read_fournisseurs()
    historique_df = dm.read_historique()
except Exception as e:
    st.error(f"Erreur de chargement des données : {e}")
    st.info(
        "Si les CSV n'existent pas, lance d'abord :\n\n"
        "```\npython -m helpers.generate_data\n```"
    )
    st.stop()

if stock_df.empty:
    st.warning(
        "Aucune donnée disponible. Génère les données : `python -m helpers.generate_data`"
    )
    st.stop()


# ============================================================
# Sidebar
# ============================================================

with st.sidebar:
    st.markdown("""
        <div style="text-align: center; padding: 1rem 0 0 0;">
            <div style="font-size: 3rem;">🌿</div>
            <h1 style="margin: 0.5rem 0 0 0;">Smart Predict</h1>
            <div style="
                font-size: 0.75rem;
                color: #94a3b8;
                letter-spacing: 0.1em;
                text-transform: uppercase;
                margin-top: 0.25rem;
            ">Entrepôt Intelligent</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    page = st.radio(
        "Navigation",
        options=[
            "🏠 Vue d'ensemble",
            "📦 Stock",
            "📈 Prédictions",
            "🚚 Commandes",
            "🤖 Robot",
        ],
        label_visibility="collapsed",
    )

    st.markdown("<hr>", unsafe_allow_html=True)

    # Bouton retour à l'accueil
    if st.button("← Retour à l'accueil", use_container_width=True):
        st.session_state["splash_shown"] = False
        st.rerun()

    # Footer sidebar
    st.markdown(f"""
        <div style="
            padding: 1rem;
            background: rgba(16, 185, 129, 0.1);
            border-radius: 0.75rem;
            border: 1px solid rgba(16, 185, 129, 0.2);
            margin-top: 1rem;
        ">
            <div style="font-size: 0.75rem; color: #94a3b8; margin-bottom: 0.25rem;">
                VERSION
            </div>
            <div style="font-weight: 600; color: #10b981;">
                v{settings.app_version}
            </div>
            <div style="
                font-size: 0.75rem;
                color: #64748b;
                margin-top: 0.75rem;
                line-height: 1.4;
            ">
                PLBD 20 · ECC
            </div>
        </div>
    """, unsafe_allow_html=True)


# ============================================================
# PAGE 1 : Vue d'ensemble
# ============================================================

def render_overview() -> None:
    st.markdown("""
        <div style="margin-bottom: 2rem;">
            <h1 style="font-size: 2.75rem; margin-bottom: 0.5rem;">
                Vue d'ensemble
            </h1>
            <p style="
                font-size: 1.125rem;
                color: #64748b;
                margin: 0;
                font-weight: 500;
            ">
                Pilotage en temps réel de votre entrepôt intelligent 🚀
            </p>
        </div>
    """, unsafe_allow_html=True)

    low_stock = dm.get_low_stock_products()
    total_units = stock_df["quantity"].sum() if not stock_df.empty else 0
    pending_orders = (
        (commandes_df["status"] == "pending").sum() if not commandes_df.empty else 0
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            render_kpi_card(
                icon="📦",
                label="Produits référencés",
                value=str(len(stock_df)),
                sublabel=f"{stock_df['category'].nunique()} catégories",
                gradient="main",
            ),
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            render_kpi_card(
                icon="📊",
                label="Unités en stock",
                value=format_number(total_units),
                sublabel="Tous produits confondus",
                gradient="success",
            ),
            unsafe_allow_html=True,
        )
    with col3:
        gradient_alert = "danger" if len(low_stock) > 0 else "success"
        st.markdown(
            render_kpi_card(
                icon="⚠️",
                label="Alertes stock",
                value=str(len(low_stock)),
                sublabel="Produits sous le seuil",
                gradient=gradient_alert,
            ),
            unsafe_allow_html=True,
        )
    with col4:
        st.markdown(
            render_kpi_card(
                icon="🚚",
                label="Commandes ouvertes",
                value=str(int(pending_orders)),
                sublabel="En attente de livraison",
                gradient="warning",
            ),
            unsafe_allow_html=True,
        )

    # Alertes stock
    st.markdown(
        render_section_header(
            "🚨", "Alertes stock", "Produits nécessitant un réapprovisionnement"
        ),
        unsafe_allow_html=True,
    )

    if low_stock.empty:
        st.success("✅ Excellent ! Aucun produit sous le seuil minimum. Stock sain.")
    else:
        st.warning(f"🔔 {len(low_stock)} produit(s) à réapprovisionner")
        display_df = low_stock[
            ["product_id", "name", "category", "quantity", "min_threshold", "location"]
        ].copy()
        display_df["déficit"] = display_df["min_threshold"] - display_df["quantity"]
        display_df = display_df.sort_values("déficit", ascending=False)
        st.dataframe(display_df, use_container_width=True, hide_index=True)

    # Catégories
    st.markdown(
        render_section_header(
            "📊", "Analyse par catégorie", "Répartition du stock dans l'entrepôt"
        ),
        unsafe_allow_html=True,
    )

    col_left, col_right = st.columns(2)

    with col_left:
        cat_counts = stock_df.groupby("category").size().reset_index(name="count")
        fig_pie = px.pie(
            cat_counts,
            values="count",
            names="category",
            title="Nombre de produits",
            hole=0.55,
        )
        fig_pie.update_traces(
            textposition="outside",
            textinfo="percent+label",
            marker=dict(line=dict(color="white", width=3)),
        )
        fig_pie = apply_plotly_theme(fig_pie)
        fig_pie.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_right:
        cat_qty = stock_df.groupby("category")["quantity"].sum().reset_index()
        cat_qty = cat_qty.sort_values("quantity", ascending=True)
        fig_bar = px.bar(
            cat_qty,
            x="quantity",
            y="category",
            orientation="h",
            title="Volume total par catégorie",
            color="quantity",
            color_continuous_scale=[[0, "#a7f3d0"], [1, "#059669"]],
        )
        fig_bar = apply_plotly_theme(fig_bar)
        fig_bar.update_layout(
            height=400,
            showlegend=False,
            coloraxis_showscale=False,
            xaxis_title="Unités",
            yaxis_title="",
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    # Tendance
    st.markdown(
        render_section_header(
            "📈", "Tendance globale", "Évolution de la demande dans le temps"
        ),
        unsafe_allow_html=True,
    )

    if historique_df.empty:
        st.info("Aucun historique de demande disponible.")
    else:
        daily = historique_df.groupby("date")["quantity"].sum().reset_index()
        daily = daily.sort_values("date")

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=daily["date"],
            y=daily["quantity"],
            mode="lines",
            fill="tozeroy",
            fillcolor="rgba(16, 185, 129, 0.1)",
            line=dict(color="#10b981", width=3),
            name="Demande quotidienne",
        ))
        fig = apply_plotly_theme(fig)
        fig.update_layout(
            title="Demande journalière totale",
            xaxis_title="Date",
            yaxis_title="Unités demandées",
            height=400,
            hovermode="x unified",
            showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True)

        last_7 = daily.tail(7)
        avg_last = last_7["quantity"].mean()
        avg_total = daily["quantity"].mean()
        delta = avg_last - avg_total
        delta_color = "#10b981" if delta >= 0 else "#ef4444"

        st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #ecfdf5 0%, #f0fdfa 100%);
                padding: 1.25rem;
                border-radius: 1rem;
                border-left: 4px solid #10b981;
                margin-top: 1rem;
            ">
                <div style="font-size: 0.875rem; color: #64748b; margin-bottom: 0.25rem;">
                    📊 Performance récente
                </div>
                <div style="font-size: 1.125rem; color: #0f172a; font-weight: 600;">
                    Moyenne 7 jours : <span style="color: #10b981;">{avg_last:.0f} unités/jour</span>
                </div>
                <div style="font-size: 0.875rem; color: #64748b; margin-top: 0.25rem;">
                    Écart à la moyenne globale :
                    <span style="color: {delta_color}; font-weight: 600;">{delta:+.0f}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)


# ============================================================
# PAGE 2 : Stock
# ============================================================

def render_stock() -> None:
    st.markdown("""
        <h1 style="font-size: 2.75rem;">Gestion du stock</h1>
        <p style="font-size: 1.125rem; color: #64748b; margin-bottom: 2rem;">
            Inventaire en temps réel de l'entrepôt 📦
        </p>
    """, unsafe_allow_html=True)

    with st.expander("🔍 Filtres avancés", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            categories = sorted(stock_df["category"].unique())
            selected_cats = st.multiselect("Catégories", categories, default=categories)
        with col2:
            show_low_only = st.checkbox("Seulement produits sous seuil")
        with col3:
            search = st.text_input("Rechercher", placeholder="Nom ou ID...")

    filtered = stock_df[stock_df["category"].isin(selected_cats)].copy()
    if show_low_only:
        filtered = filtered[filtered["quantity"] < filtered["min_threshold"]]
    if search:
        mask = (
            filtered["name"].str.contains(search, case=False, na=False)
            | filtered["product_id"].str.contains(search, case=False, na=False)
        )
        filtered = filtered[mask]

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            render_kpi_card("📋", "Produits affichés", str(len(filtered)),
                          gradient="main"),
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            render_kpi_card("📦", "Unités totales",
                          format_number(int(filtered["quantity"].sum())),
                          gradient="success"),
            unsafe_allow_html=True,
        )
    with col3:
        n_low = int((filtered["quantity"] < filtered["min_threshold"]).sum())
        st.markdown(
            render_kpi_card("⚠️", "Sous seuil", str(n_low),
                          gradient="danger" if n_low > 0 else "success"),
            unsafe_allow_html=True,
        )

    st.markdown(
        render_section_header("📋", f"Liste des produits", f"{len(filtered)} résultats"),
        unsafe_allow_html=True,
    )
    display = filtered.copy()
    display["statut"] = display.apply(
        lambda r: "🔴 Critique" if r["quantity"] < r["min_threshold"]
        else "🟢 OK" if r["quantity"] >= r["min_threshold"] * 2
        else "🟡 Attention",
        axis=1,
    )
    st.dataframe(
        display[["product_id", "name", "category", "quantity",
                 "min_threshold", "location", "statut"]],
        use_container_width=True,
        hide_index=True,
    )

    st.markdown(
        render_section_header("✏️", "Mise à jour du stock",
                             "Ajouter ou retirer des unités"),
        unsafe_allow_html=True,
    )
    with st.form("update_stock_form"):
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            product_id = st.selectbox(
                "Produit",
                options=stock_df["product_id"].tolist(),
                format_func=lambda pid: f"{pid} - {stock_df.loc[stock_df['product_id'] == pid, 'name'].iloc[0]}",
            )
        with col2:
            delta = st.number_input("Variation", value=0, step=1)
        with col3:
            st.write("")
            st.write("")
            submitted = st.form_submit_button("Appliquer", type="primary")

        if submitted and delta != 0:
            try:
                new_qty = dm.update_stock_quantity(product_id, delta)
                st.success(f"✅ Stock {product_id} mis à jour : {new_qty}")
                st.rerun()
            except ValueError as e:
                st.error(f"❌ {e}")

    st.markdown(
        render_section_header("📊", "Visualisation",
                             "Explorer la répartition du stock"),
        unsafe_allow_html=True,
    )
    view_mode = st.radio(
        "Type de visualisation",
        ["Quantité par produit", "Quantité par catégorie", "Top 10 produits"],
        horizontal=True,
        label_visibility="collapsed",
    )

    if view_mode == "Quantité par produit":
        fig = px.bar(
            filtered.sort_values("quantity", ascending=False),
            x="product_id", y="quantity", color="category",
            title="Quantité en stock par produit",
        )
    elif view_mode == "Quantité par catégorie":
        cat_data = filtered.groupby("category")["quantity"].sum().reset_index()
        fig = px.bar(
            cat_data, x="category", y="quantity",
            title="Quantité totale par catégorie", color="category",
        )
    else:
        top10 = filtered.nlargest(10, "quantity")
        fig = px.bar(
            top10, x="quantity", y="name", orientation="h",
            title="Top 10 des produits les plus stockés", color="category",
        )
        fig.update_layout(yaxis={"categoryorder": "total ascending"})

    fig = apply_plotly_theme(fig)
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)


# ============================================================
# PAGE 3 : Prédictions
# ============================================================

def render_predictions() -> None:
    st.markdown("""
        <h1 style="font-size: 2.75rem;">Prévisions de demande</h1>
        <p style="font-size: 1.125rem; color: #64748b; margin-bottom: 2rem;">
            IA prédictive avec auto-sélection du meilleur modèle 🤖
        </p>
    """, unsafe_allow_html=True)

    if historique_df.empty:
        st.warning("Aucun historique de demande disponible.")
        return

    col1, col2 = st.columns([2, 1])
    with col1:
        product_id = st.selectbox(
            "Sélectionne un produit",
            options=stock_df["product_id"].tolist(),
            format_func=lambda pid: f"{pid} - {stock_df.loc[stock_df['product_id'] == pid, 'name'].iloc[0]}",
        )
    with col2:
        horizon = st.slider(
            "Horizon (jours)",
            min_value=1, max_value=30,
            value=settings.default_forecast_horizon,
        )

    if st.button("🚀 Lancer la prédiction", type="primary"):
        with st.spinner(
            "🧠 Le modèle analyse les patterns historiques... "
            "(30-60s la première fois, instantané ensuite)"
        ):
            try:
                predictions = engine.predict(
                    product_id=product_id,
                    n_days=horizon,
                    history_csv=settings.historique_csv,
                )
                st.session_state["last_predictions"] = predictions
                st.session_state["last_product"] = product_id
                st.success("✅ Prédiction terminée avec succès")
            except Exception as e:
                st.error(f"❌ Erreur : {e}")
                return

    if "last_predictions" in st.session_state:
        predictions = st.session_state["last_predictions"]
        last_product = st.session_state["last_product"]

        st.markdown(
            render_section_header("📊", f"Prévisions pour {last_product}",
                                 "Historique récent + projection IA"),
            unsafe_allow_html=True,
        )

        hist = historique_df[historique_df["product_id"] == last_product].copy()
        hist = hist.groupby("date")["quantity"].sum().reset_index()
        hist = hist.sort_values("date").tail(60)

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=hist["date"], y=hist["quantity"],
            mode="lines", name="Historique",
            line=dict(color="#0ea5e9", width=2.5),
            fill="tozeroy",
            fillcolor="rgba(14, 165, 233, 0.1)",
        ))
        fig.add_trace(go.Scatter(
            x=predictions.index, y=predictions.values,
            mode="lines+markers", name="Prédiction IA",
            line=dict(color="#10b981", width=3, dash="dash"),
            marker=dict(size=10, line=dict(color="white", width=2)),
        ))
        fig = apply_plotly_theme(fig)
        fig.update_layout(
            title=f"Évolution + prévision sur {len(predictions)} jours",
            xaxis_title="Date", yaxis_title="Quantité",
            height=500, hovermode="x unified",
        )
        st.plotly_chart(fig, use_container_width=True)

        total = int(predictions.sum())
        avg = float(predictions.mean())
        max_day = predictions.idxmax().strftime("%Y-%m-%d")
        max_val = int(predictions.max())

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(
                render_kpi_card("📈", "Demande totale prévue",
                              f"{total} u.", gradient="main"),
                unsafe_allow_html=True,
            )
        with col2:
            st.markdown(
                render_kpi_card("📊", "Moyenne journalière",
                              f"{avg:.0f} u.", gradient="purple"),
                unsafe_allow_html=True,
            )
        with col3:
            st.markdown(
                render_kpi_card("🎯", "Pic prévu",
                              f"{max_val} u.", sublabel=max_day,
                              gradient="warning"),
                unsafe_allow_html=True,
            )

        col1, col2 = st.columns(2)
        with col1:
            pred_df = predictions.reset_index()
            pred_df.columns = ["Date", "Demande prévue"]
            pred_df["Demande prévue"] = pred_df["Demande prévue"].round(0).astype(int)
            st.dataframe(pred_df, use_container_width=True, hide_index=True)

        with col2:
            current_stock = int(
                stock_df.loc[stock_df["product_id"] == last_product, "quantity"].iloc[0]
            )
            if total > current_stock:
                st.markdown(f"""
                    <div style="
                        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
                        padding: 1.5rem;
                        border-radius: 1rem;
                        border-left: 4px solid #ef4444;
                    ">
                        <div style="font-size: 1.125rem; font-weight: 700; color: #991b1b; margin-bottom: 0.5rem;">
                            ⚠️ Réapprovisionnement requis
                        </div>
                        <div style="color: #7f1d1d;">
                            Stock actuel : <strong>{current_stock} unités</strong><br>
                            Demande prévue : <strong>{total} unités</strong><br>
                            Déficit : <strong>{total - current_stock} unités</strong>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div style="
                        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
                        padding: 1.5rem;
                        border-radius: 1rem;
                        border-left: 4px solid #10b981;
                    ">
                        <div style="font-size: 1.125rem; font-weight: 700; color: #065f46; margin-bottom: 0.5rem;">
                            ✅ Stock suffisant
                        </div>
                        <div style="color: #064e3b;">
                            Stock actuel : <strong>{current_stock} unités</strong><br>
                            Demande prévue : <strong>{total} unités</strong><br>
                            Marge de sécurité : <strong>{current_stock - total} unités</strong>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

    st.markdown(
        render_section_header("🔬", "Comparaison multi-produits",
                             "Compare jusqu'à 5 produits simultanément"),
        unsafe_allow_html=True,
    )
    selected_products = st.multiselect(
        "Sélectionne des produits à comparer",
        options=stock_df["product_id"].tolist(),
        max_selections=5,
    )

    if selected_products and st.button("Comparer", key="compare_btn"):
        with st.spinner("Calcul des prévisions..."):
            fig_compare = go.Figure()
            for pid in selected_products:
                try:
                    preds = engine.predict(
                        product_id=pid, n_days=horizon,
                        history_csv=settings.historique_csv,
                    )
                    fig_compare.add_trace(go.Scatter(
                        x=preds.index, y=preds.values,
                        mode="lines+markers", name=pid,
                        line=dict(width=2.5),
                        marker=dict(size=8),
                    ))
                except Exception as e:
                    st.warning(f"Échec prédiction {pid} : {e}")

            fig_compare = apply_plotly_theme(fig_compare)
            fig_compare.update_layout(
                title="Comparaison des prévisions",
                xaxis_title="Date", yaxis_title="Demande prévue",
                height=500, hovermode="x unified",
            )
            st.plotly_chart(fig_compare, use_container_width=True)


# ============================================================
# PAGE 4 : Commandes
# ============================================================

def render_commandes() -> None:
    st.markdown("""
        <h1 style="font-size: 2.75rem;">Commandes fournisseurs</h1>
        <p style="font-size: 1.125rem; color: #64748b; margin-bottom: 2rem;">
            Suivi et gestion des commandes 🚚
        </p>
    """, unsafe_allow_html=True)

    if commandes_df.empty:
        st.warning("Aucune commande à afficher.")
        return

    cmd_df = commandes_df.copy()
    cmd_df["order_date"] = pd.to_datetime(cmd_df["order_date"])

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(
            render_kpi_card("📋", "Total commandes", str(len(cmd_df)),
                          gradient="main"),
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            render_kpi_card("⏳", "En attente",
                          str(int((cmd_df["status"] == "pending").sum())),
                          gradient="warning"),
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            render_kpi_card("🚚", "En livraison",
                          str(int((cmd_df["status"] == "shipped").sum())),
                          gradient="purple"),
            unsafe_allow_html=True,
        )
    with col4:
        st.markdown(
            render_kpi_card("✅", "Livrées",
                          str(int((cmd_df["status"] == "delivered").sum())),
                          gradient="success"),
            unsafe_allow_html=True,
        )

    with st.expander("🔍 Filtres avancés", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            statuses = sorted(cmd_df["status"].unique())
            selected_statuses = st.multiselect("Statuts", statuses, default=statuses)
        with col2:
            suppliers = sorted(cmd_df["supplier_id"].unique())
            selected_suppliers = st.multiselect("Fournisseurs", suppliers, default=suppliers)

        date_range = st.date_input(
            "Période",
            value=(cmd_df["order_date"].min().date(), cmd_df["order_date"].max().date()),
        )

    filtered = cmd_df[
        cmd_df["status"].isin(selected_statuses)
        & cmd_df["supplier_id"].isin(selected_suppliers)
    ].copy()

    if isinstance(date_range, tuple) and len(date_range) == 2:
        start, end = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])
        filtered = filtered[
            (filtered["order_date"] >= start) & (filtered["order_date"] <= end)
        ]

    st.markdown(
        render_section_header("📋", f"Liste des commandes",
                             f"{len(filtered)} résultats filtrés"),
        unsafe_allow_html=True,
    )
    display = filtered.merge(
        fournisseurs_df[["supplier_id", "name"]].rename(columns={"name": "fournisseur"}),
        on="supplier_id", how="left",
    ).merge(
        stock_df[["product_id", "name"]].rename(columns={"name": "produit"}),
        on="product_id", how="left",
    )

    st.dataframe(
        display[["commande_id", "order_date", "product_id", "produit",
                 "quantity", "supplier_id", "fournisseur", "status"]]
        .sort_values("order_date", ascending=False),
        use_container_width=True,
        hide_index=True,
    )

    st.markdown(
        render_section_header("➕", "Nouvelle commande",
                             "Passer une commande chez un fournisseur"),
        unsafe_allow_html=True,
    )
    with st.form("new_commande_form"):
        col1, col2 = st.columns(2)
        with col1:
            new_product = st.selectbox(
                "Produit",
                options=stock_df["product_id"].tolist(),
                format_func=lambda pid: f"{pid} - {stock_df.loc[stock_df['product_id'] == pid, 'name'].iloc[0]}",
            )
            new_quantity = st.number_input("Quantité", min_value=1, value=50, step=1)
        with col2:
            new_supplier = st.selectbox(
                "Fournisseur",
                options=fournisseurs_df["supplier_id"].tolist(),
                format_func=lambda sid: f"{sid} - {fournisseurs_df.loc[fournisseurs_df['supplier_id'] == sid, 'name'].iloc[0]}",
            )
            new_status = st.selectbox("Statut initial", ["pending", "shipped"])

        submit = st.form_submit_button("Créer la commande", type="primary")
        if submit:
            try:
                cmd_id = dm.add_commande(
                    product_id=new_product,
                    quantity=int(new_quantity),
                    supplier_id=new_supplier,
                    status=new_status,
                )
                st.success(f"✅ Commande {cmd_id} créée avec succès")
                st.rerun()
            except Exception as e:
                st.error(f"❌ {e}")

    st.markdown(
        render_section_header("📊", "Analyse des commandes",
                             "Patterns et tendances"),
        unsafe_allow_html=True,
    )
    col1, col2 = st.columns(2)

    with col1:
        by_supplier = (
            filtered.merge(fournisseurs_df[["supplier_id", "name"]], on="supplier_id")
            .groupby("name")["quantity"].sum()
            .reset_index().sort_values("quantity", ascending=True)
        )
        fig1 = px.bar(
            by_supplier, x="quantity", y="name", orientation="h",
            title="Volume par fournisseur",
            color="quantity",
            color_continuous_scale=[[0, "#a7f3d0"], [1, "#10b981"]],
        )
        fig1 = apply_plotly_theme(fig1)
        fig1.update_layout(height=400, showlegend=False, coloraxis_showscale=False)
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        daily = filtered.groupby("order_date")["quantity"].sum().reset_index()
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=daily["order_date"], y=daily["quantity"],
            mode="lines+markers",
            line=dict(color="#10b981", width=2.5),
            marker=dict(size=6),
            fill="tozeroy",
            fillcolor="rgba(16, 185, 129, 0.1)",
        ))
        fig2 = apply_plotly_theme(fig2)
        fig2.update_layout(
            title="Volume dans le temps",
            xaxis_title="Date", yaxis_title="Unités",
            height=400, showlegend=False,
        )
        st.plotly_chart(fig2, use_container_width=True)


# ============================================================
# PAGE 5 : Robot (placeholder)
# ============================================================

def render_robot() -> None:
    st.markdown("""
        <h1 style="font-size: 2.75rem;">Robot d'entrepôt</h1>
        <p style="font-size: 1.125rem; color: #64748b; margin-bottom: 2rem;">
            Pilotage du robot autonome 🤖
        </p>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div style="
            background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
            padding: 2rem;
            border-radius: 1.5rem;
            border-left: 4px solid #f59e0b;
            margin-bottom: 2rem;
        ">
            <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">🚧</div>
            <div style="font-size: 1.25rem; font-weight: 700; color: #78350f; margin-bottom: 0.75rem;">
                Module en cours de développement
            </div>
            <div style="color: #92400e; line-height: 1.6;">
                Cette page affichera bientôt :<br>
                • L'état temps réel du robot (position, batterie, charge)<br>
                • Les missions en cours et en attente<br>
                • Les commandes manuelles (déplacement, retour à la base)<br>
                • L'historique des actions exécutées<br><br>
                <em>Le module robot/ est en développement par un autre membre du groupe.</em>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(
        render_section_header("🎮", "Aperçu visuel", "Données simulées pour démo"),
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(
            render_kpi_card("⚡", "État", "Inactif", gradient="success"),
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            render_kpi_card("🔋", "Batterie", "87%",
                          sublabel="-3% dernière heure", gradient="success"),
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            render_kpi_card("📍", "Position", "(0, 0)",
                          sublabel="Base de recharge", gradient="purple"),
            unsafe_allow_html=True,
        )
    with col4:
        st.markdown(
            render_kpi_card("✅", "Missions", "0",
                          sublabel="Aujourd'hui", gradient="main"),
            unsafe_allow_html=True,
        )

    st.markdown(
        render_section_header("📋", "Missions en attente",
                             "Données simulées"),
        unsafe_allow_html=True,
    )
    st.dataframe(
        {
            "ID": ["M00001", "M00002", "M00003"],
            "Type": ["Réapprovisionnement", "Picking", "Réapprovisionnement"],
            "Produit": ["P003", "P012", "P018"],
            "Quantité": [50, 10, 30],
            "Priorité": [2, 4, 5],
            "Statut": ["⏳ En attente", "⏳ En attente", "⏳ En attente"],
        },
        use_container_width=True,
        hide_index=True,
    )


# ============================================================
# Routeur
# ============================================================

if page == "🏠 Vue d'ensemble":
    render_overview()
elif page == "📦 Stock":
    render_stock()
elif page == "📈 Prédictions":
    render_predictions()
elif page == "🚚 Commandes":
    render_commandes()
elif page == "🤖 Robot":
    render_robot()