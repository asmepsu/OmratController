from components import ESC


class OmRat():
    def __init__(self, name):
        self.name = name
        self.ESC = ESC(17)

    def move(self):
        self.ESC.forward(0.5)
        print(self.name, "is moving")