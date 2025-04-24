import pigpio
import threading
from time import sleep
import pygame

class ESC:
    def __init__(self, pi, signal_pin, min_pulse=1000, max_pulse=2000, frequency=50):
        """Initialize ESC with pigpio instance"""
        self.pi = pi
        self.signal_pin = signal_pin
        self.min_pulse = min_pulse
        self.max_pulse = max_pulse
        self.frequency = frequency
        
        # Configure GPIO
        self.pi.set_mode(self.signal_pin, pigpio.OUTPUT)
        self.pi.set_PWM_frequency(self.signal_pin, self.frequency)
        self.arm()

    def arm(self):
        """Standard ESC arming sequence"""
        self.set_pulse(self.min_pulse)
        sleep(2)
        self.set_pulse(self.max_pulse)
        sleep(2)
        self.set_pulse(self.min_pulse)
        sleep(1)

    def set_pulse(self, pulse_width):
        """Set pulse width in microseconds (safe range)"""
        pulse_width = max(self.min_pulse, min(self.max_pulse, pulse_width))
        self.pi.set_servo_pulsewidth(self.signal_pin, pulse_width)

    def throttle(self, value):
        """Set throttle from -1.0 (full reverse) to 1.0 (full forward)"""
        pulse_width = self.min_pulse + (value + 1) * (self.max_pulse - self.min_pulse) / 2
        self.set_pulse(pulse_width)

class ModRat:
    def __init__(self):
        """Initialize pigpio and all hardware components"""
        self.pi = pigpio.pi()
        if not self.pi.connected:
            raise RuntimeError("Failed to connect to pigpio daemon")
        
        # Initialize ESCs with shared pigpio instance
        self.left_drive = ESC(self.pi, signal_pin=12)
        self.right_drive = ESC(self.pi, signal_pin=11)
        
        # Control variables
        self.running = False
        self.drive_value = 0.0
        self.turn_value = 0.0
        self.lock = threading.Lock()

    def set_throttle(self, drive, turn):
        """Thread-safe throttle setting"""
        with self.lock:
            self.drive_value = max(-1.0, min(1.0, drive))
            self.turn_value = max(-1.0, min(1.0, turn))

    def motor_control_loop(self):
        """Motor control thread running at fixed rate"""
        try:
            while self.running:
                # Get current throttle values
                with self.lock:
                    drive = self.drive_value
                    turn = self.turn_value
                
                # Calculate motor speeds
                left_speed = drive - turn
                right_speed = drive + turn
                
                # Normalize if necessary
                max_speed = max(abs(left_speed), abs(right_speed))
                if max_speed > 1.0:
                    left_speed /= max_speed
                    right_speed /= max_speed
                
                # Send to motors
                self.left_drive.throttle(left_speed)
                self.right_drive.throttle(right_speed)
                
                sleep(0.02)  # 50Hz update rate
                
        except Exception as e:
            print(f"Motor control error: {e}")
            self.running = False

    def start(self):
        """Start motor control thread"""
        self.running = True
        self.motor_thread = threading.Thread(target=self.motor_control_loop)
        self.motor_thread.daemon = True
        self.motor_thread.start()
        print("ModRat motor control started")

    def stop(self):
        """Clean shutdown"""
        self.running = False
        self.set_throttle(0, 0)  # Stop motors
        
        if hasattr(self, 'motor_thread') and self.motor_thread.is_alive():
            self.motor_thread.join(timeout=1)
        
        # Clean up pigpio
        self.pi.set_servo_pulsewidth(18, 0)
        self.pi.set_servo_pulsewidth(11, 0)
        self.pi.stop()
        print("ModRat shutdown complete")

# Controller interface (separate class)
class DS4Controller:
    def __init__(self, modrat):
        import pygame
        self.modrat = modrat
        pygame.init()
        pygame.joystick.init()
        
        while pygame.joystick.get_count() == 0:
            print("Connect DualShock 4 controller...")
            sleep(1)
            pygame.joystick.init()
            
        self.controller = pygame.joystick.Joystick(0)
        self.controller.init()
        print(f"Controller connected: {self.controller.get_name()}")

    def run(self):
        try:
            while self.modrat.running:
                pygame.event.pump()
                
                # Get controller inputs
                left_stick_y = -self.controller.get_axis(1)  # Forward/backward
                right_stick_x = self.controller.get_axis(2)   # Turning
                
                # Update ModRat
                print(f"Drive: {left_stick_y:.2f}, Turn: {right_stick_x:.2f}")
                self.modrat.set_throttle(left_stick_y, right_stick_x)
                
                # Check for PS button exit
                if self.controller.get_button(12):
                    self.modrat.running = False
                
                sleep(0.02)  # 50Hz update
                
        finally:
            pygame.quit()

if __name__ == "__main__":
    robot = ModRat()
    try:
        robot.start()
        controller = DS4Controller(robot)
        controller.run()
    except KeyboardInterrupt:
        print("Shutting down...")
    finally:
        robot.stop()