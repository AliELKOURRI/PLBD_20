"""
Modèle de prévision par Régression Linéaire.

Capture les tendances simples (croissance/décroissance linéaire de la demande)
mais pas la saisonnalité ni les cycles. Modèle rapide, idéal comme baseline
ou pour les produits avec un historique court.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import joblib
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error


class LinearRegressionForecaster:
    """Prévisionniste basé sur la régression linéaire temporelle."""

    def __init__(self) -> None:
        self.model: Optional[LinearRegression] = None
        self.last_date: Optional[pd.Timestamp] = None
        self.product_id: Optional[str] = None
        self._n_train: int = 0

    def fit(self, series: pd.Series) -> "LinearRegressionForecaster":
        """Entraîne le modèle sur une série temporelle indexée par date."""
        if series.empty:
            raise ValueError("La série fournie est vide, impossible d'entraîner.")

        x = np.arange(len(series)).reshape(-1, 1)
        y = series.values

        self.model = LinearRegression()
        self.model.fit(x, y)
        self.last_date = series.index[-1]
        self._n_train = len(series)
        return self

    def predict(self, n_days: int) -> pd.Series:
        """Prédit la demande pour les n_days jours à venir."""
        if self.model is None or self.last_date is None:
            raise RuntimeError("Le modèle n'a pas été entraîné. Appelle .fit() d'abord.")

        future_dates = pd.date_range(
            start=self.last_date + pd.Timedelta(days=1),
            periods=n_days,
            freq="D",
        )
        future_x = np.arange(self._n_train, self._n_train + n_days).reshape(-1, 1)
        predictions = self.model.predict(future_x)
        predictions = np.clip(predictions, a_min=0, a_max=None)

        return pd.Series(predictions, index=future_dates, name="prediction")

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
        if self.model is None:
            raise RuntimeError("Aucun modèle à sauvegarder.")
        path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(
            {
                "model": self.model,
                "last_date": self.last_date,
                "product_id": self.product_id,
                "n_train": self._n_train,
            },
            path,
        )

    @classmethod
    def load(cls, path: Path) -> "LinearRegressionForecaster":
        """Charge un modèle sauvegardé depuis le disque."""
        data = joblib.load(path)
        forecaster = cls()
        forecaster.model = data["model"]
        forecaster.last_date = data["last_date"]
        forecaster.product_id = data["product_id"]
        forecaster._n_train = data["n_train"]
        return forecaster