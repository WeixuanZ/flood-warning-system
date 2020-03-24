# Copyright (C) 2020 Weixuan Zhang
#
# SPDX-License-Identifier: MIT

from floodsystem.geo import stations_within_radius
from floodsystem.stationdata import build_station_list


def run():
    """
    Build a list of stations within 10 km of the Cambridge city centre. Print the names of the stations, listed in alphabetical order.
    """
    stations = build_station_list()
    sorted_stations = stations_within_radius(stations, (52.2053, 0.1218), 10)
    print(sorted([i.name for i in sorted_stations]))


if __name__ == "__main__":
    print("*** Task 1C: CUED Part IA Flood Warning System ***")
    run()
