# Copyright (C) 2020 Ghifari Pradana & Weixuan Zhang
#
# SPDX-License-Identifier: MIT

from datetime import timedelta
from os import environ

import numpy as np
from bokeh.io import output_file, show
from bokeh.layouts import gridplot
from bokeh.models import ColumnDataSource, GMapOptions, HoverTool, DatetimeTickFormatter, Span, BoxAnnotation
from bokeh.plotting import figure, gmap
from .analysis import polyfit
from .datafetcher import fetch_measure_levels
from matplotlib.dates import date2num


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
        return self.plot

    def __repr__(self):
        return "A map containing the following stations: {}".format([i.name for i in self.stations])


def plot_water_levels(station, dates, levels):
    """
    Function that makes a graph of the water level over time for a given station.
    Args: 
        param1 (MonitoringStation): The desired station to graph.
        param2 (list): The list of dates for the x-axis.
        param3 (list): The corresponding water level for each date, y-axis.
    Returns:
        Bokeh plot object.
    """
    output_file(station.name + ".html")
    p = figure(title=station.name, x_axis_label="Date", y_axis_label="Water level (m)")
    p.line(dates, levels, line_width=2)
    p.xaxis.formatter = DatetimeTickFormatter(
        hours=["%d %B %Y"],
        days=["%d %B %Y"],
        months=["%d %B %Y"],
        years=["%d %B %Y"],
    )
    p.xaxis.major_label_orientation = np.pi / 4
    return p


def plot_water_levels_multiple(stations, dt):
    """
    Function that displays a grid of graphs of the water level over time for a given list of stations.
    Args:
        param1 (list): List of the desired stations (type MonitoringStation) to graph
        param2 (int): Number of days.
    Returns:
        Bokeh plot object.
    """
    plots = []
    for station in stations:
        dates, levels = fetch_measure_levels(station.measure_id, dt=timedelta(days=dt))
        p = figure(title=station.name, x_axis_label="Date", y_axis_label="Water level (m)")
        p.line(dates, levels, line_width=2)
        low = Span(location=station.typical_range[0], dimension='width', line_color='gray', line_dash="4 4", line_width=2)
        p.add_layout(low)
        high = Span(location=station.typical_range[1], dimension='width', line_color='gray', line_dash="4 4", line_width=2)
        p.add_layout(high)
        low_box = BoxAnnotation(top=station.typical_range[0], fill_alpha=0.1, fill_color='red')
        mid_box = BoxAnnotation(bottom=station.typical_range[0], top=station.typical_range[1], fill_alpha=0.1, fill_color='green')
        high_box = BoxAnnotation(bottom=station.typical_range[1], fill_alpha=0.1, fill_color='red')
        p.add_layout(low_box)
        p.add_layout(mid_box)
        p.add_layout(high_box)
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
    return grid


def plot_prediction(date, data):
    """
    Function that plots the prediction made by predictor.
    Args:
        param1 (2-tuple): List of datetime objects of actual and demo data, list of datatime objects of future predicted data.
        param2 (3-tuple): Lists of water levels of actual data, demo data, predicted data.
    Returns:
        Bokeh plot object.
    """
    output_file("prediction.html")
    p = figure(plot_width=600, plot_height=600,
               title='Prediction',
               x_axis_label='Date', y_axis_label='Water level (m)')

    p.line(date[0], data[0], legend_label='Raw', line_width=2)
    p.line(date[0], data[1], line_color="orange", line_width=2, legend_label='Demo')
    p.line(date[1], data[2], line_color="green", line_width=2, legend_label='Prediction')
    p.xaxis.formatter = DatetimeTickFormatter(
        hours=["%d %B %Y"],
        days=["%d %B %Y"],
        months=["%d %B %Y"],
        years=["%d %B %Y"],
    )
    p.xaxis.major_label_orientation = np.pi / 4

    return p

def plot_water_level_with_fit(station, dates, levels, p):

    output_file(station.name + ".html")
    graph = figure(title=station.name, x_axis_label="Date", y_axis_label="Water level (m)")
    graph.line(dates, levels, line_width=2)
    poly, d0 = polyfit(dates, levels, p)
    graph.line(dates, [poly(date - d0) for date in date2num(dates)], line_width=2)
    low = Span(location=station.typical_range[0], dimension='width', line_color='gray', line_dash="4 4", line_width=2)
    graph.add_layout(low)
    high = Span(location=station.typical_range[1], dimension='width', line_color='gray', line_dash="4 4", line_width=2)
    graph.add_layout(high)
    low_box = BoxAnnotation(top=station.typical_range[0], fill_alpha=0.1, fill_color='gray')
    mid_box = BoxAnnotation(bottom=station.typical_range[0], top=station.typical_range[1], fill_alpha=0.1, fill_color='green')
    high_box = BoxAnnotation(bottom=station.typical_range[1], fill_alpha=0.1, fill_color='red')
    graph.add_layout(low_box)
    graph.add_layout(mid_box)
    graph.add_layout(high_box)
    graph.xaxis.formatter = DatetimeTickFormatter(
        hours=["%d %B %Y"],
        days=["%d %B %Y"],
        months=["%d %B %Y"],
        years=["%d %B %Y"],
    )
    graph.xaxis.major_label_orientation = np.pi / 4
    return graph