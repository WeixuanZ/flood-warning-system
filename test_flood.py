# Copyright (C) 2020 Weixuan Zhang
#
# SPDX-License-Identifier: MIT
"""Unit test for the flood module"""

from floodsystem.flood import *
from floodsystem.station import MonitoringStation

class TestClass:
    def test_stations_level_over_threshold(self):
        station1 = MonitoringStation(station_id='test_station_id_1',
                                     measure_id='test_measure_id_1',
                                     label='Test Station 1',
                                     coord=(0., 1.),
                                     typical_range=(0., 1.),
                                     river='test_river_1',
                                     town='test_town_1')
        station2 = MonitoringStation(station_id='test_station_id_2',
                                     measure_id='test_measure_id_2',
                                     label='Test Station 2',
                                     coord=(1., 1.),
                                     typical_range=(0., 1.),
                                     river='test_river_2',
                                     town='test_town_2')
        station3 = MonitoringStation(station_id='test_station_id_3',
                                     measure_id='test_measure_id_3',
                                     label='Test Station 3',
                                     coord=(1., 1.),
                                     typical_range=(0., 1.),
                                     river='test_river_3',
                                     town='test_town_3')

        station1.latest_level = 0.5
        station2.latest_level = 0.6
        station3.latest_level = 0.7
        stations = [station1, station2, station3]

        assert stations_level_over_threshold(stations, 0.5) == [(station3, 0.7), (station2, 0.6)]
