"""
--- Day 20: Particle Swarm ---

Suddenly, the GPU contacts you, asking for help. Someone has asked it to
simulate too many particles, and it won't be able to finish them all in time to
render the next frame at this rate.

It transmits to you a buffer (your puzzle input) listing each particle in order
(starting with particle 0, then particle 1, particle 2, and so on). For each
particle, it provides the X, Y, and Z coordinates for the particle's position
(p), velocity (v), and acceleration (a), each in the format <X,Y,Z>.

Each tick, all particles are updated simultaneously. A particle's properties
are updated in the following order:

Increase the X velocity by the X acceleration.
Increase the Y velocity by the Y acceleration.
Increase the Z velocity by the Z acceleration.
Increase the X position by the X velocity.
Increase the Y position by the Y velocity.
Increase the Z position by the Z velocity.

Because of seemingly tenuous rationale involving z-buffering, the GPU would
like to know which particle will stay closest to position <0,0,0> in the long
term. Measure this using the Manhattan distance, which in this situation is
simply the sum of the absolute values of a particle's X, Y, and Z position.

For example, suppose you are only given two particles, both of which stay
entirely on the X-axis (for simplicity). Drawing the current states of
particles 0 and 1 (in that order) with an adjacent a number line and diagram of
current X positions (marked in parenthesis), the following would take place:

p=< 3,0,0>, v=< 2,0,0>, a=<-1,0,0>    -4 -3 -2 -1  0  1  2  3  4
p=< 4,0,0>, v=< 0,0,0>, a=<-2,0,0>                         (0)(1)

p=< 4,0,0>, v=< 1,0,0>, a=<-1,0,0>    -4 -3 -2 -1  0  1  2  3  4
p=< 2,0,0>, v=<-2,0,0>, a=<-2,0,0>                      (1)   (0)

p=< 4,0,0>, v=< 0,0,0>, a=<-1,0,0>    -4 -3 -2 -1  0  1  2  3  4
p=<-2,0,0>, v=<-4,0,0>, a=<-2,0,0>          (1)               (0)

p=< 3,0,0>, v=<-1,0,0>, a=<-1,0,0>    -4 -3 -2 -1  0  1  2  3  4
p=<-8,0,0>, v=<-6,0,0>, a=<-2,0,0>                         (0)

At this point, particle 1 will never be closer to <0,0,0> than particle 0, and
so, in the long run, particle 0 will stay closest.

Which particle will stay closest to position <0,0,0> in the long term?

To begin, get your puzzle input.
"""
import re
import unittest


class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return 'Vector({}, {}, {})'.format(self.x, self.y, self.z)

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __eq__(self, other):
        return all((self.x == other.x, self.y == other.y, self.z == other.z))

    def __hash__(self):
        return hash((self.x, self.y, self.z))


class Particle:
    def __init__(self, pos, vel, acc, p_id=None):
        self.pos = pos
        self.vel = vel
        self.acc = acc
        self.p_id = p_id

    def update(self):
        self.vel += self.acc
        self.pos += self.vel

    @classmethod
    def from_line(cls, line, p_id=None):
        groups = re.findall(r'<([-0-9,]+)>', line)
        coordinates = (map(int, group.split(',')) for group in groups)
        vectors = (Vector(*xyz) for xyz in coordinates)
        return Particle(*vectors, p_id=p_id)

    def __repr__(self):
        return 'Particle({}, {}, {}, id={})'.format(self.pos, self.vel,
                                                    self.acc, self.p_id)

    @property
    def distance(self):
        return sum(map(abs, (self.pos.x, self.pos.y, self.pos.z)))


class TestParticleSwarm(unittest.TestCase):
    def setUp(self):
        l = 'p=<1918,-2104,2938>, v=<18,101,-32>, a=<-13,2,-14>'
        self.p = Particle.from_line(l)

    def test_parse_line(self):
        self.assertEqual(self.p.pos.x, 1918)
        self.assertEqual(self.p.vel.y, 101)
        self.assertEqual(self.p.acc.z, -14)

    def test_particle_distance(self):
        self.assertEqual(self.p.distance, 6960)

    def test_particle_update(self):
        self.p.update()
        self.assertEqual(self.p.distance, 6816)

    def test_filter_collissions(self):
        lines = [
            'p=<1918,-2104,2938>, v=<18,101,-32>, a=<-13,2,-14>',
            'p=<1918,-2104,2938>, v=<18,101,-32>, a=<-13,2,-14>',
            'p=<1918,-2104,2938>, v=<18,101,-32>, a=<-13,2,-14>',
            'p=<1900,-2104,2938>, v=<18,101,-32>, a=<-13,2,-14>',
            'p=<1900,-2104,2938>, v=<18,101,-32>, a=<-13,2,-14>',
            'p=<1901,-2104,2938>, v=<18,101,-32>, a=<-13,2,-14>',
        ]
        particles = [Particle.from_line(l, p_id=i)
                     for i, l in enumerate(lines)]
        filtered = filter_collissions(particles)
        self.assertEqual(len(filtered), 1)


def filter_collissions(particles):
    coordinates_seen = {}
    p_id_to_remove = set()
    for p in particles:
        try:
            to_remove = coordinates_seen[p.pos]
            p_id_to_remove.add(to_remove)
            p_id_to_remove.add(p.p_id)
        except KeyError:
            coordinates_seen[p.pos] = p.p_id
    return [p for p in particles if p.p_id not in p_id_to_remove]


def simulate_swarm(updates=3000, collisions=False):
    lines = open('day_20_data.txt', 'rt').readlines()
    particles = [Particle.from_line(l, p_id=i) for i, l in enumerate(lines)]
    for _ in range(updates):
        for p in particles:
            p.update()
        if collisions:
            particles = filter_collissions(particles)
    particles.sort(key=lambda x: x.distance)
    print(*particles[0:5], sep='\n')
    print('Particles left', len(particles))


if __name__ == '__main__':
    simulate_swarm(collisions=True)
    unittest.main()
