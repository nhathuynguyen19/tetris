import pygame, random, os
from modules import Tetrimino, GameGrid
from config.constants import *
from modules.utils import downcolor

pygame.init()

# path
font_regular_path = os.path.join(ASSETS_PATH, 'fonts', 'HomeVideo-BLG6G.ttf')
font_bold_path = os.path.join(ASSETS_PATH, 'fonts', 'HomeVideoBold-R90Dv.ttf')
best_score_file_path = os.path.join(ASSETS_PATH, 'data', 'best_score.txt')
logo_path = os.path.join(ASSETS_PATH, 'images', 'logo.ico')

# font
font_small = pygame.font.Font(font_regular_path, 12)
font_large = pygame.font.Font(font_bold_path, 30)
            
def draw_tetrimino(tetrimino):
    for y, row in enumerate(tetrimino.shape):
        for x, cell in enumerate(row):
                if cell == 1 and not tetrimino.check_collision(game_grid.grid): 
                    color_down = downcolor(tetrimino.color)
                    pygame.draw.rect(screen, tetrimino.color, ((tetrimino.x + x) * BLOCK_SIZE, (tetrimino.y + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                    pygame.draw.rect(screen, color_down, ((tetrimino.x + x) * BLOCK_SIZE, (tetrimino.y + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

def draw_tetrimino_game_table(tetrimino):
    tetrimino.x = 11
    tetrimino.y = 1
    for i in range(random_rotate):
        tetrimino.rotate()
    
    for y, row in enumerate(tetrimino.shape):
        for x, cell in enumerate(row):
            if cell == 1:
                color_down = downcolor(tetrimino.color)
                pygame.draw.rect(screen, tetrimino.color, ((COLUMNS + x + 3 - len(row)/2) * BLOCK_SIZE, ((3 + y - len(tetrimino.shape)/2) * BLOCK_SIZE), BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(screen, color_down, ((COLUMNS + x + 3 - len(row)/2) * BLOCK_SIZE, ((3 + y - len(tetrimino.shape)/2) * BLOCK_SIZE), BLOCK_SIZE, BLOCK_SIZE), 1)
            
def process_events():
    global is_pressed, running, last_move_time, paused_game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.KEYDOWN and not game_over:
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                tetrimino.rotate()
                if tetrimino.check_collision(game_grid.grid):
                    for i in range(3):
                        tetrimino.rotate()
            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                tetrimino.y += 1
                is_pressed = True
                if tetrimino.check_collision(game_grid.grid):
                    tetrimino.y -= 1
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                tetrimino.x -= 1
                is_pressed = True
                if tetrimino.check_collision(game_grid.grid):
                    tetrimino.x += 1
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                tetrimino.x += 1
                is_pressed = True
                if tetrimino.check_collision(game_grid.grid):
                    tetrimino.x -= 1
            if event.key == pygame.K_p:
                paused_game = not paused_game
    
    
    current_time = pygame.time.get_ticks()
    if current_time - last_move_time > move_delay and not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            tetrimino.y += 1
            if is_pressed:
                tetrimino.y -= 1
                is_pressed = False
            if tetrimino.check_collision(game_grid.grid):
                tetrimino.y -= 1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            tetrimino.x -= 1
            if is_pressed:
                tetrimino.x += 1
                is_pressed = False
            if tetrimino.check_collision(game_grid.grid):
                tetrimino.x += 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            tetrimino.x += 1
            if is_pressed:
                tetrimino.x -= 1
                is_pressed = False
            if tetrimino.check_collision(game_grid.grid):
                tetrimino.x -= 1
        
        last_move_time = current_time

def level_up():
    global level_game, lines_deleted
    if score % score_to_level_up == 0 and level_game < 10 and lines_deleted >= 10:
        level_game += 1
        lines_deleted = 0

def render_text():
    texts = [
        (f"Score: {score}", 7),
        (f"Level: {level_game}", 8),
        ("Best Score:", 10),
        (str(best_score), 11),
    ]
    for text, row in texts:
        rendered_text = font_small.render(text, True, WHITE)
        screen.blit(rendered_text, (COLUMNS * BLOCK_SIZE + 20, row * BLOCK_SIZE))
  
def check_tetrimino_bag():
    global tetrimino_bag
    if tetrimino_bag and next_position_tetrimino in tetrimino_bag:
        tetrimino_bag.remove(next_position_tetrimino)
    elif not tetrimino_bag:
        tetrimino_bag = list(range(7))
        random.shuffle(tetrimino_bag)
        
def draw_table_game():
    global screen, table_game
    table_game = pygame.Rect(COLUMNS * BLOCK_SIZE, 0, 6 * BLOCK_SIZE, ROWS * BLOCK_SIZE)
    screen.fill((20, 20, 20), table_game)
    pygame.draw.rect(screen, WHITE, (COLUMNS * BLOCK_SIZE, 0, 6 * BLOCK_SIZE, ROWS * BLOCK_SIZE), 2)
    
def update_best_score():
    global best_score
    if score > best_score:
        best_score = score
        with open(best_score_file_path, "w") as file:
            file.write(str(best_score))
    
screen = pygame.display.set_mode((GAME_WIDTH + BLOCK_SIZE * 6, GAME_HEIGHT))
pygame.display.set_caption("Tetris")
icon_logo = pygame.image.load(logo_path)
pygame.display.set_icon(icon_logo)
clock = pygame.time.Clock()
running = False
game_grid = GameGrid(ROWS, COLUMNS)
tetrimino_bag = [0, 1, 2, 3, 4, 5, 6]
current_position_tetrimino = random.choice(tetrimino_bag)

tetrimino = Tetrimino(SHAPES[current_position_tetrimino], COLORS[current_position_tetrimino])
random_rotate = random.choice([0, 1, 2, 3])
for i in range(random_rotate):
    tetrimino.rotate()
tetrimino.y = tetrimino.default_y()
next_tetrimino = tetrimino
next_position_tetrimino = current_position_tetrimino

frame_count = 0
move_delay = 40
last_move_time = 0
is_pressed = False
top_grid = 0
score = 0
score_to_level_up = 100
level_game = 1
lines_deleted = 0
table_draw = True
get_next_tetrimino = False
tetrimino_is_placed = False
game_over = False
begin_game = True
best_score = 0
table_game = None
paused_game = False

# score file data
if not os.path.exists(best_score_file_path):
    with open(best_score_file_path, 'w') as file:
        file.write("0")
with open(best_score_file_path, 'r') as file:
    best_score = int(file.read())  

while running:
    process_events()
    level_up()
    check_tetrimino_bag()
    draw_table_game()
    
    if begin_game:
        temp_next_tetrimino = next_tetrimino
        next_position_tetrimino = random.choice(tetrimino_bag)
        next_tetrimino_preview = temp_next_tetrimino
    else:
        next_tetrimino_preview = Tetrimino(SHAPES[next_position_tetrimino], COLORS[next_position_tetrimino])
        
    draw_tetrimino_game_table(next_tetrimino_preview)
    render_text()
    
    # each frame
    if frame_count % (22 - level_game*2) == 0:
        
        update_best_score()
        
        if not game_over:
            if not paused_game:
                tetrimino.y += 1
            if tetrimino.check_collision(game_grid.grid) and not game_over:
                tetrimino.y -= 1
                
                # update grid
                if tetrimino_is_placed:
                    tetrimino.place_tetrimino(game_grid.grid)
                    
                # update grid condition
                tetrimino_is_placed = True
                
                # current tetrimino
                if begin_game:
                    tetrimino = temp_next_tetrimino
                    begin_game = False
                else:
                    tetrimino = next_tetrimino
                    
                # after tetrimino
                if not begin_game:
                    next_position_tetrimino = random.choice(tetrimino_bag)
                next_tetrimino = Tetrimino(SHAPES[next_position_tetrimino], COLORS[next_position_tetrimino])
                random_rotate = random.choice([0, 1, 2, 3])
                for i in range(random_rotate):
                    next_tetrimino.rotate()
                next_tetrimino.y = next_tetrimino.default_y()
                
                
    # delete line
    score, lines_deleted = game_grid.delete_lines(score, lines_deleted)
                
    # check game over
    if top_grid >= ROWS:
        game_over = True
        tetrimino_is_placed = False

    #draw game scene
    top_grid = game_grid.draw_grid(screen)
    if not game_over:
        draw_tetrimino(tetrimino)
    
    # after overgame
    if game_over:
        game_over_text = font_large.render("Game Over", True, WHITE)
        screen.blit(game_over_text, (BLOCK_SIZE * COLUMNS // 2 - game_over_text.get_width() // 2, BLOCK_SIZE * ROWS // 2 - game_over_text.get_height() // 2))
    
    # end frame
    pygame.display.flip()
    pygame.draw.rect(screen, BLACK, (0, 0, COLUMNS * BLOCK_SIZE, ROWS * BLOCK_SIZE))
    frame_count += 1
    clock.tick(60)
    
pygame.quit()