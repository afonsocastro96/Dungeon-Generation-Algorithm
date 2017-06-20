import random
import dungeon

MIN_ROOM_HEIGHT = 4
MIN_ROOM_WIDTH = 2

UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

class Room():
    def __init__(self, x_size, y_size):
        self.x_size = x_size
        self.y_size = y_size
        self.matrix = []
        dungeon.init_matrix(self.matrix, self.x_size, self.y_size)


    def populate_division(self):
        self.room_x = random.randint(1, self.x_size-MIN_ROOM_HEIGHT-2)
        self.room_y = random.randint(1, self.y_size-MIN_ROOM_WIDTH-2)
        self.room_x_size = random.randint(MIN_ROOM_HEIGHT, self.x_size-self.room_x-1)
        self.room_y_size = random.randint(MIN_ROOM_WIDTH, self.y_size-self.room_y-1)
        self.place_room(self.room_x, self.room_y, self.room_x_size, self.room_y_size)


    def generate_exit_points(self, directions):
        return generate_exit_points(self, directions)


    def place_room(self, room_x, room_y, room_x_size, room_y_size):
        for x in range(room_x, room_x + room_x_size):
            for y in range(room_y, room_y + room_y_size):
                self.matrix[y][x] = dungeon.FLOOR

def generate_exit_points(self, sides):
    exit_points = []
    if UP in sides:
        x = random.randint(self.room_x, self.room_x+self.room_x_size-1)
        exit_points.append((x, self.room_y-1))
    if DOWN in sides:
        x = random.randint(self.room_x, self.room_x+self.room_x_size-1)
        exit_points.append((x, self.room_y+self.room_y_size))
    if LEFT in sides:
        y = random.randint(self.room_y, self.room_y+self.room_y_size-1)
        exit_points.append((self.room_x-1, y))
    if RIGHT in sides:
        y = random.randint(self.room_y, self.room_y+self.room_y_size-1)
        exit_points.append((self.room_x+self.room_x_size, y))
    return exit_points


if __name__ == "__main__":
    room = Room(10, 15)
    room.populate_division()
    room.generate_exit_points([UP, LEFT])
    dungeon.print_matrix(room.matrix)
