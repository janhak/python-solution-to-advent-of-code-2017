"""
A new system policy has been put in place that requires all accounts to use a
passphrase instead of simply a password. A passphrase consists of a series of
words (lowercase letters) separated by spaces. To ensure security, a valid
passphrase must contain no duplicate words.
For example:
aa bb cc dd ee is valid.
aa bb cc dd aa is not valid - the word aa appears more than once.
aa bb cc dd aaa is valid - aa and aaa count as different words.
The system's full passphrase list is available as your puzzle input. How many
passphrases are valid?
"""
import unittest


def passphrases_from_file(a_file):
    with open(a_file, 'rt') as f:
        for line in f:
            yield line


def passphrase_valid_unique_words(passphrase):
    """Valid if no two words are identical"""
    words = passphrase.split()
    all_words = len(words)
    uniqe_words = len(set(words))
    return all_words == uniqe_words


def passphrase_valid(passphrase):
    """Valid if no two words in the passphrase are anagrams."""
    words = passphrase.split()
    no_anagrams = set(frozenset(word) for word in words)
    all_words = len(words)
    words_with_no_anagrams = len(no_anagrams)
    return all_words == words_with_no_anagrams


class TestPassphraseValidator(unittest.TestCase):
    def test_is_passphrase_valid(self):
        phrases = (
            ('aa bb cc dd ee', True),
            ('aa bb cc dd aa', False),
            ('aa bb cc dd aaa', True)
            )
        for p, valid in phrases:
            with self.subTest(phrase=p, valid=valid):
                self.assertEqual(passphrase_valid_unique_words(p), valid)


if __name__ == '__main__':
    phrases = passphrases_from_file('day_04_passphrases.txt')
    valid_pp = sum(1 for pp in phrases if passphrase_valid(pp))
    print('Valid passphrases: ', valid_pp)
