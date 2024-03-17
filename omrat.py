from components import ESC
from components import SteeringServo

class OmRat():
    def __init__(self):
        self.drive = ESC(signal_pin = 12)
        self.steering = SteeringServo(signal_pin = 13)

    def move(self):
        self.drive.forward(0.5)

    def turn(self, angle):
        self.steering.turn(angle)