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
        self.font = pygame.font.SysFont(None, 24)  # Font for rendering text
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
        self.perform_best_move()

    def generate_bag(self):
        bag = SHAPES[:]
        random.shuffle(bag)
        return bag

    def new_shape(self):
        if not self.bag:
            self.bag = self.generate_bag()
        shape = copy.deepcopy(self.bag.pop())
        return shape

    def next_shape(self):
        self.current_shape = self.upcoming_shapes.pop(0)
        self.upcoming_shapes.append(self.new_shape())
        self.shape_position = [0, (SCREEN_WIDTH // GRID_SIZE) // 2 - 2]  # Reset position
        self.rotation_state = 0  # Reset rotation

    def draw_grid(self):
        for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
            for x in range(PANEL_WIDTH, SCREEN_WIDTH + PANEL_WIDTH, GRID_SIZE):
                pygame.draw.rect(self.screen, WHITE, (x, y, GRID_SIZE, GRID_SIZE), 1)
                
                # Draw y-axis labels
                if x == PANEL_WIDTH:
                    label = self.font.render(f"{y // GRID_SIZE}", True, WHITE)
                    self.screen.blit(label, (x - GRID_SIZE, y + GRID_SIZE // 4))
                    
                # Draw x-axis labels
                if y == 0:
                    label = self.font.render(f"{(x - PANEL_WIDTH) // GRID_SIZE}", True, WHITE)
                    self.screen.blit(label, (x + GRID_SIZE // 4, y - GRID_SIZE))

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
                self.next_shape()
                self.hold_used = False
                self.rotation_state = 0  # Reset rotation state
                self.perform_best_move()

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
        self.next_shape()
        self.hold_used = False
        self.rotation_state = 0  # Reset rotation state
        self.perform_best_move()

    def hold_piece(self):
        if not self.hold_used:
            if self.hold_shape:
                self.current_shape, self.hold_shape = self.hold_shape, copy.deepcopy(self.current_shape)
                self.shape_position = [0, (SCREEN_WIDTH // GRID_SIZE) // 2 - 2]
                self.rotation_state = 0  # Reset rotation state
                self.perform_best_move()
            else:
                self.hold_shape = copy.deepcopy(self.current_shape)
                self.next_shape()
                self.shape_position = [0, (SCREEN_WIDTH // GRID_SIZE) // 2 - 2]
                self.rotation_state = 0  # Reset rotation state
                self.perform_best_move()
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

    def evaluate_board(self, grid):
        score = 0
        
        # Count the number of holes
        holes = 0
        holes_by_column = [0] * len(grid[0])
        for col in range(len(grid[0])):
            block_found = False
            for row in range(len(grid)):
                if grid[row][col] != 0:
                    block_found = True
                elif block_found:
                    holes += 1
                    holes_by_column[col] += 1
        
        # Calculate the height of the stack
        stack_height = max([row for row in range(len(grid)) if any(grid[row])], default=-1) + 1
        
        # Calculate the aggregate height
        aggregate_height = sum(next((len(grid) - row for row in range(len(grid)) if grid[row][col]), 0) for col in range(len(grid[0])))
        
        # Calculate the bumpiness
        bumpiness = sum(abs(
            next((len(grid) - row for row in range(len(grid)) if grid[row][col]), 0) - 
            next((len(grid) - row for row in range(len(grid)) if grid[row][col+1]), 0)
        ) for col in range(len(grid[0]) - 1))
        
        # Calculate the number of complete lines
        complete_lines = sum(all(grid[row][col] != 0 for col in range(len(grid[0]))) for row in range(len(grid)))
        
        # Calculate the line clear potential
        line_clear_potential = 0
        for row in range(len(grid)):
            if all(grid[row][col] != 0 for col in range(len(grid[0]))):
                line_clear_potential += 1
        
        # Calculate the landing height of the piece
        landing_height = stack_height - self.shape_position[0]

        # Calculate the number of wells
        wells = 0
        for col in range(1, len(grid[0]) - 1):
            if all(grid[row][col] == 0 and grid[row][col - 1] != 0 and grid[row][col + 1] != 0 for row in range(len(grid))):
                wells += 1
        
        # Assign weights to each metric
        score -= holes * 20
        score -= stack_height * 2
        score -= aggregate_height * 1
        score -= bumpiness * 1
        score -= (wells - 1) * 100  # Penalty for more than one well
        score += complete_lines * 1  # Increased weight for complete lines
        score += line_clear_potential * 50  # Reward for potential future line clears
        score += landing_height * 2  # Reward for lower landing height
        
        # Extra bonus for clearing multiple lines at once
        if complete_lines == 4:
            score += 1000  # Extra bonus for a Tetris (clearing four lines at once)
        elif complete_lines == 3:
            score += 3  # Extra bonus for clearing three lines at once
        elif complete_lines == 2:
            score += 1  # Extra bonus for clearing two lines at once
        
        return score




    def simulate_move(self, shape, position):
        new_grid = copy.deepcopy(self.grid)
        shape_x, shape_y = position
        shape_matrix = shape['shape']
        for y, row in enumerate(shape_matrix):
            for x, cell in enumerate(row):
                if cell:
                    new_grid[shape_y + y][shape_x + x] = {'shape': cell, 'color': shape['color']}
        return new_grid

    def evaluate_move(self, shape, position):
        new_grid = self.simulate_move(shape, position)
        return self.evaluate_board(new_grid)

    def select_best_move(self):
        possible_moves = []
        for rotation in range(4):
            new_shape = copy.deepcopy(self.current_shape)
            for _ in range(rotation):
                new_shape['shape'] = [list(row) for row in zip(*new_shape['shape'][::-1])]
            for col in range(len(self.grid[0]) - len(new_shape['shape'][0]) + 1):
                position = (col, 0)
                while not self.check_collision_at_position(new_shape['shape'], position):
                    position = (position[0], position[1] + 1)
                position = (position[0], position[1] - 1)
                if position[1] >= 0:  # Ensure it's within the grid
                    possible_moves.append((copy.deepcopy(new_shape), position, rotation))
        
        best_score = float('-inf')
        best_move = None
        for shape, position, rotation in possible_moves:
            score = self.evaluate_move(shape, position)
            if score > best_score:
                best_score = score
                best_move = (shape, position, rotation)
        
        return best_move

    def check_collision_at_position(self, shape, position):
        shape_x, shape_y = position
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    if (shape_y + y >= len(self.grid) or
                            shape_x + x < 0 or
                            shape_x + x >= len(self.grid[0]) or
                            self.grid[shape_y + y][shape_x + x]):
                        return True
        return False

    def perform_best_move(self):
        best_move = self.select_best_move()
        
        if self.hold_shape:
            # Evaluate the current best move
            best_move_score = float('-inf')
            if best_move:
                best_shape, best_position, best_rotation = best_move
                best_move_score = self.evaluate_move(best_shape, best_position)
            
            # Evaluate the best move if holding the piece
            original_shape = copy.deepcopy(self.current_shape)
            self.current_shape, self.hold_shape = self.hold_shape, original_shape
            self.shape_position = [0, (SCREEN_WIDTH // GRID_SIZE) // 2 - 2]
            hold_best_move = self.select_best_move()
            hold_best_move_score = float('-inf')
            if hold_best_move:
                hold_shape, hold_position, hold_rotation = hold_best_move
                hold_best_move_score = self.evaluate_move(hold_shape, hold_position)
            
            # Compare the best move and hold best move
            if hold_best_move_score > best_move_score:
                self.perform_hold()
                best_move = hold_best_move
        
        if best_move:
            shape, position, rotation = best_move
            shape_name = shape['name']
            position_x, position_y = position
            print(f"Performing best move for shape {shape_name}: Position ({position_x}, {position_y}) with rotation {rotation}")
            for _ in range(rotation):
                self.rotate_shape("clockwise")
                self.update_display_with_delay()
            self.shape_position = [position_y, position_x]
            self.update_display_with_delay()
            self.hard_drop_with_delay()
        else:
            print("No valid moves found.")

    def perform_hold(self):
        self.hold_piece()
        self.perform_best_move()

    def update_display_with_delay(self):
        self.screen.fill(BLACK)
        pygame.draw.rect(self.screen, GREY, (0, 0, PANEL_WIDTH, SCREEN_HEIGHT))  # Left panel
        pygame.draw.rect(self.screen, GREY, (SCREEN_WIDTH + PANEL_WIDTH, 0, PANEL_WIDTH, SCREEN_HEIGHT))  # Right panel
        self.draw_grid()
        self.draw_shape(self.current_shape, self.shape_position)
        self.draw_locked_shapes()
        self.draw_hold_shape()
        self.draw_upcoming_shapes()
        pygame.display.flip()
        pygame.time.wait(10)  # Delay of 200 milliseconds

    def hard_drop_with_delay(self):
        while not self.check_collision():
            self.shape_position[0] += 1
            self.update_display_with_delay()
        self.shape_position[0] -= 1
        self.lock_shape()
        self.clear_lines()
        self.next_shape()
        self.hold_used = False
        self.rotation_state = 0  # Reset rotation state
        self.perform_best_move()

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
