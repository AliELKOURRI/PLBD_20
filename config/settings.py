"""
Configuration centralisée du projet.

Toutes les variables de configuration sont définies ici, lues depuis le fichier
.env via Pydantic Settings. Cela garantit :
- Une source unique de vérité (pas de duplication entre fichiers)
- Une validation automatique des types (int, str, Path...)
- Des valeurs par défaut sensées si .env est incomplet
- Un import simple : `from config.settings import settings`
"""

from __future__ import annotations

from pathlib import Path
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


# Racine du projet (calcule depuis ce fichier : config/settings.py -> ../)
PROJECT_ROOT = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    """Configuration globale du projet, validée par Pydantic."""

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # ============ Application ============
    app_name: str = "Smart Predict AI"
    app_version: str = "0.1.0"
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"

    # ============ Chemins de données ============
    data_dir: Path = Field(default=PROJECT_ROOT / "data")
    models_dir: Path = Field(default=PROJECT_ROOT / "data" / "models")

    # ============ Robot Raspberry Pi ============
    pi_host: str = "192.168.1.42"
    pi_port: int = 9000

    # ============ Backend FastAPI (futur) ============
    backend_host: str = "127.0.0.1"
    backend_port: int = 8000

    # ============ Paramètres de prédiction ============
    default_forecast_horizon: int = 7
    min_history_days_for_sarima: int = 14
    min_history_days_for_arima: int = 20

    # ============ Paramètres de stock ============
    low_stock_alert_ratio: float = 1.0

    # ============ Chemins dérivés (propriétés calculées) ============

    @property
    def stock_csv(self) -> Path:
        return self.data_dir / "stock.csv"

    @property
    def commandes_csv(self) -> Path:
        return self.data_dir / "commandes.csv"

    @property
    def fournisseurs_csv(self) -> Path:
        return self.data_dir / "fournisseurs.csv"

    @property
    def historique_csv(self) -> Path:
        return self.data_dir / "raw" / "historique_demande.csv"

    @property
    def backend_url(self) -> str:
        return f"http://{self.backend_host}:{self.backend_port}"


# CETTE LIGNE EST CRUCIALE — c'est elle qui crée l'instance importable
settings = Settings()