from config.constants import COLUMNS, ROWS

class Tetrimino():
    def __init__(self, shape, color):
        self.shape = shape
        self.color = color
        self.x = (COLUMNS // 2) - (len(self.shape[0]) // 2)
        self.y = 0
        
    def rotate(self):
        transposed = list(zip(*self.shape))
        self.shape = [list(row)[::-1] for row in transposed]
        
    def check_collision(self, grid):
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    if x + self.x < 0 or x + self.x >= COLUMNS or y + self.y >= ROWS:
                        return True
                    if grid[y + self.y][x + self.x] != (0, 0, 0) and y + self.y >= 0:
                        return True
        return False
    
    def place_tetrimino(self, grid):
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell == 1:
                    if self.y + y >= 0 and self.y + y <= ROWS and self.x + x >= 0 and self.x + x <= COLUMNS:
                        grid[self.y + y][self.x + x] = self.color
    
    def default_y(self):
        return 0 - len(self.shape)