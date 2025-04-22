from modrat import ModRat
from time import sleep

rat = ModRat()

rat.left_drive.throttle(0)
sleep(1)

while True:
    for i in range(10):
        rat.left_drive.throttle(i/10)
        sleep(1)
        rat.left_drive.throttle(0)
        sleep(1)
