# Copyright (C) 2020 Weixuan Zhang
#
# SPDX-License-Identifier: MIT
"""This module contains a collection of functions related to
geographical data.

"""

from math import sqrt, asin, sin, cos, radians

from .utils import sorted_by_key  # noqa


def haversine(a, b):
    """
    Function that calculates the haversine distances between two points in kilometers.
    Args:
        param1 (tuple): The coordinate of the first point as (latitude, longitude).
        param2 (tuple): The coordinate of the second point as (latitude, longitude).
    Returns:
        float: Haversine distance.
    """

    r = 6371
    a_lat, a_long = a[0], a[1]
    b_lat, b_long = b[0], b[1]

    return 2 * r * asin(sqrt(sin(radians((b_lat - a_lat) / 2)) ** 2 + cos(radians(a_lat)) * cos(radians(b_lat)) * sin(
        radians((b_long - a_long) / 2)) ** 2))


def stations_by_distance(stations, p):
    """
    Function that returns the sorted distances between the input stations and a specified point p.
    Args:
        param1 (list): List of stations (type MonitoringStation).
        param2 (tuple): Coordinate of the origin.
    Returns:
        list: List of (station, distance) sorted by distance.
    """

    distances = []
    for station in stations:
        distances.append((station.name, station.town, haversine(station.coord, p)))
    return sorted_by_key(distances, 2)


def stations_within_radius(stations, centre, r):
    """
    Function that returns a list of all stations (type MonitoringStation) within radius r of a geographic coordinate.
    Args:
        param1 (list): List of stations (type MonitoringStation).
        param2 (tuple): Coordinate of centre in (latitude, longitude).
        param3 (float): Radius in kilometers.
    Returns:
        list: List of stations (type MonitoringStation) within the distance.
    """

    stations_within = []
    for station in stations:
        if haversine(station.coord, centre) <= r:
            stations_within.append(station)
    return stations_within


def rivers_with_station(stations):
    """
    Function that, given a list of station objects, returns a container with the names of the rivers with a monitoring station.
    Args:
        param1 (list): List of stations (type MonitoringStation).
    Returns:
        set: Set of names of rivers with a monitoring station.
    """

    return {station.river for station in stations}


def stations_by_river(stations):
    """
    Function that returns a dictionary that maps river names (the ‘key’) to a list of station objects on a given river.
    Args:
        param1 (list): List of stations (type MonitoringStation).
    Returns:
        dict: Keys - river names.
    """

    stations_on_river = {}
    for station in stations:
        if station.river not in stations_on_river:
            stations_on_river[station.river] = [station]
        else:
            stations_on_river[station.river].append(station)
    return stations_on_river

