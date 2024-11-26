from config.constants import COLUMNS

class Tetrimino():
    def __init__(self, shape, color):
        self.shape = shape
        self.color = color
        self.x = (COLUMNS // 2) - (len(self.shape[0]) // 2)
        self.y = 0

    def set_y(self, y):
        self.y = y
        
    def rotate(self):
        transposed = list(zip(*self.shape))
        self.shape = [list(row)[::-1] for row in transposed]