# Copyright (C) 2018 Garth N. Wells Modified by Weixuan Zhang & Ghifari Pradana
#
# SPDX-License-Identifier: MIT
"""This module provides a model for a monitoring station, and tools
for manipulating/modifying station data

"""


class MonitoringStation:
    """This class represents a river level monitoring station"""

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
        return self._station_id
    @property
    def measure_id(self):
        return self._measure_id
    @property
    def name(self):
        return self._name
    @property
    def coord(self):
        return self._coord
    @property
    def typical_range(self):
        return self._typical_range
    @property
    def river(self):
        return self._river
    @property
    def town(self):
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
        Args:
        param 1 (MonitoringStation): The instance of the class itself.
        Returns:
        Boolean: Returns whether or not the data is consistent
        """

        if type(self._typical_range) == tuple and self._typical_range != (0.,0.):
            if self._typical_range[0] < self.typical_range[1]:
                return True
        print(self.typical_range + "so it failed")
        return False

def inconsistent_typical_range_stations(stations):
    """
    This function checks takes in the list of stations and checks to make sure the typical
    range for each are consistent.
    Args:
        param1 (list): List of stations (type MonitoringStation).
    Returns:
        list: List (type String) of all the stations with inconsistent typical ranges in alphabetical order
    """
    inconsistent_stations = []
    for station in stations:
        if station.typical_range_consistent() == False:
            inconsistent_stations.append(station.name)
    return sorted(inconsistent_stations)