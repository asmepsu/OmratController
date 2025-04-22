import pigpio
import time

# Connect to the pigpio daemon
pi = pigpio.pi()

if not pi.connected:
    print("Failed to connect to pigpio daemon!")
    exit()

# Servo configuration
SERVO_PIN = 13  # BCM GPIO 13 (physical pin 33)
MIN_PULSE = 500  # 0 degrees (µs)
MAX_PULSE = 2500  # 180 degrees (µs)
FREQUENCY = 50    # 50Hz (standard for servos)

def set_angle(pulse_width):
    pi.set_servo_pulsewidth(SERVO_PIN, pulse_width)

try:
    print("Starting servo sweep...")
    while True:
        # Sweep from 0 to 180 degrees
        for pulse in range(MIN_PULSE, MAX_PULSE, 10):
            set_angle(pulse)
            print(f"Angle: {round((pulse - 500)/11.1)}°")
            time.sleep(0.01)
        
        # Sweep back from 180 to 0 degrees
        for pulse in range(MAX_PULSE, MIN_PULSE, -10):
            set_angle(pulse)
            print(f"Angle: {round((pulse - 500)/11.1)}°")
            time.sleep(0.01)

except KeyboardInterrupt:
    print("\nStopping servo...")
finally:
    # Clean up
    pi.set_servo_pulsewidth(SERVO_PIN, 0)  # Stop servo pulses
    pi.stop()