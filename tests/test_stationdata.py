# Copyright (C) 2018 Garth N. Wells
#
# SPDX-License-Identifier: MIT
"""Unit test for the stationdata module"""

from floodsystem.stationdata import build_station_list, update_water_levels


def test_build_station_list():
    """Test building list of stations"""
    station_list = build_station_list()
    assert len(station_list) > 0


def test_update_level():
    """Test update to latest water level"""

    # Build list of stations
    stations = build_station_list()
    for station in stations:
        assert station.latest_level is None

    # Update latest level data for all stations
    update_water_levels(stations)
    counter = 0
    for station in stations:
        if station.latest_level is not None:
            counter += 1

    assert counter > 0
