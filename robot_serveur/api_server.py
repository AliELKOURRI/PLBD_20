"""
Serveur API Flask pour le robot — a deployer sur le Raspberry Pi.

Lance-le sur le Pi :
    cd ~/robot_server
    python api_server.py
"""

from __future__ import annotations

import threading
import time

from flask import Flask, jsonify, request

# ── Imports hardware (uniquement sur le Raspberry Pi) ──────────────────
try:
    from picamera2 import Picamera2
    import RPi.GPIO as GPIO
    from board import SCL, SDA
    import busio
    import cv2
    import numpy as np
    from adafruit_pca9685 import PCA9685
    from adafruit_motor import motor, servo
    from gpiozero import DistanceSensor, LED, TonalBuzzer

    HARDWARE_AVAILABLE = True
except ImportError:
    HARDWARE_AVAILABLE = False

app = Flask(__name__)

# ══════════════════════════════════════════════════════════════════════
# ETAT GLOBAL
# ══════════════════════════════════════════════════════════════════════

robot_state = {
    "status": "idle",
    "battery": 100,
    "position": "(0, 0)",
    "mission_active": False,
    "mission_color_pick": None,
    "mission_color_drop": None,
    "mission_etat": "VIDE",
    "last_color_detected": None,
    "distance_cm": None,
    "line_sensors": {"left": 0, "center": 0, "right": 0},
    "arm_state": "repos",
    "log": [],
}

mission_thread = None
mission_stop_event = threading.Event()

# ══════════════════════════════════════════════════════════════════════
# HARDWARE INIT
# ══════════════════════════════════════════════════════════════════════

if HARDWARE_AVAILABLE:
    cam = Picamera2()
    cam.start()
    time.sleep(2)

    tb = TonalBuzzer(18)
    led1 = LED(25)
    led2 = LED(11)
    i2c = busio.I2C(SCL, SDA)

    pca = PCA9685(i2c, address=0x5F)
    pwm = PCA9685(i2c, address=0x5F)
    pca.frequency = 50
    pwm.frequency = 50

    MOTOR_M1_IN1 = 10
    MOTOR_M1_IN2 = 11
    MOTOR_M2_IN1 = 9
    MOTOR_M2_IN2 = 8
    motor1 = motor.DCMotor(pwm.channels[MOTOR_M1_IN1], pwm.channels[MOTOR_M1_IN2])
    motor2 = motor.DCMotor(pwm.channels[MOTOR_M2_IN1], pwm.channels[MOTOR_M2_IN2])
    motor1.decay_mode = motor.SLOW_DECAY
    motor2.decay_mode = motor.SLOW_DECAY

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17, GPIO.IN)
    GPIO.setup(27, GPIO.IN)
    GPIO.setup(22, GPIO.IN)

    Tr = 23
    Ec = 24
    sensor = DistanceSensor(echo=Ec, trigger=Tr, max_distance=2)

    COULEURS_HSV = {
        "Rouge": [(0, 100, 100), (10, 255, 255), (160, 100, 100), (179, 255, 255)],
        "Vert": [(35, 50, 50), (85, 255, 255)],
        "Bleu": [(90, 50, 50), (130, 255, 255)],
        "Jaune": [(20, 100, 100), (35, 255, 255)],
        "Orange": [(10, 100, 100), (20, 255, 255)],
        "Violet": [(130, 50, 50), (160, 255, 255)],
        "Rose": [(160, 50, 50), (170, 255, 255)],
        "Marron": [(10, 50, 20), (20, 200, 200)],
        "Gris": [(0, 0, 50), (179, 50, 200)],
        "Noir": [(0, 0, 0), (179, 255, 50)],
        "Blanc": [(0, 0, 200), (179, 50, 255)],
    }


# ══════════════════════════════════════════════════════════════════════
# FONCTIONS HARDWARE DE BASE
# ══════════════════════════════════════════════════════════════════════

def _log(msg):
    print(f"  [ROBOT] {msg}")
    robot_state["log"] = (robot_state["log"] + [msg])[-20:]


def _set_angle_raw(channel, angle):
    """Bouge un servo SANS log ni sleep — pour la boucle rapide."""
    if not HARDWARE_AVAILABLE:
        return
    s = servo.Servo(pca.channels[channel], min_pulse=500, max_pulse=2400, actuation_range=180)
    s.angle = angle


def _set_angle(channel, angle):
    _log(f"Servo {channel} -> {angle}")
    _set_angle_raw(channel, angle)
    time.sleep(0.5)


def _motor_set(m1, m2):
    """Commande directe moteurs SANS log."""
    if not HARDWARE_AVAILABLE:
        return
    motor1.throttle = m1
    motor2.throttle = m2


def _avancer():
    _log("Avancer")
    _motor_set(0.07, 0.07)


def _stop():
    _log("Stop")
    _motor_set(0, 0)


def _reculer():
    _log("Reculer")
    _motor_set(-0.1, -0.1)


def _checkdist():
    if not HARDWARE_AVAILABLE:
        return 999.0
    return sensor.distance * 100


def _read_line_sensors():
    if not HARDWARE_AVAILABLE:
        return {"left": 0, "center": 0, "right": 0}
    return {
        "left": GPIO.input(17),
        "center": GPIO.input(27),
        "right": GPIO.input(22),
    }


# ══════════════════════════════════════════════════════════════════════
# BRAS ROBOTIQUE
# ══════════════════════════════════════════════════════════════════════

def _prendre():
    _log("=== PRENDRE OBJET ===")
    if not HARDWARE_AVAILABLE:
        return
    _set_angle(4, 130)
    time.sleep(0.5)
    _set_angle(1, 180)
    time.sleep(1)
    _set_angle(2, 150)
    time.sleep(1)
    _set_angle(3, 70)
    time.sleep(0.5)
    _set_angle(4, 50)
    time.sleep(0.5)
    _set_angle(2, 90)
    time.sleep(1)
    _set_angle(3, 90)
    time.sleep(0.5)
    _set_angle(1, 90)
    time.sleep(1)


def _deposer():
    _log("=== DEPOSER OBJET ===")
    if not HARDWARE_AVAILABLE:
        return
    _set_angle(1, 180)
    time.sleep(1)
    _set_angle(2, 150)
    time.sleep(1)
    _set_angle(3, 70)
    time.sleep(0.5)
    _set_angle(4, 130)
    time.sleep(0.5)
    _set_angle(2, 90)
    time.sleep(1)
    _set_angle(3, 90)
    time.sleep(0.5)
    _set_angle(4, 90)
    time.sleep(0.5)
    _set_angle(1, 90)
    time.sleep(1)


# ══════════════════════════════════════════════════════════════════════
# SUIVEUR DE LIGNE
# ══════════════════════════════════════════════════════════════════════

def _suiveur():
    """Suiveur de ligne pour appels manuels (avec logs)."""
    if not HARDWARE_AVAILABLE:
        return
    l, c, r = GPIO.input(17), GPIO.input(27), GPIO.input(22)
    if l == 1 and c == 1 and r == 1:
        _set_angle(0, 80)
    elif l == 1 and c == 1 and r == 0:
        _set_angle(0, 120)
    elif l == 1 and c == 0 and r == 0:
        _set_angle(0, 140)
    elif l == 0 and c == 1 and r == 1:
        _set_angle(0, 70)
    elif l == 0 and c == 1 and r == 0:
        _set_angle(0, 80)
    elif l == 0 and c == 0 and r == 1:
        _set_angle(0, 50)
    elif l == 0 and c == 0 and r == 0:
        _motor_set(0, 0)
        _set_angle(0, 80)


def _suiveur_rapide():
    """Suiveur de ligne pour la boucle mission (SANS log, SANS sleep)."""
    if not HARDWARE_AVAILABLE:
        return False
    l, c, r = GPIO.input(17), GPIO.input(27), GPIO.input(22)
    if l == 1 and c == 1 and r == 1:
        _set_angle_raw(0, 80)
    elif l == 1 and c == 1 and r == 0:
        _set_angle_raw(0, 120)
    elif l == 1 and c == 0 and r == 0:
        _set_angle_raw(0, 140)
    elif l == 0 and c == 1 and r == 1:
        _set_angle_raw(0, 70)
    elif l == 0 and c == 1 and r == 0:
        _set_angle_raw(0, 80)
    elif l == 0 and c == 0 and r == 1:
        _set_angle_raw(0, 50)
    elif l == 0 and c == 0 and r == 0:
        _motor_set(0, 0)
        _set_angle_raw(0, 80)
        return False
    return True


def _rechercher_ligne():
    _log("Recherche ligne...")
    if not HARDWARE_AVAILABLE:
        return
    if GPIO.input(17) == 0 and GPIO.input(27) == 0 and GPIO.input(22) == 0:
        _set_angle(0, 40)
        time.sleep(0.5)
        _avancer()
        time.sleep(3)
        _stop()
        if GPIO.input(17) == 0 and GPIO.input(27) == 0 and GPIO.input(22) == 0:
            _reculer()
            time.sleep(3)
            _stop()
            _set_angle(0, 150)
            time.sleep(0.5)
            _avancer()
            time.sleep(3)
            _stop()
        else:
            _suiveur()


def _reprendre_ligne():
    _log("Reprise ligne...")
    if not HARDWARE_AVAILABLE:
        return
    motor1.throttle = -0.1
    motor2.throttle = -0.1
    time.sleep(1)
    _stop()
    time.sleep(0.2)
    motor1.throttle = -0.5
    motor2.throttle = 0.5
    time.sleep(1)
    _stop()
    time.sleep(0.2)
    motor1.throttle = 0.1
    motor2.throttle = 0.1
    time.sleep(1)
    _stop()

    if GPIO.input(17) == 1 or GPIO.input(27) == 1 or GPIO.input(22) == 1:
        _log("Ligne retrouvee")
        _suiveur()
    else:
        _log("Ligne non trouvee -> recherche")
        _rechercher_ligne()


# ══════════════════════════════════════════════════════════════════════
# EVITEMENT OBSTACLE
# ══════════════════════════════════════════════════════════════════════

def _eviter_obstacle():
    _log("=== CONTOURNEMENT OBSTACLE ===")
    if not HARDWARE_AVAILABLE:
        return

    _stop()
    time.sleep(0.2)

    _log("Tourne droite")
    motor1.throttle = 0.5
    motor2.throttle = -0.5
    time.sleep(3)

    _log("Avance pour depasser")
    motor1.throttle = 0.1
    motor2.throttle = 0.1
    time.sleep(5)

    _log("Tourne gauche")
    motor1.throttle = -0.5
    motor2.throttle = 0.5
    time.sleep(4)

    _log("Realignement")
    motor1.throttle = 0.1
    motor2.throttle = 0.1
    time.sleep(3)

    _stop()
    _log("Fin contournement")


# ══════════════════════════════════════════════════════════════════════
# DETECTION COULEUR
# ══════════════════════════════════════════════════════════════════════

def _detecter_couleur():
    if not HARDWARE_AVAILABLE:
        return "Inconnue"

    frame_rgb = cam.capture_array()
    frame_bgr = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)
    h, w, _ = frame_bgr.shape
    pourcentage = 0.3
    seuil = 500

    x1 = int(w * (0.5 - pourcentage / 2))
    x2 = int(w * (0.5 + pourcentage / 2))
    y1 = int(h * (0.5 - pourcentage / 2))
    y2 = int(h * (0.5 + pourcentage / 2))

    zone = frame_bgr[y1:y2, x1:x2]
    hsv = cv2.cvtColor(zone, cv2.COLOR_BGR2HSV)

    max_pixels = 0
    couleur = "Inconnue"

    for nom, plages in COULEURS_HSV.items():
        if nom == "Rouge":
            low1, high1, low2, high2 = plages
            mask1 = cv2.inRange(hsv, np.array(low1), np.array(high1))
            mask2 = cv2.inRange(hsv, np.array(low2), np.array(high2))
            mask = mask1 + mask2
        else:
            low, high = plages
            mask = cv2.inRange(hsv, np.array(low), np.array(high))

        pixels = cv2.countNonZero(mask)
        if pixels > max_pixels:
            max_pixels = pixels
            couleur = nom

    if max_pixels < seuil:
        couleur = "Inconnue"

    return couleur


# ══════════════════════════════════════════════════════════════════════
# MISSION AUTONOME (boucle principale)
# ══════════════════════════════════════════════════════════════════════

def _mission_loop(couleur_prendre, couleur_deposer):
    """
    Boucle de mission complete :
    1. Avance en suivant la ligne (version rapide, sans sleep)
    2. Verifie les obstacles avec ultrason
    3. Detecte les couleurs pour prendre/deposer
    4. Contourne les obstacles
    """
    robot_state["status"] = "mission"
    robot_state["mission_active"] = True
    robot_state["mission_etat"] = "VIDE"
    etat = "VIDE"
    compteur = 0

    _log(f"=== MISSION DEMARREE : Prendre={couleur_prendre}, Deposer={couleur_deposer} ===")

    try:
        while not mission_stop_event.is_set():
            compteur += 1

            # ── Lecture ultrason ──
            distance = _checkdist()
            robot_state["distance_cm"] = round(distance, 1)
            robot_state["line_sensors"] = _read_line_sensors()

            # ══════════════════════════════════════
            # OBSTACLE PROCHE
            # ══════════════════════════════════════
            if distance < 15:
                _motor_set(0, 0)
                _log(f"Obstacle a {distance:.0f} cm")

                couleur = _detecter_couleur()
                robot_state["last_color_detected"] = couleur
                _log(f"Couleur: {couleur}")

                if couleur == couleur_prendre and etat == "VIDE":
                    _log(">>> PRISE DU PRODUIT")
                    _prendre()
                    etat = "CHARGE"
                    robot_state["arm_state"] = "charge"
                    robot_state["mission_etat"] = "CHARGE"
                    continue

                elif couleur == couleur_deposer and etat == "CHARGE":
                    _log(">>> DEPOT DU PRODUIT")
                    _deposer()
                    etat = "VIDE"
                    robot_state["arm_state"] = "repos"
                    robot_state["mission_etat"] = "VIDE"
                    _log("=== DEPOT REUSSI ===")
                    continue

                else:
                    _log(">>> CONTOURNEMENT")
                    _eviter_obstacle()
                    _rechercher_ligne()
                    continue

            # ══════════════════════════════════════
            # DETECTION COULEUR (toutes les 10 iterations)
            # ══════════════════════════════════════
            if compteur % 10 == 0:
                couleur = _detecter_couleur()
                robot_state["last_color_detected"] = couleur

                if couleur != "Inconnue":
                    if couleur == couleur_prendre and etat == "VIDE":
                        _motor_set(0, 0)
                        _log(f"Zone PRENDRE ({couleur})")
                        _prendre()
                        etat = "CHARGE"
                        robot_state["arm_state"] = "charge"
                        robot_state["mission_etat"] = "CHARGE"
                        continue

                    elif couleur == couleur_deposer and etat == "CHARGE":
                        _motor_set(0, 0)
                        _log(f"Zone DEPOSER ({couleur})")
                        _deposer()
                        etat = "VIDE"
                        robot_state["arm_state"] = "repos"
                        robot_state["mission_etat"] = "VIDE"
                        _log("=== DEPOT REUSSI ===")
                        continue

            # ══════════════════════════════════════
            # NAVIGATION : moteurs + suiveur rapide
            # ══════════════════════════════════════
            _motor_set(0.07, 0.07)
            _suiveur_rapide()

            time.sleep(0.02)

    except Exception as e:
        _log(f"ERREUR MISSION: {e}")

    # Arret propre
    _motor_set(0, 0)
    robot_state["status"] = "idle"
    robot_state["mission_active"] = False
    robot_state["mission_etat"] = "VIDE"
    _log("=== MISSION ARRETEE ===")


# ══════════════════════════════════════════════════════════════════════
# ROUTES API
# ══════════════════════════════════════════════════════════════════════

@app.route("/api/ping", methods=["GET"])
def ping():
    return jsonify({"ok": True, "hardware": HARDWARE_AVAILABLE})


@app.route("/api/status", methods=["GET"])
def get_status():
    robot_state["distance_cm"] = round(_checkdist(), 1)
    robot_state["line_sensors"] = _read_line_sensors()
    return jsonify(robot_state)


@app.route("/api/log", methods=["GET"])
def get_log():
    return jsonify({"log": robot_state["log"]})


# ── Mouvement manuel ──────────────────────────────────────────────────

@app.route("/api/move/forward", methods=["POST"])
def move_forward():
    _avancer()
    robot_state["status"] = "moving"
    return jsonify({"ok": True, "action": "forward"})


@app.route("/api/move/backward", methods=["POST"])
def move_backward():
    _reculer()
    robot_state["status"] = "moving"
    return jsonify({"ok": True, "action": "backward"})


@app.route("/api/move/stop", methods=["POST"])
def move_stop():
    _stop()
    robot_state["status"] = "idle"
    return jsonify({"ok": True, "action": "stop"})


@app.route("/api/move/left", methods=["POST"])
def move_left():
    _log("Tourner gauche")
    if HARDWARE_AVAILABLE:
        motor1.throttle = -0.1
        motor2.throttle = 0.1
    robot_state["status"] = "turning"
    return jsonify({"ok": True, "action": "left"})


@app.route("/api/move/right", methods=["POST"])
def move_right():
    _log("Tourner droite")
    if HARDWARE_AVAILABLE:
        motor1.throttle = 0.1
        motor2.throttle = -0.1
    robot_state["status"] = "turning"
    return jsonify({"ok": True, "action": "right"})


# ── Servo ─────────────────────────────────────────────────────────────

@app.route("/api/servo", methods=["POST"])
def set_servo():
    data = request.get_json(force=True)
    channel = data.get("channel", 0)
    angle = data.get("angle", 90)
    _set_angle(channel, angle)
    return jsonify({"ok": True, "channel": channel, "angle": angle})


# ── Bras ──────────────────────────────────────────────────────────────

@app.route("/api/arm/pick", methods=["POST"])
def arm_pick():
    _prendre()
    robot_state["arm_state"] = "charge"
    return jsonify({"ok": True, "action": "pick"})


@app.route("/api/arm/drop", methods=["POST"])
def arm_drop():
    _deposer()
    robot_state["arm_state"] = "repos"
    return jsonify({"ok": True, "action": "drop"})


# ── Capteurs ──────────────────────────────────────────────────────────

@app.route("/api/sensor/distance", methods=["GET"])
def get_distance():
    d = round(_checkdist(), 1)
    robot_state["distance_cm"] = d
    return jsonify({"distance_cm": d})


@app.route("/api/sensor/line", methods=["GET"])
def get_line():
    s = _read_line_sensors()
    robot_state["line_sensors"] = s
    return jsonify(s)


@app.route("/api/sensor/color", methods=["GET"])
def get_color():
    c = _detecter_couleur()
    robot_state["last_color_detected"] = c
    return jsonify({"color": c})


# ── Suivi de ligne ────────────────────────────────────────────────────

@app.route("/api/followline", methods=["POST"])
def follow_line():
    _avancer()
    _suiveur()
    return jsonify({"ok": True, "action": "follow_line"})


# ── Mission autonome ──────────────────────────────────────────────────

@app.route("/api/mission/start", methods=["POST"])
def start_mission():
    global mission_thread
    if robot_state["mission_active"]:
        return jsonify({"ok": False, "error": "Mission deja active"}), 409

    data = request.get_json(force=True)
    pick = data.get("couleur_prendre", "Rouge")
    drop = data.get("couleur_deposer", "Bleu")

    robot_state["mission_color_pick"] = pick
    robot_state["mission_color_drop"] = drop

    mission_stop_event.clear()
    mission_thread = threading.Thread(
        target=_mission_loop, args=(pick, drop), daemon=True
    )
    mission_thread.start()
    return jsonify({"ok": True, "pick": pick, "drop": drop})


@app.route("/api/mission/stop", methods=["POST"])
def stop_mission():
    if not robot_state["mission_active"]:
        return jsonify({"ok": False, "error": "Aucune mission active"}), 409
    mission_stop_event.set()
    _stop()
    robot_state["status"] = "idle"
    robot_state["mission_active"] = False
    return jsonify({"ok": True, "action": "mission_stopped"})


# ── LED / Buzzer ──────────────────────────────────────────────────────

@app.route("/api/led/on", methods=["POST"])
def led_on():
    _log("LED ON")
    if HARDWARE_AVAILABLE:
        led1.on()
        led2.on()
    return jsonify({"ok": True, "action": "led_on"})


@app.route("/api/led/off", methods=["POST"])
def led_off():
    _log("LED OFF")
    if HARDWARE_AVAILABLE:
        led1.off()
        led2.off()
    return jsonify({"ok": True, "action": "led_off"})


@app.route("/api/buzzer", methods=["POST"])
def buzzer_route():
    data = request.get_json(force=True)
    duration = data.get("duration", 1)
    _log(f"Buzzer {duration}s")
    if HARDWARE_AVAILABLE:
        tb.play("C4")
        time.sleep(duration)
        tb.stop()
    return jsonify({"ok": True, "action": "buzzer", "duration": duration})


# ══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 50)
    print("  Robot API Server")
    print(f"  Hardware: {'OK' if HARDWARE_AVAILABLE else 'SIMULATION'}")
    print("  http://0.0.0.0:9000")
    print("=" * 50)
    app.run(host="0.0.0.0", port=9000, debug=False, threaded=True)
