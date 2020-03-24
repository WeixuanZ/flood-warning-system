# Copyright (C) 2020 Weixuan Zhang
#
# SPDX-License-Identifier: MIT

from floodsystem.geo import rivers_with_station, stations_by_river
from floodsystem.stationdata import build_station_list


def run():
    """
    * Print how many rivers have at least one monitoring station
    * Prints the first 10 of these rivers in alphabetical order
    * Print the names of the stations located on the following rivers in alphabetical order:
        - 'River Aire'
        - 'River Cam'
        - 'River Thames'
    """
    stations = build_station_list()
    rivers = rivers_with_station(stations)
    print(len(rivers))
    print(sorted(rivers)[:10])

    print()

    stations_on_river = stations_by_river(stations)
    for river in ['River Aire', 'River Cam', 'River Thames']:
        print(river + ':')
        print(sorted([i.name for i in stations_on_river[river]]))


if __name__ == "__main__":
    print("*** Task 1D: CUED Part IA Flood Warning System ***")
    run()
