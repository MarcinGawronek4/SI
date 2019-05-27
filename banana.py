import constants


class Banana:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 0
        self.image = constants.S_BANANA
        self.drawable = True
        self.walkcost = 3

    def __str__(self):
        return "Table x: " + str(self.x) + " y: " + str(self.y)
