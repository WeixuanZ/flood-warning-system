# Copyright (C) 2020 Weixuan Zhang
#
# SPDX-License-Identifier: MIT
"""This module contains a collection of functions related to
flooding.

"""

from .utils import sorted_by_key


def stations_level_over_threshold(stations, tol):
    """
    Function that returns stations whose latest relative water level is over some threshold.
    Args:
        param1 (list): List of stations (type MonitoringStation).
        param2 (float): The threshold relative water level.
    Returns:
        list: List of tuples in the format (station (type MonitoringStation), relative water level) sorted by the relative level in descending order.
    """
    available_data = [(station, station.relative_water_level()) for station in stations if
                      station.relative_water_level() is not None]
    return sorted_by_key([i for i in available_data if i[1] > tol], 1, reverse=True)
