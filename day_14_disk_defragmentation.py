from itertools import product
from day_10_knots import KnotHash, binary_hash, input_from_bytes
SIZE = 128


def memory_use(bin_hash):
    return sum(int(i) for i in bin_hash)


def memory_row(bin_hash):
    return [int(i) for i in bin_hash]


class RegionCounter:
    def __init__(self, memory):
        self.memory = memory

    def count(self):
        self.seen = set()
        self.regions = 0
        for x, y in product(range(SIZE), range(SIZE)):
            if memory[x][y] and (x, y) not in self.seen:
                self.regions += 1
                self.dfs(x, y)
        return self.regions

    def dfs(self, i, j):
        if (i, j) in self.seen:
            return
        if not memory[i][j]:
            return
        self.seen.add((i, j))
        for n in self.valid_neighbours(i, j):
            self.dfs(*n)

    def valid_neighbours(self, i, j):
        neighbours = ((i - 1, j), (i + 1, j), (i, j + 1), (i, j - 1))
        return (n for n in neighbours if self.valid(*n))

    def valid(self, i, j, size=SIZE):
        return i in range(SIZE) and j in range(SIZE)


if __name__ == '__main__':
    keys = (input_from_bytes('nbysizxe-{}'.format(n)) for n in range(SIZE))
    knots = (KnotHash(256, key) for key in keys)
    sparse_hashes = (knot.hash() for knot in knots)
    bin_hashes = (binary_hash(sh) for sh in sparse_hashes)
    memory = [memory_row(bh) for bh in bin_hashes]
    print('Memory regions', RegionCounter(memory).count())
