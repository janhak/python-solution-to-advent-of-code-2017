import unittest
import string


def exchange(line_up, pos_a, pos_b):
    line_up[pos_a], line_up[pos_b] = line_up[pos_b], line_up[pos_a]
    return line_up


def partner(line_up, name_a, name_b):
    return exchange(line_up, line_up.index(name_a), line_up.index(name_b))


def spin(line_up, n):
    return line_up[-n:] + line_up[:-n]


def dance(line_up, instructions, times=1):
    seen = []
    for i in range(times):
        s = ''.join(line_up)
        if s in seen:
            return seen[times % i]
        seen.append(s)
        for raw_instr in instructions:
            instruction, arguments = INSTRUCTIONS[raw_instr[0]]
            line_up = instruction(line_up, *arguments(raw_instr))
    return ''.join(line_up)


INSTRUCTIONS = {
    's': (spin, lambda x: [int(x[1:])]),
    'x': (exchange, lambda x: map(int, x[1:].split('/'))),
    'p': (partner, lambda x: x[1:].split('/')),
}


def instructions_from_file(a_file):
    with open(a_file, 'rt') as f:
        line = f.readline()
    return line.strip().split(',')


class TestDance(unittest.TestCase):
    def test_exchange(self):
        l = list(range(5))
        self.assertEqual(exchange(l, 0, 4), [4, 1, 2, 3, 0])

    def test_partner(self):
        l = ['a', 'b', 'c', 'd', 'e']
        self.assertEqual(partner(l, 'a', 'd'), ['d', 'b', 'c', 'a', 'e'])

    def test_spin(self):
        l = list('abcde')
        self.assertEqual(spin(l, 3), list('cdeab'))


if __name__ == '__main__':
    # unittest.main()
    inst = instructions_from_file('day_16_data.txt')
    line_up = list(string.ascii_lowercase[:16])
    answer = dance(line_up, inst, times=1000000000)
    print(answer)
