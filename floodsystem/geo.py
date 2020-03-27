# Copyright (C) 2020 Weixuan Zhang & Ghifari Pradana
#
# SPDX-License-Identifier: MIT
"""This module contains a collection of functions related to
geographical data.

"""

from functools import reduce
from itertools import groupby
from math import sqrt, asin, sin, cos, radians

try:
    from .utils import sorted_by_key  # noqa
except ImportError:
    from utils import sorted_by_key


def haversine(a, b):
    """
    Function that calculates the haversine distances between two points in kilometers.

    Args:
        a (tuple): The coordinate of the first point as (latitude, longitude).
        b (tuple): The coordinate of the second point as (latitude, longitude).

    Returns:
        float: Haversine distance.
    """

    r = 6371
    a_lat, a_lng = a[0], a[1]
    b_lat, b_lng = b[0], b[1]

    return (
        2
        * r
        * asin(
            sqrt(
                sin(radians((b_lat - a_lat) / 2)) ** 2
                + cos(radians(a_lat))
                * cos(radians(b_lat))
                * sin(radians((b_lng - a_lng) / 2)) ** 2
            )
        )
    )


def stations_by_distance(stations, p):
    """
    Function that returns the sorted distances between the input stations and a specified point p.

    Args:
        stations (list): List of stations (MonitoringStation).
        p (tuple): Coordinate of the origin.

    Returns:
        list: List of (station, distance) sorted by distance.
    """

    return sorted_by_key([(i.name, i.town, haversine(i.coord, p)) for i in stations], 2)


def stations_within_radius(stations, centre, r):
    """
    Function that returns a list of all stations (MonitoringStation)
    within radius r of a geographic coordinate.

    Args:
        stations (list): List of stations (MonitoringStation).
        centre (tuple): Coordinate of centre in (latitude, longitude).
        r (float): Radius in kilometers.

    Returns:
        list: List of stations (MonitoringStation) within the distance.
    """

    return [station for station in stations if haversine(station.coord, centre) <= r]


def rivers_with_station(stations):
    """
    Function that, given a list of station objects,
    returns a container with the names of the rivers with a monitoring station.

    Args:
        stations (list): List of stations (MonitoringStation).

    Returns:
        set: Set of names of rivers with a monitoring station.
    """

    return {station.river for station in stations}


def stations_by_river(stations):
    """
    Function that returns a dictionary that maps river names (the ‘key’)
    to a list of station objects on a given river.

    Args:
        stations (list): List of stations (MonitoringStation).

    Returns:
        dict: Keys - river names.
    """

    return {
        key: list(value)
        for key, value in groupby(
            sorted(stations, key=lambda x: x.river), lambda x: x.river
        )
    }


def rivers_by_station_number(stations, N):
    """
    Function that returns a list of tuples containing the river name and the number of stations it has.

    Args:
        stations (list): List of stations (MonitoringStation)
        N (int): The number of desired rivers with the largest number of stations

    Returns:
        list: tuple of (river, number of stations on river) sorted in descending order
    """

    return list(
        reduce(
            lambda acc, val: acc + [val]
            if (len(acc) < N or val[1] == acc[-1][1])
            else acc,
            sorted(
                [(key, len(i)) for key, i in stations_by_river(stations).items()],
                key=lambda x: (-x[1], x[0]),
            ),
            [],
        )
    )
