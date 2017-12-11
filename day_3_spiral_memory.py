import unittest


def allocate_memory(n):
    # Allocate memory according to spiral algorithm and return coordinates
    # Algorithm to move over the structure
    # last move - next move
    # R - U unless impossible then R
    # L - D unless impossible then L
    # D - R unless impossible then D
    # U - L unless impossible then U
    up = (1, 0)
    right = (0, 1)
    left = (0, -1)
    down = (-1, 0)
    next_move = {
        right: (up, right),
        left: (down, left),
        down: (right, down),
        up: (left, up),
    }
    memory = {(0, 0): 1, (0, 1): 2}
    prev_move = right
    position = (0, 1)
    number = 2
    while number < n:
        possible_moves = next_move[prev_move]
        for move in possible_moves:
            new_position = (position[0] + move[0], position[1] + move[1])
            if new_position not in memory:
                number += 1
                memory[new_position] = number
                prev_move = move
                position = new_position
                break
    return position


def dist(x, y):
    return abs(x) + abs(y)


class TestSpiralMemory(unittest.TestCase):
    def test_known_allocate_memory(self):
        data = (
            (3, (1, 1)),
            (12, (1, 2)),
            (2, (0, 1)),
            (13, (2, 2)),
            (21, (-2, -2)), )
        for no, position in data:
            with self.subTest(n=no, p=position):
                self.assertEqual(allocate_memory(no), position)


if __name__ == '__main__':
    print(dist(*allocate_memory(325489)))
    unittest.main()
