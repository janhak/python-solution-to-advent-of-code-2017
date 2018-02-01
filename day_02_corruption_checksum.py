import unittest


def lines(a_file):
    with open(a_file, 'rt') as f:
        for line in f:
            yield [int(no) for no in line.split()]


def minmax_checksum(line):
    return max(line) - min(line)


def modulo_checksum(line):
    for i, x in enumerate(line):
        for y in line[i + 1::]:
            if x % y == 0:
                return x / y
            if y % x == 0:
                return y / x


def calculate_checksum(a_file, line_checksum):
    line_checksums = (line_checksum(l) for l in lines(a_file))
    return sum(line_checksums)


class TestChecksums(unittest.TestCase):
    def test_modulo_checksum(self):
        data = (
            ([5, 9, 2, 8], 4),
            ([9, 4, 7, 3], 3),
            ([3, 8, 6, 5], 2), )
        for line, check in data:
            with self.subTest(line=line, checksum=check):
                self.assertEqual(modulo_checksum(line), check)


if __name__ == '__main__':
    print('Answer corruption checksum is: ',
          calculate_checksum(
              'day_2_spreadsheet.txt', line_checksum=minmax_checksum))

    print('Answer modulo corruption checksum is: ',
          calculate_checksum(
              'day_2_spreadsheet.txt', line_checksum=modulo_checksum))

    unittest.main()
