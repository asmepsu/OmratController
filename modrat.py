from components import ESC
from components import SteeringServo

class ModRat():
    def __init__(self):
        self.left_drive = ESC(signal_pin=18)
        self.right_drive = ESC(signal_pin=11)
        
    def throttle(self, drive: float, turn: float):
        """
        Controls the movement of the tank treads.
        
        Args:
            drive: Forward/backward speed (-1.0 to 1.0, where 1.0 is full forward)
            turn: Left/right turn (-1.0 to 1.0, where 1.0 is full right)
        """
        # Clamp values to valid range [-1.0, 1.0]
        drive = max(-1.0, min(1.0, drive))
        turn = max(-1.0, min(1.0, turn))
        
        # Calculate left and right motor speeds
        left_speed = drive - turn
        right_speed = drive + turn
        
        # Normalize speeds to stay within [-1.0, 1.0] (optional but recommended)
        max_speed = max(abs(left_speed), abs(right_speed))
        if max_speed > 1.0:
            left_speed /= max_speed
            right_speed /= max_speed
        
        # Send commands to ESCs
        self.left_drive.throttle(left_speed)
        self.right_drive.throttle(right_speed)

    
    