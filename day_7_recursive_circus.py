"""
--- Day 7: Recursive Circus ---

Wandering further through the circuits of the computer, you come upon a tower
of programs that have gotten themselves into a bit of trouble. A recursive
algorithm has gotten out of hand, and now they're balanced precariously in a
large tower.

One program at the bottom supports the entire tower. It's holding a large disc,
and on the disc are balanced several more sub-towers. At the bottom of these
sub-towers, standing on the bottom disc, are other programs, each holding their
own disc, and so on. At the very tops of these sub-sub-sub-...-towers, many
programs stand simply keeping the disc below them balanced but with no disc of
their own.

You offer to help, but first you need to understand the structure of these
towers. You ask each program to yell out their name, their weight, and (if
they're holding a disc) the names of the programs immediately above them
balancing on that disc. You write this information down (your puzzle input).
Unfortunately, in their panic, they don't do this in an orderly fashion; by the
time you're done, you're not sure which program gave which information.

For example, if your list is the following:

pbga (66)
xhth (57)
ebii (61)
havc (66)
ktlj (57)
fwft (72) -> ktlj, cntj, xhth
qoyq (66)
padx (45) -> pbga, havc, qoyq
tknk (41) -> ugml, padx, fwft
jptl (61)
ugml (68) -> gyxo, ebii, jptl
gyxo (61)
cntj (57)

...then you would be able to recreate the structure of the towers that looks like this:

                gyxo
              /
         ugml - ebii
       /      \
      |         jptl
      |
      |         pbga
     /        /
tknk --- padx - havc
     \        \
      |         qoyq
      |
      |         ktlj
       \      /
         fwft - cntj
              \
                xhth

In this example, tknk is at the bottom of the tower (the bottom program), and
is holding up ugml, padx, and fwft. Those programs are, in turn, holding up
other programs; in this example, none of those programs are holding up any
other programs, and are all the tops of their own towers. (The actual tower
balancing in front of you is much larger.)

Before you're ready to help them, you need to make sure your information is
correct. What is the name of the bottom program?
"""

def yield_lines(a_file):
    with open(a_file, 'rt') as f:
        for line in f:
            yield line


def parse_line(line):
    children = None
    try:
        parent, children = line.split('->')
        name, weight = parse_parent(parent)
        children = parse_child(children)
    except ValueError:
        name, weight = parse_parent(line)
    return Node(name, weight, children=children)


def parse_parent(line):
    blocks = line.split()
    parent = blocks[0]
    weight = int(blocks[1].replace('(', '').replace(')', ''))
    return parent, weight


def parse_child(line):
    children = line.split(',')
    return (c.strip() for c in children)


class Node:
    def __init__(self, name, weight, parent=None, children=None):
        self.name = name
        self.weight = weight
        self.parent = parent
        self.children = list(children) if children else []

    def link_children(self, node_map):
        children = [node_map[name] for name in self.children]
        self.children = children
        for child in self.children:
            child.parent = self

    def __repr__(self):
        return (f'Node(name={self.name!r},'
                f' weight={self.weight!r},'
                f' children={[c.name for c in self.children]})')


if __name__ == '__main__':
    lines = yield_lines('day_7_data.txt')
    nodes = (parse_line(l) for l in lines)
    node_map = {node.name: node for node in nodes}
    for node in node_map.values():
        node.link_children(node_map)
    root = next(filter(lambda x: x.parent is None, node_map.values()))
    print(root)
