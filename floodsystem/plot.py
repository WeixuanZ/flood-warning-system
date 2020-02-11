# Copyright (C) 2020 Ghifari Pradana
#
# SPDX-License-Identifier: MIT

from bokeh.plotting import figure, show, output_file

def plot_water_levels(station, dates, levels):
    """
    Function that makes a graph of the water level over time for a given station.
    Args: 
        param1 (MonitoringStation): The desired station to graph
        param2 (list): The list of dates for the x-axis
        param3 (list): The corresponding water level for each date, y-axis
    """
    output_file(station.name + ".html")
    p = figure(title= station.name, x_axis_label= "Time", y_axis_label= "Water level/m")
    p.line(dates,levels, line_width= 2)

    show(p)