# Copyright (C) 2020 Ghifari Pradana
#
# SPDX-License-Identifier: MIT

from floodsystem.geo import stations_by_river, rivers_by_station_number
from floodsystem.stationdata import build_station_list
from floodsystem.utils import sorted_by_key  # noqa

def run():
    stations = build_station_list()
    print(rivers_by_station_number(stations,11))

if __name__ == "__main__":
    print("*** Task 1E: CUED Part IA Flood Warning System ***")
    run() 

