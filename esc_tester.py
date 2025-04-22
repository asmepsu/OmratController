import pigpio
import time

pi = pigpio.pi()

if not pi.connected:
    print("Failed to connect to Pigpio daemon!")
    exit()

ESC_PIN = 18  # BCM GPIO18 (physical pin 12)
FREQUENCY = 50

# Calibration sequence
def calibrate_esc():
    print("Calibrating ESC...")
    pi.set_servo_pulsewidth(ESC_PIN, 2000)  # Max throttle
    time.sleep(2)
    pi.set_servo_pulsewidth(ESC_PIN, 1000)  # Min throttle
    time.sleep(2)
    pi.set_servo_pulsewidth(ESC_PIN, 1500)  # Neutral
    time.sleep(2)
    print("Calibration complete.")

try:
    calibrate_esc()
    
    print("Testing ESC...")
    pi.set_servo_pulsewidth(ESC_PIN, 1600)  # Slight forward
    time.sleep(4)
    pi.set_servo_pulsewidth(ESC_PIN, 1400)  # Slight reverse
    time.sleep(4)
    
finally:
    pi.set_servo_pulsewidth(ESC_PIN, 0)  # Disable servo pulses
    pi.stop()