import unittest
from itertools import islice


class Generator:
    def __init__(self,
                 factor,
                 seed,
                 divisor=2147483647,
                 as_bin=True,
                 multiple=None):
        self.seed = seed
        self.factor = factor
        self.divisor = divisor
        self._prev = self.seed
        self.as_bin = as_bin
        self.multiple = multiple

    def __iter__(self):
        return self

    def __next__(self):
        self._prev = (self._prev * self.factor) % self.divisor
        if self.multiple and self._prev % self.multiple != 0:
            return next(self)
        return format(self._prev, 'b')[-16:] if self.as_bin else self._prev


class TestGenerators(unittest.TestCase):
    def test_generator_can_yield_one_value(self):
        a = Generator(factor=16807, seed=65, as_bin=False)
        self.assertEqual(next(a), 1092455)

    def test_first_values_match_example(self):
        b = Generator(factor=48271, seed=8921, as_bin=False)
        expected = (
            430625591,
            1233683848,
            1431495498,
            137874439,
            285222916, )
        for value, exp in zip(b, expected):
            with self.subTest(value=value, expected=exp):
                self.assertEqual(value, exp)

    def test_first_values_match_binary_example(self):
        a = Generator(factor=16807, seed=65, as_bin=True)
        expected = (
            '1010101101100111',
            '1111011100111001',
            '1110001101001010',
            '0001011011000111',
            '1001100000100100', )
        for value, exp in zip(a, expected):
            with self.subTest(value=value, expected=exp):
                self.assertEqual(value, exp)

    def test_multiple_generators(self):
        b = Generator(factor=48271, seed=8921, as_bin=False, multiple=8)
        expected = (
            1233683848,
            862516352,
            1159784568,
            1616057672,
            412269392, )
        for value, exp in zip(b, expected):
            with self.subTest(value=value, expected=exp):
                self.assertEqual(value, exp)


def find_matches(pairs_to_consider=40000000, m_a=None, m_b=None):
    gen_a = Generator(factor=16807, seed=618, multiple=m_a)
    gen_b = Generator(factor=48271, seed=814, multiple=m_b)
    pairs = islice(zip(gen_a, gen_b), pairs_to_consider)
    matching_pairs = (a == b for a, b in pairs)
    return sum(matching_pairs)


if __name__ == '__main__':
    # unittest.main()
    print('Total {} pairs found matching.'.format(
        find_matches(pairs_to_consider=5000000, m_a=4, m_b=8)))
