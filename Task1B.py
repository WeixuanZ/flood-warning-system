# Copyright (C) 2020 Weixuan Zhang
#
# SPDX-License-Identifier: MIT

from floodsystem.geo import stations_by_distance
from floodsystem.stationdata import build_station_list


def run():
    """
    Prints a list of tuples (station name, town, distance) for the 10 closest and the 10 furthest stations from the Cambridge city centre, (52.2053, 0.1218).
    """
    stations = build_station_list()
    sorted_stations = stations_by_distance(stations, (52.2053, 0.1218))
    print("The closest 10 stations are: {}".format(sorted_stations[:10]))
    print("The furthest 10 stations are: {}".format(sorted_stations[-10:]))


if __name__ == "__main__":
    print("*** Task 1B: CUED Part IA Flood Warning System ***")
    run()
