GAME_WIDTH = 200
GAME_HEIGHT = 400
BLOCK_SIZE = 20
COLUMNS = GAME_WIDTH // BLOCK_SIZE
ROWS = GAME_HEIGHT // BLOCK_SIZE

LIGHT_BLUE = (1, 237, 250)  
YELLOW = (254, 251, 52)   
PURPLE = (120, 37, 111)      
GREEN = (83, 218, 63)        
RED = (253, 63, 89)          
BLUE = (72, 93, 197)          
ORANGE = (254, 72, 25)  
WHITE = (255, 255, 255)   
BLACK = (0, 0, 0)
GRAY = (192, 192, 192)

COLORS = [
    LIGHT_BLUE, YELLOW, PURPLE, GREEN, RED, BLUE, ORANGE
] 

SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1, 1, 1], [0, 1, 0]],
    [[0, 1 ,1], [1, 1, 0]],
    [[1, 1, 0], [0, 1, 1]],
    [[1, 0], [1, 0], [1, 1]],
    [[0, 1], [0, 1], [1, 1]]
]       