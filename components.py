import RPi.GPIO as GPIO
import time
import threading

class ESC():
    DIST_PER_SEC = 35.0  # cm/s
    SEC_PER_TURN = 2.087  # seconds per full turn
    POWER_MULTIPLIER = 1.0  # Not directly used in PWM, shown for compatibility

    def __init__(self, signal_pin):
        self.signal_pin = signal_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.signal_pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.signal_pin, 50)  # Initializing PWM at 50Hz
        self.pwm.start(7.5)  # Start PWM with 7.5% duty cycle (neutral position for many ESCs)

    def forward(self, power=0.5):
        # Convert power to a duty cycle within an operational range for the ESC
        # Example assumes linear relationship and needs calibration for specific ESC
        duty_cycle = 7.5 + (power * 5.0)  # Adjust based on calibration
        self.pwm.ChangeDutyCycle(duty_cycle)
        return time.time()

    def stop(self):
        # Stopping the motor by setting it to the neutral position
        # Adjust this value if your ESC's neutral position is different
        self.pwm.ChangeDutyCycle(7.5)

    def forwardDistance(self, dist):
        # Calculate the time needed to travel the distance at the given speed
        time_needed = dist / ESC.DIST_PER_SEC
        self.forward()
        threading.Timer(time_needed, self.stop).start()

    def cleanup(self):
        # Clean up GPIO and stop PWM
        self.pwm.stop()
        GPIO.cleanup()

class SteeringServo():
    def __init__(self, signal_pin):
        self.signal_pin = signal_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.signal_pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.signal_pin, 50)  # Initializing PWM at 50Hz
        self.pwm.start(7.5)  # Start PWM with 7.5% duty cycle (neutral position for many servos)

    def turn(self, angle=0):
        # Convert angle to a duty cycle within an operational range for the servo
        # Example assumes linear relationship and needs calibration for specific servo
        duty_cycle = 7.5 + (angle / 18.0)  # Adjust based on calibration
        self.pwm.ChangeDutyCycle(duty_cycle)
        return time.time()

    def cleanup(self):
        # Clean up GPIO and stop PWM
        self.pwm.stop()
        GPIO.cleanup()

class Camera():
    def __init__(self, name):
        self.name = name