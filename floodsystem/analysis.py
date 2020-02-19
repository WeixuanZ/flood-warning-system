# Copyright (C) 2020 Ghifari Pradana
#
# SPDX-License-Identifier: MIT
import numpy as np
from matplotlib.dates import date2num


def polyfit(dates, levels, p):
    """
    Function that given the water level time history (dates, levels) for a station computes a least-squares fit of a polynomial of degree p to water level data.
    Args:
        param1 (list): The list of dates.
        param2 (list): The corresponding water level for each date
        param3 (int): Degree of the polynomial.
    Returns:
        Polynomial object.
        Shift of the time.
    """
    dates_num = date2num(dates)
    x = [date - dates_num[-1] for date in dates_num]
    y = levels
    print([x, y, len(x), len(y)])
    p_coeff = np.polyfit(x, y, p)
    poly = np.poly1d(p_coeff)
    return poly, dates_num[-1]
