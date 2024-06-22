import pygame
import random
import copy

# Initialize pygame
pygame.init()

# Screen dimensions
GRID_SIZE = 30
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
PANEL_WIDTH = 150
TOTAL_WIDTH = SCREEN_WIDTH + PANEL_WIDTH * 2

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (50, 50, 50)
COLORS = {
    'I': (64, 194, 146),
    'J': (101, 77, 216),
    'L': (199, 117, 67),
    'O': (191, 168, 63),
    'T': (178, 78, 167),
    'Z': (193, 65, 71),
    'S': (143, 191, 64)
}

# Shapes (Tetris pieces) with their respective colors
SHAPES = [
    {'shape': [[1, 1, 1, 1]], 'color': COLORS['I'], 'name': 'I'},  # I
    {'shape': [[0, 1, 0], [1, 1, 1]], 'color': COLORS['T'], 'name': 'T'},  # T
    {'shape': [[1, 1, 0], [0, 1, 1]], 'color': COLORS['Z'], 'name': 'Z'},  # Z
    {'shape': [[0, 1, 1], [1, 1, 0]], 'color': COLORS['S'], 'name': 'S'},  # S
    {'shape': [[1, 1], [1, 1]], 'color': COLORS['O'], 'name': 'O'},  # O
    {'shape': [[0, 0, 1], [1, 1, 1]], 'color': COLORS['L'], 'name': 'L'},  # L
    {'shape': [[1, 0, 0], [1, 1, 1]], 'color': COLORS['J'], 'name': 'J'}  # J
]

# Kick tables for each rotation state
I_KICK_TABLE = {
    (0, 1): [(0, 0), (-2, 0), (1, 0), (-2, -1), (1, 2)],
    (1, 0): [(0, 0), (2, 0), (-1, 0), (2, 1), (-1, -2)],
    (1, 2): [(0, 0), (-1, 0), (2, 0), (-1, 2), (2, -1)],
    (2, 1): [(0, 0), (1, 0), (-2, 0), (1, -2), (-2, 1)],
    (2, 3): [(0, 0), (2, 0), (-1, 0), (2, 1), (-1, -2)],
    (3, 2): [(0, 0), (-2, 0), (1, 0), (-2, -1), (1, 2)],
    (3, 0): [(0, 0), (1, 0), (-2, 0), (1, -2), (-2, 1)],
    (0, 3): [(0, 0), (-1, 0), (2, 0), (-1, 2), (2, -1)],
    (0, 2): [(0, 0)],  # Add entries for 180-degree rotations
    (1, 3): [(0, 0)],
    (2, 0): [(0, 0)],
    (3, 1): [(0, 0)]
}

JLSTZ_KICK_TABLE = {
    (0, 1): [(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)],
    (1, 0): [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)],
    (1, 2): [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)],
    (2, 1): [(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)],
    (2, 3): [(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)],
    (3, 2): [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)],
    (3, 0): [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)],
    (0, 3): [(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)],
    (0, 2): [(0, 0)],  # Add entries for 180-degree rotations
    (1, 3): [(0, 0)],
    (2, 0): [(0, 0)],
    (3, 1): [(0, 0)]
}

class Tetris:
    def __init__(self):
        self.screen = pygame.display.set_mode((TOTAL_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()
        self.reset_game()

    def reset_game(self):
        self.grid = [[0] * (SCREEN_WIDTH // GRID_SIZE) for _ in range(SCREEN_HEIGHT // GRID_SIZE)]
        self.bag = self.generate_bag()
        self.current_shape = self.new_shape()
        self.shape_position = [0, (SCREEN_WIDTH // GRID_SIZE) // 2 - 2]  # Spawning two tiles from the left
        self.hold_shape = None
        self.hold_used = False
        self.upcoming_shapes = [self.new_shape() for _ in range(5)]
        self.rotation_state = 0  # Add rotation state

    def generate_bag(self):
        bag = SHAPES[:]
        random.shuffle(bag)
        return bag

    def new_shape(self):
        if not self.bag:
            self.bag = self.generate_bag()
        return copy.deepcopy(self.bag.pop())

    def draw_grid(self):
        for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
            for x in range(PANEL_WIDTH, SCREEN_WIDTH + PANEL_WIDTH, GRID_SIZE):
                pygame.draw.rect(self.screen, WHITE, (x, y, GRID_SIZE, GRID_SIZE), 1)

    def draw_shape(self, shape_info, position):
        shape, color = shape_info['shape'], shape_info['color']
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(self.screen, color, (
                        (position[1] + x) * GRID_SIZE + PANEL_WIDTH,
                        (position[0] + y) * GRID_SIZE,
                        GRID_SIZE, GRID_SIZE))

    def draw_locked_shapes(self):
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell:
                    color = cell['color']
                    pygame.draw.rect(self.screen, color, (
                        x * GRID_SIZE + PANEL_WIDTH,
                        y * GRID_SIZE,
                        GRID_SIZE, GRID_SIZE))

    def draw_hold_shape(self):
        if self.hold_shape:
            shape, color = self.hold_shape['shape'], self.hold_shape['color']
            for y, row in enumerate(shape):
                for x, cell in enumerate(row):
                    if cell:
                        pygame.draw.rect(self.screen, color, (
                            (x + 1) * GRID_SIZE,
                            (y + 1) * GRID_SIZE,
                            GRID_SIZE, GRID_SIZE))

    def draw_upcoming_shapes(self):
        for i, shape_info in enumerate(self.upcoming_shapes):
            shape, color = shape_info['shape'], shape_info['color']
            for y, row in enumerate(shape):
                for x, cell in enumerate(row):
                    if cell:
                        pygame.draw.rect(self.screen, color, (
                            (x + (SCREEN_WIDTH // GRID_SIZE) + 1) * GRID_SIZE + PANEL_WIDTH,
                            (y + i * 4 + 1) * GRID_SIZE,
                            GRID_SIZE, GRID_SIZE))

    def move_shape(self, dx, dy):
        self.shape_position[0] += dy
        self.shape_position[1] += dx
        if self.check_collision():
            self.shape_position[0] -= dy
            self.shape_position[1] -= dx
            if dy == 1:  # If collision happened while moving down
                self.lock_shape()
                self.clear_lines()
                self.current_shape = self.upcoming_shapes.pop(0)
                self.upcoming_shapes.append(self.new_shape())
                self.shape_position = [0, (SCREEN_WIDTH // GRID_SIZE) // 2 - 2]
                self.hold_used = False
                self.rotation_state = 0  # Reset rotation state

    def rotate_shape(self, direction):
        original_shape = copy.deepcopy(self.current_shape['shape'])
        if direction == "clockwise":
            new_shape = [list(row) for row in zip(*original_shape[::-1])]
            new_rotation_state = (self.rotation_state + 1) % 4
        elif direction == "counterclockwise":
            new_shape = [list(row) for row in zip(*original_shape)][::-1]
            new_rotation_state = (self.rotation_state - 1) % 4
        elif direction == "180":
            new_shape = [list(row) for row in zip(*original_shape[::-1])]
            new_shape = [list(row) for row in zip(*new_shape[::-1])]
            new_rotation_state = (self.rotation_state + 2) % 4

        kicks = self.get_kicks(self.current_shape['name'], self.rotation_state, new_rotation_state)
        for dx, dy in kicks:
            self.current_shape['shape'] = new_shape
            self.shape_position[0] += dy
            self.shape_position[1] += dx
            if not self.check_collision():
                self.rotation_state = new_rotation_state
                return
            self.shape_position[0] -= dy
            self.shape_position[1] -= dx
        self.current_shape['shape'] = original_shape

    def get_kicks(self, shape_name, rotation_state, new_rotation_state):
        if shape_name == 'I':
            return I_KICK_TABLE.get((rotation_state, new_rotation_state), [(0, 0)])
        elif shape_name in ['J', 'L', 'S', 'T', 'Z']:
            return JLSTZ_KICK_TABLE.get((rotation_state, new_rotation_state), [(0, 0)])
        return [(0, 0)]

    def hard_drop(self):
        while not self.check_collision():
            self.shape_position[0] += 1
        self.shape_position[0] -= 1
        self.lock_shape()
        self.clear_lines()
        self.current_shape = self.upcoming_shapes.pop(0)
        self.upcoming_shapes.append(self.new_shape())
        self.shape_position = [0, (SCREEN_WIDTH // GRID_SIZE) // 2 - 2]
        self.hold_used = False
        self.rotation_state = 0  # Reset rotation state

    def hold_piece(self):
        if not self.hold_used:
            if self.hold_shape:
                self.current_shape, self.hold_shape = self.hold_shape, copy.deepcopy(self.current_shape)
                self.shape_position = [0, (SCREEN_WIDTH // GRID_SIZE) // 2 - 2]
                self.rotation_state = 0  # Reset rotation state
            else:
                self.hold_shape = copy.deepcopy(self.current_shape)
                self.current_shape = self.upcoming_shapes.pop(0)
                self.upcoming_shapes.append(self.new_shape())
                self.shape_position = [0, (SCREEN_WIDTH // GRID_SIZE) // 2 - 2]
                self.rotation_state = 0  # Reset rotation state
            self.hold_used = True

    def check_collision(self):
        shape = self.current_shape['shape']
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    if (y + self.shape_position[0] >= len(self.grid) or
                            x + self.shape_position[1] < 0 or
                            x + self.shape_position[1] >= len(self.grid[0]) or
                            self.grid[y + self.shape_position[0]][x + self.shape_position[1]]):
                        return True
        return False

    def lock_shape(self):
        shape = self.current_shape['shape']
        color = self.current_shape['color']
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    self.grid[y + self.shape_position[0]][x + self.shape_position[1]] = {'shape': cell, 'color': color}

    def clear_lines(self):
        new_grid = [row for row in self.grid if any(cell == 0 for cell in row)]
        lines_cleared = len(self.grid) - len(new_grid)
        new_grid = [[0] * (SCREEN_WIDTH // GRID_SIZE) for _ in range(lines_cleared)] + new_grid
        self.grid = new_grid

    def run(self):
        running = True
        fall_time = 0
        fall_speed = 500  # milliseconds per fall step
        while running:
            self.screen.fill(BLACK)
            pygame.draw.rect(self.screen, GREY, (0, 0, PANEL_WIDTH, SCREEN_HEIGHT))  # Left panel
            pygame.draw.rect(self.screen, GREY, (SCREEN_WIDTH + PANEL_WIDTH, 0, PANEL_WIDTH, SCREEN_HEIGHT))  # Right panel
            self.draw_grid()
            self.draw_shape(self.current_shape, self.shape_position)
            self.draw_locked_shapes()
            self.draw_hold_shape()
            self.draw_upcoming_shapes()
            current_time = pygame.time.get_ticks()

            if current_time - fall_time > fall_speed:
                self.move_shape(0, 1)
                fall_time = current_time

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.move_shape(-1, 0)
                    elif event.key == pygame.K_RIGHT:
                        self.move_shape(1, 0)
                    elif event.key == pygame.K_DOWN:
                        self.move_shape(0, 1)
                    elif event.key == pygame.K_SPACE:
                        self.hard_drop()
                    elif event.key == pygame.K_UP:
                        self.rotate_shape("clockwise")
                    elif event.key == pygame.K_w:
                        self.rotate_shape("counterclockwise")
                    elif event.key == pygame.K_e:
                        self.rotate_shape("180")
                    elif event.key == pygame.K_r:
                        self.reset_game()
                    elif event.key == pygame.K_c:
                        self.hold_piece()
            self.clock.tick(60)
            pygame.display.flip()
        pygame.quit()

if __name__ == "__main__":
    Tetris().run()
