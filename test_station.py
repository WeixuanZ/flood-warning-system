# Copyright (C) 2018 Garth N. Wells Modified by Ghifari Pradana & Weixuan Zhang
#
# SPDX-License-Identifier: MIT
"""Unit test for the station module"""

from floodsystem.station import *


class TestClass:
    def test_create_monitoring_station(self):
        # Create a station
        s_id = "test-s-id"
        m_id = "test-m-id"
        label = "some station"
        coord = (-2.0, 4.0)
        trange = (-2.3, 3.4445)
        river = "River X"
        town = "My Town"
        s = MonitoringStation(s_id, m_id, label, coord, trange, river, town)

        assert s.station_id == s_id
        assert s.measure_id == m_id
        assert s.name == label
        assert s.coord == coord
        assert s.typical_range == trange
        assert s.river == river
        assert s.town == town

    def test_typical_range_consistent(self):
        assert MonitoringStation("111", "111", "station1", (0., 1.), (1., 4.), "River 1",
                                 "Town 1").typical_range_consistent() == True
        assert MonitoringStation("111", "111", "station1", (0., 1.), None, "River 1",
                                 "Town 1").typical_range_consistent() == False
        assert MonitoringStation("111", "111", "station1", (0., 1.), (1, -4), "River 1",
                                 "Town 1").typical_range_consistent() == False
        assert MonitoringStation("111", "111", "station1", (0., 1.), (0.5, 0.2), "River 1",
                                 "Town 1").typical_range_consistent() == False

    def test_inconsistent_typical_range_stations(self):
        station1 = MonitoringStation(station_id="111",
                                     measure_id="111",
                                     label="Station A",
                                     coord=(0, 1),
                                     typical_range=(1., 4.),
                                     river="River 1",
                                     town="Town 1")
        station2 = MonitoringStation(station_id="222",
                                     measure_id="222",
                                     label="Station B",
                                     coord=(1, 1),
                                     typical_range=None,
                                     river="River 2",
                                     town="Town 2")
        station3 = MonitoringStation(station_id="333",
                                     measure_id="333",
                                     label="Station C",
                                     coord=(0, 3),
                                     typical_range=(1, -4),
                                     river="River 2",
                                     town="Town 3")
        station4 = MonitoringStation(station_id="444",
                                     measure_id="444",
                                     label="Station D",
                                     coord=(8, 3),
                                     typical_range=(0.5, 0.2),
                                     river="River 3",
                                     town="Town 4")
        assert inconsistent_typical_range_stations([station1]) == []
        assert inconsistent_typical_range_stations([station1, station2]) == [station2.name]
        assert inconsistent_typical_range_stations([station2, station3]) == [station2.name, station3.name]
        assert inconsistent_typical_range_stations([station4, station2, station3]) == [station2.name, station3.name,
                                                                                       station4.name]

    def test_relative_water_level(self):
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
                                     typical_range=(1., 0.),
                                     river='test_river_2',
                                     town='test_town_2')
        assert station1.relative_water_level() is None
        station1.latest_level = 0.
        assert station1.relative_water_level() == 0.
        station1.latest_level = 1.
        assert station1.relative_water_level() == 1.
        station1.latest_level = 0.5
        assert station1.relative_water_level() == 0.5
        station1.latest_level = 2.
        assert station1.relative_water_level() == 2.

        station2.latest_level = 0.5
        assert station2.relative_water_level() is None
