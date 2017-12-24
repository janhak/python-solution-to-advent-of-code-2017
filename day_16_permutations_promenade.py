import unittest
import string


def exchange(line_up, pos_a, pos_b):
    line_up[pos_a], line_up[pos_b] = line_up[pos_b], line_up[pos_a]
    return line_up


def partner(line_up, name_a, name_b):
    return exchange(line_up, line_up.index(name_a), line_up.index(name_b))


def spin(line_up, n):
    return line_up[-n:] + line_up[:-n]


def dance(line_up, instructions):
    for i in instructions:
        if i[0] == 's':
            instr_type = spin
            arguments = [int(i[1:])]
        elif i[0] == 'x':
            instr_type = exchange
            arguments = map(int, i[1:].split('/'))
        elif i[0] == 'p':
            instr_type = partner
            arguments = i[1:].split('/')
        print(i, instr_type, arguments)
        line_up = instr_type(line_up, *arguments)
    return ''.join(line_up)


INSTRUCTIONS = {
    's': spin,
    'x': exchange,
    'p': partner,
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
    print(dance(line_up, inst))
