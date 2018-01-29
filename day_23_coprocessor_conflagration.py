"""
--- Day 23: Coprocessor Conflagration ---
You decide to head directly to the CPU and fix the printer from there. As you
get close, you find an experimental coprocessor doing so much work that the
local programs are afraid it will halt and catch fire. This would cause serious
issues for the rest of the computer, so you head in and see what you can do.

The code it's running seems to be a variant of the kind you saw recently on
that tablet. The general functionality seems very similar, but some of the
instructions are different:

set X Y sets register X to the value of Y.
sub X Y decreases register X by the value of Y.
mul X Y sets register X to the result of multiplying the value contained in
register X by the value of Y.
jnz X Y jumps with an offset of the value of Y, but only if the value of X is
not zero. (An offset of 2 skips the next instruction, an offset of -1 jumps to
the previous instruction, and so on.)

Only the instructions listed above are used. The eight registers here,
named a through h, all start at 0.

The coprocessor is currently set to some kind of debug mode, which allows for
testing, but prevents it from doing any meaningful work.

If you run the program (your puzzle input), how many times is the mul
instruction invoked?
"""
from collections import defaultdict


def line_to_instruction(line):
    """Parse raw line return a tuple of instruction and args"""
    inst, *args = line.strip().split()
    args = [arg if arg.isalpha() else int(arg) for arg in args]
    return inst, args


class Processor:
    def __init__(self, instructions):
        self.mem = defaultdict(int)
        self.mul_invoked = 0
        self.inst = list(instructions)
        self.next_inst = 0

    def __getitem__(self, x):
        if isinstance(x, int):
            return x
        else:
            return self.mem[x]

    def __setitem__(self, x, y):
        self.mem[x] = y

    def op_set(self, x, y):
        self[x] = self[y]

    def op_sub(self, x, y):
        self[x] -= self[y]

    def op_mul(self, x, y):
        self[x] *= self[y]
        self.mul_invoked += 1

    def op_jnz(self, x, y):
        if self[x] != 0:
            return self[y]

    def execute(self):
        while self.next_inst in range(0, len(self.inst)):
            inst, args = self.inst[self.next_inst]
            delta = getattr(self, 'op_%s' % inst)(*args)
            self.next_inst += delta if delta is not None else 1


def second_part():
    h = 0
    for b in range(109300, 126301, 17):
        for d in range(2, b):
            if b % d == 0:
                h += 1
                break
    return h


if __name__ == '__main__':
    lines = open('day_23_data.txt', 'rt').readlines()
    instructions = (line_to_instruction(l) for l in lines)
    runner = Processor(instructions)
    runner.execute()
    print('Multiplication invoked:', runner.mul_invoked)
    print('Second part, h is:', second_part())
