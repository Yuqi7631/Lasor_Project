# Lasor_Project
This is a Python program designed to automatically solve levels in the "Lazors" game by placing various types of blocks on a grid to direct laser paths through designated points. The project reads custom puzzle files (`. bff` format) and outputs solutions with block placements needed to solve each level.

# Authors
Yuqi Feng, Selina(Yilin) Luo

# Usage
## Running the Program 
You can get the `. bff` file and run the program by passing the file path as an augment.
In your terminal, navigate to the directory containing `lasor.py` and run:
```markdown
python lasor.py file_path
```
Here, replace file_path with the path to your `. bff` file.

## Output
The program will generate an image file named `file_name.png` that displays the solution and shows the time taken to solve it.

 Grey = no block allowed
  
 White = blocks allowed
  
 Skyblue= reflect block
  
 Lightpink = fixed opaque block
  
 Green= refract block



# Sample Solution
## Sample .bff file
### Grid Information
GRID START<br>
x o o <br>
o o o <br>
o o x<br>
GRID STOP<br>

### Block Information

- **B**: 3 (Blocking blocks available)

### Laser Information

- **Lasers**:
  - `L 3 0 -1 1` (Starting at `(3, 0)`, direction `(-1, 1)`)
  - `L 1 6 1 -1` (Starting at `(1, 6)`, direction `(1, -1)`)
  - `L 3 6 -1 -1` (Starting at `(3, 6)`, direction `(-1, -1)`)
  - `L 4 3 1 -1` (Starting at `(4, 3)`, direction `(1, -1)`)

### Target Points

- **Targets**:
  - `P 0 3`
  - `P 6 1`
## Sample Image
![alt test](solution_output.png)
## Solutions
mad_1_solution:
 
![mad_1](mad_1.png)

mad_4_solution:

![mad_4](mad_4.png)
 
mad_7_solution:

![](mad_7.png)

numbered_6_solution:

![](numbered_6.png)

showstopper_4_solution:
 
![](showstopper_4.png)

tiny_5_solution:

![](tiny_5.png)

yarn_5_solution:

![](yarn_5.png)

 Good luck!
