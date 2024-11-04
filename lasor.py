import itertools
import copy
import sys
from PIL import Image, ImageDraw
import time

def grid_info(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        inside_grid = False  
        grid_content = []   
        L_value = []
        P_value = []
        A_value = 0
        B_value = 0
        C_value = 0
        for line in file:
            line = line.strip()  
            if line == "GRID START":
                inside_grid = True  
                continue
            if line == "GRID STOP":
                inside_grid = False  
                continue
            if inside_grid:
                grid_content.append(line.split())
            if line.startswith("A"):
                parts = line.split()
                if len(parts) == 2:
                    A_value = int(parts[1])
            if line.startswith("B"):
                parts = line.split()
                if len(parts) == 2:
                    B_value = int(parts[1])
            if line.startswith("C"):
                parts = line.split()
                if len(parts) == 2:
                    C_value = int(parts[1])
            if line.startswith("L"):
                values = line[1:].strip().split()
                if len(values) == 4:
                    L_value.append(tuple(map(int, values)))
                else:
                    print(f"Warning: Invalid laser data format in line: {line}")
            if line.startswith("P"):
                values = line[1:].strip().split()
                if len(values) == 2:
                    P_value.append(tuple(map(int, values)))
                else:
                    print(f"Warning: Invalid point data format in line: {line}")
        if grid_content:
            column = len(grid_content[0])
            row = len(grid_content)
        else:
            print("No grid")
    return grid_content, A_value, B_value, C_value, L_value, P_value, column, row 

class Laser:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.active = True
        self.path = [(x, y)]

    def move(self):
        if self.active:
            self.x += self.vx
            self.y += self.vy
            self.path.append((self.x, self.y))

    def reflect_x(self):
        self.vx = -self.vx
        self.vy = self.vy
    
    def reflect_y(self):
        self.vx = self.vx
        self.vy = -self.vy

    def stop(self):
        self.active = False

    def create_reflected_x(self):
        return Laser(self.x, self.y, -self.vx, self.vy)
    
    def create_reflected_y(self):
        return Laser(self.x, self.y, self.vx, -self.vy)

class Block:
    def __init__(self, type, x, y):
        self.type = type 
        self.x = x
        self.y = y

    def interact_with_laser(self, laser: Laser):
        # Change the direction of the laser based on block's type
        if self.type == 'A':
            if (self.x-1, self.y) in set(laser.path) or (self.x+1, self.y) in set(laser.path):
                laser.reflect_x()
            if (self.x, self.y-1) in set(laser.path) or (self.x, self.y+1) in set(laser.path):
                laser.reflect_y()
        elif self.type == 'B': 
            laser.stop()
        elif self.type == 'C':
            reflected_laser = None
            if (self.x-1, self.y) in set(laser.path) or (self.x+1, self.y) in set(laser.path):
                reflected_laser =  laser.create_reflected_x()
            if (self.x, self.y-1) in set(laser.path) or (self.x, self.y+1) in set(laser.path):
                 reflected_laser =  laser.create_reflected_y()
            return reflected_laser
        return None

class Grid:
    def __init__(self, grid_content, column, row):
        self.grid_content = grid_content
        self.column = column
        self.row = row
        self.width = 2*column+1
        self.length = 2*row+1
        self.grid_blocks = [[None for _ in range(self.width)] for _ in range(self.length)]
        for y in range(row):
            for x in range(column):
                cell = self.grid_content[y][x]
                if cell == 'A' or cell == 'B' or cell == 'C':
                    self.grid_blocks[2*y+1][2*x+1] = Block(cell, 2*x+1, 2*y+1)
                elif cell == 'x':
                    self.grid_blocks[2*y+1][2*x+1] = 'x' 
    
    def place_block(self, block_type, x, y):
        # Place a block at a specific position
        if self.grid_blocks[y][x] is None:
            self.grid_blocks[y][x] = Block(block_type, x, y)
            return True
        return False

def on_grid_check(x, y, grid_blocks):
    return 0 <= x <= len(grid_blocks[0]) and 0 <= y <= len(grid_blocks)

def on_block_check(x, y, block:Block):
    boundary = [(block.x-1, y), (block.x+1, y),(x, block.y+1),(x, block.y-1)]
    return (x,y) in boundary

# Simulate laser propagation and record the laser path
def move_lasers(grid_blocks, lasers):
    active_lasers = copy.deepcopy(lasers)
    all_paths = []
    while active_lasers:
        new_lasers = []
        for laser in active_lasers:
            laser.move()
            x, y = laser.x, laser.y
            if not on_grid_check(x, y, grid_blocks):
                laser.active = False
                continue
            block = grid_blocks[int(y)][int(x)]
            if block and isinstance(block, Block):
                new_laser = block.interact_with_laser(laser)
                if new_laser:
                    new_lasers.append(new_laser)
            all_paths.append((laser.x, laser.y))
        # update laser list
        active_lasers = [laser for laser in active_lasers if laser.active]
        active_lasers.extend(new_lasers)
    return all_paths

# Check if the current block placement allows all target points to be hit
def check_solution(grid_blocks, lasers, targets):
    paths = move_lasers(grid_blocks, lasers)
    hit_targets = set()
    for x, y in paths:
        if (x, y) in targets:
            hit_targets.add((x, y))
    return hit_targets == targets

def solve_lazor_game(file_path):
    grid_content, A_value, B_value, C_value, L_value, P_value, column, row = grid_info(file_path)

    # Create game grid
    game_grid = Grid(grid_content, column, row)
    # Initialize laser list
    lasers = [Laser(x, y, vx, vy) for (x, y, vx, vy) in L_value]
    # Initialize target points
    targets = set((x, y) for (x, y) in P_value)
    # Aquire empty positions
    empty_positions = [(x, y) for y in range(row) for x in range(column) if game_grid.grid_blocks[2*y+1][2*x+1] is None]
    print(empty_positions)
    # Generate all possible block placement combinations.
    total_blocks = A_value + B_value + C_value
    print(total_blocks)
    if total_blocks > len(empty_positions):
        print("Error: Not enough empty positions for the blocks.")
        return None
    block_types = ['A'] * A_value + ['B'] * B_value + ['C'] * C_value
    print(block_types)
    positions_combinations = itertools.combinations(empty_positions, total_blocks)
    block_types_permutations = set(itertools.permutations(block_types))
    print(positions_combinations)
    print(block_types_permutations)
    for positions in positions_combinations:
        for block_types_perm in block_types_permutations:
            # Place block on grid
            for (x, y), block_type in zip(positions, block_types_perm):
                game_grid.place_block(block_type, 2*x+1, 2*y+1)
            # Check if find the solution
            if check_solution(game_grid.grid_blocks, lasers, targets):
                print("Solution found!")
                return game_grid, lasers, targets, column, row
            # Reset grid
            for (x, y) in positions:
                game_grid.grid_blocks[2*y+1][2*x+1] = None
    print("No solution found.")
    return None

# Create image to show solution
def save_solution_image(grid_content, column, row, lasers, targets, image_filename="solution_output.png", cell_size=50):
    grid = Grid(grid_content, column, row)
    width = column * cell_size
    height = row * cell_size
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)

    # Draw the grid and blocks
    for y in range(row):
        for x in range(column):
            top_left = (x * cell_size, y * cell_size)
            bottom_right = ((x + 1) * cell_size, (y + 1) * cell_size)
            cell = grid.grid_blocks[y][x]
            if cell == 'x':
                draw.rectangle([top_left, bottom_right], fill="gray")
            elif cell is None:
                draw.rectangle([top_left, bottom_right], outline="black")
            elif isinstance(cell, Block):
                if cell.block_type == 'A':
                    draw.rectangle([top_left, bottom_right], fill="blue")
                elif cell.block_type == 'B':
                    draw.rectangle([top_left, bottom_right], fill="red")
                elif cell.block_type == 'C':
                    draw.rectangle([top_left, bottom_right], fill="green")

    # draw targets
    for (tx, ty) in targets:
        cx = tx * cell_size
        cy = ty * cell_size
        draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill="orange")

    # draw laser path
    for laser in lasers:
        path = laser.path
        if path:
            for i in range(len(path) - 1):
                start = (path[i][0] * cell_size, path[i][1] * cell_size)
                end = (path[i + 1][0] * cell_size, path[i + 1][1] * cell_size)
                draw.line([start, end], fill="red", width=2)

    image.save(image_filename)
    print(f"Solution image saved as {image_filename}")


if __name__ == '__main__':
    if len(sys.argv) < 2 :
        print("Usage: python3 lasor.py file_path")
        sys.exit(1)
    else:
        file_path = sys.argv[1]
        start_time = time.time() 
        result = solve_lazor_game(file_path)
        if result is not None:
            game_grid, lasers, targets, column, row = result
            save_solution_image(game_grid.grid_content, column, row, lasers, targets)
            end_time = time.time()
            solution_time = (end_time - start_time)/60
            print(f"Time taken to find the solution{solution_time:.4f} min")
        else:
            print("No solution found 2.")
        
        