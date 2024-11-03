import sys

def grid_info(file_name):
    with open(file_name, "r", encoding="utf-8") as file:
        inside_grid = False  
        grid_content = []   
        L_value = []
        P_value = []
        A_value = 0
        B_value = 0
        C_value = 0

        for line in file:
            line = line.strip()  
            if "GRID START" in line:
                inside_grid = True  
                continue
            if "GRID STOP" in line:
                inside_grid = False  
                continue
            if inside_grid:
                grid_content.append(line)
            if "A" in line:
                A_value = line[2]
            if "B" in line:
                B_value = line[2]
            if "C" in line:
                C_value = line[2]
            if "L" in line:
                L_value.append(line[1:])
            if "P" in line:
                P_value.append(line[1:])

        if grid_content:
            column = int((len(grid_content[0])+1) / 2)
            row = len(grid_content)
        else:
            print("No grid")
    return grid_content, A_value, B_value, C_value, L_value, P_value, column, row 

class Grid:

    def __init__(self, A, B, C, position=None):
        self.A = A
        self.B = B
        self.C = C
        self.position = position

    def interact_with_laser(self, laser):
        pass


class Laser:

    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

    def move(self):
        self.x += self.vx
        self.y += self.vy
