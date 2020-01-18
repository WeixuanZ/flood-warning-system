# Copyright (C) 2020 Weixuan Zhang
#
# SPDX-License-Identifier: MIT
"""This module contains a collection of functions related to
geographical data.

"""

from math import sqrt, asin, sin, cos, radians

from .utils import sorted_by_key  # noqa


def haversine(a, b):
    '''
    Function that calculates the haversine distances between two points in kilometers.
    Args:
        param1 (tuple): The coordinate of the first point as (latitude, longitude).
        param2 (tuple): The coordinate of the second point as (latitude, longitude).
    Returns:
        float: Haversine distance.
    '''

    r = 6371
    a_lat, a_long = a[0], a[1]
    b_lat, b_long = b[0], b[1]

    return 2 * r * asin(sqrt(sin(radians((b_lat - a_lat) / 2)) ** 2 + cos(radians(a_lat)) * cos(radians(b_lat)) * sin(radians((b_long - a_long) / 2)) ** 2))


def stations_by_distance(stations, p):
    '''
    Function that returns the sorted distances between the input stations and a specified point p.
    Args:
        param1 (list): List of stations (MonitoringStation object).
        param2 (tuple): Coordinate of the origin.
    Retuens:
        list: List of (station, distance) sorted by distance.
    '''

    distances = []
    for station in stations:
        distances.append((station, haversine(station.coord, p)))
    return sorted_by_key(distances, 1)
