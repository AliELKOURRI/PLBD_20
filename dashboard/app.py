"""
Smart Predict AI — Dashboard Streamlit (mono-fichier).

Toutes les sections de l'application dans un seul fichier, avec une navigation
par sidebar (radio). C'est plus simple à maintenir et à présenter qu'une
architecture multi-pages.

Lancer le dashboard depuis la racine du projet :
    streamlit run dashboard/app.py
"""

from __future__ import annotations

# Ajout du répertoire racine au PYTHONPATH pour que les imports fonctionnent
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from datetime import date

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from config.settings import settings
from helpers.data_manager import DataManager
from prediction.prediction_engine import PredictionEngine


# ============================================================
# Configuration générale de la page
# ============================================================

st.set_page_config(
    page_title=settings.app_name,
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# Helpers (anciennement dans utils.py)
# ============================================================

@st.cache_resource
def get_data_manager() -> DataManager:
    """Instance unique du DataManager, partagée pour toute la session."""
    return DataManager(data_dir=settings.data_dir)


@st.cache_resource
def get_prediction_engine() -> PredictionEngine:
    """Instance unique du PredictionEngine, partagée pour toute la session."""
    return PredictionEngine(models_dir=settings.models_dir)


def format_number(value: float, suffix: str = "") -> str:
    """Format compact pour les KPIs (1234 -> 1.2k, etc.)."""
    if value >= 1_000_000:
        return f"{value/1_000_000:.1f}M{suffix}"
    if value >= 1_000:
        return f"{value/1_000:.1f}k{suffix}"
    return f"{int(value)}{suffix}"


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
# Sidebar : navigation + infos
# ============================================================

with st.sidebar:
    st.title("🏭 Smart Predict AI")
    st.caption("Entrepôt intelligent")
    st.markdown("---")

    page = st.radio(
        "📂 Navigation",
        options=[
            "🏠 Vue d'ensemble",
            "📦 Stock",
            "📈 Prédictions",
            "🚚 Commandes",
            "🤖 Robot",
        ],
        label_visibility="visible",
    )

    st.markdown("---")
    st.caption(f"**{settings.app_name}** v{settings.app_version}")
    st.caption("PLBD 20 — École Centrale Casablanca")


# ============================================================
# PAGE 1 : Vue d'ensemble
# ============================================================

def render_overview() -> None:
    st.title("🏭 Vue d'ensemble")
    st.markdown("---")

    # KPIs principaux
    col1, col2, col3, col4 = st.columns(4)
    low_stock = dm.get_low_stock_products()
    total_units = stock_df["quantity"].sum() if not stock_df.empty else 0
    pending_orders = (
        (commandes_df["status"] == "pending").sum() if not commandes_df.empty else 0
    )

    col1.metric(
        "📦 Produits en stock",
        len(stock_df),
        help="Nombre de références produit dans l'entrepôt.",
    )
    col2.metric(
        "📊 Unités totales",
        format_number(total_units),
        help="Somme des quantités sur tous les produits.",
    )
    col3.metric(
        "⚠️ Produits sous seuil",
        len(low_stock),
        delta=f"-{len(low_stock)}" if len(low_stock) > 0 else None,
        delta_color="inverse",
    )
    col4.metric("🚚 Commandes en attente", int(pending_orders))

    st.markdown("---")

    # Alertes stock
    st.subheader("⚠️ Alertes stock")
    if low_stock.empty:
        st.success("✅ Aucun produit sous le seuil minimum. Stock sain.")
    else:
        st.warning(f"{len(low_stock)} produit(s) à réapprovisionner.")
        display_df = low_stock[
            ["product_id", "name", "category", "quantity", "min_threshold", "location"]
        ].copy()
        display_df["déficit"] = display_df["min_threshold"] - display_df["quantity"]
        display_df = display_df.sort_values("déficit", ascending=False)
        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
        )

    # Répartition par catégorie
    st.markdown("---")
    st.subheader("📊 Répartition du stock par catégorie")

    col_left, col_right = st.columns(2)

    with col_left:
        if not stock_df.empty:
            cat_counts = stock_df.groupby("category").size().reset_index(name="count")
            fig_pie = px.pie(
                cat_counts,
                values="count",
                names="category",
                title="Nombre de produits par catégorie",
                hole=0.4,
            )
            fig_pie.update_layout(height=400)
            st.plotly_chart(fig_pie, use_container_width=True)

    with col_right:
        if not stock_df.empty:
            cat_qty = stock_df.groupby("category")["quantity"].sum().reset_index()
            fig_bar = px.bar(
                cat_qty,
                x="category",
                y="quantity",
                title="Volume total par catégorie",
                color="category",
            )
            fig_bar.update_layout(showlegend=False, height=400)
            st.plotly_chart(fig_bar, use_container_width=True)

    # Tendance globale de la demande
    st.markdown("---")
    st.subheader("📈 Tendance globale de la demande")

    if historique_df.empty:
        st.info("Aucun historique de demande disponible.")
    else:
        daily = historique_df.groupby("date")["quantity"].sum().reset_index()
        daily = daily.sort_values("date")

        fig = px.line(
            daily,
            x="date",
            y="quantity",
            title="Demande journalière totale (toutes catégories confondues)",
            labels={"date": "Date", "quantity": "Unités demandées"},
        )
        fig.update_traces(line=dict(width=2))
        fig.update_layout(height=400, hovermode="x unified")
        st.plotly_chart(fig, use_container_width=True)

        last_7 = daily.tail(7)
        avg_last = last_7["quantity"].mean()
        avg_total = daily["quantity"].mean()
        st.caption(
            f"Moyenne sur 7 derniers jours : **{avg_last:.0f} unités/jour** "
            f"(écart moyenne globale : {avg_last - avg_total:+.0f})"
        )


# ============================================================
# PAGE 2 : Stock
# ============================================================

def render_stock() -> None:
    st.title("📦 Gestion du stock")
    st.markdown("---")

    # Filtres
    with st.expander("🔍 Filtres", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            categories = sorted(stock_df["category"].unique())
            selected_cats = st.multiselect("Catégories", categories, default=categories)
        with col2:
            show_low_only = st.checkbox("Seulement produits sous seuil")
        with col3:
            search = st.text_input("Rechercher", placeholder="Nom ou ID...")

    # Application des filtres
    filtered = stock_df[stock_df["category"].isin(selected_cats)].copy()
    if show_low_only:
        filtered = filtered[filtered["quantity"] < filtered["min_threshold"]]
    if search:
        mask = (
            filtered["name"].str.contains(search, case=False, na=False)
            | filtered["product_id"].str.contains(search, case=False, na=False)
        )
        filtered = filtered[mask]

    # KPIs filtrés
    col1, col2, col3 = st.columns(3)
    col1.metric("Produits affichés", len(filtered))
    col2.metric("Unités totales", int(filtered["quantity"].sum()))
    col3.metric(
        "Sous seuil",
        int((filtered["quantity"] < filtered["min_threshold"]).sum()),
    )

    st.markdown("---")

    # Tableau avec statut visuel
    st.subheader(f"Liste des produits ({len(filtered)} résultats)")
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

    # Mise à jour manuelle
    st.markdown("---")
    st.subheader("✏️ Mise à jour manuelle du stock")

    with st.form("update_stock_form"):
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            product_id = st.selectbox(
                "Produit",
                options=stock_df["product_id"].tolist(),
                format_func=lambda pid: f"{pid} - {stock_df.loc[stock_df['product_id'] == pid, 'name'].iloc[0]}",
            )
        with col2:
            delta = st.number_input(
                "Variation (+ ou -)", value=0, step=1,
                help="Positif = ajout, négatif = retrait",
            )
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

    # Visualisation
    st.markdown("---")
    st.subheader("📊 Visualisation du stock")

    view_mode = st.radio(
        "Type de visualisation",
        ["Quantité par produit", "Quantité par catégorie", "Top 10 produits"],
        horizontal=True,
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

    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)


# ============================================================
# PAGE 3 : Prédictions
# ============================================================

def render_predictions() -> None:
    st.title("📈 Prévisions de demande")
    st.markdown("---")

    if historique_df.empty:
        st.warning("Aucun historique de demande disponible.")
        return

    # Sélection produit + horizon
    col1, col2 = st.columns([2, 1])
    with col1:
        product_id = st.selectbox(
            "Sélectionne un produit",
            options=stock_df["product_id"].tolist(),
            format_func=lambda pid: f"{pid} - {stock_df.loc[stock_df['product_id'] == pid, 'name'].iloc[0]}",
        )
    with col2:
        horizon = st.slider(
            "Horizon de prévision (jours)",
            min_value=1, max_value=30,
            value=settings.default_forecast_horizon,
        )

    # Lancement
    if st.button("🚀 Lancer la prédiction", type="primary"):
        with st.spinner(
            "Entraînement du modèle (auto-sélection entre Régression, ARIMA, SARIMA)... "
            "Cela peut prendre 30-60s la première fois pour ce produit."
        ):
            try:
                predictions = engine.predict(
                    product_id=product_id,
                    n_days=horizon,
                    history_csv=settings.historique_csv,
                )
                st.session_state["last_predictions"] = predictions
                st.session_state["last_product"] = product_id
                st.success("✅ Prédiction terminée")
            except Exception as e:
                st.error(f"❌ Erreur : {e}")
                return

    # Affichage des résultats
    if "last_predictions" in st.session_state:
        predictions = st.session_state["last_predictions"]
        last_product = st.session_state["last_product"]

        st.markdown("---")
        st.subheader(f"📊 Prévisions pour {last_product}")

        # Historique récent + prévisions
        hist = historique_df[historique_df["product_id"] == last_product].copy()
        hist = hist.groupby("date")["quantity"].sum().reset_index()
        hist = hist.sort_values("date").tail(60)

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=hist["date"], y=hist["quantity"],
            mode="lines", name="Historique",
            line=dict(color="#1f77b4", width=2),
        ))
        fig.add_trace(go.Scatter(
            x=predictions.index, y=predictions.values,
            mode="lines+markers", name="Prédiction",
            line=dict(color="#ff7f0e", width=3, dash="dash"),
            marker=dict(size=8),
        ))
        fig.update_layout(
            title=f"Historique récent + Prévision sur {len(predictions)} jours",
            xaxis_title="Date", yaxis_title="Quantité demandée",
            height=500, hovermode="x unified",
        )
        st.plotly_chart(fig, use_container_width=True)

        # Tableau + stats
        st.subheader("📋 Détail des prévisions")
        pred_df = predictions.reset_index()
        pred_df.columns = ["Date", "Demande prévue"]
        pred_df["Demande prévue"] = pred_df["Demande prévue"].round(0).astype(int)

        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(pred_df, use_container_width=True, hide_index=True)
        with col2:
            total = int(predictions.sum())
            avg = float(predictions.mean())
            max_day = predictions.idxmax().strftime("%Y-%m-%d")
            max_val = int(predictions.max())

            st.metric("Demande totale prévue", f"{total} unités")
            st.metric("Moyenne journalière", f"{avg:.1f} unités/jour")
            st.metric("Pic prévu", f"{max_val} unités", delta=f"le {max_day}")

            current_stock = int(
                stock_df.loc[stock_df["product_id"] == last_product, "quantity"].iloc[0]
            )
            if total > current_stock:
                st.error(
                    f"⚠️ Stock actuel ({current_stock}) insuffisant pour la "
                    f"demande prévue ({total}). Réapprovisionnement recommandé."
                )
            else:
                st.success(
                    f"✅ Stock actuel ({current_stock}) suffisant pour la "
                    f"demande prévue ({total})."
                )

    # Comparaison multi-produits
    st.markdown("---")
    st.subheader("🔬 Comparaison multi-produits")

    selected_products = st.multiselect(
        "Compare la demande prévue pour plusieurs produits",
        options=stock_df["product_id"].tolist(),
        max_selections=5,
    )

    if selected_products and st.button("Comparer", key="compare_btn"):
        with st.spinner("Calcul des prévisions..."):
            fig_compare = go.Figure()
            for pid in selected_products:
                try:
                    preds = engine.predict(
                        product_id=pid,
                        n_days=horizon,
                        history_csv=settings.historique_csv,
                    )
                    fig_compare.add_trace(go.Scatter(
                        x=preds.index, y=preds.values,
                        mode="lines+markers", name=pid,
                    ))
                except Exception as e:
                    st.warning(f"Échec prédiction {pid} : {e}")

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
    st.title("🚚 Commandes fournisseurs")
    st.markdown("---")

    if commandes_df.empty:
        st.warning("Aucune commande à afficher.")
        return

    cmd_df = commandes_df.copy()
    cmd_df["order_date"] = pd.to_datetime(cmd_df["order_date"])

    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total commandes", len(cmd_df))
    col2.metric("En attente", int((cmd_df["status"] == "pending").sum()))
    col3.metric("En livraison", int((cmd_df["status"] == "shipped").sum()))
    col4.metric("Livrées", int((cmd_df["status"] == "delivered").sum()))

    st.markdown("---")

    # Filtres
    with st.expander("🔍 Filtres", expanded=False):
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

    # Filtrage
    filtered = cmd_df[
        cmd_df["status"].isin(selected_statuses)
        & cmd_df["supplier_id"].isin(selected_suppliers)
    ].copy()

    if isinstance(date_range, tuple) and len(date_range) == 2:
        start, end = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])
        filtered = filtered[
            (filtered["order_date"] >= start) & (filtered["order_date"] <= end)
        ]

    # Tableau enrichi
    st.subheader(f"📋 Commandes ({len(filtered)} résultats)")
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

    # Création nouvelle commande
    st.markdown("---")
    st.subheader("➕ Nouvelle commande")

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

    # Visualisations
    st.markdown("---")
    st.subheader("📊 Analyse des commandes")

    col1, col2 = st.columns(2)
    with col1:
        by_supplier = (
            filtered.merge(fournisseurs_df[["supplier_id", "name"]], on="supplier_id")
            .groupby("name")["quantity"].sum()
            .reset_index().sort_values("quantity", ascending=True)
        )
        fig1 = px.bar(
            by_supplier, x="quantity", y="name", orientation="h",
            title="Volume commandé par fournisseur",
            labels={"name": "Fournisseur", "quantity": "Unités"},
        )
        fig1.update_layout(height=400)
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        daily = filtered.groupby("order_date")["quantity"].sum().reset_index()
        fig2 = px.line(
            daily, x="order_date", y="quantity",
            title="Volume commandé dans le temps",
            labels={"order_date": "Date", "quantity": "Unités"},
        )
        fig2.update_layout(height=400)
        st.plotly_chart(fig2, use_container_width=True)


# ============================================================
# PAGE 5 : Robot (placeholder)
# ============================================================

def render_robot() -> None:
    st.title("🤖 Robot d'entrepôt")
    st.markdown("---")

    st.info(
        "🚧 **Module en cours de développement**\n\n"
        "Cette page affichera :\n"
        "- L'état temps réel du robot (position, batterie, charge)\n"
        "- Les missions en cours et en attente\n"
        "- Les commandes manuelles (déplacement, retour à la base)\n"
        "- L'historique des actions exécutées\n\n"
        "Le module `robot/` est en développement par un autre membre du groupe."
    )

    st.markdown("---")
    st.subheader("Aperçu visuel (données simulées)")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("État", "🟢 Inactif")
    col2.metric("Batterie", "87%", delta="-3%")
    col3.metric("Position", "(0, 0)")
    col4.metric("Missions terminées", "0")

    st.markdown("---")
    st.subheader("Missions en attente (mock)")
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

    st.caption(
        "💡 Quand le module robot sera intégré, ces données proviendront du "
        "`MissionManager` et du `RobotController` en temps réel."
    )


# ============================================================
# Routeur : appelle la fonction de la page sélectionnée
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