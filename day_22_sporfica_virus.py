"""
--- Day 22: Sporifica Virus ---
Diagnostics indicate that the local grid computing cluster has been
contaminated with the Sporifica Virus. The grid computing cluster is a
seemingly-infinite two-dimensional grid of compute nodes. Each node is either
clean or infected by the virus.

To prevent overloading the nodes (which would render them useless to the virus)
or detection by system administrators, exactly one virus carrier moves through
the network, infecting or cleaning nodes as it moves. The virus carrier is
always located on a single node in the network (the current node) and keeps
track of the direction it is facing.

To avoid detection, the virus carrier works in bursts; in each burst, it wakes
up, does some work, and goes back to sleep. The following steps are all
executed in order one time each burst:

If the current node is infected, it turns to its right. Otherwise, it turns to
its left. (Turning is done in-place; the current node does not change.) If the
current node is clean, it becomes infected. Otherwise, it becomes cleaned.
(This is done after the node is considered for the purposes of changing
direction.) The virus carrier moves forward one node in the direction it is
facing. Diagnostics have also provided a map of the node infection status (your
puzzle input). Clean nodes are shown as .; infected nodes are shown as #. This
map only shows the center of the grid; there are many more nodes beyond those
shown, but none of them are currently infected.

The virus carrier begins in the middle of the map facing up.

For example, suppose you are given a map like this:

..#
#..
...

Then, the middle of the infinite grid looks like this, with the virus carrier's
position marked with [ ]:

. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
. . . . . # . . .
. . . #[.]. . . .
. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
The virus carrier is on a clean node, so it turns left, infects the node, and
moves left:

. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
. . . . . # . . .
. . .[#]# . . . .
. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
The virus carrier is on an infected node, so it turns right, cleans the node,
and moves up:

. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
. . .[.]. # . . .
. . . . # . . . .
. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
Four times in a row, the virus carrier finds a clean, infects it, turns left,
and moves forward, ending in the same place and still facing up:

. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
. . #[#]. # . . .
. . # # # . . . .
. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
Now on the same node as before, it sees an infection, which causes it to turn
right, clean the node, and move forward:

. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
. . # .[.]# . . .
. . # # # . . . .
. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
After the above actions, a total of 7 bursts of activity had taken place. Of
them, 5 bursts of activity caused an infection.

After a total of 70, the grid looks like this, with the virus carrier facing
up:

. . . . . # # . .
. . . . # . . # .
. . . # . . . . #
. . # . #[.]. . #
. . # . # . . # .
. . . . . # # . .
. . . . . . . . .
. . . . . . . . .
By this time, 41 bursts of activity caused an infection (though most of those
nodes have since been cleaned).

After a total of 10000 bursts of activity, 5587 bursts will have caused an
infection.

Given your actual map, after 10000 bursts of activity, how many bursts cause a
node to become infected? (Do not count nodes that begin infected.)
"""
import collections
from enum import Enum
import unittest


class State(Enum):
    CLEAN = 1
    WEAKENED = 2
    INFECTED = 3
    FLAGGED = 4


class Virus:
    directions = ['UP', 'RIGHT', 'DOWN', 'LEFT']
    direction_to_move = {
        'UP': (-1, 0),
        'RIGHT': (0, 1),
        'DOWN': (1, 0),
        'LEFT': (0, -1)
    }

    def __init__(self, grid, start, facing='UP'):
        self.grid = grid
        self.x, self.y = start
        self._facing = self.directions.index(facing)
        self.infected = 0

    def turn_right(self):
        self._facing = (self._facing + 1) % len(self.directions)

    def turn_left(self):
        self._facing = (self._facing - 1) % len(self.directions)

    def reverse(self):
        self.turn_right()
        self.turn_right()

    @property
    def facing(self):
        return self.directions[self._facing]

    @property
    def pos(self):
        return (self.x, self.y)

    def burst(self):
        # turn
        if self.grid[self.pos] == State.INFECTED:
            self.turn_right()
        elif self.grid[self.pos] == State.CLEAN:
            self.turn_left()
        elif self.grid[self.pos] == State.FLAGGED:
            self.reverse()
        self.infect()
        # move
        move = self.direction_to_move[self.facing]
        self.x += move[0]
        self.y += move[1]

    def infect(self):
        # infect
        if self.grid[self.pos] == State.CLEAN:
            self.grid[self.pos] = State.WEAKENED
        elif self.grid[self.pos] == State.WEAKENED:
            self.grid[self.pos] = State.INFECTED
            self.infected += 1
        elif self.grid[self.pos] == State.INFECTED:
            self.grid[self.pos] = State.FLAGGED
        elif self.grid[self.pos] == State.FLAGGED:
            self.grid[self.pos] = State.CLEAN


class TestVirus(unittest.TestCase):
    def setUp(self):
        grid = grid_from_lines(('..#', '#..', '...'))
        self.v = Virus(grid, (1, 1))

    def test_turning(self):
        self.assertEqual(self.v.facing, 'UP')
        self.v.turn_right()
        self.assertEqual(self.v.facing, 'RIGHT')
        self.v.turn_right()
        self.assertEqual(self.v.facing, 'DOWN')
        self.v.turn_right()
        self.assertEqual(self.v.facing, 'LEFT')
        self.v.turn_right()
        self.assertEqual(self.v.facing, 'UP')

    def test_reversing(self):
        self.assertEqual(self.v.facing, 'UP')
        self.v.reverse()
        self.assertEqual(self.v.facing, 'DOWN')
        self.v.reverse()
        self.assertEqual(self.v.facing, 'UP')

    def test_infecting(self):
        self.assertEqual(self.v.pos, (1, 1))
        self.v.burst()
        self.assertEqual(self.v.pos, (1, 0))
        self.assertEqual(self.v.facing, 'LEFT')
        self.assertEqual(self.v.infected, 0)
        self.v.burst()
        self.assertEqual(self.v.facing, 'UP')
        self.assertEqual(self.v.pos, (0, 0))
        self.assertEqual(self.v.infected, 0)
        self.v.burst()
        self.assertEqual(self.v.facing, 'LEFT')
        self.assertEqual(self.v.pos, (0, -1))
        self.assertEqual(self.v.infected, 0)
        for _ in range(2):
            self.v.burst()
        self.assertEqual(self.v.pos, (1, 0))
        self.assertEqual(self.v.infected, 0)
        for _ in range(95):
            self.v.burst()
        self.assertEqual(self.v.infected, 26)


def grid_from_lines(lines):
    grid = collections.defaultdict(lambda: State.CLEAN)
    for i, line in enumerate(lines):
        for j, cell in enumerate(line.strip()):
            grid[(i, j)] = State.CLEAN if cell == '.' else State.INFECTED
    return grid


if __name__ == '__main__':
    unittest.main()
    lines = open('day_22_data.txt', 'rt').readlines()
    grid = grid_from_lines(lines)
    start = (len(lines) // 2, len(lines) // 2)
    v = Virus(grid, start)
    bursts = 100
    for _ in range(bursts):
        v.burst()
    print('After {} bursts virus infected'.format(bursts), v.infected)
