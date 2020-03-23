# Copyright (C) 2020 Ghifari Pradana
#
# SPDX-License-Identifier: MIT
"""This module contains function for polynomial fitting on data"""
import numpy as np
from matplotlib.dates import date2num


def polyfit(dates, levels, p):
    """
    Function that finds the least-square fit polynomial from
    
    Args:
        dates (list): The list of dates for the x-axis.
        levels (list): The corresponding water level for each date, y-axis.
        p (int): The degree of polynomial that is desired.
    
    Returns:
        numpy poly1d Object: Contains the coefficients of the resulting polynomial
        float: The number of days since the origin of the Gregorain Calendar that was shifted to find the polynomial.
    """
    dates_num = date2num(dates)
    x = [date - dates_num[-1] for date in dates_num]
    y = levels
    p_coeff = np.polyfit(x, y, p)
    poly = np.poly1d(p_coeff)
    return poly, dates_num[-1]
