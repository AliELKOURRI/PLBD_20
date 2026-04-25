"""
Moteur de prévision unifié.

Sélectionne automatiquement le meilleur modèle (Régression, ARIMA, SARIMA)
pour chaque produit en se basant sur la performance d'évaluation.

Expose une API simple pour entraîner, sauvegarder, charger et prédire.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Dict, Literal, Optional, Union

import pandas as pd

from prediction.arima_sarima import ARIMAForecaster, SARIMAForecaster
from prediction.regression import LinearRegressionForecaster

logger = logging.getLogger(__name__)

ForecasterType = Union[LinearRegressionForecaster, ARIMAForecaster, SARIMAForecaster]
ModelName = Literal["linear", "arima", "sarima", "auto"]


class PredictionEngine:
    """Moteur de prévision multi-modèles, multi-produits."""

    def __init__(self, models_dir: Path) -> None:
        """
        Args:
            models_dir: Dossier où sauvegarder/charger les modèles entraînés.
        """
        self.models_dir = Path(models_dir)
        self.models_dir.mkdir(parents=True, exist_ok=True)
        self._cache: Dict[str, ForecasterType] = {}

    def _load_history(self, history_csv: Path) -> pd.DataFrame:
        """Charge et valide le CSV d'historique de demande."""
        if not history_csv.exists():
            raise FileNotFoundError(f"Fichier introuvable : {history_csv}")

        df = pd.read_csv(history_csv, parse_dates=["date"])
        required = {"date", "product_id", "quantity"}
        missing = required - set(df.columns)
        if missing:
            raise ValueError(f"Colonnes manquantes dans le CSV : {missing}")

        return df

    def _get_product_series(
        self, df: pd.DataFrame, product_id: str
    ) -> pd.Series:
        """Extrait la série temporelle d'un produit, agrégée par jour."""
        product_df = df[df["product_id"] == product_id].copy()
        if product_df.empty:
            raise ValueError(f"Aucune donnée pour le produit {product_id}.")

        # Agrégation journalière (au cas où il y a plusieurs lignes par jour)
        series = product_df.groupby("date")["quantity"].sum().sort_index()

        # Remplit les jours manquants avec 0 (pas de demande ce jour-là)
        full_index = pd.date_range(series.index.min(), series.index.max(), freq="D")
        series = series.reindex(full_index, fill_value=0)
        series.name = product_id
        return series

    def train(
        self,
        history_csv: Path,
        product_id: str,
        model: ModelName = "auto",
    ) -> ForecasterType:
        """
        Entraîne un modèle pour un produit donné.

        Args:
            history_csv: Chemin vers historique_demande.csv.
            product_id: Identifiant du produit (ex: 'P001').
            model: 'linear', 'arima', 'sarima' ou 'auto' pour sélection automatique.

        Returns:
            Le modèle entraîné (et sauvegardé sur disque).
        """
        df = self._load_history(history_csv)
        series = self._get_product_series(df, product_id)

        if model == "auto":
            forecaster = self._auto_select(series, product_id)
        else:
            forecaster = self._train_one(series, product_id, model)

        # Sauvegarde
        save_path = self.models_dir / f"{product_id}_{forecaster.__class__.__name__}.pkl"
        forecaster.save(save_path)
        self._cache[product_id] = forecaster
        logger.info(f"Modèle entraîné et sauvegardé : {save_path}")

        return forecaster

    def _train_one(
        self, series: pd.Series, product_id: str, model: ModelName
    ) -> ForecasterType:
        """Entraîne un modèle spécifique."""
        forecaster: ForecasterType
        if model == "linear":
            forecaster = LinearRegressionForecaster()
        elif model == "arima":
            forecaster = ARIMAForecaster()
        elif model == "sarima":
            forecaster = SARIMAForecaster()
        else:
            raise ValueError(f"Modèle inconnu : {model}")

        forecaster.product_id = product_id
        forecaster.fit(series)
        return forecaster

    def _auto_select(self, series: pd.Series, product_id: str) -> ForecasterType:
        """
        Sélectionne automatiquement le meilleur modèle en comparant le RMSE
        sur un split train/test.
        """
        candidates: Dict[str, ForecasterType] = {}
        scores: Dict[str, float] = {}

        # Toujours évaluer la régression linéaire (baseline)
        try:
            lr = LinearRegressionForecaster()
            lr.product_id = product_id
            scores["linear"] = lr.evaluate(series)["rmse"]
            lr.fit(series)
            candidates["linear"] = lr
        except Exception as e:
            logger.warning(f"Régression linéaire échouée : {e}")

        # ARIMA si assez de points
        if len(series) >= 20:
            try:
                arima = ARIMAForecaster()
                arima.product_id = product_id
                scores["arima"] = arima.evaluate(series)["rmse"]
                arima.fit(series)
                candidates["arima"] = arima
            except Exception as e:
                logger.warning(f"ARIMA échoué : {e}")

        # SARIMA si assez de points pour la saisonnalité
        if len(series) >= 14:  # 2 cycles hebdomadaires minimum
            try:
                sarima = SARIMAForecaster()
                sarima.product_id = product_id
                scores["sarima"] = sarima.evaluate(series)["rmse"]
                sarima.fit(series)
                candidates["sarima"] = sarima
            except Exception as e:
                logger.warning(f"SARIMA échoué : {e}")

        if not candidates:
            raise RuntimeError("Aucun modèle n'a pu être entraîné.")

        # Sélection du meilleur (RMSE le plus bas)
        best_name = min(scores, key=scores.get)
        logger.info(
            f"Modèle sélectionné pour {product_id} : {best_name} "
            f"(RMSE={scores[best_name]:.2f})"
        )
        return candidates[best_name]

    def predict(
        self,
        product_id: str,
        n_days: int,
        history_csv: Optional[Path] = None,
    ) -> pd.Series:
        """
        Prédit la demande pour un produit.

        Si le modèle n'est pas en cache, tente de le charger depuis le disque.
        Si introuvable et que history_csv est fourni, l'entraîne automatiquement.
        """
        # 1. Cache mémoire
        if product_id in self._cache:
            return self._cache[product_id].predict(n_days)

        # 2. Cherche un modèle sauvegardé sur disque
        for cls in (SARIMAForecaster, ARIMAForecaster, LinearRegressionForecaster):
            path = self.models_dir / f"{product_id}_{cls.__name__}.pkl"
            if path.exists():
                forecaster = cls.load(path)
                self._cache[product_id] = forecaster
                return forecaster.predict(n_days)

        # 3. Pas de modèle sauvegardé : on entraîne si history_csv est fourni
        if history_csv is not None:
            forecaster = self.train(history_csv, product_id, model="auto")
            return forecaster.predict(n_days)

        raise RuntimeError(
            f"Aucun modèle trouvé pour {product_id}, et pas d'historique fourni "
            f"pour entraîner."
        )

    def predict_all(
        self,
        history_csv: Path,
        n_days: int,
    ) -> pd.DataFrame:
        """
        Prédit la demande pour TOUS les produits du CSV.

        Returns:
            DataFrame avec colonnes [date, product_id, prediction].
        """
        df = self._load_history(history_csv)
        products = df["product_id"].unique()

        all_predictions = []
        for product_id in products:
            try:
                preds = self.predict(product_id, n_days, history_csv=history_csv)
                pred_df = preds.reset_index()
                pred_df.columns = ["date", "prediction"]
                pred_df["product_id"] = product_id
                all_predictions.append(pred_df)
            except Exception as e:
                logger.error(f"Échec prédiction {product_id} : {e}")

        if not all_predictions:
            return pd.DataFrame(columns=["date", "product_id", "prediction"])

        return pd.concat(all_predictions, ignore_index=True)[
            ["date", "product_id", "prediction"]
        ]