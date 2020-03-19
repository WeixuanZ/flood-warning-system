# Copyright (C) 2018 Garth N. Wells Modified by Weixuan Zhang & Ghifari Pradana
#
# SPDX-License-Identifier: MIT
"""This module provides a model for a monitoring station, and tools
for manipulating/modifying station data

"""


class MonitoringStation:
    """This class represents a river level monitoring station
    
    Attributes:
        latest_level (float): The latest water level of the station
    """

    def __init__(self, station_id, measure_id, label, coord, typical_range,
                 river, town):
        self._station_id = station_id
        self._measure_id = measure_id

        # Handle case of erroneous data where data system returns
        # '[label, label]' rather than 'label'
        self._name = label
        if isinstance(label, list):
            self._name = label[0]

        self._coord = coord
        self._typical_range = typical_range
        self._river = river
        self._town = town

        self.latest_level = None

    @property
    def station_id(self):
        """str: station_id"""
        return self._station_id

    @property
    def measure_id(self):
        """str: measure_id"""
        return self._measure_id

    @property
    def name(self):
        """str: Station name"""
        return self._name

    @property
    def coord(self):
        """tuple: Coorinates of the station in (latitude, longitude)"""
        return self._coord

    @property
    def typical_range(self):
        """tuple: Typical water level range of the station (typical_low, typical_high)"""
        return self._typical_range

    @property
    def river(self):
        """str: River name"""
        return self._river

    @property
    def town(self):
        """str: Town name"""
        return self._town

    def __repr__(self):
        d = "Station name:     {}\n".format(self.name)
        d += "   id:            {}\n".format(self.station_id)
        d += "   measure id:    {}\n".format(self.measure_id)
        d += "   coordinate:    {}\n".format(self.coord)
        d += "   town:          {}\n".format(self.town)
        d += "   river:         {}\n".format(self.river)
        d += "   typical range: {}".format(self.typical_range)
        return d

    def typical_range_consistent(self):
        """
        This method checks whether the data it receives about the typical ranges are consistent(That data is available 
        and the low range is lower than the high range).
        
        Returns:
            Boolean: Returns whether or not the data is consistent
        """

        return type(self._typical_range) is tuple and self._typical_range != (0., 0.) and self._typical_range[0] < \
            self.typical_range[1]

    def relative_water_level(self):
        """
        This method returns the latest water level as a fraction of the typical range.
        
        Returns:
            float: 0.0 (corresponds to a level at the typical low) to 1.0 (corresponds to a level at the typical high)
        """

        return (self.latest_level - self.typical_range[0]) / (self.typical_range[1] - self.typical_range[
            0]) if self.latest_level is not None and self.typical_range_consistent() is True else None


def inconsistent_typical_range_stations(stations):
    """
    This function checks takes in the list of stations and checks to make sure the typical
    range for each are consistent.
    
    Args:
        stations (list): List of stations (type MonitoringStation).
    
    Returns:
        list: List (type String) of all the stations with inconsistent typical ranges in alphabetical order
    """

    return sorted([i.name for i in stations if i.typical_range_consistent() is False])
