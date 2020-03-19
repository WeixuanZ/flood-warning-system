# Copyright (C) 2020 Weixuan Zhang
#
# SPDX-License-Identifier: MIT

from bokeh.io import show

from floodsystem.plot import Map
from floodsystem.stationdata import build_station_list


def run():
    stations = build_station_list()
    location_map = Map(stations).build()
    show(location_map)


if __name__ == "__main__":
    print("*** Extension: CUED Part IA Flood Warning System ***")
    run()
