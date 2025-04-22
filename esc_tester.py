import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)  # Disable warnings
GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)

pwm = GPIO.PWM(12, 50)  # 50Hz
pwm.start(5)  # Start at 5% duty cycle

try:
    print("Initializing...")
    time.sleep(2)
    pwm.ChangeDutyCycle(10)
    time.sleep(2)
    pwm.ChangeDutyCycle(5)
    print("ESC initialized.")
    time.sleep(4)
    
    print("Running...")
    pwm.ChangeDutyCycle(7.5)
    time.sleep(4)
    pwm.ChangeDutyCycle(9)
    
    # Keep PWM active
    while True:
        time.sleep(1)
        
except KeyboardInterrupt:
    pwm.stop()
    GPIO.cleanup()