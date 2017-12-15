"""
--- Day 6: Memory Reallocation ---

A debugger program here is having an issue: it is trying to repair a memory
reallocation routine, but it keeps getting stuck in an infinite loop.

In this area, there are sixteen memory banks; each memory bank can hold any
number of blocks. The goal of the reallocation routine is to balance the blocks
between the memory banks.

The reallocation routine operates in cycles. In each cycle, it finds the memory
bank with the most blocks (ties won by the lowest-numbered memory bank) and
redistributes those blocks among the banks. To do this, it removes all of the
blocks from the selected bank, then moves to the next (by index) memory bank
and inserts one of the blocks. It continues doing this until it runs out of
blocks; if it reaches the last memory bank, it wraps around to the first one.

The debugger would like to know how many redistributions can be done before a
blocks-in-banks configuration is produced that has been seen before.

For example, imagine a scenario with only four memory banks:

- The banks start with 0, 2, 7, and 0 blocks. The third bank has the most blocks,
so it is chosen for redistribution.

- Starting with the next bank (the fourth bank) and then continuing to the
first bank, the second bank, and so on, the 7 blocks are spread out over the
memory banks. The fourth, first, and second banks get two blocks each, and the
third bank gets one back. The final result looks like this: 2 4 1 2.

- Next, the second bank is chosen because it contains the most blocks (four).
Because there are four memory banks, each gets one block. The result is: 3 1 2
3. Now, there is a tie between the first and fourth memory banks, both of which
have three blocks. The first bank wins the tie, and its three blocks are
distributed evenly over the other three banks, leaving it with none: 0 2 3 4.

- The fourth bank is chosen, and its four blocks are distributed such that each
of the four banks receives one: 1 3 4 1.

- The third bank is chosen, and the same thing happens: 2 4 1 2. At this point,
we've reached a state we've seen before: 2 4 1 2 was already seen. The infinite
loop is detected after the fifth block redistribution cycle, and so the answer
in this example is 5.

Given the initial block counts in your puzzle input, how many redistribution
cycles must be completed before a configuration is produced that has been seen
before?
"""
import unittest


class MemoryReallocator:
    def __init__(self, memory):
        self.memory = memory
        self.memory_snapshots = set()
        self.record_memory()
        self._cycle = 0

    @property
    def largest_bank(self):
        return self.memory.index(max(self.memory))

    def reallocate(self):
        while True:
            self.cycle()

    def cycle(self):
        largest_bank = self.largest_bank
        to_distribute = self.empty_bank(largest_bank)
        self.reallocate_from(largest_bank, to_distribute)
        self._cycle += 1
        self.record_memory()

    def reallocate_from(self, bank, blocks):
        while blocks:
            bank = self.next_bank(bank)
            self.memory[bank] += 1
            blocks -= 1

    def empty_bank(self, bank_idx):
        blocks = self.memory[bank_idx]
        self.memory[bank_idx] = 0
        return blocks

    def next_bank(self, bank_idx):
        next_bank = bank_idx + 1
        try:
            self.memory[next_bank]
        except IndexError:
            next_bank = 0
        return next_bank

    def record_memory(self):
        to_record = tuple(self.memory)
        if to_record in self.memory_snapshots:
            raise RecursionError(
                "Infinite loop detected after %s cycles" % self._cycle)
        self.memory_snapshots.add(to_record)


class TestMemoryReallocator(unittest.TestCase):
    def test_snapshot_holds_initial_memory(self):
        mr = MemoryReallocator([1, 2, 3])
        self.assertIn((1, 2, 3), mr.memory_snapshots)

    def test_empty_largest_bank(self):
        mr = MemoryReallocator([1, 18])
        mr.empty_bank(mr.largest_bank)
        self.assertEqual(mr.largest_bank, 0)
        self.assertEqual(mr.memory, [1, 0])

    def test_record_memory_raises_with_non_uniqe_memory(self):
        mr = MemoryReallocator([1, 18])
        with self.assertRaises(RecursionError):
            mr.record_memory()

    def test_reallocate_from_distributes_blocks(self):
        mr = MemoryReallocator([0, 2, 7, 0])
        mr.cycle()
        self.assertEqual(mr.memory, [2, 4, 1, 2])

    def test_reallocate_stops(self):
        mr = MemoryReallocator([0, 2, 7, 0])
        with self.assertRaises(RecursionError):
            mr.reallocate()


if __name__ == '__main__':
    memory = [4, 10, 4, 1, 8, 4, 9, 14, 5, 1, 14, 15, 0, 15, 3, 5]
    mr = MemoryReallocator(memory)
    mr.reallocate()
