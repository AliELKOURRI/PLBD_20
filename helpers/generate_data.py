"""
Générateur de données synthétiques pour le projet d'entrepôt intelligent.

Crée 4 CSV cohérents entre eux :
- stock.csv : état initial du stock pour ~30 produits
- fournisseurs.csv : liste de fournisseurs
- commandes.csv : historique de commandes passées
- raw/historique_demande.csv : 1 an de demandes journalières avec saisonnalité

Usage :
    python -m helpers.generate_data

Pour personnaliser, modifie les constantes en haut du fichier.
"""

from __future__ import annotations

import logging
from datetime import date, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

from helpers.data_manager import DataManager

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# ============ Paramètres modifiables ============

NUM_PRODUCTS = 30           # Nombre de produits à générer
NUM_SUPPLIERS = 5           # Nombre de fournisseurs
HISTORY_DAYS = 365          # Jours d'historique de demande
NUM_PAST_COMMANDES = 80     # Nombre de commandes passées à générer

# Catégories de produits
CATEGORIES = ["Électronique", "Alimentaire", "Textile", "Outillage", "Bureautique"]

# Localisations dans l'entrepôt (allée-rangée)
LOCATIONS = [f"A{i}-R{j}" for i in range(1, 6) for j in range(1, 7)]

# Seed pour la reproductibilité (mêmes données à chaque génération)
RANDOM_SEED = 42


# ============ Génération ============


def generate_fournisseurs(n: int, rng: np.random.Generator) -> pd.DataFrame:
    """Génère le CSV des fournisseurs."""
    suppliers = []
    names = [
        "LogiSupply", "FastDeliver", "EuroStock", "PrimeFournitures",
        "MaghrebDistrib", "AtlasGoods", "RapidoExpress", "TopWholesale",
    ]
    for i in range(n):
        suppliers.append({
            "supplier_id": f"S{i+1:03d}",
            "name": rng.choice(names),
            "delivery_days": int(rng.integers(2, 15)),
            "reliability_score": round(float(rng.uniform(0.70, 0.99)), 2),
        })
    return pd.DataFrame(suppliers)


def generate_stock(n: int, rng: np.random.Generator) -> pd.DataFrame:
    """Génère le CSV de stock initial."""
    product_names = [
        "Câble USB", "Clavier", "Souris", "Écran 24''", "Disque SSD",
        "Riz 5kg", "Huile olive", "Sucre 1kg", "Café 250g", "Pâtes 500g",
        "T-shirt M", "Jean", "Veste cuir", "Chaussettes", "Casquette",
        "Marteau", "Tournevis", "Perceuse", "Mètre ruban", "Clé anglaise",
        "Cahier A4", "Stylo bille", "Agrafeuse", "Ciseaux", "Calculatrice",
        "Tablette", "Chargeur", "Casque audio", "Webcam", "Imprimante",
    ]
    products = []
    for i in range(n):
        category = CATEGORIES[i % len(CATEGORIES)]
        name = product_names[i] if i < len(product_names) else f"Produit-{i+1}"
        products.append({
            "product_id": f"P{i+1:03d}",
            "name": name,
            "category": category,
            "quantity": int(rng.integers(20, 200)),
            "min_threshold": int(rng.integers(10, 30)),
            "location": rng.choice(LOCATIONS),
        })
    return pd.DataFrame(products)


def generate_historique(
    product_ids: list[str],
    n_days: int,
    rng: np.random.Generator,
) -> pd.DataFrame:
    """
    Génère un historique de demande avec saisonnalité hebdomadaire.

    Pour chaque produit, la demande journalière suit :
    - Une baseline propre au produit (popularité)
    - Un cycle hebdomadaire (pic en semaine, creux le weekend)
    - Une légère tendance haussière ou baissière
    - Du bruit aléatoire
    """
    end_date = date.today()
    start_date = end_date - timedelta(days=n_days - 1)
    dates = pd.date_range(start_date, end_date, freq="D")

    records = []
    for product_id in product_ids:
        # Baseline propre au produit (entre 5 et 50 unités/jour en moyenne)
        baseline = rng.uniform(5, 50)
        # Tendance : -0.05 à +0.05 unité par jour
        trend_per_day = rng.uniform(-0.05, 0.05)
        # Amplitude saisonnière : 30% à 60% de la baseline
        seasonal_amplitude = baseline * rng.uniform(0.30, 0.60)
        # Bruit : 10% à 25% de la baseline
        noise_std = baseline * rng.uniform(0.10, 0.25)

        for i, d in enumerate(dates):
            # Cycle hebdomadaire : pic le mercredi (jour 2), creux le dimanche (jour 6)
            day_of_week = d.dayofweek
            seasonal_factor = np.sin(2 * np.pi * (day_of_week - 2) / 7)
            seasonal = seasonal_amplitude * seasonal_factor

            # Composantes
            trend = trend_per_day * i
            noise = rng.normal(0, noise_std)

            quantity = max(0, int(round(baseline + trend + seasonal + noise)))
            records.append({
                "date": d.strftime("%Y-%m-%d"),
                "product_id": product_id,
                "quantity": quantity,
            })

    return pd.DataFrame(records)


def generate_commandes(
    product_ids: list[str],
    supplier_ids: list[str],
    n_commandes: int,
    rng: np.random.Generator,
) -> pd.DataFrame:
    """Génère un historique de commandes passées sur les 6 derniers mois."""
    end_date = date.today()
    start_date = end_date - timedelta(days=180)

    statuses = ["delivered", "delivered", "delivered", "shipped", "pending"]

    commandes = []
    daily_counters: dict[str, int] = {}

    for _ in range(n_commandes):
        # Date aléatoire dans la fenêtre
        days_offset = int(rng.integers(0, (end_date - start_date).days + 1))
        order_date = start_date + timedelta(days=days_offset)
        date_str = order_date.strftime("%Y%m%d")

        # ID unique par jour
        daily_counters[date_str] = daily_counters.get(date_str, 0) + 1
        commande_id = f"CMD-{date_str}-{daily_counters[date_str]:03d}"

        commandes.append({
            "commande_id": commande_id,
            "product_id": rng.choice(product_ids),
            "quantity": int(rng.integers(10, 100)),
            "supplier_id": rng.choice(supplier_ids),
            "order_date": order_date.strftime("%Y-%m-%d"),
            "status": rng.choice(statuses),
        })

    df = pd.DataFrame(commandes)
    # Tri chronologique pour plus de lisibilité
    return df.sort_values("order_date").reset_index(drop=True)


# ============ Point d'entrée ============


def main() -> None:
    """Génère et sauvegarde tous les CSV via DataManager."""
    logger.info("Génération des données synthétiques en cours...")

    rng = np.random.default_rng(RANDOM_SEED)
    data_manager = DataManager(data_dir=Path("data"))

    # 1. Fournisseurs
    fournisseurs_df = generate_fournisseurs(NUM_SUPPLIERS, rng)
    data_manager.write_fournisseurs(fournisseurs_df)
    logger.info(f"  {len(fournisseurs_df)} fournisseurs générés")

    # 2. Stock
    stock_df = generate_stock(NUM_PRODUCTS, rng)
    data_manager.write_stock(stock_df)
    logger.info(f"  {len(stock_df)} produits dans le stock")

    # 3. Historique de demande (le plus volumineux)
    product_ids = stock_df["product_id"].tolist()
    historique_df = generate_historique(product_ids, HISTORY_DAYS, rng)
    historique_df["date"] = pd.to_datetime(historique_df["date"])
    data_manager.write_historique(historique_df)
    logger.info(
        f"  {len(historique_df)} lignes d'historique "
        f"({HISTORY_DAYS} jours x {NUM_PRODUCTS} produits)"
    )

    # 4. Commandes passées
    supplier_ids = fournisseurs_df["supplier_id"].tolist()
    commandes_df = generate_commandes(product_ids, supplier_ids, NUM_PAST_COMMANDES, rng)
    data_manager.write_commandes(commandes_df)
    logger.info(f"  {len(commandes_df)} commandes passées générées")

    logger.info("Génération terminée. Données disponibles dans data/")


if __name__ == "__main__":
    main()