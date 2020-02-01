# Copyright (C) 2020 Ghifari Pradana
#
# SPDX-License-Identifier: MIT

from floodsystem.flood import stations_highest_rel_level
from floodsystem.stationdata import build_station_list, update_water_levels

def run():

    stations = build_station_list()
    update_water_levels(stations)
    high_risk_stations = stations_highest_rel_level(stations,10)
    for station in high_risk_stations:
        print(station.name, station.relative_water_level())

if __name__ == "__main__":
    print("*** Task 2C: CUED Part IA Flood Warning System ***")
    run()