# -*- coding: utf-8 -*-
"""Useful methods.

This module defines some useful methods for the application.

Attributes:
    SCALE (int): The scale conversion of float to int.

"""
SCALE = 7


def degree_to_int(degree):
    """Convert the float degree to int.
    """
    fl = float(degree)
    return int(fl * (10 ** SCALE))


def int_to_degree(integer):
    """Convert the int integer to a float.
    """
    i = int(integer)
    return float(i / (10 ** SCALE))


def pre_order(size):
    """List in pre order of integers ranging from 0 to size in a balanced
    binary tree.
    """
    interval_list = [None] * size
    interval_list[0] = (0, size)
    tail = 1

    for head in range(size):
        start, end = interval_list[head]
        mid = (start + end) // 2

        if mid > start:
            interval_list[tail] = (start, mid)
            tail += 1

        if mid + 1 < end:
            interval_list[tail] = (mid + 1, end)
            tail += 1

        interval_list[head] = mid

    return interval_list


def search(element, indices, values, sorted=True):
    """Search element in a list of values.

    Args:
        element (int or str): The element to search.
        indices (:obj:`list` of :obj:`int`): The list of indices to consider in
            the search.
        values (:obj:`list` of :obj:`int` or `str`): The list of values.
        sorted (bool, optional): True if values are sorted, false otherwise.

    Returns:
        (:obj:`tuple` of :obj:`int):
        (int: The index of the selected index in the indices list,
         int: The index of the selected value in the values list)

    """
    # If values is a sorted list, we only need the limits of that list
    if sorted:
        def get_index(i):
            return i
        start, end = (indices[0], indices[1])
    # If values is not sorted, we need the list of indices of values if it was
    # sorted
    else:
        def get_index(i):
            return indices[min(i, len(indices) - 1)]
        start, end = (0, len(indices))

    return binary_search(element, values, start, end, get_index)


def binary_search(element, values, start, end, get_index):
    """Binary search of element in values.
    """
    i = start
    j = end
    while i < j:
        mid = (i + j) // 2
        midvalue = values[get_index(mid)]
        if midvalue < element:
            i = mid + 1
        else:
            j = mid
    return (i, get_index(i))


def most_similar(indices, values, similarity):
    """Find the value with greatest score of similarity.
    """
    max_result = None, None, None
    for (rang, index) in enumerate(indices):
        score = similarity(values[index])
        max_score = max_result[0]
        if score == 1:
            return score, rang, index
        elif max_score is None or score > max_score:
            max_result = score, rang, index
    return max_result
