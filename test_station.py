# Copyright (C) 2018 Garth N. Wells Modified by Ghifari Pradana
#
# SPDX-License-Identifier: MIT
"""Unit test for the station module"""

from floodsystem.station import MonitoringStation, inconsistent_typical_range_stations


def test_create_monitoring_station():

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

def test_typical_range_consistent():
    assert MonitoringStation("111", "111", "station1", (0.,1.), (1,4), "River 1", "Town 1").typical_range == True
    assert MonitoringStation("111", "111", "station1", (0.,1.), None, "River 1", "Town 1") == False
    assert MonitoringStation("111", "111", "station1", (0.,1.), (1,-4), "River 1", "Town 1") == False
    assert MonitoringStation("111", "111", "station1", (0.,1.), (0.5,0.2), "River 1", "Town 1") == False

def test_inconsistent_typical_range_stations():
    station1 = MonitoringStation(station_id="111",
                                 measure_id="111",
                                 label="Station A",
                                 coord=(0,1),
                                 typical_range=(1.,4.),
                                 river="River 1",
                                 town="Town 1")
    station2 = MonitoringStation(station_id="222",
                                 measure_id="222",
                                 label="Station B",
                                 coord=(1,1),
                                 typical_range=None,
                                 river="River 2",
                                 town="Town 2")
    station3 = MonitoringStation(station_id="333",
                                 measure_id="333",
                                 label="Station C",
                                 coord=(0,3),
                                 typical_range=(1,-4),
                                 river="River 2",
                                 town="Town 3")
    station4 = MonitoringStation(station_id="444",
                                 measure_id="444",
                                 label="Station D",
                                 coord=(8,3),
                                 typical_range=(0.5,0.2),
                                 river="River 3",
                                 town="Town 4")
    assert inconsistent_typical_range_stations([station1]) == []
    assert inconsistent_typical_range_stations([station1, station2]) == (station2.name)
    assert inconsistent_typical_range_stations([station2, station3]) == (station2.name, station3.name)
    assert inconsistent_typical_range_stations([station4, station2, station3]) == (station2.name, station3.name, station4.name)




