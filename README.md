# Raspberry Pi 4 Home Automation Webpage and LED Control

A local-Wi-Fi home automation demonstration using a Raspberry Pi 4, a four-channel relay module, four low-voltage DC loads, and a transistor-driven LED with PWM brightness control.

## Features

- Webpage with four independent relay ON/OFF controls.
- LED brightness slider from 0% to 100%.
- Flask API between the browser and Raspberry Pi GPIO.
- GPIO configuration kept separately in `config.py`.

## Project files

```text
raspberry_pi_home_automation/
├── app.py
├── config.py
├── requirements.txt
├── README.md
├── .gitignore
├── templates/
│   └── index.html
└── static/
    ├── app.js
    └── style.css
```

## Hardware pin mapping

The code uses BCM GPIO numbering:

| Function | BCM GPIO | Physical header pin |
|---|---:|---:|
| Relay IN1 | GPIO 17 | 11 |
| Relay IN2 | GPIO 27 | 13 |
| Relay IN3 | GPIO 22 | 15 |
| Relay IN4 | GPIO 23 | 16 |
| LED PWM driver input | GPIO 18 | 12 |
| 5V (only if relay board supply requirements permit) | 5V | 2 |
| Ground | GND | 6 |

**Important:** This is a suggested mapping based on the project configuration. Confirm it against your actual wiring before running the program. GPIO pins are 3.3V logic and must never receive 5V.

## Relay active level

Many relay modules are active-LOW, so `RELAY_ACTIVE_HIGH = False` is used in `config.py`. Confirm this for your exact relay board. If the board is active-HIGH, change it to `True`.

Do not connect relay module VCC to the Pi's 5V pin unless the module's coil current and power requirements are suitable. Use a separate regulated supply if needed. Follow the relay board's JD-VCC/opto-isolation instructions, if present. Connect grounds as required by the chosen interface.

## LED transistor driver

The example expects an NPN transistor driver controlled from GPIO18 through a base resistor. Use a current-limiting resistor for the LED. Verify the transistor pinout (base, collector, emitter) from its datasheet. The LED and transistor circuit must share a suitable ground reference with the Pi. Do not connect a high-current LED strip directly to a GPIO pin.

## Install and run on Raspberry Pi OS

1. Connect the Raspberry Pi 4 and your control device to the same local Wi-Fi network.
2. Copy this project folder to the Raspberry Pi.
3. Open a terminal in the project folder.
4. Install the system GPIO package and virtual-environment support:

   ```bash
   sudo apt update
   sudo apt install -y python3-gpiozero python3-lgpio python3-venv
   ```

5. Create and activate a virtual environment that can access the system GPIO packages:

   ```bash
   python3 -m venv --system-site-packages .venv
   source .venv/bin/activate
   ```

6. Install Flask:

   ```bash
   pip install -r requirements.txt
   ```

7. Check `config.py` and confirm the GPIO mapping and relay active level.
8. Run the server:

   ```bash
   python app.py
   ```

9. Find the Raspberry Pi's local IP address:

   ```bash
   hostname -I
   ```

10. On a phone or computer connected to the same Wi-Fi, open:

   ```text
   http://RASPBERRY_PI_IP:5000
   ```

   Replace `RASPBERRY_PI_IP` with the IP address printed by `hostname -I`.

Press `Ctrl+C` in the terminal to stop the server. The program turns outputs off during normal shutdown.

## Test checklist

- Test one relay channel at a time with a safe low-voltage load.
- Confirm the webpage shows the correct ON/OFF state.
- Test all four channels independently.
- Move the LED slider through 0%, 25%, 50%, 75%, and 100%.
- Confirm the LED driver and external supply do not overheat.
- Test from a second device on the same Wi-Fi network.

## Safety and limitations

- This project is intended for a trusted local network. The sample app has no login or authentication. Do not expose port 5000 to the public internet or configure router port forwarding.
- Use only low-voltage DC demonstration loads as specified for this project.
- Select a relay module and external power supply rated for the connected loads.
- Do not power motors, pumps, or other high-current devices from Raspberry Pi GPIO or the Pi's 5V header.
- Add suitable flyback/suppression protection for inductive DC loads where required.
- GPIO Zero's PWM implementation and the available pin factory depend on the Raspberry Pi OS configuration. Verify operation on the actual Raspberry Pi before submission.

## API endpoints

- `GET /api/state` — returns relay states and LED brightness.
- `POST /api/relay/1` through `/api/relay/4` — JSON body: `{"state": true}` or `{"state": false}`.
- `POST /api/led` — JSON body: `{"brightness": 0}` through `{"brightness": 100}`.
