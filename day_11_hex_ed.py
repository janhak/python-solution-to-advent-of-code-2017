"""
-- Day 11: Hex Ed ---

Crossing the bridge, you've barely reached the other side of the stream when a
program comes up to you, clearly in distress. "It's my child process," she
says, "he's gotten lost in an infinite grid!"

Fortunately for her, you have plenty of experience with infinite grids.

Unfortunately for you, it's a hex grid.

The hexagons ("hexes") in this grid are aligned such that adjacent hexes can be
found to the north, northeast, southeast, south, southwest, and northwest:

  \ n  /
nw +--+ ne
  /    \
-+      +-
  \    /
sw +--+ se
  / s  \

You have the path the child process took. Starting where he started, you need
to determine the fewest number of steps required to reach him. (A "step" means
to move from the hex you are in to any adjacent hex.)

For example:

- ne,ne,ne is 3 steps away.
- ne,ne,sw,sw is 0 steps away (back where you started).
- ne,ne,s,s is 2 steps away (se,se).
- se,sw,se,sw,sw is 3 steps away (s,s,sw).
"""


class CubeC:
    """Cube coordinates representing a hexagonal grid."""

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        assert x + y + z == 0

    def __add__(self, other):
        return CubeC(self.x + other.x, self.y + other.y, self.z + other.z)

    @property
    def distance_from_origin(self):
        return max(map(abs, (self.x, self.y, self.z)))

    def __repr__(self):
        return f'{self.__class__.__name__}({self.x}, {self.y}, {self.z})'


MOVE = {
    'nw': CubeC(1, 0, -1),
    'n': CubeC(1, -1, 0),
    'ne': CubeC(0, -1, 1),
    'se': CubeC(-1, 0, 1),
    's': CubeC(-1, 1, 0),
    'sw': CubeC(0, 1, -1),
}

ORIGIN = CubeC(0, 0, 0)


def process_headings(headings, start=ORIGIN):
    pos = start
    for heading in headings:
        pos += MOVE[heading]
    return pos


def distance_from_headings(headings, start=ORIGIN):
    pos = start
    for heading in headings:
        pos += MOVE[heading]
        yield pos.distance_from_origin


def headings_from_file(a_file):
    with open(a_file, 'rt') as f:
        raw_line = f.readline()
        return raw_line.strip().split(',')


if __name__ == '__main__':
    headings = headings_from_file('day_11_data.txt')
    pos = process_headings(headings)
    print('Final position', pos, 'distance:', pos.distance_from_origin)
    # Part 2
    furthest_ever = max(distance_from_headings(headings))
    print('Furthest I got away from origin was', furthest_ever)
