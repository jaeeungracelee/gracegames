import pygame
import random

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700
BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
PURPLE = (255, 0, 255)
RED = (255, 0, 0)

SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1, 1], [0, 0, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]]
]

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("tetris!")

class Tetromino:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.shape = random.choice(SHAPES)
        self.color = random.choice([CYAN, BLUE, ORANGE, YELLOW, GREEN, PURPLE, RED])

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def rotate(self):
        self.shape = list(zip(*self.shape[::-1]))

class TetrisGame:
    def __init__(self):
        self.grid = [[BLACK for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = self.new_piece()
        self.game_over = False
        self.score = 0

    def new_piece(self):
        return Tetromino(GRID_WIDTH // 2 - 1, 0)

    def valid_move(self, piece, x, y):
        for i, row in enumerate(piece.shape):
            for j, cell in enumerate(row):
                if cell:
                    if (x + j < 0 or x + j >= GRID_WIDTH or
                        y + i >= GRID_HEIGHT or
                        self.grid[y + i][x + j] != BLACK):
                        return False
        return True

    def lock_piece(self, piece):
        for i, row in enumerate(piece.shape):
            for j, cell in enumerate(row):
                if cell:
                    self.grid[piece.y + i][piece.x + j] = piece.color
        self.clear_lines()
        self.current_piece = self.new_piece()
        if not self.valid_move(self.current_piece, self.current_piece.x, self.current_piece.y):
            self.game_over = True

    def clear_lines(self):
        lines_cleared = 0
        for i, row in enumerate(self.grid):
            if all(cell != BLACK for cell in row):
                del self.grid[i]
                self.grid.insert(0, [BLACK for _ in range(GRID_WIDTH)])
                lines_cleared += 1
        self.score += lines_cleared ** 2 * 100

    def update(self):
        if not self.game_over:
            if self.valid_move(self.current_piece, self.current_piece.x, self.current_piece.y + 1):
                self.current_piece.move(0, 1)
            else:
                self.lock_piece(self.current_piece)

    def draw(self):
        screen.fill(BLACK)
        for y, row in enumerate(self.grid):
            for x, color in enumerate(row):
                pygame.draw.rect(screen, color, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE - 1, BLOCK_SIZE - 1))
        
        for i, row in enumerate(self.current_piece.shape):
            for j, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, self.current_piece.color, 
                                     ((self.current_piece.x + j) * BLOCK_SIZE, 
                                      (self.current_piece.y + i) * BLOCK_SIZE, 
                                      BLOCK_SIZE - 1, BLOCK_SIZE - 1))

        font = pygame.font.Font(None, 36)
        score_text = font.render(f"score: {self.score}", True, WHITE)
        screen.blit(score_text, (SCREEN_WIDTH - 150, 10))

        if self.game_over:
            font = pygame.font.Font(None, 48)
            game_over_text = font.render("game over", True, WHITE)
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 30))

        pygame.display.flip()

def main():
    clock = pygame.time.Clock()
    game = TetrisGame()
    fall_time = 0
    fall_speed = 0.5  

    while True:
        fall_time += clock.get_rawtime()
        clock.tick()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if game.valid_move(game.current_piece, game.current_piece.x - 1, game.current_piece.y):
                        game.current_piece.move(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    if game.valid_move(game.current_piece, game.current_piece.x + 1, game.current_piece.y):
                        game.current_piece.move(1, 0)
                elif event.key == pygame.K_DOWN:
                    if game.valid_move(game.current_piece, game.current_piece.x, game.current_piece.y + 1):
                        game.current_piece.move(0, 1)
                elif event.key == pygame.K_UP:
                    rotated_shape = list(zip(*game.current_piece.shape[::-1]))
                    if game.valid_move(game.current_piece, game.current_piece.x, game.current_piece.y):
                        game.current_piece.rotate()

        if fall_time / 1000 > fall_speed:
            game.update()
            fall_time = 0

        game.draw()

if __name__ == "__main__":
    main()
    pygame.quit()