#!/usr/bin/env python3

"""module: syllable_filter
author: R Steiner
license: MIT, copyright (c) 2016 R Steiner

Contains class SyllableFilter.
"""


class SyllableFilter:
    """This script takes a list of words and returns only those with the
    specified number of syllables. Syllables will be counted heuristically,
    as the number of vowels.

    Methods:
    __init__ -- constructor for a SyllableFilter object.
    count_syllables -- returns the number of syllables (vowels) in a word.
    filter_words -- returns a list of the words from the corpus with the desired
    number of syllables.
    """
    def __init__(self, **kwargs):
        """Constructor for the SyllableFilter class.

        Keyword arguments:
        corpus -- The path to the file containing the words in the corpus. The
        file should have one word per line. (default:
        "../databases/iphod/IPhOD2_Words_phono_only.txt")
        vowels -- Either a list of the characters used as vowels in the corpus,
        or the path to a file containing these, with one vowel per line.
        (default: "../databases/iphod/cmu_vowels.txt")
        sep -- A string to use as the delimiter for separating phonemes in the
        words in the corpus. It can be an empty string (""), which will break
        the words into individual characters. (default: ".")
        """
        corpus = kwargs.get("corpus",
                            "../databases/iphod/iphod_words_phono_only.txt")
        vowels = kwargs.get("vowels", "../databases/iphod/cmu_vowels.txt")
        self.sep = kwargs.get("sep", ".")
        # Read the corpus file line-by-line, and create a list from the lines.
        with open(corpus, 'r') as corpusfile:
            self.corpus = [word[:-1] for word in corpusfile]
        # If user provided a string for "vowels", assume it is a file path and
        # read it. Create a list of the lines in the file.
        if type(vowels) == str:
            with open(vowels, 'r') as vowelfile:
                self.vowels = [vowel[:-1] for vowel in vowelfile]
        # If they did not provide a string, check to make sure they provided a
        # list (of vowels) instead. If they did not, raise an error.
        else:
            assert(type(vowels) == list)
            self.vowels = vowels

    def count_syllables(self, word):
        """Returns the number of syllables (vowels) in a word.

        Arguments:
        word -- the word to be analyzed
        """

        counter = 0
        phonemes = word.split(self.sep)
        for phoneme in phonemes:
            counter += 1 if phoneme in self.vowels else 0
        return counter

    def filter_words(self, nsyll):
        """Returns a list of the words with the desired number of syllables.

        Arguments:
        nsyll -- an integer or list of integers containing the number of
        syllables desired.
        """

        nsyll = [nsyll] if type(nsyll) == int else nsyll
        self.match = list(filter(lambda w: self.count_syllables(w) in nsyll,
                                 self.corpus))

if __name__ == "__main__":
    my_filter = SyllableFilter()
    my_filter.filter_words(1)
    with open("../databases/iphod/iphod_words_monosyllabic_phono_only.txt",
              "w") as f:
        f.write("\n".join(my_filter.match))
