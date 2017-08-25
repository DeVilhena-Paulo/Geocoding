# -*- coding: utf-8 -*-
"""String similarity methods.

This module defines the class used for computing the score of similarity
between two strings. Even with the ideas for computing this score are well know
(ngrams), the exactly method is not and that`s why an own implementation was
needed.
"""


class Similarity():
    """Class defining the string similarity methods using uni and bigrams.

    One object of this class will have a set of uni and bigrams of a string s
    as an attribute. The string s is an argument of __init__ and this set is
    used in the score method to compute the score of similarity between s and
    one second string t, for example.

    Attributes:
        slice_set (:obj:`set` of :obj:`str`): The set of uni and bigrams.
        slice_set_score (int): The score of the attribute slice_set, that is,
            the sum of the length of the strings in that set.

    """

    def __init__(self, s):
        """
        Args:
            s (str): The string to compute the 1 and 2 grams set.

        """
        self.slice_set = set(list(s) + self.k_letters_list(s, 2))
        self.slice_set_score = self.set_score(self.slice_set)

    def k_letters_list(self, s, k):
        """List of all the strings formed by k consecutive letters of s.

        Divide a string s into a list of strings, where each string is formed
        by k consecutive letters of s.

        Args:
            s (str): The string to divide.
            k (int): The number of consecutive letters.

        Returns:
            (:obj:`list` of :obj:`str`): The list of strings with k consecutive
                letters of s.

        """
        return [s[i:(i + k)] for i in range(0, len(s) - (k - 1))]

    def set_score(self, words_set):
        """Sum of the lentgh of all elements from a set of strings.
        """
        return sum([len(word) for word in words_set])

    def score(self, t):
        """String similarity score.

        The score of similarity between two strings s and t is defined as the
        score of the intersection over the score of the union of two sets: the
        set of unigrams and bigrams of s and t.

        Args:
            t (str): The string to compare.

        Returns:
            (float): The score of similarity between t and the string s passed
                as argument in the initialization of the class.

        """
        # Union of the unigram and bigram of t
        slice_set = set(list(t) + self.k_letters_list(t, 2))
        slice_set_score = self.set_score(slice_set)

        # The intersection between the slice_set of s and t.
        intersection = slice_set & self.slice_set
        intersection_score = self.set_score(intersection)

        union_score = slice_set_score + self.slice_set_score - \
            intersection_score

        # The union_score is zero only if both s and t are empty
        if union_score == 0:
            return 0

        return intersection_score / union_score
