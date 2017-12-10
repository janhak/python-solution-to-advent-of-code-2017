def lines(a_file):
    with open(a_file, 'rt') as f:
        for line in f:
            yield [int(no) for no in line.split()]


def line_checksum(line):
    return max(line) - min(line)

def calculate_checksum(a_file):
    line_checksums = (line_checksum(l) for l in lines(a_file))
    return sum(line_checksums)

if __name__ == '__main__':
    print('Answer corruption checksum is: ', calculate_checksum('day_2_spreadsheet.txt'))
