# Copyright (C) 2020 Weixuan Zhang
#
# SPDX-License-Identifier: MIT
"""Unit test for the geo module"""

from floodsystem.geo import *
from floodsystem.station import MonitoringStation


class TestClass:
    def test_haversine(self):
        assert haversine((0.,0.), (0.,0.)) == 0.0
        assert round(haversine((0.,0.),(1.,1.)),2) == 157.25
        assert round(haversine((1., 1.), (0.,0.)), 2) == 157.25
        assert round(haversine((0., 0.), (1.,0.)), 2) == 111.19
        assert round(haversine((0., 0.), (0.,1.)), 2) == 111.19

    def test_stations_by_distance(self):
        station1 = MonitoringStation(station_id='test_station_id_1',
                measure_id='test_measure_id_1',
                label='Test Station 1',
                coord=(0.,1.),
                typical_range=(0.,1.),
                river='test_river_1',
                town='test_town_1')
        station2 = MonitoringStation(station_id='test_station_id_2',
                                     measure_id='test_measure_id_2',
                                     label='Test Station 2',
                                     coord=(1., 1.),
                                     typical_range=(0., 1.),
                                     river='test_river_2',
                                     town='test_town_2')
        stations = [station1, station2]
        sorted_stations = stations_by_distance(stations, (0.,0.))
        assert sorted_stations[0][0:2] == ('Test Station 1', 'test_town_1')
        assert sorted_stations[1][0:2] == ('Test Station 2', 'test_town_2')



