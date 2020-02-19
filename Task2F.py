# Copyright (C) 2020 Ghifari Pradana
#
# SPDX-License-Identifier: MIT

from datetime import timedelta

from bokeh.io import show

from floodsystem.datafetcher import fetch_measure_levels
from floodsystem.flood import stations_highest_rel_level
from floodsystem.plot import plot_water_level_with_fit
from floodsystem.stationdata import build_station_list, update_water_levels


def run():
    stations = build_station_list()
    update_water_levels(stations)
    high_risk_stations = stations_highest_rel_level(stations, 5)

    for station in high_risk_stations:
        dates, levels = fetch_measure_levels(station.measure_id, dt=timedelta(days=2))
        graph = plot_water_level_with_fit(station, dates, levels, 4)
        show(graph)


if __name__ == "__main__":
    print("*** Task 2F: CUED Part IA Flood Warning System ***")
    run()
