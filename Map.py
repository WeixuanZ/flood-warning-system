# Copyright (C) 2020 Weixuan Zhang
#
# SPDX-License-Identifier: MIT

from floodsystem.geo import Map
from floodsystem.stationdata import build_station_list


def run():
    stations = build_station_list()
    location_map = Map(stations)
    location_map.build()


if __name__ == "__main__":
    print("*** Extension: CUED Part IA Flood Warning System ***")
    run()
