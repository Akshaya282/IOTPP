"""
Hardware configuration for Raspberry Pi 4.

Pin numbers use BCM GPIO numbering, NOT physical header pin numbers.
Change these values only after checking your actual wiring.
"""

# BCM GPIO numbers connected to relay module IN1, IN2, IN3 and IN4.
RELAY_PINS = [17, 27, 22, 23]

# BCM GPIO18 (physical header pin 12) drives the LED transistor circuit.
LED_PWM_PIN = 18

# Most 5V relay modules are active-LOW, but this MUST be checked on your board.
# False: GPIO LOW = relay ON; GPIO HIGH = relay OFF.
# True:  GPIO HIGH = relay ON; GPIO LOW = relay OFF.
RELAY_ACTIVE_HIGH = False

PWM_FREQUENCY = 1000  # Hz
