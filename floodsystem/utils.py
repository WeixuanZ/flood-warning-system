# Copyright (C) 2018 Garth N. Wells
#
# SPDX-License-Identifier: MIT
"""This module contains utility functions."""


def sorted_by_key(x, i, reverse=False):
    """For a list of lists/tuples, return list sorted by the ith
    component of the list/tuple, 
    
    Examples:
        Sort on first entry of tuple:

            >>> sorted_by_key([(1, 2), (5, 1)], 0)
            [(1, 2), (5, 1)]

        Sort on second entry of tuple:
        
            >>> sorted_by_key([(1, 2), (5, 1)], 1)
            [(5, 1), (1, 2)]
    
    Args:
        x (list): A list of lists/tuples to be sorted
        i (int): Sort according to which element of the inner lists/tuples
        reverse (bool, optional): Default False
    
    Returns:
        list: Sorted list of lists/tuples
    
    """

    return sorted(x, key=lambda x: x[i], reverse=reverse)
