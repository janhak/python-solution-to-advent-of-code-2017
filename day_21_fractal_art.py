"""
--- Day 21: Fractal Art ---
You find a program trying to generate some art. It uses a strange process that
involves repeatedly enhancing the detail of an image through a set of rules.

The image consists of a two-dimensional square grid of pixels that are either
on (#) or off (.). The program always begins with this pattern:

.#.
..#
###

Because the pattern is both 3 pixels wide and 3 pixels tall, it is said to have
a size of 3.

Then, the program repeats the following process:

If the size is evenly divisible by 2, break the pixels up into 2x2 squares, and
convert each 2x2 square into a 3x3 square by following the corresponding
enhancement rule. Otherwise, the size is evenly divisible by 3; break the
pixels up into 3x3 squares, and convert each 3x3 square into a 4x4 square by
following the corresponding enhancement rule. Because each square of pixels is
replaced by a larger one, the image gains pixels and so its size increases.

The artist's book of enhancement rules is nearby (your puzzle input); however,
it seems to be missing rules. The artist explains that sometimes, one must
rotate or flip the input pattern to find a match. (Never rotate or flip the
output pattern, though.) Each pattern is written concisely: rows are listed as
single units, ordered top-down, and separated by slashes. For example, the
following rules correspond to the adjacent patterns:

../.#  =  ..
          .#

                .#.
.#./..#/###  =  ..#
                ###

                        #..#
#..#/..../#..#/.##.  =  ....
                        #..#
                        .##.

When searching for a rule to use, rotate and flip the pattern as necessary. For
example, all of the following patterns match the same rule:

.#.   .#.   #..   ###
..#   #..   #.#   ..#
###   ###   ##.   .#.

Suppose the book contained the following two rules:

../.# => ##./#../...
.#./..#/### => #..#/..../..../#..#

As before, the program begins with this pattern:

.#.
..#
###

The size of the grid (3) is not divisible by 2, but it is divisible by 3. It
divides evenly into a single square; the square matches the second rule, which
produces:

#..#
....
....
#..#

The size of this enhanced grid (4) is evenly divisible by 2, so that rule is
used. It divides evenly into four squares:

#.|.#
..|..
--+--
..|..
#.|.#

Each of these squares matches the same rule (../.# => ##./#../...), three of
which require some flipping and rotation to line up with the rule. The output
for the rule is the same in all four cases:

##.|##.
#..|#..
...|...
---+---
##.|##.
#..|#..
...|...

Finally, the squares are joined into a new grid:

##.##.
#..#..
......
##.##.
#..#..
......

Thus, after 2 iterations, the grid contains 12 pixels that are on.

How many pixels stay on after 5 iterations?
"""
import unittest


class Grid:
    def __init__(self, rows):
        self.rows = tuple(tuple(row) for row in rows)
        self.size = len(self.rows)

    @classmethod
    def from_line(self, line):
        rows = line.split(r'/')
        return Grid(rows)

    def __eq__(self, other):
        return self.rows == other.rows

    def __hash__(self):
        return hash(self.rows)

    def __repr__(self):
        return '{}({!r})'.format(self.__class__.__name__, self.rows)

    def flipped_hor(self):
        return Grid(reversed(self.rows))

    def flipped_ver(self):
        return Grid(tuple(reversed(row)) for row in self.rows)

    def rotated(self, times=1):
        rows = self.rows
        for _ in range(times):
            columns = reversed(rows)
            rows = tuple(zip(*columns))
        return Grid(rows)

    @property
    def pixels_on(self):
        return sum(row.count('#') for row in self.rows)

    def permutations(self):
        return (
            self,
            self.flipped_hor(),
            self.flipped_ver(),
            self.rotated(times=1),
            self.rotated(times=2),
            self.rotated(times=3), )

    def split(self):
        if self.size % 2 == 0:
            split_size = 2
            splits = self.size // 2
        elif self.size % 3 == 0:
            split_size = 3
            splits = self.size // 3
        else:
            raise ValueError(
                'Grid of size not divisible by 2 and 3 encountered.')
        split_rows = [[
            row[split_size * i:split_size * (i + 1)] for i in range(splits)
        ] for row in self.rows]
        cols = [row[i] for row in split_rows for i in range(splits)]
        raise ValueError('Continue here')
        print(cols)
        return cols

    def enchance(self):
        subgrids = self.split()
        pass


class RuleBook:
    def __init__(self, rules):
        self.rules = {}
        for pattern, target in rules:
            pattern_grid = Grid.from_line(pattern)
            target_grid = Grid.from_line(target)
            for permutation in pattern_grid.permutations():
                self.rules[permutation] = target_grid

    @classmethod
    def from_raw_lines(cls, lines):
        rules = (line.strip().split(' => ') for line in lines)
        return RuleBook(rules)

    def match(self, grid):
        return self.rules[grid]


class TestGrid(unittest.TestCase):
    def setUp(self):
        self.grid = Grid.from_line('../.#')

    def test_creation_from_line(self):
        self.assertEqual(self.grid.rows, (('.', '.'), ('.', '#')))

    def test_flip_horizontal(self):
        flipped = self.grid.flipped_hor()
        self.assertEqual(flipped.rows, (('.', '#'), ('.', '.')))

    def test_flip_vertical(self):
        flipped = self.grid.flipped_ver()
        self.assertEqual(flipped.rows, (('.', '.'), ('#', '.')))

    def test_single_clockwise_rotation(self):
        rotated = self.grid.rotated()
        self.assertEqual(rotated.rows, (('.', '.'), ('#', '.')))

    def test_four_clockwise_rotations(self):
        rotated = self.grid.rotated(times=4)
        self.assertEqual(rotated.rows, (('.', '.'), ('.', '#')))

    def test_pixels_on(self):
        self.assertEqual(self.grid.pixels_on, 1)

    def test_split(self):
        self.assertTrue(self.grid in self.grid.split())

    def test_big_split(self):
        grid = Grid.from_line('#..#/..../..../#..#')
        to_find = Grid.from_line('#./..')
        print(grid.split())
        self.assertTrue(to_find in grid.split())
        self.assertEqual(len(grid.split()), 4)


class TestRuleBook(unittest.TestCase):
    def setUp(self):
        lines = ('../.# => ##./#../...',
                 '.#./..#/### => #..#/..../..../#..#\n')
        self.rule_book = RuleBook.from_raw_lines(lines)

    def test_rule_book_initializes(self):
        self.assertTrue(Grid.from_line('../.#') in self.rule_book.rules)

    def test_match_pattern(self):
        possible_patterns = ('#./..', '.#/..', '../#.', '../.#')
        for line in possible_patterns:
            pattern = Grid.from_line(line)
            result = self.rule_book.match(pattern)
            self.assertEqual(result.rows, (('#', '#', '.'),
                                           ('#', '.', '.'),
                                           ('.', '.', '.')))


if __name__ == '__main__':
    lines = open('day_21_data.txt', 'rt').readlines()
    rule_book = RuleBook.from_raw_lines(lines)
    unittest.main()
