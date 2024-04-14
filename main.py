from omrat import OmRat
from time import sleep

rat = OmRat()

test_values = [[0.5, -30], [0.75, 0], [1.0, 30]]
# bounce back and forth through the test values
while True:
    for value in test_values:
        rat.move(value[0])
        rat.turn(value[1])
        sleep(3)