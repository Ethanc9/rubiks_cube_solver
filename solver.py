# Representation of the cube:
# Each face is represented by a 3x3 list
# The order of faces is: Up, Left, Front, Right, Back, Down
# Colors are represented by their first letter: W (White), Y (Yellow), R (Red), O (Orange), G (Green), B (Blue)

def create_solved_cube():
    return [
        [['W', 'W', 'W'], ['W', 'W', 'W'], ['W', 'W', 'W']],  # Up
        [['O', 'O', 'O'], ['O', 'O', 'O'], ['O', 'O', 'O']],  # Left
        [['G', 'G', 'G'], ['G', 'G', 'G'], ['G', 'G', 'G']],  # Front
        [['R', 'R', 'R'], ['R', 'R', 'R'], ['R', 'R', 'R']],  # Right
        [['B', 'B', 'B'], ['B', 'B', 'B'], ['B', 'B', 'B']],  # Back
        [['Y', 'Y', 'Y'], ['Y', 'Y', 'Y'], ['Y', 'Y', 'Y']]   # Down
    ]

def rotate_face_clockwise(face):
    return [list(row) for row in zip(*face[::-1])]

def apply_move(cube, move):
    faces = {
        'U': 0, 'L': 1, 'F': 2, 'R': 3, 'B': 4, 'D': 5
    }
    affected_faces = {
        'U': (1, 2, 3, 4), 'L': (0, 2, 5, 4), 'F': (0, 3, 5, 1),
        'R': (0, 4, 5, 2), 'B': (0, 1, 5, 3), 'D': (2, 3, 4, 1)
    }
    
    face = faces[move[0]]
    if len(move) == 1:
        cube[face] = rotate_face_clockwise(cube[face])
        times = 1
    elif move[1] == '2':
        cube[face] = rotate_face_clockwise(rotate_face_clockwise(cube[face]))
        times = 2
    else:  # move[1] == "'"
        cube[face] = rotate_face_clockwise(rotate_face_clockwise(rotate_face_clockwise(cube[face])))
        times = 3
    
    aff = affected_faces[move[0]]
    for _ in range(times):
        temp = [cube[aff[0]][2][i] for i in range(3)]
        cube[aff[0]][2] = [cube[aff[3]][i][0] for i in range(2, -1, -1)]
        cube[aff[3]] = [[cube[aff[2]][0][i]] + cube[aff[3]][i][1:] for i in range(3)]
        cube[aff[2]][0] = [cube[aff[1]][i][2] for i in range(2, -1, -1)]
        for i in range(3):
            cube[aff[1]][i][2] = temp[i]

def apply_algorithm(cube, alg):
    for move in alg.split():
        apply_move(cube, move)

def solve_white_cross(cube):
    # Simplified white cross solver
    edges = [(1, 1, 2), (2, 1, 0), (3, 1, 2), (4, 1, 0)]
    for face, row, col in edges:
        if cube[face][row][col] == 'W':
            # Move white edge to yellow face
            apply_algorithm(cube, f"{['L', 'F', 'R', 'B'][face-1]}2")
    
    # Now solve white edges on yellow face
    for _ in range(4):
        if cube[5][0][1] == 'W':
            while cube[2][1][1] != cube[2][2][1]:
                apply_move(cube, 'D')
            apply_algorithm(cube, 'F2')
        else:
            apply_move(cube, 'D')

def solve_white_corners(cube):
    # Simplified white corners solver
    corners = [(1, 2, 2), (2, 2, 0), (3, 2, 2), (4, 2, 0)]
    for _ in range(4):
        for face, row, col in corners:
            if cube[face][row][col] == 'W':
                # Move white corner to bottom layer
                while cube[5][0][0] != 'W':
                    apply_algorithm(cube, f"{['L', 'F', 'R', 'B'][face-1]} D {['L', 'F', 'R', 'B'][face-1]}'")
                # Insert corner
                while cube[2][1][1] != cube[2][2][1]:
                    apply_move(cube, 'D')
                apply_algorithm(cube, "D' R' D R")
        apply_move(cube, 'D')

def solve_middle_layer(cube):
    # Simplified middle layer solver
    for _ in range(4):
        if cube[2][1][2] != 'Y' and cube[3][1][0] != 'Y':
            while cube[2][1][1] != cube[2][1][2]:
                apply_move(cube, 'D')
            if cube[2][1][2] == cube[3][1][1]:
                apply_algorithm(cube, "D R' D' R D F D' F'")
            else:
                apply_algorithm(cube, "D' L D L' D' F' D F")
        else:
            apply_move(cube, 'D')

def solve_yellow_cross(cube):
    # Simplified yellow cross solver
    while sum(cube[5][0][i] == cube[5][1][i] == 'Y' for i in [1, 3]) + \
          sum(cube[5][i][1] == cube[5][1][1] == 'Y' for i in [0, 2]) < 4:
        apply_algorithm(cube, "F R U R' U' F'")

def solve_yellow_corners(cube):
    # Simplified yellow corners solver
    while sum(cube[5][i][j] == 'Y' for i in range(3) for j in range(3)) < 9:
        apply_algorithm(cube, "U R U' L' U R' U' L")

def orient_last_layer(cube):
    # Simplified last layer orientation
    for _ in range(4):
        while cube[2][0][1] != cube[2][1][1]:
            apply_algorithm(cube, "R U R' U R U2 R'")
        apply_move(cube, 'U')

def solve_rubiks_cube(cube):
    solve_white_cross(cube)
    solve_white_corners(cube)
    solve_middle_layer(cube)
    solve_yellow_cross(cube)
    solve_yellow_corners(cube)
    orient_last_layer(cube)

# Example usage
cube = create_solved_cube()
# Scramble the cube here if needed
solve_rubiks_cube(cube)