"""
--- Day 25: The Halting Problem ---
Following the twisty passageways deeper and deeper into the CPU, you finally
reach the core of the computer. Here, in the expansive central chamber, you
find a grand apparatus that fills the entire room, suspended nanometers above
your head.

You had always imagined CPUs to be noisy, chaotic places, bustling with
activity. Instead, the room is quiet, motionless, and dark.

Suddenly, you and the CPU's garbage collector startle each other. "It's not
often we get many visitors here!", he says. You inquire about the stopped
machinery.

"It stopped milliseconds ago; not sure why. I'm a garbage collector, not a
doctor." You ask what the machine is for.

"Programs these days, don't know their origins. That's the Turing machine! It's
what makes the whole computer work." You try to explain that Turing machines
are merely models of computation, but he cuts you off. "No, see, that's just
what they want you to think. Ultimately, inside every CPU, there's a Turing
machine driving the whole thing! Too bad this one's broken. We're doomed!"

You ask how you can help. "Well, unfortunately, the only way to get the
computer running again would be to create a whole new Turing machine from
scratch, but there's no way you can-" He notices the look on your face, gives
you a curious glance, shrugs, and goes back to sweeping the floor.

You find the Turing machine blueprints (your puzzle input) on a tablet in a
nearby pile of debris. Looking back up at the broken Turing machine above, you
can start to identify its parts:

- A tape which contains 0 repeated infinitely to the left and right.
- A cursor, which can move left or right along the tape and read or write
  values at its current position.
- A set of states, each containing rules about what to do based on the current
  value under the cursor.

Each slot on the tape has two possible values: 0 (the starting value for all
slots) and 1. Based on whether the cursor is pointing at a 0 or a 1, the
current state says what value to write at the current position of the cursor,
whether to move the cursor left or right one slot, and which state to use next.

For example, suppose you found the following blueprint:

Begin in state A.
Perform a diagnostic checksum after 6 steps.

In state A:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state B.
  If the current value is 1:
    - Write the value 0.
    - Move one slot to the left.
    - Continue with state B.

In state B:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the left.
    - Continue with state A.
  If the current value is 1:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state A.

Running it until the number of steps required to take the listed diagnostic
checksum would result in the following tape configurations (with the cursor
marked in square brackets):

... 0  0  0 [0] 0  0 ... (before any steps; about to run state A)
... 0  0  0  1 [0] 0 ... (after 1 step;     about to run state B)
... 0  0  0 [1] 1  0 ... (after 2 steps;    about to run state A)
... 0  0 [0] 0  1  0 ... (after 3 steps;    about to run state B)
... 0 [0] 1  0  1  0 ... (after 4 steps;    about to run state A)
... 0  1 [1] 0  1  0 ... (after 5 steps;    about to run state B)
... 0  1  1 [0] 1  0 ... (after 6 steps;    about to run state A)

The CPU can confirm that the Turing machine is working by taking a diagnostic
checksum after a specific number of steps (given in the blueprint). Once the
specified number of steps have been executed, the Turing machine should pause;
once it does, count the number of times 1 appears on the tape. In the above
example, the diagnostic checksum is 3.

Recreate the Turing machine and save the computer! What is the diagnostic
checksum it produces once it's working again?
"""
from collections import defaultdict


class StateMachine:
    def __init__(self):
        self.tape = defaultdict(int)
        self.state = State(self.tape)

    def run_instruction(self, no=1):
        for _ in range(1, no + 1):
            self.state.action()

    @property
    def checksum(self):
        return sum(v for v in self.tape.values())


class State:
    def __init__(self, tape):
        self.new_state(State_A)
        self.tape = tape
        self.pos = 0

    def new_state(self, state):
        self.__class__ = state

    def action(self):
        if self.current_value == 0:
            return self.act_zero()
        elif self.current_value == 1:
            return self.act_one()

    def act_zero(self):
        raise NotImplementedError()

    def act_one(self):
        raise NotImplementedError()

    def move_left(self):
        self.pos -= 1

    def move_right(self):
        self.pos += 1

    def write(self, value):
        self.tape[self.pos] = value

    @property
    def current_value(self):
        return self.tape[self.pos]

    def __repr__(self):
        return '{}(pos={})'.format(self.__class__.__name__, self.pos)


class State_A(State):
    def act_zero(self):
        self.write(1)
        self.move_right()
        self.new_state(State_B)

    def act_one(self):
        self.write(0)
        self.move_left()
        self.new_state(State_C)


class State_B(State):
    def act_zero(self):
        self.write(1)
        self.move_left()
        self.new_state(State_A)

    def act_one(self):
        self.write(1)
        self.move_right()
        self.new_state(State_D)


class State_C(State):
    def act_zero(self):
        self.write(1)
        self.move_right()
        self.new_state(State_A)

    def act_one(self):
        self.write(0)
        self.move_left()
        self.new_state(State_E)


class State_D(State):
    def act_zero(self):
        self.write(1)
        self.move_right()
        self.new_state(State_A)

    def act_one(self):
        self.write(0)
        self.move_right()
        self.new_state(State_B)


class State_E(State):
    def act_zero(self):
        self.write(1)
        self.move_left()
        self.new_state(State_F)

    def act_one(self):
        self.write(1)
        self.move_left()
        self.new_state(State_C)


class State_F(State):
    def act_zero(self):
        self.write(1)
        self.move_right()
        self.new_state(State_D)

    def act_one(self):
        self.write(1)
        self.move_right()
        self.new_state(State_A)


# Example State Machine
# class State_A(State):
#     def act_zero(self):
#         self.tape[self.pos] = 1
#         self.pos += 1
#         self.new_state(State_B)

#     def act_one(self):
#         self.tape[self.pos] = 0
#         self.pos -= 1
#         self.new_state(State_B)

# class State_B(State):
#     def act_zero(self):
#         self.tape[self.pos] = 1
#         self.pos -= 1
#         self.new_state(State_A)

#     def act_one(self):
#         self.tape[self.pos] = 1
#         self.pos += 1
#         self.new_state(State_A)

if __name__ == '__main__':
    machine = StateMachine()
    machine.run_instruction(no=12919244)
    print('After 12919244 instructions:')
    print('Checksum', machine.checksum)
    print('State', machine.state)
