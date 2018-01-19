class Board:
    size = 10
    # coordinates
    x, y = [], []

    # pass x and y as list of coordinate
    def __init__(self, x, y, size=10):
        self.size = size
        self.x = x
        self.y = y
