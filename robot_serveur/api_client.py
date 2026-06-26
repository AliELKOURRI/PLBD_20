"""
Client Python pour communiquer avec le serveur API du robot.

Utilise par le dashboard Streamlit pour envoyer des commandes
au Raspberry Pi via HTTP.

Usage :
    from robot.api_client import RobotClient
    client = RobotClient("192.168.1.42", 9000)
    client.forward()
    status = client.status()
"""

from __future__ import annotations

from typing import Any

import requests


class RobotClient:
    """Client HTTP pour piloter le robot a distance."""

    def __init__(self, host: str, port: int, timeout: float = 5.0):
        self.base_url = f"http://{host}:{port}"
        self.timeout = timeout

    def _get(self, path: str) -> dict[str, Any]:
        try:
            r = requests.get(f"{self.base_url}{path}", timeout=self.timeout)
            r.raise_for_status()
            return r.json()
        except requests.ConnectionError:
            return {"ok": False, "error": "Robot injoignable"}
        except requests.Timeout:
            return {"ok": False, "error": "Timeout"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def _post(self, path: str, data: dict | None = None) -> dict[str, Any]:
        try:
            r = requests.post(
                f"{self.base_url}{path}",
                json=data or {},
                timeout=self.timeout,
            )
            r.raise_for_status()
            return r.json()
        except requests.ConnectionError:
            return {"ok": False, "error": "Robot injoignable"}
        except requests.Timeout:
            return {"ok": False, "error": "Timeout"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ── Connectivite ──────────────────────────────────────────

    def ping(self) -> dict:
        return self._get("/api/ping")

    def is_connected(self) -> bool:
        r = self.ping()
        return r.get("ok", False)

    # ── Etat ──────────────────────────────────────────────────

    def status(self) -> dict:
        return self._get("/api/status")

    # ── Mouvement ─────────────────────────────────────────────

    def forward(self) -> dict:
        return self._post("/api/move/forward")

    def backward(self) -> dict:
        return self._post("/api/move/backward")

    def left(self) -> dict:
        return self._post("/api/move/left")

    def right(self) -> dict:
        return self._post("/api/move/right")

    def stop(self) -> dict:
        return self._post("/api/move/stop")

    # ── Bras ──────────────────────────────────────────────────

    def pick(self) -> dict:
        return self._post("/api/arm/pick")

    def drop(self) -> dict:
        return self._post("/api/arm/drop")

    def servo(self, channel: int, angle: int) -> dict:
        return self._post("/api/servo", {"channel": channel, "angle": angle})

    # ── Capteurs ──────────────────────────────────────────────

    def distance(self) -> dict:
        return self._get("/api/sensor/distance")

    def line_sensors(self) -> dict:
        return self._get("/api/sensor/line")

    def color(self) -> dict:
        return self._get("/api/sensor/color")

    # ── Mission ───────────────────────────────────────────────

    def start_mission(self, couleur_prendre: str, couleur_deposer: str) -> dict:
        return self._post("/api/mission/start", {
            "couleur_prendre": couleur_prendre,
            "couleur_deposer": couleur_deposer,
        })

    def stop_mission(self) -> dict:
        return self._post("/api/mission/stop")

    # ── Suivi de ligne ────────────────────────────────────────

    def follow_line(self) -> dict:
        return self._post("/api/followline")

    # ── LED / Buzzer ──────────────────────────────────────────

    def led_on(self) -> dict:
        return self._post("/api/led/on")

    def led_off(self) -> dict:
        return self._post("/api/led/off")

    def buzzer(self, duration: float = 1.0) -> dict:
        return self._post("/api/buzzer", {"duration": duration})
