# Copyright (C) 2020 Weixuan Zhang & Ghifari Pradana
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

    return sorted_by_key(filter(
        lambda x: x[1] > tol, 
        [(station, station.relative_water_level()) for station in stations 
                            if station.relative_water_level() is not None]
        ), 1, reverse=True)


def stations_highest_rel_level(stations, N):
    """
    Function that returns the N number of most at risk stations.
    Args:
        param1 (list): List of stations (type MonitoringStation).
        param2 (int): Length of the desired list
    Returns:
        list: List of stations(type MonitoringStation)
    """

    return map(lambda x: x[0],
        sorted_by_key([(station, station.relative_water_level()) for station in stations 
                            if station.relative_water_level() is not None], 1, reverse=True)[:N]
        )
    
