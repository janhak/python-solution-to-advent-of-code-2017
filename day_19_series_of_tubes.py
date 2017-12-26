"""
--- Day 19: A Series of Tubes ---

Somehow, a network packet got lost and ended up here. It's trying to follow a
routing diagram (your puzzle input), but it's confused about where to go.

Its starting point is just off the top of the diagram. Lines (drawn with |, -,
and +) show the path it needs to take, starting by going down onto the only
line connected to the top of the diagram. It needs to follow this path until it
reaches the end (located somewhere within the diagram) and stop there.

Sometimes, the lines cross over each other; in these cases, it needs to
continue going the same direction, and only turn left or right when there's no
other option. In addition, someone has left letters on the line; these also
don't change its direction, but it can use them to keep track of where it's
been. For example:

     |
     |  +--+
     A  |  C
 F---|----E|--+
     |  |  |  D
     +B-+  +--+

Given this diagram, the packet needs to take the following path:

Starting at the only line touching the top of the diagram, it must go down,
pass through A, and continue onward to the first +. Travel right, up, and
right, passing through B in the process. Continue down (collecting C), right,
and up (collecting D). Finally, go all the way left through E and stopping at
F. Following the path to the end, the letters it sees on its path are ABCDEF.

The little packet looks up at you, hoping you can help it find the way. What
letters will it see (in the order it would see them) if it follows the path?
(The routing diagram is very wide; make sure you view it without line
wrapping.)

To begin, get your puzzle input.
"""
import unittest
import string


def labyrinth_from_lines(lines):
    labyrinth = dict()
    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            if char not in (' ', '\n'):
                labyrinth[(row, col)] = char
    return labyrinth


def step(pos, direction, lab):
    symbol = lab[pos]
    x, y = pos
    if symbol == '+':
        if direction[0] != 0:
            directions = ((0, -1), (0, 1))
        elif direction[1] != 0:
            directions = ((1, 0), (-1, 0))
        direction = next(
            d for d in directions if lab.get((x + d[0], y + d[1])) is not None)
    next_pos = (x + direction[0], y + direction[1])
    return (next_pos, direction)


def walk_labyrinth(start, lab, direction=(1, 0)):
    pos = start
    visited_letters = []
    steps_taken = 0
    while True:
        try:
            if lab[pos] in string.ascii_uppercase:
                visited_letters += lab[pos]
        except KeyError:
            return (''.join(visited_letters), steps_taken)
        pos, direction = step(pos, direction, lab)
        steps_taken += 1


class TestFinder(unittest.TestCase):
    def setUp(self):
        testinput = (
            "     |          \n",
            "     |  +--+    \n",
            "     A  |  C    \n",
            " F---|----E|--+ \n",
            "     |  |  |  D \n",
            "     +B-+  +--+ \n", )
        self.lab = labyrinth_from_lines(testinput)

    def test_create_labyrinth(self):
        self.assertEqual(self.lab[(0, 5)], '|')
        self.assertEqual(self.lab[(2, 5)], 'A')
        self.assertEqual(self.lab[(5, 14)], '+')

    def test_single_step(self):
        pos = step((0, 5), (1, 0), self.lab)
        self.assertEqual(pos, ((1, 5), (1, 0)))

    def test_walk_labyrinth(self):
        path = walk_labyrinth((0, 5), self.lab)
        self.assertEqual(path, ('ABCDEF', 38))


if __name__ == '__main__':
    lines = open('day_19_data.txt', 'rt').readlines()
    labyrinth = labyrinth_from_lines(lines)
    path = walk_labyrinth((0, 15), labyrinth)
    print(path)
    unittest.main()
