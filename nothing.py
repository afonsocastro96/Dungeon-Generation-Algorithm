import dungeon
import random

class Nothing():
    def __init__(self, x_size, y_size):
        self.x_size = x_size
        self.y_size = y_size
        self.matrix = []
        dungeon.init_matrix(self.matrix, self.x_size, self.y_size)

    def populate_division(self):
        pass

    def generate_exit_points(self, directions):
        exit_points = []
        x = random.randint(0, self.x_size-1)
        y = random.randint(0, self.y_size-1)
        while len(exit_points) < len(directions):    
            exit_points.append((x,y))
            self.matrix[y][x] = dungeon.CORRIDOR
        return exit_points

if __name__ == "__main__":
    nothing = Nothing(9, 9)
    nothing.populate_division()
    nothing.generate_exit_points([])
    dungeon.print_matrix(nothing.matrix)

