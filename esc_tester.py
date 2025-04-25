import pigpio
import time

# Connect to pigpio daemon
pi = pigpio.pi()
if not pi.connected:
    print("Failed to connect to pigpio daemon!")
    exit()

# ESC configuration
ESC_PINS = [12, 13]  # BCM GPIO numbers
MIN_PULSE = 1150     # Minimum pulse width (µs)
MAX_PULSE = 1200     # Maximum pulse width (µs)
FREQUENCY = 50       # 50Hz standard for ESCs

def initialize_escs():
    """Initialize both ESCs with proper arming sequence"""
    for pin in ESC_PINS:
        pi.set_mode(pin, pigpio.OUTPUT)
        pi.set_PWM_frequency(pin, FREQUENCY)
        pi.set_servo_pulsewidth(pin, 1000)
    
    print("Arming ESCs...")
    time.sleep(2)
    
    # Optional calibration sequence
    # for pin in ESC_PINS:
    #     pi.set_servo_pulsewidth(pin, MAX_PULSE)
    # time.sleep(2)
    # pi.set_servo_pulsewidth(pin, MIN_PULSE)
    # time.sleep(2)

def set_pulses(pulse_width):
    """Set pulse width for both ESCs"""
    pulse_width = max(MIN_PULSE, min(MAX_PULSE, pulse_width))
    for pin in ESC_PINS:
        pi.set_servo_pulsewidth(pin, pulse_width)
    print(f"Pulse width: {pulse_width} µs (Both ESCs)")

def cleanup():
    """Stop signals and cleanup"""
    for pin in ESC_PINS:
        pi.set_servo_pulsewidth(pin, 0)  # Stop pulses
    pi.stop()
    print("Cleanup complete - ESCs stopped")

try:
    initialize_escs()
    
    print("Running ESC test on GPIO 12 & 13")
    print(f"Pulse range: {MIN_PULSE}-{MAX_PULSE}µs")
    print("Press Ctrl+C to exit")
    
    while True:
        # Sweep up
        for pulse in range(MIN_PULSE, MAX_PULSE, 10):
            set_pulses(pulse)
            time.sleep(0.1)
        
        # Sweep down
        for pulse in range(MAX_PULSE, MIN_PULSE, -10):
            set_pulses(pulse)
            time.sleep(0.1)

except KeyboardInterrupt:
    print("\nUser interrupted")
finally:
    cleanup()