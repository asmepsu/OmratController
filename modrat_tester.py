from modrat import ModRat
from time import sleep

print("starting modrat_tester.py")
rat = ModRat()
sleep(10)

print("testing")
rat.left_drive.throttle(0)
sleep(1)

print("running test")
while True:
    for i in range(10):
        rat.left_drive.throttle(i/10)
        print(f"Left drive throttle: {i/10}")
        sleep(1)
        rat.left_drive.throttle(0)
        sleep(1)
