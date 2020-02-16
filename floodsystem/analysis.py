# Copyright (C) 2020 Ghifari Pradana
#
# SPDX-License-Identifier: MIT
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import date2num


def polyfit(dates, levels, p):
    dates_num = date2num(dates)
    x = [date - dates_num[-1] for date in dates_num]
    y = levels
    print([x,y,len(x),len(y)])
    p_coeff = np.polyfit(x,y,p)
    poly = np.poly1d(p_coeff)
    return poly, dates_num[-1]