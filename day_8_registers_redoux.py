"""
--- Day 8: I Heard You Like Registers ---

You receive a signal directly from the CPU. Because of your recent assistance
with jump instructions, it would like you to compute the result of a series of
unusual register instructions.

Each instruction consists of several parts: the register to modify, whether to
increase or decrease that register's value, the amount by which to increase or
decrease it, and a condition. If the condition fails, skip the instruction
without modifying the register. The registers all start at 0. The instructions
look like this:

b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10

These instructions would be processed as follows:

- Because a starts at 0, it is not greater than 1, and so b is not modified.
- a is increased by 1 (to 1) because b is less than 5 (it is 0).
- c is decreased by -10 (to 10) because a is now greater than or equal to 1 (it is 1).
- c is increased by -20 (to -10) because c is equal to 10.

After this process, the largest value in any register is 1.

You might also encounter <= (less than or equal to) or != (not equal to).
However, the CPU doesn't have the bandwidth to tell you what all the registers
are named, and leaves that to you to determine.

What is the largest value in any register after completing the instructions in
your puzzle input?
"""
import unittest
from collections import defaultdict


def lines_from_file(a_file):
    """Generates the lines for a text file."""
    with open(a_file, 'rt') as f:
        for line in f:
            yield line


MEMORY = defaultdict(int)


def parse_line(line):
    modification, condition = line.split('if')
    register, change = parse_modification(modification)
    condition = parse_condition(condition)
    return register, change, condition


def parse_modification(line):
    reg, change, amount = line.split()
    amount = int(amount)
    if change == 'dec':
        amount *= -1
    return reg, amount


def parse_condition(line):
    reg, operator, value = line.strip().split()
    return 'MEMORY[{!r}] {} {}'.format(reg, operator, value)


class TestParsers(unittest.TestCase):
    def test_parse_modification(self):
        samples = (
            ('um inc -671', ('um', -671)),
            ('j dec -10', ('j', 10)),
            ('j dec 10', ('j', -10)), )
        for line, expected in samples:
            with self.subTest(line=line, expected=expected):
                self.assertEqual(parse_modification(line), expected)

    def test_parse_condition(self):
        line = 'a >= 1'
        expected = "MEMORY['a'] >= 1"
        self.assertEqual(parse_condition(line), expected)


if __name__ == '__main__':
    # unittest.main()
    temp_values = set()
    lines = lines_from_file('day_8_data.txt')
    for l in lines:
        reg, change, condition = parse_line(l)
        if eval(condition):
            MEMORY[reg] += change
            temp_values.add(MEMORY[reg])

    print('Maximum value', max(MEMORY.values()))
    print('Maximum value during execution', max(temp_values))
