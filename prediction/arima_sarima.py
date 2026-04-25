"""
Modèles de prévision ARIMA et SARIMA.

ARIMA (AutoRegressive Integrated Moving Average) : capture les dépendances
temporelles dans une série stationnaire.

SARIMA (Seasonal ARIMA) : ajoute une composante saisonnière, idéal pour des
demandes avec des cycles réguliers (semaine, mois, année).
"""

from __future__ import annotations

import warnings
from pathlib import Path
from typing import Optional, Tuple

import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX

# Statsmodels génère beaucoup de warnings sur la convergence — on les masque
warnings.filterwarnings("ignore")


class ARIMAForecaster:
    """Prévisionniste basé sur ARIMA (sans saisonnalité)."""

    def __init__(self, order: Tuple[int, int, int] = (1, 1, 1)) -> None:
        """
        Args:
            order: Tuple (p, d, q) — ordres AR, différenciation, MA.
                   (1, 1, 1) est un bon défaut pour la plupart des séries.
        """
        self.order = order
        self.fitted_model = None
        self.last_date: Optional[pd.Timestamp] = None
        self.product_id: Optional[str] = None

    def fit(self, series: pd.Series) -> "ARIMAForecaster":
        """Entraîne le modèle sur une série temporelle."""
        if series.empty:
            raise ValueError("La série fournie est vide, impossible d'entraîner.")
        if len(series) < 10:
            raise ValueError(
                f"ARIMA nécessite au moins 10 points, reçu {len(series)}."
            )

        model = ARIMA(series, order=self.order)
        self.fitted_model = model.fit()
        self.last_date = series.index[-1]
        return self

    def predict(self, n_days: int) -> pd.Series:
        """Prédit la demande pour les n_days jours à venir."""
        if self.fitted_model is None:
            raise RuntimeError("Le modèle n'a pas été entraîné. Appelle .fit() d'abord.")

        forecast = self.fitted_model.forecast(steps=n_days)
        forecast = np.clip(forecast.values, a_min=0, a_max=None)

        future_dates = pd.date_range(
            start=self.last_date + pd.Timedelta(days=1),
            periods=n_days,
            freq="D",
        )
        return pd.Series(forecast, index=future_dates, name="prediction")

    def evaluate(self, series: pd.Series, test_size: float = 0.2) -> dict:
        """Évalue le modèle en split train/test temporel."""
        n = len(series)
        n_test = max(1, int(n * test_size))
        train, test = series.iloc[:-n_test], series.iloc[-n_test:]

        self.fit(train)
        predictions = self.predict(n_test)

        return {
            "mae": float(mean_absolute_error(test.values, predictions.values)),
            "rmse": float(np.sqrt(mean_squared_error(test.values, predictions.values))),
        }

    def save(self, path: Path) -> None:
        """Sauvegarde le modèle entraîné sur disque."""
        if self.fitted_model is None:
            raise RuntimeError("Aucun modèle à sauvegarder.")
        path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(
            {
                "fitted_model": self.fitted_model,
                "order": self.order,
                "last_date": self.last_date,
                "product_id": self.product_id,
            },
            path,
        )

    @classmethod
    def load(cls, path: Path) -> "ARIMAForecaster":
        """Charge un modèle sauvegardé depuis le disque."""
        data = joblib.load(path)
        forecaster = cls(order=data["order"])
        forecaster.fitted_model = data["fitted_model"]
        forecaster.last_date = data["last_date"]
        forecaster.product_id = data["product_id"]
        return forecaster


class SARIMAForecaster:
    """Prévisionniste basé sur SARIMA (avec saisonnalité)."""

    def __init__(
        self,
        order: Tuple[int, int, int] = (1, 1, 1),
        seasonal_order: Tuple[int, int, int, int] = (1, 1, 1, 7),
    ) -> None:
        """
        Args:
            order: Tuple (p, d, q) pour la partie non saisonnière.
            seasonal_order: Tuple (P, D, Q, s) — ordres saisonniers + période.
                            s=7 pour saisonnalité hebdomadaire,
                            s=12 pour mensuelle, s=365 pour annuelle.
        """
        self.order = order
        self.seasonal_order = seasonal_order
        self.fitted_model = None
        self.last_date: Optional[pd.Timestamp] = None
        self.product_id: Optional[str] = None

    def fit(self, series: pd.Series) -> "SARIMAForecaster":
        """Entraîne le modèle sur une série temporelle."""
        if series.empty:
            raise ValueError("La série fournie est vide, impossible d'entraîner.")

        seasonal_period = self.seasonal_order[3]
        min_required = 2 * seasonal_period
        if len(series) < min_required:
            raise ValueError(
                f"SARIMA avec période {seasonal_period} nécessite au moins "
                f"{min_required} points, reçu {len(series)}."
            )

        model = SARIMAX(
            series,
            order=self.order,
            seasonal_order=self.seasonal_order,
            enforce_stationarity=False,
            enforce_invertibility=False,
        )
        self.fitted_model = model.fit(disp=False)
        self.last_date = series.index[-1]
        return self

    def predict(self, n_days: int) -> pd.Series:
        """Prédit la demande pour les n_days jours à venir."""
        if self.fitted_model is None:
            raise RuntimeError("Le modèle n'a pas été entraîné. Appelle .fit() d'abord.")

        forecast = self.fitted_model.forecast(steps=n_days)
        forecast = np.clip(forecast.values, a_min=0, a_max=None)

        future_dates = pd.date_range(
            start=self.last_date + pd.Timedelta(days=1),
            periods=n_days,
            freq="D",
        )
        return pd.Series(forecast, index=future_dates, name="prediction")

    def evaluate(self, series: pd.Series, test_size: float = 0.2) -> dict:
        """Évalue le modèle en split train/test temporel."""
        n = len(series)
        n_test = max(1, int(n * test_size))
        train, test = series.iloc[:-n_test], series.iloc[-n_test:]

        self.fit(train)
        predictions = self.predict(n_test)

        return {
            "mae": float(mean_absolute_error(test.values, predictions.values)),
            "rmse": float(np.sqrt(mean_squared_error(test.values, predictions.values))),
        }

    def save(self, path: Path) -> None:
        """Sauvegarde le modèle entraîné sur disque."""
        if self.fitted_model is None:
            raise RuntimeError("Aucun modèle à sauvegarder.")
        path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(
            {
                "fitted_model": self.fitted_model,
                "order": self.order,
                "seasonal_order": self.seasonal_order,
                "last_date": self.last_date,
                "product_id": self.product_id,
            },
            path,
        )

    @classmethod
    def load(cls, path: Path) -> "SARIMAForecaster":
        """Charge un modèle sauvegardé depuis le disque."""
        data = joblib.load(path)
        forecaster = cls(order=data["order"], seasonal_order=data["seasonal_order"])
        forecaster.fitted_model = data["fitted_model"]
        forecaster.last_date = data["last_date"]
        forecaster.product_id = data["product_id"]
        return forecaster