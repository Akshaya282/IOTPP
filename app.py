from flask import Flask, jsonify, render_template, request
from gpiozero import OutputDevice, PWMLED
from threading import Lock
from config import RELAY_PINS, LED_PWM_PIN, RELAY_ACTIVE_HIGH, PWM_FREQUENCY

app = Flask(__name__)

# Relay modules are often active-LOW. Confirm this with your actual board.
# RELAY_ACTIVE_HIGH=False means GPIO LOW energizes a relay input.
relays = [
    OutputDevice(pin, active_high=RELAY_ACTIVE_HIGH, initial_value=False)
    for pin in RELAY_PINS
]

# PWMLED generates a PWM signal on the selected GPIO pin.
led = PWMLED(LED_PWM_PIN, frequency=PWM_FREQUENCY, initial_value=0)

state_lock = Lock()


@app.route("/")
def index():
    return render_template("index.html")


@app.get("/api/state")
def get_state():
    with state_lock:
        return jsonify({
            "relays": [relay.is_active for relay in relays],
            "brightness": round(led.value * 100)
        })


@app.post("/api/relay/<int:channel>")
def set_relay(channel):
    if channel < 1 or channel > len(relays):
        return jsonify({"error": "Relay channel must be between 1 and 4."}), 404

    data = request.get_json(silent=True) or {}
    if not isinstance(data.get("state"), bool):
        return jsonify({"error": "JSON field 'state' must be true or false."}), 400

    with state_lock:
        relay = relays[channel - 1]
        if data["state"]:
            relay.on()
        else:
            relay.off()
        current_state = relay.is_active

    return jsonify({"channel": channel, "state": current_state})


@app.post("/api/led")
def set_led_brightness():
    data = request.get_json(silent=True) or {}
    try:
        brightness = int(data.get("brightness"))
    except (TypeError, ValueError):
        return jsonify({"error": "Brightness must be an integer from 0 to 100."}), 400

    if not 0 <= brightness <= 100:
        return jsonify({"error": "Brightness must be between 0 and 100."}), 400

    with state_lock:
        led.value = brightness / 100.0

    return jsonify({"brightness": brightness})


@app.errorhandler(500)
def internal_error(_error):
    return jsonify({"error": "Internal server error. Check the Raspberry Pi terminal."}), 500


def cleanup():
    """Turn off all outputs before the application exits."""
    for relay in relays:
        relay.off()
        relay.close()
    led.off()
    led.close()


if __name__ == "__main__":
    try:
        # 0.0.0.0 makes the webpage reachable by other devices on the same Wi-Fi.
        app.run(host="0.0.0.0", port=5000, debug=False)
    except KeyboardInterrupt:
        pass
    finally:
        cleanup()
