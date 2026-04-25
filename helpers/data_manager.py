"""
Gestionnaire centralisé des données CSV.

Fournit une API unique pour lire et écrire les fichiers CSV du projet :
- stock.csv : état actuel du stock par produit
- commandes.csv : commandes passées aux fournisseurs
- fournisseurs.csv : liste des fournisseurs et leurs caractéristiques
- raw/historique_demande.csv : historique des demandes (pour ML)

Toutes les écritures sont protégées par un verrou (filelock) pour empêcher
la corruption des fichiers en cas d'accès concurrent.
"""

from __future__ import annotations

import logging
from datetime import date, datetime
from pathlib import Path
from typing import Optional

import pandas as pd
from filelock import FileLock

logger = logging.getLogger(__name__)


# Schémas attendus pour chaque CSV (nom de colonne -> type pandas)
STOCK_SCHEMA = {
    "product_id": "string",
    "name": "string",
    "category": "string",
    "quantity": "int64",
    "min_threshold": "int64",
    "location": "string",
}

COMMANDES_SCHEMA = {
    "commande_id": "string",
    "product_id": "string",
    "quantity": "int64",
    "supplier_id": "string",
    "order_date": "string",
    "status": "string",
}

FOURNISSEURS_SCHEMA = {
    "supplier_id": "string",
    "name": "string",
    "delivery_days": "int64",
    "reliability_score": "float64",
}

HISTORIQUE_SCHEMA = {
    "date": "string",
    "product_id": "string",
    "quantity": "int64",
}


class DataManager:
    """Gestionnaire centralisé d'accès aux CSV du projet."""

    def __init__(self, data_dir: Path) -> None:
        """
        Args:
            data_dir: Dossier racine des données (ex: Path('./data')).
        """
        self.data_dir = Path(data_dir)
        self.raw_dir = self.data_dir / "raw"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.raw_dir.mkdir(parents=True, exist_ok=True)

    # ============ Chemins des fichiers ============

    @property
    def stock_path(self) -> Path:
        return self.data_dir / "stock.csv"

    @property
    def commandes_path(self) -> Path:
        return self.data_dir / "commandes.csv"

    @property
    def fournisseurs_path(self) -> Path:
        return self.data_dir / "fournisseurs.csv"

    @property
    def historique_path(self) -> Path:
        return self.raw_dir / "historique_demande.csv"

    def _lock_path(self, csv_path: Path) -> Path:
        """Chemin du fichier verrou associé à un CSV."""
        return csv_path.with_suffix(csv_path.suffix + ".lock")

    # ============ Lecture ============

    def _read_csv(self, path: Path, schema: dict) -> pd.DataFrame:
        """Lit un CSV avec validation du schéma."""
        if not path.exists():
            logger.warning(f"Fichier introuvable : {path}, retour DataFrame vide.")
            return pd.DataFrame(columns=list(schema.keys())).astype(schema)

        df = pd.read_csv(path)
        missing = set(schema.keys()) - set(df.columns)
        if missing:
            raise ValueError(
                f"Colonnes manquantes dans {path.name} : {missing}"
            )

        # On ne garde que les colonnes attendues, dans l'ordre du schéma
        df = df[list(schema.keys())]
        return df.astype(schema, errors="ignore")

    def read_stock(self) -> pd.DataFrame:
        """Lit le CSV de stock."""
        return self._read_csv(self.stock_path, STOCK_SCHEMA)

    def read_commandes(self) -> pd.DataFrame:
        """Lit le CSV des commandes."""
        return self._read_csv(self.commandes_path, COMMANDES_SCHEMA)

    def read_fournisseurs(self) -> pd.DataFrame:
        """Lit le CSV des fournisseurs."""
        return self._read_csv(self.fournisseurs_path, FOURNISSEURS_SCHEMA)

    def read_historique(self) -> pd.DataFrame:
        """Lit le CSV de l'historique de demande."""
        df = self._read_csv(self.historique_path, HISTORIQUE_SCHEMA)
        # Convertit la colonne date en datetime pour les calculs ML
        if not df.empty:
            df["date"] = pd.to_datetime(df["date"])
        return df

    # ============ Écriture (atomique avec verrou) ============

    def _write_csv(self, df: pd.DataFrame, path: Path) -> None:
        """Écrit un DataFrame dans un CSV de manière atomique et protégée."""
        lock = FileLock(self._lock_path(path), timeout=10)
        with lock:
            # Écriture via fichier temporaire puis rename = atomique sur OS
            tmp_path = path.with_suffix(path.suffix + ".tmp")
            df.to_csv(tmp_path, index=False)
            tmp_path.replace(path)
            logger.debug(f"CSV écrit : {path}")

    def write_stock(self, df: pd.DataFrame) -> None:
        """Écrit le DataFrame de stock complet."""
        self._validate_columns(df, STOCK_SCHEMA, "stock")
        self._write_csv(df, self.stock_path)

    def write_commandes(self, df: pd.DataFrame) -> None:
        """Écrit le DataFrame de commandes complet."""
        self._validate_columns(df, COMMANDES_SCHEMA, "commandes")
        self._write_csv(df, self.commandes_path)

    def write_fournisseurs(self, df: pd.DataFrame) -> None:
        """Écrit le DataFrame de fournisseurs complet."""
        self._validate_columns(df, FOURNISSEURS_SCHEMA, "fournisseurs")
        self._write_csv(df, self.fournisseurs_path)

    def write_historique(self, df: pd.DataFrame) -> None:
        """Écrit le DataFrame d'historique complet."""
        self._validate_columns(df, HISTORIQUE_SCHEMA, "historique")
        # Convertit la date en string pour le stockage CSV
        df_to_save = df.copy()
        if pd.api.types.is_datetime64_any_dtype(df_to_save["date"]):
            df_to_save["date"] = df_to_save["date"].dt.strftime("%Y-%m-%d")
        self._write_csv(df_to_save, self.historique_path)

    @staticmethod
    def _validate_columns(df: pd.DataFrame, schema: dict, name: str) -> None:
        """Vérifie que le DataFrame contient toutes les colonnes du schéma."""
        missing = set(schema.keys()) - set(df.columns)
        if missing:
            raise ValueError(
                f"Colonnes manquantes pour écrire {name} : {missing}"
            )

    # ============ Opérations atomiques métier ============

    def update_stock_quantity(self, product_id: str, delta: int) -> int:
        """
        Modifie la quantité d'un produit de manière atomique (lock + read + write).

        Args:
            product_id: Identifiant du produit.
            delta: Variation de quantité (positif = ajout, négatif = retrait).

        Returns:
            La nouvelle quantité du produit après mise à jour.

        Raises:
            ValueError: Si le produit n'existe pas ou si la nouvelle quantité serait négative.
        """
        lock = FileLock(self._lock_path(self.stock_path), timeout=10)
        with lock:
            df = self._read_csv(self.stock_path, STOCK_SCHEMA)
            mask = df["product_id"] == product_id
            if not mask.any():
                raise ValueError(f"Produit {product_id} introuvable dans le stock.")

            current = int(df.loc[mask, "quantity"].iloc[0])
            new_quantity = current + delta
            if new_quantity < 0:
                raise ValueError(
                    f"Stock insuffisant pour {product_id} : {current} disponible, "
                    f"demande de retrait de {-delta}."
                )

            df.loc[mask, "quantity"] = new_quantity
            self._write_csv(df, self.stock_path)
            logger.info(
                f"Stock {product_id} mis à jour : {current} -> {new_quantity} "
                f"(delta={delta:+d})"
            )
            return new_quantity

    def add_commande(
        self,
        product_id: str,
        quantity: int,
        supplier_id: str,
        order_date: Optional[date] = None,
        status: str = "pending",
    ) -> str:
        """
        Ajoute une commande dans le CSV.

        Args:
            product_id: Identifiant du produit commandé.
            quantity: Quantité commandée.
            supplier_id: Identifiant du fournisseur.
            order_date: Date de la commande (par défaut : aujourd'hui).
            status: Statut de la commande ('pending', 'shipped', 'delivered', 'cancelled').

        Returns:
            L'identifiant de la commande créée (CMD-YYYYMMDD-XXX).
        """
        if order_date is None:
            order_date = date.today()

        lock = FileLock(self._lock_path(self.commandes_path), timeout=10)
        with lock:
            df = self._read_csv(self.commandes_path, COMMANDES_SCHEMA)

            # Génère un ID unique : CMD-AAAAMMJJ-NNN
            today_str = order_date.strftime("%Y%m%d")
            today_count = df["commande_id"].str.startswith(f"CMD-{today_str}").sum()
            commande_id = f"CMD-{today_str}-{today_count + 1:03d}"

            new_row = pd.DataFrame([{
                "commande_id": commande_id,
                "product_id": product_id,
                "quantity": quantity,
                "supplier_id": supplier_id,
                "order_date": order_date.strftime("%Y-%m-%d"),
                "status": status,
            }])
            df = pd.concat([df, new_row], ignore_index=True)
            self._write_csv(df, self.commandes_path)
            logger.info(
                f"Commande créée : {commande_id} - {quantity}x {product_id} "
                f"chez {supplier_id}"
            )
            return commande_id

    def add_demande(
        self,
        product_id: str,
        quantity: int,
        demande_date: Optional[date] = None,
    ) -> None:
        """
        Ajoute une ligne dans l'historique de demande.

        Utile pour enregistrer les sorties de stock réelles et enrichir
        progressivement les données pour le ML.
        """
        if demande_date is None:
            demande_date = date.today()

        lock = FileLock(self._lock_path(self.historique_path), timeout=10)
        with lock:
            df = self._read_csv(self.historique_path, HISTORIQUE_SCHEMA)
            new_row = pd.DataFrame([{
                "date": demande_date.strftime("%Y-%m-%d"),
                "product_id": product_id,
                "quantity": quantity,
            }])
            df = pd.concat([df, new_row], ignore_index=True)
            self._write_csv(df, self.historique_path)

    # ============ Requêtes utiles ============

    def get_low_stock_products(self) -> pd.DataFrame:
        """Retourne les produits dont la quantité est sous le seuil minimum."""
        df = self.read_stock()
        return df[df["quantity"] < df["min_threshold"]].copy()

    def get_product_info(self, product_id: str) -> Optional[dict]:
        """Retourne les infos d'un produit, ou None s'il n'existe pas."""
        df = self.read_stock()
        row = df[df["product_id"] == product_id]
        if row.empty:
            return None
        return row.iloc[0].to_dict()