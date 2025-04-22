import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)
pwm = GPIO.PWM(12, 50)  # Initializing PWM at 50Hz
pwm.start(5)  # Start PWM with 5% duty cycle (neutral position for many ESCs)
time.sleep(2)
pwm.ChangeDutyCycle(10)
time.sleep(2)
pwm.ChangeDutyCycle(5)

print("ESC initialized.")
time.sleep(4)
pwm.ChangeDutyCycle(7.5)

