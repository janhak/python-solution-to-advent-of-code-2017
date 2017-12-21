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
import unittest
from enum import Enum


class Head(Enum):
    n = 'n'
    ne = 'ne'
    se = 'se'
    s = 's'
    sw = 'sw'
    nw = 'nw'


class HexCor:
    def __init__(self, ring, cell):
        self.ring = ring
        self.cell = cell

    @property
    def n_axis(self):
        return self.cell == 0

    @property
    def ne_axis(self):
        return self.cell == self.ring

    @property
    def se_axis(self):
        return self.cell == self.ring * 2

    @property
    def s_axis(self):
        return self.cell == self.ring * 3

    @property
    def sw_axis(self):
        return self.cell == self.ring * 4

    @property
    def nw_axis(self):
        return self.cell == self.ring * 5

    @property
    def ne_quad(self):
        return 0 < self.cell < self.ring

    @property
    def e_quad(self):
        return self.ring < self.cell < self.ring * 2

    @property
    def se_quad(self):
        return self.ring * 2 < self.cell < self.ring * 3

    @property
    def sw_quad(self):
        return self.ring * 3 < self.cell < self.ring * 4

    @property
    def w_quad(self):
        return self.ring * 4 < self.cell < self.ring * 5

    @property
    def nw_quad(self):
        return self.ring * 5 < self.cell < self.ring * 6

    @property
    def origin(self):
        return self.ring == 0

    def __eq__(self, other):
        if isinstance(other, HexCor):
            return (self.cell == other.cell and self.ring == other.ring)
        else:
            raise NotImplemented(
                "Can compare HexCor only against its own class")

    def __repr__(self):
        return 'HexCor({!r}, {!r})'.format(self.ring, self.cell)


def hex_distance(path):
    origin = HexCor(0, 0)
    pos = origin
    for step in path:
        if pos.origin:
            movement_map = {
                Head.n: HexCor(pos.ring + 1, 0),
                Head.ne: HexCor(pos.ring + 1, 1),
                Head.se: HexCor(pos.ring + 1, 2),
                Head.s: HexCor(pos.ring + 1, (pos.ring + 1) * 3),
                Head.sw: HexCor(pos.ring + 1, (pos.ring + 1) * 3 - 1),
                Head.nw: HexCor(pos.ring + 1, (2**(pos.ring + 1) * 3) - 1)
            }
        elif pos.n_axis:
            movement_map = {
                Head.n: HexCor(pos.ring + 1, 0),
                Head.ne: HexCor(pos.ring + 1, 1),
                Head.se: HexCor(pos.ring, 1),
                Head.s: HexCor(pos.ring - 1, 0),
                Head.sw: HexCor(pos.ring, (2**pos.ring * 3) - 1),
                Head.nw: HexCor(pos.ring + 1, (2**(pos.ring + 1) * 3) - 1)
            }
        elif pos.s_axis:
            movement_map = {
                Head.n: HexCor(pos.ring - 1, ((pos.ring - 1) * 3)),
                Head.ne: HexCor(pos.ring, (pos.ring * 3 - 1)),
                Head.se: HexCor(pos.ring + 1, ((pos.ring + 1) * 3) - 1),
                Head.s: HexCor(pos.ring + 1, ((pos.ring + 1) * 3)),
                Head.sw: HexCor(pos.ring + 1, ((pos.ring + 1) * 3) + 1),
                Head.nw: HexCor(pos.ring, (pos.ring * 3) + 1)
            }
        elif pos.ne_axis:
            movement_map = {
                Head.n: HexCor(pos.ring + 1, pos.cell),
                Head.ne: HexCor(pos.ring + 1, pos.cell + 1),
                Head.se: HexCor(pos.ring + 1, pos.cell + 2),
                Head.s: HexCor(pos.ring, pos.cell + 1),
                Head.sw: HexCor(pos.ring - 1, pos.cell - 1),
                Head.nw: HexCor(pos.ring, pos.cell - 1)
            }
        elif pos.sw_axis:
            movement_map = {
                Head.n: HexCor(pos.ring, pos.cell + 1),
                Head.ne: HexCor(pos.ring - 1, (pos.ring - 1) * 4),
                Head.se: HexCor(pos.ring, pos.cell - 1),
                Head.s: HexCor(pos.ring + 1, (pos.ring + 1) * 4 - 1),
                Head.sw: HexCor(pos.ring + 1, (pos.ring + 1) * 4),
                Head.nw: HexCor(pos.ring + 1, (pos.ring + 1) * 4 + 1)
            }
        elif pos.se_axis:
            movement_map = {
                Head.n: HexCor(pos.ring, pos.cell - 1),
                Head.ne: HexCor(pos.ring + 1, (pos.ring + 1) * 2 - 1),
                Head.se: HexCor(pos.ring + 1, (pos.ring + 1) * 2),
                Head.s: HexCor(pos.ring + 1, (pos.ring + 1) * 2 + 1),
                Head.sw: HexCor(pos.ring, pos.cell + 1),
                Head.nw: HexCor(pos.ring - 1, (pos.ring - 1) * 2)
            }
        elif pos.nw_axis:
            movement_map = {
                Head.n: HexCor(pos.ring + 1, (pos.ring + 1) * 5 + 1),
                Head.ne: HexCor(pos.ring, (pos.cell + 1) % (2**pos.ring * 3)),
                Head.se: HexCor(pos.ring - 1, (pos.ring - 1) * 5 - 1),
                Head.s: HexCor(pos.ring, pos.cell - 1),
                Head.sw: HexCor(pos.ring + 1, (pos.ring + 1) * 5 - 1),
                Head.nw: HexCor(pos.ring + 1, (pos.ring + 1) * 5)
            }
        elif pos.ne_quad:
            movement_map = {
                Head.n: HexCor(pos.ring + 1, pos.cell),
                Head.ne: HexCor(pos.ring + 1, pos.cell + 1),
                Head.se: HexCor(pos.ring, pos.cell + 1),
                Head.s: HexCor(pos.ring - 1, pos.cell),
                Head.sw: HexCor(pos.ring - 1, pos.cell - 1),
                Head.nw: HexCor(pos.ring, pos.cell - 1)
            }
        elif pos.e_quad:
            movement_map = {
                Head.n: HexCor(pos.ring, pos.cell - 1),
                Head.ne: HexCor(pos.ring + 1, pos.cell + 1),
                Head.se: HexCor(pos.ring + 1, pos.cell + 2),
                Head.s: HexCor(pos.ring, pos.cell + 1),
                Head.sw: HexCor(pos.ring - 1, pos.cell - 1),
                Head.nw: HexCor(pos.ring - 1, pos.cell - 1)
            }
        else:
            raise NotImplementedError('not implemented')
        pos = movement_map[step]
    return pos


class TestHexDistance(unittest.TestCase):
    def test_one_step_away(self):
        for d in Head:
            path = [d]
            with self.subTest(path=path):
                self.assertEqual(hex_distance(path).ring, 1)

    def test_no_steps_at_origin(self):
        self.assertEqual(hex_distance([]).ring, 0)

    def test_staying_on_north_axis(self):
        path = [Head.n, Head.n, Head.s]
        self.assertEqual(hex_distance(path), HexCor(1, 0))

    def test_staying_on_north_south_axis(self):
        path = [Head.n, Head.n, Head.s, Head.s, Head.s, Head.s, Head.s]
        self.assertEqual(hex_distance(path), HexCor(3, 9))

    def test_ne_axis(self):
        path = [Head.n, Head.se, Head.n]
        self.assertEqual(hex_distance(path), HexCor(2, 1))

    def test_ne_sw_axis(self):
        path = [Head.s, Head.nw, Head.sw, Head.sw, Head.ne, Head.ne, Head.ne]
        self.assertEqual(hex_distance(path), HexCor(0, 0))

    def test_se_axis(self):
        path = [Head.se, Head.se, Head.n]
        self.assertEqual(hex_distance(path), HexCor(2, 3))

    def test_se_sw_axis(self):
        path = [Head.se, Head.se, Head.nw, Head.nw]
        self.assertEqual(hex_distance(path), HexCor(0, 0))

    def test_walk_circle(self):
        path = [Head.n, Head.se, Head.s, Head.sw, Head.nw, Head.n, Head.ne]
        self.assertEqual(hex_distance(path), HexCor(1, 0))

    def test_ne_quad(self):
        path = [Head.n, Head.ne]
        path_position = (
            (path + [Head.n], HexCor(3, 1)),
            (path + [Head.ne], HexCor(3, 2)),
            (path + [Head.se], HexCor(2, 2)),
            (path + [Head.s], HexCor(1, 1)),
            (path + [Head.sw], HexCor(1, 0)),
            (path + [Head.nw], HexCor(2, 0)), )
        for p, pos in path_position:
            with self.subTest(path=p, pos=pos):
                self.assertEqual(hex_distance(p), pos)

    def test_trip_to_the_east(self):
        path = [Head.se, Head.se, Head.n, Head.ne, Head.s]
        self.assertEqual(hex_distance(path), HexCor(3, 5))


if __name__ == '__main__':
    # I think I wrote a refactoring code-kata!
    unittest.main()
