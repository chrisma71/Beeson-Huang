import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 300
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Colors
colors = [
    (0, 0, 0),  # Black
    (255, 0, 0),  # Red
    (0, 255, 0),  # Green
    (0, 0, 255),  # Blue
    (255, 255, 0),  # Yellow
    (255, 165, 0),  # Orange
    (128, 0, 128),  # Purple
    (0, 255, 255)  # Cyan
]

# Tetris shapes
shapes = [
    [[1, 1, 1],
     [0, 1, 0]],

    [[0, 2, 2],
     [2, 2, 0]],

    [[3, 3, 0],
     [0, 3, 3]],

    [[4, 4, 4, 4]],

    [[5, 5],
     [5, 5]],

    [[6, 6, 6],
     [6, 0, 0]],

    [[7, 7, 7],
     [0, 0, 7]]
]

# Grid dimensions
grid_width = screen_width // 30
grid_height = screen_height // 30

# Create grid
grid = [[0 for _ in range(grid_width)] for _ in range(grid_height)]

# Game variables
clock = pygame.time.Clock()
fall_time = 0
fall_speed = 0.5


def create_shape():
    return random.choice(shapes)


def draw_grid():
    for y in range(grid_height):
        for x in range(grid_width):
            color = colors[grid[y][x]]
            pygame.draw.rect(screen, color, pygame.Rect(x * 30, y * 30, 30, 30))
            pygame.draw.rect(screen, (128, 128, 128), pygame.Rect(x * 30, y * 30, 30, 30), 1)


def draw_shape(shape, offset):
    shape_color = shape[0][0]
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, colors[shape_color],
                                 pygame.Rect((offset[0] + x) * 30, (offset[1] + y) * 30, 30, 30))
                pygame.draw.rect(screen, (128, 128, 128),
                                 pygame.Rect((offset[0] + x) * 30, (offset[1] + y) * 30, 30, 30), 1)


def check_collision(shape, offset):
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                try:
                    if grid[offset[1] + y][offset[0] + x]:
                        return True
                except IndexError:
                    return True
    return False


def merge_shape(shape, offset):
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                grid[offset[1] + y][offset[0] + x] = cell


def remove_complete_lines():
    global grid
    new_grid = [row for row in grid if any(cell == 0 for cell in row)]
    new_grid = [[0 for _ in range(grid_width)] for _ in range(grid_height - len(new_grid))] + new_grid
    grid = new_grid


current_shape = create_shape()
current_offset = [grid_width // 2 - len(current_shape[0]) // 2, 0]

# Main game loop
running = True
while running:
    screen.fill((0, 0, 0))
    draw_grid()
    draw_shape(current_shape, current_offset)

    fall_time += clock.get_rawtime()
    clock.tick()

    if fall_time / 1000 >= fall_speed:
        current_offset[1] += 1
        if check_collision(current_shape, current_offset):
            current_offset[1] -= 1
            merge_shape(current_shape, current_offset)
            remove_complete_lines()
            current_shape = create_shape()
            current_offset = [grid_width // 2 - len(current_shape[0]) // 2, 0]
            if check_collision(current_shape, current_offset):
                running = False  # Game over
        fall_time = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                current_offset[0] -= 1
                if check_collision(current_shape, current_offset):
                    current_offset[0] += 1
            elif event.key == pygame.K_RIGHT:
                current_offset[0] += 1
                if check_collision(current_shape, current_offset):
                    current_offset[0] -= 1
            elif event.key == pygame.K_DOWN:
                current_offset[1] += 1
                if check_collision(current_shape, current_offset):
                    current_offset[1] -= 1
            elif event.key == pygame.K_UP:
                current_shape = [list(row) for row in zip(*current_shape[::-1])]
                if check_collision(current_shape, current_offset):
                    current_shape = [list(row) for row in zip(*current_shape)[::-1]]

    pygame.display.flip()

pygame.quit()
