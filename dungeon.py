import random
import math
import sys

import room
import maze
import nothing

DIVISION_MARGIN = 1
STRICTNESS = 0.2
MIN_SECTOR_SIZE = 10
FLOOR_WIDTH = 40
FLOOR_HEIGHT = 40
STAIRS_GENERATION_TIMEOUT = 10000

WALL = '#'
FLOOR = ' '
CORRIDOR = '.'
UP_STAIRCASE = '<'
DOWN_STAIRCASE = '>'

division_probabilities = {
    'ROOM': 0.8,
    'MAZE': 0.81,
    'NOTHING': 1    
}

dungeon = []


def split_vertically(sector):
    if sector.x_size < MIN_SECTOR_SIZE * 2 + 1:
        sector.generate_division()
    else:
        acceptable_splits = range(sector.x + int(math.ceil(sector.x_size * STRICTNESS)),
                                  sector.x + int(math.floor(sector.x_size * (1 - STRICTNESS))))
        acceptable_splits = [x for x in acceptable_splits if
                             sector.x + MIN_SECTOR_SIZE <= x < (sector.x + sector.x_size - MIN_SECTOR_SIZE)]
        pos = random.randint(0, len(acceptable_splits) - 1)
        split = acceptable_splits[pos]
        sector.sectors.append(Sector(sector.x, sector.y, split - sector.x, sector.y_size))
        sector.sectors.append(Sector(split + 1, sector.y, sector.x_size - split + sector.x - 1, sector.y_size))
        for subsector in sector.sectors:
            subsector.split()


def split_horizontally(sector):
    if sector.y_size < MIN_SECTOR_SIZE * 2 + 1:
        sector.generate_division()
    else:
        acceptable_splits = range(sector.y + int(math.ceil(sector.y_size * STRICTNESS)),
                                  sector.y + int(math.floor(sector.y_size * (1 - STRICTNESS))))
        acceptable_splits = [y for y in acceptable_splits if
                             sector.y + MIN_SECTOR_SIZE <= y < (sector.y + sector.y_size - MIN_SECTOR_SIZE)]
        pos = random.randint(0, len(acceptable_splits) - 1)
        split = acceptable_splits[pos]
        sector.sectors.append(Sector(sector.x, sector.y, sector.x_size, split - sector.y))
        sector.sectors.append(Sector(sector.x, split + 1, sector.x_size, sector.y_size - split + sector.y - 1))
        for subsector in sector.sectors:
            subsector.split()


def init_matrix(matrix, x_size, y_size):
    for y in range(y_size):
        temp = []
        for x in range(x_size):
            temp.append(WALL)
        matrix.append(temp)


def set_matrix_tile(matrix, x, y, tile):
    matrix[y][x] = tile


def get_matrix_tile(matrix, x, y):
    return matrix[y][x]


def print_matrix(matrix):
    for line in matrix:
        for tile in line:
            print tile,
        print ''


class Sector:
    def __init__(self, x, y, x_size, y_size):
        self.x = x
        self.y = y
        self.x_size = x_size
        self.y_size = y_size
        self.sectors = []
        self.exit_points = {}
        self.division = None

    def split(self):
        if self.x_size != self.y_size:
            if self.y_size > self.x_size:
                split_horizontally(self)
            else:
                split_vertically(self)
        else:
            if random.randint(0, 1) == 0:
                split_horizontally(self)
            else:
                split_vertically(self)

    def generate_division(self):
        prob = random.random()
        if prob < division_probabilities['ROOM']:
            self.division = room.Room(self.x_size-DIVISION_MARGIN*2, self.y_size-DIVISION_MARGIN*2)
        elif prob < division_probabilities['MAZE']:
            self.division = maze.Maze(self.x_size-DIVISION_MARGIN*2, self.y_size-DIVISION_MARGIN*2)
        else:
            self.division = nothing.Nothing(self.x_size-DIVISION_MARGIN*2, self.y_size-DIVISION_MARGIN*2)
        self.division.populate_division()
        self.determine_exit_point_directions()
        
        for y in range(0, self.division.y_size):
            for x in range(0, self.division.x_size):
                set_matrix_tile(dungeon, x + DIVISION_MARGIN + self.x, y + DIVISION_MARGIN + self.y, self.division.matrix[y][x])

        floor.sectors.append(self)

    def determine_exit_point_directions(self):
        directions = [maze.UP, maze.DOWN, maze.LEFT, maze.RIGHT]
        if self.x == 1:
            directions.remove(maze.LEFT)
        elif self.x + self.x_size > FLOOR_HEIGHT:
            directions.remove(maze.RIGHT)
        if self.y == 1:
            directions.remove(maze.UP)
        elif self.y + self.y_size > FLOOR_WIDTH:
            directions.remove(maze.DOWN)
        self.exit_directions = directions
        exit_points = [(self.x+x+1, self.y+y+1) for (x,y) in self.division.generate_exit_points(directions)]
        for i in range(len(directions)):
            self.exit_points[directions[i]] = exit_points[i]

    def determine_connections_to_make(self):
        for exit_direction in self.exit_directions:
            if exit_direction == maze.UP:
                neighbours = []
                for sector in floor.sectors:
                    for x in range(self.x, self.x + self.x_size):
                        if sector.is_point_in_sector(x, self.y - 2):
                            try:
                                self.exit_directions.remove(maze.UP)
                                sector.exit_directions.remove(maze.DOWN)
                            except ValueError:
                                continue
                            neighbours.append(sector)
                            break
                if len(neighbours) > 0:
                    chosen_sector = random.randint(0, len(neighbours)-1)
                    floor.connections_to_make.append((self.exit_points[maze.UP], neighbours[chosen_sector].exit_points[maze.DOWN]))
            elif exit_direction == maze.DOWN:
                neighbours = []
                for sector in floor.sectors:
                    for x in range(self.x, self.x + self.x_size):
                        if sector.is_point_in_sector(x, self.y + self.y_size + 2):
                            try:
                                self.exit_directions.remove(maze.DOWN)
                                sector.exit_directions.remove(maze.UP)
                            except ValueError:
                                continue
                            neighbours.append(sector)
                            continue
                if len(neighbours) > 0:
                    chosen_sector = random.randint(0, len(neighbours)-1)
                    floor.connections_to_make.append((self.exit_points[maze.DOWN], neighbours[chosen_sector].exit_points[maze.UP]))
            elif exit_direction == maze.LEFT:
                neighbours = []
                for sector in floor.sectors:
                    for y in range(self.y, self.y + self.y_size):
                        if sector.is_point_in_sector(self.x - 2, y):
                            try:
                                self.exit_directions.remove(maze.LEFT)
                                sector.exit_directions.remove(maze.RIGHT)
                            except ValueError:
                                continue
                            neighbours.append(sector)
                            break
                if len(neighbours) > 0:
                    chosen_sector = random.randint(0, len(neighbours)-1)
                    floor.connections_to_make.append((self.exit_points[maze.LEFT], neighbours[chosen_sector].exit_points[maze.RIGHT]))
            elif exit_direction == maze.RIGHT:
                neighbours = []
                for sector in floor.sectors:
                    for y in range(self.y, self.y + self.y_size):
                        if sector.is_point_in_sector(self.x + self.x_size + 2, y):
                            try:
                                self.exit_directions.remove(maze.RIGHT)
                                sector.exit_directions.remove(maze.LEFT)
                            except ValueError:
                                continue
                            neighbours.append(sector)
                            continue
                if len(neighbours) > 0:
                    chosen_sector = random.randint(0, len(neighbours)-1)
                    floor.connections_to_make.append((self.exit_points[maze.RIGHT], neighbours[chosen_sector].exit_points[maze.LEFT]))

    def is_point_in_sector(self, x, y):
        if x >= self.x and x < self.x + self.x_size and y >= self.y and y < self.y + self.y_size:
            return True
        else:
            return False


class Floor:
    def __init__(self, x_size, y_size):
        self.sectors = []
        self.connections_to_make = []
        self.root_sector = Sector(1, 1, x_size, y_size)
        init_matrix(dungeon, x_size + 2, y_size + 2)


    def generate_sectors(self):
        self.root_sector.split()


    def connect_points(self):
        for connection_to_make in self.connections_to_make:
            x1 = connection_to_make[0][0]
            x2 = connection_to_make[1][0]
            y1 = connection_to_make[0][1]
            y2 = connection_to_make[1][1]
            set_matrix_tile(dungeon, x1, y1, CORRIDOR)
            if abs(x2 - x1) > abs(y2 - y1):
                if x2 > x1:
                    positions_to_change_y = [random.randint(x1+1, x2-1) for i in range(abs(y2-y1))]
                else:
                    positions_to_change_y = [random.randint(x2+1, x1-1) for i in range(abs(y2-y1))]
                while (x1, y1) != (x2, y2):
                    if x1 in positions_to_change_y:
                        if y1 > y2:
                            y1 -= 1
                        else:
                            y1 += 1
                        positions_to_change_y.remove(x1)
                    else:
                        if x1 > x2:
                            x1 -= 1
                        else:
                            x1 += 1
                    set_matrix_tile(dungeon, x1, y1, CORRIDOR)
            else:
                if y2 > y1:
                    positions_to_change_x = [random.randint(y1+1, y2-1) for i in range(abs(x2-x1))]
                else:
                    positions_to_change_x = [random.randint(y2+1, y1-1) for i in range(abs(x2-x1))]
                while (x1, y1) != (x2, y2):
                    if y1 in positions_to_change_x:
                        if x1 > x2:
                            x1 -= 1
                        else:
                            x1 += 1
                        positions_to_change_x.remove(y1)
                    else:
                        if y1 > y2:
                            y1 -= 1
                        else:
                            y1 += 1
                    set_matrix_tile(dungeon, x1, y1, CORRIDOR)

    def generate_staircases(self):
        x = 0
        y = 0
        timeout = 0
        tiles_to_search = [FLOOR]
        while get_matrix_tile(dungeon, x, y) not in tiles_to_search:
            if timeout > STAIRS_GENERATION_TIMEOUT:
                tiles_to_search.append(CORRIDOR)
            x = random.randint(1, FLOOR_HEIGHT)
            y = random.randint(1, FLOOR_WIDTH)
            timeout += 1
        set_matrix_tile(dungeon, x, y, UP_STAIRCASE)
        while get_matrix_tile(dungeon, x, y) not in tiles_to_search:
            if timeout > STAIRS_GENERATION_TIMEOUT:
                tiles_to_search.append(CORRIDOR)
            x = random.randint(1, FLOOR_HEIGHT)
            y = random.randint(1, FLOOR_WIDTH)
            timeout += 1
        set_matrix_tile(dungeon, x, y, DOWN_STAIRCASE)



if __name__ == "__main__":
    try:
        if len(sys.argv) >= 2:
            FLOOR_HEIGHT = int(sys.argv[1])
        if len(sys.argv) >= 3:
            FLOOR_WIDTH = int(sys.argv[2])
        if len(sys.argv) >= 4:
            MIN_SECTOR_SIZE = int(sys.argv[3])
        if len(sys.argv) >= 5:
            room.MIN_ROOM_HEIGHT = int(sys.argv[4])
        if len(sys.argv) >= 6:
            room.MIN_ROOM_WIDTH = int(sys.argv[5])
        if len(sys.argv) >= 7:
            STRICTNESS = float(sys.argv[6])
        if len(sys.argv) >= 8:
            STAIRS_GENERATION_TIMEOUT = int(sys.argv[7])
        floor = Floor(FLOOR_HEIGHT, FLOOR_WIDTH)
        floor.generate_sectors()
        for sector in floor.sectors:
            sector.determine_connections_to_make()
        floor.connect_points()
        floor.generate_staircases()
        print_matrix(dungeon)
    except Exception:
        print "Error while generating dungeon floor. Please choose different arguments or try again."