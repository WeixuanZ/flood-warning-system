# Copyright (C) 2020 Weixuan Zhang & Ghifari Pradana
#
# SPDX-License-Identifier: MIT
"""Unit test for the geo module"""

from floodsystem.geo import *
from floodsystem.station import MonitoringStation


class TestClass:
    def test_haversine(self):
        assert haversine((0., 0.), (0., 0.)) == 0.0
        assert round(haversine((0., 0.), (1., 1.)), 2) == 157.25
        assert round(haversine((1., 1.), (0., 0.)), 2) == 157.25
        assert round(haversine((0., 0.), (1., 0.)), 2) == 111.19
        assert round(haversine((0., 0.), (0., 1.)), 2) == 111.19

    def test_stations_by_distance(self):
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
        stations = [station1, station2]
        sorted_stations = stations_by_distance(stations, (0., 0.))
        assert sorted_stations[0][0:2] == ('Test Station 1', 'test_town_1')
        assert sorted_stations[1][0:2] == ('Test Station 2', 'test_town_2')

    def test_stations_within_radius(self):
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
                                     coord=(10., 10.),
                                     typical_range=(0., 1.),
                                     river='test_river_3',
                                     town='test_town_3')
        stations = [station1, station2, station3]
        stations_within = sorted([i.name for i in stations_within_radius(stations, (0., 0.), 200)])
        assert len(stations_within) == 2
        assert stations_within[0] == "Test Station 1"
        assert stations_within[1] == "Test Station 2"

    def test_rivers_and_stations(self):
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
                                     coord=(10., 10.),
                                     typical_range=(0., 1.),
                                     river='test_river_2',
                                     town='test_town_3')
        stations = [station1, station2, station3]
        rivers = rivers_with_station(stations)
        assert len(rivers) == 2
        assert 'test_river_1' in rivers
        assert 'test_river_2' in rivers

        stations_on_river = stations_by_river(stations)
        assert sorted(stations_on_river['test_river_2'], key=lambda x: x.name) == [station2, station3]
        assert stations_on_river['test_river_1'] == [station1]
    
    def test_rivers_by_station_number(self):
        station1 = MonitoringStation(station_id="111",
                                     measure_id="111",
                                     label="Station 1",
                                     coord=(0,1),
                                     typical_range=(0.1,0.4),
                                     river="River 1",
                                     town="Town 1")
        station2 = MonitoringStation(station_id="222",
                                     measure_id="222",
                                     label="Station 2",
                                     coord=(1,1),
                                     typical_range=(0.3,0.8),
                                     river="River 2",
                                     town="Town 2")
        station3 = MonitoringStation(station_id="333",
                                     measure_id="333",
                                     label="Station 3",
                                     coord=(0,3),
                                     typical_range=(0.43,0.88),
                                     river="River 2",
                                     town="Town 3")
        station4 = MonitoringStation(station_id="444",
                                     measure_id="444",
                                     label="Station 4",
                                     coord=(8,3),
                                     typical_range=(0.1,0.9),
                                     river="River 3",
                                     town="Town 4")
        assert rivers_by_station_number([station1], 1) == (("River 1",1))
        assert rivers_by_station_number([station1, station2, station3],1) == (("River 2",2))
        assert rivers_by_station_number([station1, station2, station3],2) == (("River 2",2),("River 1", 1))
        assert rivers_by_station_number([station1, station2, station3,station4],3) == (("River 2",2),("River 1", 1), ("River 3",1))
        assert rivers_by_station_number([station1, station2, station3,station4],4) == (("River 2",2),("River 1", 1), ("River 3",1))
