import pygame
import time

def main():
    # Initialize pygame
    pygame.init()
    pygame.joystick.init()
    
    # Check for controllers
    while pygame.joystick.get_count() == 0:
        print("No controllers detected! Connect your DS4 via USB or Bluetooth.")
        print("On Windows: Use DS4Windows for Bluetooth")
        print("On RPi: Use bluetoothctl to pair your controller")
        print("Retrying in 3 seconds... (Ctrl+C to quit)")
        time.sleep(3)
        pygame.joystick.init()  # Reinitialize to detect new controllers
    
    # Initialize the controller
    controller = pygame.joystick.Joystick(0)
    controller.init()
    
    print(f"Controller connected: {controller.get_name()}")
    print("Press the PS button (Button 12) + Share button (Button 8) to exit")
    
    try:
        while True:
            pygame.event.pump()  # Process events
            
            # Get all button states (DS4 has 13 buttons)
            buttons = [controller.get_button(i) for i in range(min(controller.get_numbuttons(), 13))]
            
            # Get analog stick values
            axes = [controller.get_axis(i) for i in range(min(controller.get_numaxes(), 6))]
            
            # Get D-pad values (if available)
            hat = controller.get_hat(0) if controller.get_numhats() > 0 else (0, 0)
            
            # Clear screen and print values
            print("\033[H\033[J")  # Clears terminal (works on Windows Terminal and RPi)
            print("=== DualShock 4 Controller Input ===")
            print(f"Buttons: {buttons}")
            print(f"Axes: {[f'{x:.2f}' for x in axes]}")
            print(f"D-Pad: {hat}")
            
            # Exit on PS + Share buttons (Windows and RPi compatible)
            if buttons[12] and buttons[8]:  # PS + Share buttons
                print("\nPS + Share pressed. Exiting...")
                break
                
            time.sleep(0.05)
            
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        pygame.quit()

if __name__ == "__main__":
    main()