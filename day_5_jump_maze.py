"""
--- Day 5: A Maze of Twisty Trampolines, All Alike ---

An urgent interrupt arrives from the CPU: it's trapped in a maze of jump
instructions, and it would like assistance from any programs with spare cycles
to help find the exit.

The message includes a list of the offsets for each jump. Jumps are relative:
-1 moves to the previous instruction, and 2 skips the next one. Start at the
first instruction in the list. The goal is to follow the jumps until one leads
outside the list.

In addition, these instructions are a little strange; after each jump, the
offset of that instruction increases by 1. So, if you come across an offset of
3, you would move three instructions forward, but change it to a 4 for the next
time it is encountered.

For example, consider the following list of jump offsets:

0
3
0
1
-3

Positive jumps ("forward") move downward; negative jumps move upward. For
legibility in this example, these offset values will be written all on one
line, with the current instruction marked in parentheses. The following steps
would be taken before an exit is found:

(0) 3  0  1  -3  - before we have taken any steps.
(1) 3  0  1  -3  - jump with offset 0 (that is, don't jump at all).
Fortunately, the instruction is then incremented to 1.
 2 (3) 0  1  -3  - step forward because of the instruction we just modified.
The first instruction is incremented again, now to 2.
 2  4  0  1 (-3) - jump all the way to the end; leave a 4 behind.
 2 (4) 0  1  -2  - go back to where we just were; increment -3 to -2.
 2  5  0  1  -2  - jump 4 steps forward, escaping the maze. In this example,
the exit is reached in 5 steps.

How many steps does it take to reach the exit?
"""
import unittest


class Interrupt:
    def __init__(self, instructions, part_two=False):
        self.instructions = instructions
        self.position = 0
        self.jumps = 0
        self.part_two = part_two

    def jump(self):
        """Carry out the next jump instruction."""
        jump_by = self.instructions[self.position]
        self.change_offset()
        self.position += jump_by
        self.jumps += 1

    def change_offset(self):
        """Adjust the jump offset at the current position."""
        offset = 1
        if self.part_two and self.instructions[self.position] >= 3:
            offset = -1
        self.instructions[self.position] += offset

    @property
    def escaped(self):
        try:
            self.instructions[self.position]
            return False
        except IndexError:
            return True

    def escape_maze(self):
        """Returns numbers of jumps it took interrupt to escape."""
        while not self.escaped:
            self.jump()
        return self.jumps


def read_maze_txt(a_file):
    with open(a_file, 'rt') as f:
        for line in f:
            yield int(line)


class TestTrampolineMaze(unittest.TestCase):
    def test_interrupt_starts_at_zero(self):
        interrupt = Interrupt([0])
        self.assertEqual(interrupt.position, 0)

    def test_interrupt_has_not_escaped_before_jumping(self):
        interrupt = Interrupt([2])
        self.assertFalse(interrupt.escaped)

    def test_interrupt_can_escape(self):
        interrupt = Interrupt([4, 1, 1])
        interrupt.jump()
        self.assertTrue(interrupt.escaped)

    def test_interrupt_can_jump(self):
        instr = [1, 0]
        interrupt = Interrupt(instr)
        interrupt.jump()
        self.assertEqual(interrupt.position, 1)
        self.assertEqual(interrupt.jumps, 1)

    def test_interrupt_escapes_the_sample_maze(self):
        interrupt = Interrupt([0, 3, 0, 1, -3])
        self.assertEqual(interrupt.escape_maze(), 5)
        self.assertEqual(interrupt.instructions, [2, 5, 0, 1, -2])


if __name__ == '__main__':
    maze = read_maze_txt('day_5_maze.txt')
    instructions = list(maze)
    int_ = Interrupt(instructions, part_two=True)
    print(int_.escape_maze())
    unittest.main()
