# Copyright (C) 2020 Ghifari Pradana
#
# SPDX-License-Identifier: MIT

from floodsystem.station import inconsistent_typical_range_stations
from floodsystem.stationdata import build_station_list


def run():
    stations = build_station_list()
    print(inconsistent_typical_range_stations(stations))


if __name__ == "__main__":
    run()
