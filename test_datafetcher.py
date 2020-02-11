# Copyright (C) 2018 Garth N. Wells
#
# SPDX-License-Identifier: MIT
"""Unit test for the stationdata module"""

import datetime

from floodsystem.datafetcher import fetch_measure_levels
from floodsystem.stationdata import build_station_list


def test_build_station_list():

    # Build list of stations
    stations = build_station_list()

    # Find station 'Cam'
    for station in stations:
        if station.name == 'Cam':
            station_cam = station
            break

    # Assert that station is found
    assert station_cam

    # Fetch data over past 2 days
    dt = 2
    dates2, levels2 = fetch_measure_levels(
        station_cam.measure_id, dt=datetime.timedelta(days=dt))
    assert len(dates2) == len(levels2)

    # Fetch data over past 10 days
    dt = 10
    dates10, levels10 = fetch_measure_levels(
        station_cam.measure_id, dt=datetime.timedelta(days=dt))
    assert len(dates10) == len(levels10)
    assert len(dates10) > len(levels2)
def test_(self):
        station1 = MonitoringStation(station_id='test_station_id_1',
                                     measure_id='test_measure_id_1',
                                     label='Test Station 1',
                                     coord=(0., 1.),
                                     typical_range=(0., 1.),
                                     river='test_river_1',
                                     town='test_town_1')
        location_map = Map([station1])
        location_map.build()
        assert path.isfile('./map.html')
