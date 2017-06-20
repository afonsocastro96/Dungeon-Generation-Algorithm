import random
import dungeon

UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

matrix = []


class Maze():
    def __init__(self, x_size, y_size):
        global matrix
        self.x_size = x_size
        self.y_size = y_size
        if x_size % 2 == 0:
            self.x_size -= 1

        if y_size % 2 == 0:
            self.y_size -= 1
        matrix = []
        init_maze(self.x_size, self.y_size)
        self.matrix = matrix

    def populate_division(self):
        generate_maze()
        generate_loops()

    def generate_exit_points(self, directions):
        return generate_exit_points(directions)


def init_maze(x_size, y_size):
    for y in range(y_size):
        temp = []
        for x in range(x_size):
            if x % 2 == 1 and y % 2 == 1:
                temp.append(dungeon.FLOOR)
            else:
                temp.append(dungeon.WALL)
        matrix.append(temp)


def get_valid_directions(coord, visited_cells, x_size, y_size):
    directions = []
    if (coord[0] + 1, coord[1]) not in visited_cells and coord[0] < maze_to_stack_notation(x_size):
        directions.append(RIGHT)
    if (coord[0] - 1, coord[1]) not in visited_cells and coord[0] > 0:
        directions.append(LEFT)
    if (coord[0], coord[1] + 1) not in visited_cells and coord[1] < maze_to_stack_notation(y_size):
        directions.append(DOWN)
    if (coord[0], coord[1] - 1) not in visited_cells and coord[1] > 0:
        directions.append(UP)
    return directions


def maze_to_stack_notation(val):
    return (val - 1) / 2


def stack_to_maze_notation(val):
    return 2 * val + 1


def generate_maze():
    visited_cells = []
    visit_stack = []
    x_size = len(matrix[0]) - 1
    y_size = len(matrix) - 1

    x = random.randint(0, maze_to_stack_notation(x_size))
    y = random.randint(0, maze_to_stack_notation(y_size))

    visited_cells.append((x, y))
    visit_stack.append((x, y))

    current_cell = (x, y)

    while len(visit_stack) != 0:
        directions = get_valid_directions(current_cell, visited_cells, x_size, y_size)
        if len(directions) == 0:
            current_cell = visit_stack.pop()
            continue
        else:
            direction = directions[random.randint(0, len(directions) - 1)]
            if direction == UP:
                matrix[stack_to_maze_notation(current_cell[1]) - 1][
                    stack_to_maze_notation(current_cell[0])] = dungeon.FLOOR
                current_cell = (current_cell[0], current_cell[1] - 1)
            elif direction == DOWN:
                matrix[stack_to_maze_notation(current_cell[1]) + 1][
                    stack_to_maze_notation(current_cell[0])] = dungeon.FLOOR
                current_cell = (current_cell[0], current_cell[1] + 1)
            elif direction == LEFT:
                matrix[stack_to_maze_notation(current_cell[1])][
                    stack_to_maze_notation(current_cell[0]) - 1] = dungeon.FLOOR
                current_cell = (current_cell[0] - 1, current_cell[1])
            else:
                matrix[stack_to_maze_notation(current_cell[1])][
                    stack_to_maze_notation(current_cell[0]) + 1] = dungeon.FLOOR
                current_cell = (current_cell[0] + 1, current_cell[1])
            visited_cells.append(current_cell)
            visit_stack.append(current_cell)


def generate_loops():
    x_size = len(matrix[0]) - 1
    y_size = len(matrix) - 1
    cells_to_change = []
    for x in range(1, x_size):
        for y in range(1, y_size):
            if matrix[y][x] != dungeon.WALL:
                continue
            if matrix[y][x - 1] == dungeon.FLOOR and matrix[y][x + 1] == dungeon.FLOOR and \
                            matrix[y][x + 2] == dungeon.FLOOR and matrix[y][x - 2] == dungeon.FLOOR and matrix[y - 1][
                x] == dungeon.WALL and \
                            matrix[y + 1][x] == dungeon.WALL:
                cells_to_change.append((x, y))

            elif matrix[y][x - 1] == dungeon.WALL and matrix[y][x + 1] == dungeon.WALL and matrix[y - 1][
                x] == dungeon.FLOOR and \
                            matrix[y + 1][x] == dungeon.FLOOR and matrix[y - 2][x] == dungeon.FLOOR and matrix[y + 2][
                x] == dungeon.FLOOR:
                cells_to_change.append((x, y))

    for cell in cells_to_change:
        matrix[cell[1]][cell[0]] = dungeon.FLOOR


def generate_exit_points(sides):
    x_size = len(matrix[0]) - 1
    y_size = len(matrix) - 1

    candidates = []

    if UP in sides:
        candidates_aux = []
        for x in range(1, x_size):
            if matrix[1][x] == dungeon.FLOOR:
                candidates_aux.append((x, 0))
        candidates.append(candidates_aux)
    if DOWN in sides:
        candidates_aux = []
        for x in range(1, x_size):
            if matrix[y_size - 1][x] == dungeon.FLOOR:
                candidates_aux.append((x, y_size))
        candidates.append(candidates_aux)
    if LEFT in sides:
        candidates_aux = []
        for y in range(1, y_size):
            if matrix[y][1] == dungeon.FLOOR:
                candidates_aux.append((0, y))
        candidates.append(candidates_aux)
    if RIGHT in sides:
        candidates_aux = []
        for y in range(1, y_size):
            if matrix[y][x_size - 1] == dungeon.FLOOR:
                candidates_aux.append((x_size, y))
        candidates.append(candidates_aux)

    exits = [direction[random.randint(0, len(direction) - 1)] for direction in candidates]
    return exits


if __name__ == "__main__":
    maze = Maze(17, 17)
    maze.populate_division()
    maze.generate_exit_points([LEFT, UP])

    dungeon.print_matrix(maze.matrix)
