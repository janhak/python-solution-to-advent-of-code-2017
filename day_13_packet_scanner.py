"""
Packet Scanner
"""

# Firewall will be represented by list where index corresponds to depth and
# value corresponds to range.


class Layer:
    def __init__(self, depth, layer_range):
        self.depth = depth
        self.layer_range = layer_range

    def blocks(self, time):
        return time % (2 * (self.layer_range - 1)) == 0

    @property
    def severity(self):
        return self.depth * self.layer_range

    def __repr__(self):
        return 'Layer({}, {})'.format(self.depth, self.layer_range)


def lines_from_file(a_file):
    with open(a_file, 'rt') as f:
        for line in f:
            yield line.strip()


def parse_line(line):
    """Returns a tuple of depth, range integers from a line."""
    depth, range_ = map(int, line.split(':'))
    return depth, range_


def firewall_from_file(a_file):
    """
    Creates a firewall represented by a dict where keys correspond to
    active layers at a given depth.
    """
    lines = lines_from_file(a_file)
    layers = (parse_line(l) for l in lines)
    firewall = {d: Layer(d, r) for d, r in layers}
    return firewall


def trip_severity(firewall):
    time = 0
    total_severity = 0
    while firewall:
        next_layer = firewall.pop(time, None)
        try:
            if next_layer.blocks(time):
                total_severity += next_layer.severity
                print('Blocked at {} picoseconds by {}'
                      .format(time, next_layer))
        except AttributeError:
            pass
        time += 1
    return total_severity


if __name__ == '__main__':
    f = firewall_from_file('day_13_data.txt')
    print('Total trip severity:', trip_severity(f))
