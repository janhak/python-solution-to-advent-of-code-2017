from day_10_knots import KnotHash, binary_hash, input_from_bytes


def memory_use(bin_hash):
    return sum(int(i) for i in bin_hash)


if __name__ == '__main__':
    SIZE = 128
    keys = (input_from_bytes('nbysizxe-{}'.format(n)) for n in range(SIZE))
    knots = (KnotHash(256, key) for key in keys)
    sparse_hashes = (knot.hash() for knot in knots)
    bin_hashes = (binary_hash(sh) for sh in sparse_hashes)
    mem_per_row = (memory_use(bh) for bh in bin_hashes)
    print('Memory used:', sum(mem_per_row))
