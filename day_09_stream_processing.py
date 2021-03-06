"""
--- Day 9: Stream Processing ---

A large stream blocks your path. According to the locals, it's not safe to
cross the stream at the moment because it's full of garbage. You look down at
the stream; rather than water, you discover that it's a stream of characters.

You sit for a while and record part of the stream (your puzzle input). The
characters represent groups - sequences that begin with { and end with }.
Within a group, there are zero or more other things, separated by commas:
either another group or garbage. Since groups can contain other groups, a }
only closes the most-recently-opened unclosed group - that is, they are
nestable. Your puzzle input represents a single, large group which itself
contains many smaller ones.

Sometimes, instead of a group, you will find garbage. Garbage begins with < and
ends with >. Between those angle brackets, almost any character can appear,
including { and }. Within garbage, < has no special meaning.

In a futile attempt to clean up the garbage, some program has canceled some of
the characters within it using !: inside garbage, any character that comes
after ! should be ignored, including <, >, and even another !.

You don't see any characters that deviate from these rules. Outside garbage,
you only find well-formed groups, and garbage always terminates according to
the rules above.

Here are some self-contained pieces of garbage:

<>, empty garbage.
<random characters>, garbage containing random characters.
<<<<>, because the extra < are ignored.
<{!>}>, because the first > is canceled.
<!!>, because the second ! is canceled, allowing the > to terminate the garbage.
<!!!>>, because the second ! and the first > are canceled.
<{o"i!a,<{i<a>, which ends at the first >.
Here are some examples of whole streams and the number of groups they contain:

{}, 1 group.
{{{}}}, 3 groups.
{{},{}}, also 3 groups.
{{{},{},{{}}}}, 6 groups.
{<{},{},{{}}>}, 1 group (which itself contains garbage).
{<a>,<a>,<a>,<a>}, 1 group.
{{<a>},{<a>},{<a>},{<a>}}, 5 groups.
{{<!>},{<!>},{<!>},{<a>}}, 2 groups (since all but the last > are canceled).

Your goal is to find the total score for all groups in your input. Each group
is assigned a score which is one more than the score of the group that
immediately contains it. (The outermost group gets a score of 1.)

{}, score of 1.
{{{}}}, score of 1 + 2 + 3 = 6.
{{},{}}, score of 1 + 2 + 2 = 5.
{{{},{},{{}}}}, score of 1 + 2 + 3 + 3 + 3 + 4 = 16.
{<a>,<a>,<a>,<a>}, score of 1.
{{<ab>},{<ab>},{<ab>},{<ab>}}, score of 1 + 2 + 2 + 2 + 2 = 9.
{{<!!>},{<!!>},{<!!>},{<!!>}}, score of 1 + 2 + 2 + 2 + 2 = 9.
{{<a!>},{<a!>},{<a!>},{<ab>}}, score of 1 + 2 = 3.

What is the total score for all groups in your input?
"""
import unittest


def read_stream(a_file):
    with open(a_file, 'rt') as f:
        return f.readline()


def clean_stream(stream):
    stream = ''.join(filter_negators(stream))
    return ''.join(filter_garbage(stream))


def score_stream(stream):
    total_score = 0
    next_group_score = 0
    for char in stream:
        if char == '{':
            next_group_score += 1
        elif char == '}':
            total_score += next_group_score
            next_group_score -= 1
    return total_score


def filter_negators(stream):
    """Filters out all characters after ! negation mark from stream."""
    stream = iter(stream)
    for char in stream:
        if char == '!':
            next(stream)
            continue
        yield char


def filter_garbage(stream):
    """Filters out all characters in <> from stream."""
    stream = iter(stream)
    garbage_count = 0
    for char in stream:
        if char == '<':
            while True:
                terminator = next(stream)
                if terminator == '>':
                    break
                garbage_count += 1
            continue
        yield char
    print('Final garbage count', garbage_count)


def clean_and_score(stream):
    stream = clean_stream(stream)
    return score_stream(stream)


class TestStreamProcessor(unittest.TestCase):
    def test_negator(self):
        stream = 'g!!k!s'
        self.assertEqual(''.join(filter_negators(stream)), 'gk')

    def test_garbage_filter(self):
        stream = 'g<<flkajds>gh'
        self.assertEqual(''.join(filter_garbage(stream)), 'ggh')

    def test_score_stream(self):
        data = (
            ('{}', 1),
            ('{{{}}}', 6),
            ('{{},{}}', 5),
            ('{{{},{},{{}}}}', 16),
            ('{<a>,<a>,<a>,<a>}', 1),
            ('{{<ab>},{<ab>},{<ab>},{<ab>}}', 9),
            ('{{<!!>},{<!!>},{<!!>},{<!!>}}', 9),
            ('{{<a!>},{<a!>},{<a!>},{<ab>}}', 3), )
        for stream, score in data:
            with self.subTest(stream=stream, score=score):
                self.assertEqual(clean_and_score(stream), score)


if __name__ == '__main__':
    # unittest.main()
    print(clean_and_score(read_stream('day_09_data.txt')))
