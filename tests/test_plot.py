# Copyright (C) 2020 Ghifari Pradana
#
# SPDX-License-Identifier: MIT

from os import path

from matplotlib.dates import num2date
from bokeh.io import show

from floodsystem.plot import *
from floodsystem.station import MonitoringStation


class TestClass:
    def test_map(self):
        station1 = MonitoringStation(
            station_id="test_station_id_1",
            measure_id="test_measure_id_1",
            label="Test Station 1",
            coord=(0.0, 1.0),
            typical_range=(0.0, 1.0),
            river="test_river_1",
            town="test_town_1",
        )
        location_map = Map([station1])
        show(location_map.build())
        assert path.isfile("./map.html")

    def test_plot(self):
        station1 = MonitoringStation(
            station_id="test_station_id_1",
            measure_id="test_measure_id_1",
            label="Test Station 1",
            coord=(0.0, 1.0),
            typical_range=(0.0, 1.0),
            river="test_river_1",
            town="test_town_1",
        )
        show(plot_water_levels(station1, [0, 1, 2], [0.1, 0.2, 0.3]))
        assert path.isfile(station1.name + ".html")

    def test_plot_water_level_with_fit(self):
        station2 = MonitoringStation(
            station_id="test_station_id_2",
            measure_id="test_measure_id_2",
            label="Test Station 2",
            coord=(0.0, 1.0),
            typical_range=(0.0, 1.0),
            river="test_river_2",
            town="test_town_2",
        )
        dates = num2date([5, 4, 3, 2, 1])
        levels = [16, 9, 4, 1, 0]

        show(plot_water_level_with_fit(station2, dates, levels, 2))
        assert path.isfile(station2.name + ".html")
