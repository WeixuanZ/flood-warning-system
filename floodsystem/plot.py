# Copyright (C) 2020 Ghifari Pradana & Weixuan Zhang
#
# SPDX-License-Identifier: MIT

from datetime import timedelta
from os import environ

import numpy as np
from bokeh.io import output_file, show
from bokeh.layouts import gridplot
from bokeh.models import ColumnDataSource, GMapOptions, HoverTool, DatetimeTickFormatter
from bokeh.plotting import figure, gmap

from .datafetcher import fetch_measure_levels


class Map:
    """This class represents a map of stations."""

    def __init__(self, stations, origin=(52.2070, 0.1131)):
        self.stations = stations
        self.locations = [i.coord for i in self.stations]
        self.options = GMapOptions(lat=origin[0], lng=origin[1], map_type="roadmap", zoom=11)
        self.tools = "crosshair,pan,wheel_zoom,box_select,lasso_select,reset,save"
        self.plot = gmap(environ.get('API_KEY'), self.options, title="Station locations", tools=self.tools,
                         active_scroll="wheel_zoom")

    def build(self):
        output_file("map.html")
        source = ColumnDataSource(data=dict(lat=[i[0] for i in self.locations], lng=[i[1] for i in self.locations],
                                            name=[i.name for i in self.stations],
                                            river=[i.river for i in self.stations],
                                            town=[i.town for i in self.stations]))
        self.plot.circle(x="lng", y="lat", size=15, fill_color="blue", fill_alpha=0.8, source=source)
        hover_tool = HoverTool(tooltips=[
            ("Station Name", "@name"),
            ("River Name", "@river"),
            ("Town", "@town"),
            ("(Latitude,Longitude)", "(@lat, @lng)")
        ])
        self.plot.add_tools(hover_tool)
        show(self.plot)

    def __repr__(self):
        return "A map containing the following stations: {}".format([i.name for i in self.stations])


def plot_water_levels(station, dates, levels):
    """
    Function that makes a graph of the water level over time for a given station.
    Args: 
        param1 (MonitoringStation): The desired station to graph
        param2 (list): The list of dates for the x-axis
        param3 (list): The corresponding water level for each date, y-axis
    """
    output_file(station.name + ".html")
    p = figure(title=station.name, x_axis_label="Time", y_axis_label="Water level (m)")
    p.line(dates, levels, line_width=2)
    p.xaxis.formatter = DatetimeTickFormatter(
        hours=["%d %B %Y"],
        days=["%d %B %Y"],
        months=["%d %B %Y"],
        years=["%d %B %Y"],
    )
    p.xaxis.major_label_orientation = np.pi / 4
    show(p)


def plot_water_levels_multiple(stations, dt):
    """
    Function that displays a grid of graphs of the water level over time for a given list of stations.
    Args:
        param1 (list): List of the desired stations (type MonitoringStation) to graph
        param2 (int): Number of days.
    """
    plots = []
    for station in stations:
        dates, levels = fetch_measure_levels(station.measure_id, dt=timedelta(days=dt))
        p = figure(title=station.name, x_axis_label="Time", y_axis_label="Water level (m)")
        p.line(dates, levels, line_width=2)
        p.xaxis.formatter = DatetimeTickFormatter(
            hours=["%d %B %Y"],
            days=["%d %B %Y"],
            months=["%d %B %Y"],
            years=["%d %B %Y"],
        )
        p.xaxis.major_label_orientation = np.pi / 4
        plots.append(p)

    output_file("grid.html")
    grid = gridplot(plots, ncols=3, plot_width=300, plot_height=250)
    show(grid)
