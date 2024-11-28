import pygame
from config.constants import COLUMNS, ROWS, BLACK, BLOCK_SIZE
from .utils import downcolor

class GameGrid:
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.grid = [[(0, 0, 0) for _ in range(columns)] for _ in range(rows)]
        
    def delete_lines(self, score, lines_delete):
        for y in range(self.rows - 1, -1, -1):
            full_line = True
            for x in range(COLUMNS):
                if self.grid[y][x] == (0, 0, 0):
                    full_line = False
                    break
            if full_line:
                del self.grid[y]
                self.grid.insert(0, [(0, 0, 0) for _ in range(COLUMNS)])
                score += 10
                lines_delete += 1
                break
        return score, lines_delete
    
    def draw_grid(self, screen):
        temp = 0
        for y in range(ROWS - 1, -1, -1):
            is_count_top = True
            for x in range(COLUMNS - 1, -1, -1):
                color_down = downcolor(self.grid[y][x])
                if self.grid[y][x] == BLACK:
                    pygame.draw.rect(screen, (20, 20, 20), (BLOCK_SIZE * x, BLOCK_SIZE * y, BLOCK_SIZE, BLOCK_SIZE))
                else:
                    pygame.draw.rect(screen, self.grid[y][x], (BLOCK_SIZE * x, BLOCK_SIZE * y, BLOCK_SIZE, BLOCK_SIZE))
                    
                pygame.draw.rect(screen, color_down, (BLOCK_SIZE * x, BLOCK_SIZE * y, BLOCK_SIZE, BLOCK_SIZE), 1)
                if self.grid[y][x] != (0, 0, 0):
                    if is_count_top:
                        temp += 1
                        is_count_top = False
        top_grid = temp
        return top_grid