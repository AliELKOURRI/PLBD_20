"""
Moteur de prévision unifié.

Sélectionne automatiquement le meilleur modèle (Régression, ARIMA, SARIMA)
pour chaque produit en se basant sur la performance d'évaluation.

Expose une API simple pour entraîner, sauvegarder, charger et prédire,
avec aussi des fonctions d'introspection (quel modèle est utilisé) et
d'évaluation (métriques de performance sur données réelles).
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Dict, Literal, Optional, Union

import numpy as np
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

        series = product_df.groupby("date")["quantity"].sum().sort_index()
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
        """Entraîne un modèle pour un produit donné."""
        df = self._load_history(history_csv)
        series = self._get_product_series(df, product_id)

        if model == "auto":
            forecaster = self._auto_select(series, product_id)
        else:
            forecaster = self._train_one(series, product_id, model)

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
        """Sélectionne automatiquement le meilleur modèle."""
        candidates: Dict[str, ForecasterType] = {}
        scores: Dict[str, float] = {}

        try:
            lr = LinearRegressionForecaster()
            lr.product_id = product_id
            scores["linear"] = lr.evaluate(series)["rmse"]
            lr.fit(series)
            candidates["linear"] = lr
        except Exception as e:
            logger.warning(f"Régression linéaire échouée : {e}")

        if len(series) >= 20:
            try:
                arima = ARIMAForecaster()
                arima.product_id = product_id
                scores["arima"] = arima.evaluate(series)["rmse"]
                arima.fit(series)
                candidates["arima"] = arima
            except Exception as e:
                logger.warning(f"ARIMA échoué : {e}")

        if len(series) >= 14:
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
        if product_id in self._cache:
            return self._cache[product_id].predict(n_days)

        for cls in (SARIMAForecaster, ARIMAForecaster, LinearRegressionForecaster):
            path = self.models_dir / f"{product_id}_{cls.__name__}.pkl"
            if path.exists():
                forecaster = cls.load(path)
                self._cache[product_id] = forecaster
                return forecaster.predict(n_days)

        if history_csv is not None:
            forecaster = self.train(history_csv, product_id, model="auto")
            return forecaster.predict(n_days)

        raise RuntimeError(
            f"Aucun modèle trouvé pour {product_id}, et pas d'historique fourni."
        )

    def get_model_info(self, product_id: str) -> dict:
        """
        Retourne les informations sur le modèle utilisé pour ce produit.

        Returns:
            Dict avec 'model_name', 'icon', 'color', 'description'.
        """
        if product_id not in self._cache:
            for cls in (SARIMAForecaster, ARIMAForecaster, LinearRegressionForecaster):
                path = self.models_dir / f"{product_id}_{cls.__name__}.pkl"
                if path.exists():
                    self._cache[product_id] = cls.load(path)
                    break

        if product_id not in self._cache:
            raise RuntimeError(f"Aucun modèle pour {product_id}.")

        forecaster = self._cache[product_id]
        class_name = forecaster.__class__.__name__

        info_map = {
            "LinearRegressionForecaster": {
                "model_name": "Régression Linéaire",
                "icon": "📐",
                "color": "#0ea5e9",
                "description": (
                    "Capture les tendances linéaires (croissance ou décroissance "
                    "régulière de la demande). Modèle simple et rapide, idéal "
                    "pour les produits avec un historique court ou une demande "
                    "très stable."
                ),
            },
            "ARIMAForecaster": {
                "model_name": "ARIMA",
                "icon": "📈",
                "color": "#8b5cf6",
                "description": (
                    "AutoRegressive Integrated Moving Average. Capture les "
                    "dépendances temporelles complexes dans la série. Adapté "
                    "aux produits avec des dynamiques non-linéaires mais sans "
                    "saisonnalité marquée."
                ),
            },
            "SARIMAForecaster": {
                "model_name": "SARIMA",
                "icon": "🔄",
                "color": "#10b981",
                "description": (
                    "Seasonal ARIMA. Ajoute une composante saisonnière à ARIMA. "
                    "Idéal pour les produits avec des cycles réguliers "
                    "(hebdomadaires, mensuels). Le modèle le plus complet."
                ),
            },
        }

        return info_map.get(class_name, {
            "model_name": class_name,
            "icon": "🤖",
            "color": "#64748b",
            "description": "Modèle de prévision.",
        })

    def evaluate_model(
        self,
        product_id: str,
        history_csv: Path,
        test_ratio: float = 0.2,
    ) -> dict:
        """
        Évalue le modèle d'un produit sur un split train/test temporel.

        Méthodologie : on entraîne sur les premiers (1-test_ratio) % de l'historique,
        on prédit les test_ratio % derniers (qu'on connaît déjà), on compare.

        Args:
            product_id: Identifiant du produit.
            history_csv: Chemin vers l'historique de demande.
            test_ratio: Proportion de la fin de série utilisée comme test (0.2 = 20%).

        Returns:
            Dict avec les métriques et les séries (réel vs prédit) pour graphique.
        """
        df = self._load_history(history_csv)
        series = self._get_product_series(df, product_id)

        n = len(series)
        n_test = max(1, int(n * test_ratio))
        train_series = series.iloc[:-n_test]
        test_series = series.iloc[-n_test:]

        # Récupère le type de modèle utilisé
        if product_id not in self._cache:
            self.predict(product_id, n_days=1, history_csv=history_csv)
        forecaster_class = self._cache[product_id].__class__

        # Réentraîne un modèle de même type sur le train uniquement
        eval_forecaster = forecaster_class()
        eval_forecaster.product_id = product_id
        eval_forecaster.fit(train_series)

        # Prédit la période de test
        predictions = eval_forecaster.predict(n_test)

        # Aligne les séries pour comparaison
        actual_values = test_series.values
        predicted_values = predictions.values[:len(actual_values)]

        # Calcul des métriques
        errors = actual_values - predicted_values
        abs_errors = np.abs(errors)
        squared_errors = errors ** 2

        mae = float(np.mean(abs_errors))
        rmse = float(np.sqrt(np.mean(squared_errors)))

        # MAPE : on évite la division par zéro
        non_zero_mask = actual_values != 0
        if non_zero_mask.sum() > 0:
            mape = float(
                np.mean(
                    np.abs(errors[non_zero_mask] / actual_values[non_zero_mask])
                ) * 100
            )
        else:
            mape = 0.0

        # Score de fiabilité sur 100 : 100 = parfait, 0 = très mauvais
        reliability_score = max(0.0, min(100.0, 100.0 - mape))

        return {
            "mae": round(mae, 2),
            "rmse": round(rmse, 2),
            "mape": round(mape, 2),
            "reliability_score": round(reliability_score, 1),
            "test_dates": test_series.index.tolist(),
            "actual_values": actual_values.tolist(),
            "predicted_values": predicted_values.tolist(),
            "n_train": len(train_series),
            "n_test": n_test,
            "test_ratio": test_ratio,
        }

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