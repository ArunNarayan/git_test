import pygame
import random

# Constants
TILE_SIZE = 32

# Simple maze layout (1=wall, 0=dot)
LEVEL_MAP = [
    "11111111111111111111111",
    "10000000001100000000001",
    "10111111101101111111001",
    "10111111101101111111001",
    "10000000000000000000001",
    "10111101111111101111001",
    "10000100000000001000001",
    "11110111101111111011111",
    "10000000000000000000001",
    "11111111111111111111111",
]

ROWS = len(LEVEL_MAP)
COLS = len(LEVEL_MAP[0])
WIDTH, HEIGHT = COLS * TILE_SIZE, ROWS * TILE_SIZE
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)


def load_maze():
    maze = []
    for row in LEVEL_MAP:
        maze.append(list(row))
    return maze


def draw_maze(screen, maze):
    for r, row in enumerate(maze):
        for c, cell in enumerate(row):
            if cell == '1':
                pygame.draw.rect(
                    screen, BLUE,
                    (c * TILE_SIZE, r * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            else:
                pygame.draw.circle(
                    screen, WHITE,
                    (c * TILE_SIZE + TILE_SIZE // 2, r * TILE_SIZE + TILE_SIZE // 2),
                    4)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    maze = load_maze()

    pacman_pos = [1, 1]
    ghost_pos = [COLS - 2, ROWS - 2]
    score = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_LEFT]:
            dx = -1
        elif keys[pygame.K_RIGHT]:
            dx = 1
        elif keys[pygame.K_UP]:
            dy = -1
        elif keys[pygame.K_DOWN]:
            dy = 1

        new_x = pacman_pos[0] + dx
        new_y = pacman_pos[1] + dy
        if maze[new_y][new_x] != '1':
            pacman_pos = [new_x, new_y]
            if maze[new_y][new_x] == '0':
                maze[new_y][new_x] = ' '
                score += 10

        # Ghost random movement
        g_dx, g_dy = random.choice([(1,0), (-1,0), (0,1), (0,-1)])
        g_new_x = ghost_pos[0] + g_dx
        g_new_y = ghost_pos[1] + g_dy
        if 0 <= g_new_x < COLS and 0 <= g_new_y < ROWS and maze[g_new_y][g_new_x] != '1':
            ghost_pos = [g_new_x, g_new_y]

        if pacman_pos == ghost_pos:
            running = False

        screen.fill(BLACK)
        draw_maze(screen, maze)
        pygame.draw.circle(screen, YELLOW,
                           (pacman_pos[0]*TILE_SIZE + TILE_SIZE//2,
                            pacman_pos[1]*TILE_SIZE + TILE_SIZE//2),
                           TILE_SIZE//2 - 2)
        pygame.draw.rect(screen, RED,
                         (ghost_pos[0]*TILE_SIZE,
                          ghost_pos[1]*TILE_SIZE,
                          TILE_SIZE, TILE_SIZE))

        pygame.display.flip()
        clock.tick(FPS)

    print("Game Over! Score:", score)
    pygame.quit()


if __name__ == '__main__':
    main()
