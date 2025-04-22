import pigpio
import time

pi = pigpio.pi()  # Connect to local Pi

if not pi.connected:
    print("Failed to connect to Pigpio daemon!")
    exit()

PWM_PIN = 18  # BCM numbering (GPIO18 = physical pin 12)
FREQUENCY = 50  # 50Hz for servos/ESCs

try:
    print("Starting PWM test...")
    
    while True:
        # 5% duty (1ms pulse)
        print("5% duty (1ms pulse)")
        pi.set_PWM_dutycycle(PWM_PIN, 12.75)  # 5% of 255
        pi.set_PWM_frequency(PWM_PIN, FREQUENCY)
        time.sleep(3)
        
        # 7.5% duty (1.5ms pulse)
        print("7.5% duty (1.5ms pulse)")
        pi.set_PWM_dutycycle(PWM_PIN, 19.125)  # 7.5% of 255
        time.sleep(3)
        
        # 10% duty (2ms pulse)
        print("10% duty (2ms pulse)")
        pi.set_PWM_dutycycle(PWM_PIN, 25.5)  # 10% of 255
        time.sleep(3)

except KeyboardInterrupt:
    print("\nStopping PWM...")
    pi.set_PWM_dutycycle(PWM_PIN, 0)  # Turn off PWM
    pi.stop()