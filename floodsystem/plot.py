# Copyright (C) 2020 Ghifari Pradana
#
# SPDX-License-Identifier: MIT

from bokeh.plotting import figure, show, output_file

def plot_water_levels(station, dates, levels):

    output_file(station.name + ".html")
    p = figure(title= station.name, x_axis_label= "Time", y_axis_label= "Water level/m")
    p.line(dates,levels, line_width= 2)

    show(p)