# Copyright (C) 2020 Weixuan Zhang
#
# SPDX-License-Identifier: MIT

from datetime import timedelta
from os import environ
import numpy as np

from bokeh.layouts import layout, column, row
from bokeh.models import ColumnDataSource, Div, TextInput, Tabs, Panel, TapTool, HoverTool, GMapOptions, ColorBar, DataTable, TableColumn
from bokeh.plotting import curdoc, gmap
from bokeh.transform import log_cmap
from bokeh.palettes import Spectral10, Turbo256, linear_palette
from fuzzywuzzy import process
from matplotlib.dates import date2num
from sklearn.cluster import DBSCAN

from floodsystem.datafetcher import fetch_measure_levels
from floodsystem.flood import stations_highest_rel_level, stations_level_over_threshold
from floodsystem.plot import map_palette, plot_water_levels_dynamic, plot_water_levels_multiple, plot_prediction
from floodsystem.predictor import predict
from floodsystem.stationdata import build_station_list, update_water_levels
from floodsystem.analysis import polyfit
from floodsystem.geo import rivers_by_station_number, rivers_with_station

# map_select = True

## Fetching and preparing data

stations = build_station_list()
update_water_levels(stations)
highrisk_stations = stations_highest_rel_level(stations, 6)


def convert_to_datasource(stations):
    return ColumnDataSource(data=dict(lat=[i.coord[0] for i in stations],
                                    lng=[i.coord[1] for i in stations],
                                    name=[i.name for i in stations],
                                    measure_id=[i.measure_id for i in stations],
                                    river=[i.river for i in stations],
                                    town=[i.town for i in stations],
                                    typical_low=[i.typical_range[0] if i.typical_range is not None else 'nan' for i in
                                                 stations],
                                    typical_high=[i.typical_range[1] if i.typical_range is not None else 'nan' for i in
                                                  stations],
                                    latest_level=[i.latest_level if i.latest_level is not None else 'nan' for i in
                                                  stations],
                                    relative_level=[
                                        i.relative_water_level() if i.relative_water_level() is not None else 'nan' for
                                        i in stations],
                                    color=[map_palette(i) for i in stations]))


source = convert_to_datasource(stations)
name_to_indx = dict()  # building a hash table for quick search up of indices
for indx, i in enumerate(source.data['name']):
    name_to_indx[i] = indx

## Map

origin = (52.2070, 0.1131)
options = GMapOptions(lat=origin[0], lng=origin[1], map_type="roadmap", zoom=11)
tools = "crosshair,pan,wheel_zoom,reset,save"
location_map = gmap(environ.get('API_KEY'), options, title="Station locations", tools=tools, active_scroll="wheel_zoom")
r = location_map.circle(x="lng", y="lat", size=15, fill_color='color', fill_alpha=0.8, source=source)
hover_tool = HoverTool(tooltips=[
    ("Station Name", "@name"),
    ("River Name", "@river"),
    ("Town", "@town"),
    ("Latitude,Longitude", "(@lat, @lng)"),
    ("Typical Range (m)", "@typical_low - @typical_high"),
    ("Latest Level (m)", "@latest_level")
])
tap_tool = TapTool()
location_map.add_tools(hover_tool, tap_tool)
location_map.plot_width = 700
location_map.plot_height = 500
location_map.sizing_mode = 'scale_width'

## Selected station plot

select_input = TextInput(value="Cambridge Jesus Lock", title="Name of station:")
select_text = Div(
    text="<p>Select a station either by clicking on the map, or using the search field below, to display its historical level.</p>")

# initialise data for plot of selected station
init_indx = list(source.data['name']).index(select_input.value)
init_dates, init_levels = fetch_measure_levels(source.data['measure_id'][init_indx], dt=timedelta(days=30))
selected_plot_source = ColumnDataSource(
    data=dict(dates=init_dates, levels=init_levels))  # data for the selected station plot
current_selection = [select_input.value, init_indx]  # cache for current selection, avoid repeat update


def update_text_select(attr, old, new):
    """
    Function that updates the selected plot according to the name text provided.
    """
    global current_selection
    print('Current Selection: ' + str(current_selection))
    input_text = select_input.value
    if input_text == current_selection[0]:  # without fuzzy match, the new station is equal to the current station
        return
    if input_text != '':
        selected_station_name = process.extractOne(input_text, source.data['name'])[0]
        if selected_station_name == current_selection[
            0]:  # after fuzzy match, the new station is equal to the current station
            select_input.value = selected_station_name
            return
        print('Input: ' + input_text + ', Matched: ' + selected_station_name)
        indx = name_to_indx[selected_station_name]
        current_selection = [selected_station_name, indx]  # update the current selection cache
        r.data_source.selected.indices = [indx]  # update the selection on map
        select_input.value = selected_station_name  # update the displayed text in the text input box
        # TODO recenter map
        dates, levels = fetch_measure_levels(source.data['measure_id'][indx],
                                             dt=timedelta(days=30))  # get the data for the newly selected station
        selected_plot_source.data.update(dict(dates=dates, levels=levels))
    else:
        current_selection = [None, None]  # update the current selection
        r.data_source.selected.indices = []
        selected_plot_source.data.update(dict(dates=[], levels=[]))


select_input.on_change('value', update_text_select)


def update_map_select(attr, old, new):
    """
    Function that updates the selected plot according to selection on map.
     """
    global current_selection
    print('Current Selection: ' + str(current_selection))
    # if map_select is True and indx != []:
    if new:  # if the selection is not empty
        indx = new[0]
        if indx == current_selection[1]:
            return
        selected_station_name = source.data['name'][indx]
        print('Selected on map: ' + selected_station_name)
        current_selection = [selected_station_name, indx]  # update the current selection cache
        select_input.value = selected_station_name  # update the displayed text in the text input box
        dates, levels = fetch_measure_levels(source.data['measure_id'][indx], dt=timedelta(days=30))
        selected_plot_source.data.update(dict(dates=dates, levels=levels))


r.data_source.selected.on_change('indices', update_map_select)

selected_plot = plot_water_levels_dynamic(selected_plot_source)
selected_plot.plot_height = 350
selected_plot.plot_width = 600
selected_plot.sizing_mode = 'scale_width'

## High risk stations

highrisk_title = Div(
    text="""<h3>High Risk Stations</h3><p>The six stations with the highest relative water levels are shown below.</p> """)
highrisk_plots = plot_water_levels_multiple(highrisk_stations, dt=10, width=250, height=250)
highrisk_plots.sizing_mode = 'scale_width'

## Prediction

predict_text = Div(
    text="""<p>Choose one of the high risk stations to see the prediction by a recurrent neural network and least-squares polynomial fit.</p>""")

predict_date = []
predict_level = []
predict_plots = []
for station in highrisk_stations:
    try:
        date, level = predict(station.name, dataset_size=1000, lookback=200, iteration=100, display=300,
                              use_pretrained=True, batch_size=256, epoch=20)
    except:
        date, level = [], []
    predict_plot = plot_prediction(date, level)
    poly, d0 = polyfit(date[0], level[0], 4)
    predict_plot.line(date[0]+date[1], [poly(date - d0) for date in date2num(date[0]+date[1])], line_width=2, line_color='gray', legend_label='Polynomial Fit', line_dash='dashed')
    predict_plot.plot_width = 400
    predict_plot.plot_height = 400
    predict_plot.sizing_mode = 'scale_width'
    predict_plots.append(Panel(child=predict_plot, title=station.name))

predict_tabs = Tabs(tabs=predict_plots)


## Warning

warning_text = Div(text="""<h3>Flooding Warnings</h3><p>All the stations with relative water level above 1.2 are shown in the map below. DBSCAN clustering algorithm is used.</p> """)

risky_stations_with_level = stations_level_over_threshold(stations, 1.2)
risky_stations = [i[0] for i in risky_stations_with_level]
risky_source = convert_to_datasource(risky_stations)

mapper = log_cmap(field_name='relative_level', palette=Spectral10, low=1.0, high=risky_stations[0].relative_water_level())
origin2 = (52.561928, -1.464854)
options2 = GMapOptions(lat=origin2[0], lng=origin2[1], map_type="roadmap", zoom=5)
location_map2 = gmap(environ.get('API_KEY'), options2, title="Stations above typical range", tools=tools, active_scroll="wheel_zoom")
r2 = location_map2.circle(x="lng", y="lat", size=15, color=mapper, fill_alpha=0.5, source=risky_source)
hover_tool = HoverTool(tooltips=[
    ("Station Name", "@name"),
    ("River Name", "@river"),
    ("Town", "@town"),
    ("Latitude,Longitude", "(@lat, @lng)"),
    ("Typical Range (m)", "@typical_low - @typical_high"),
    ("Latest Level (m)", "@latest_level")
])
location_map2.add_tools(hover_tool)
color_bar = ColorBar(color_mapper=mapper['transform'], width=8,  location=(0,0))
location_map2.add_layout(color_bar, 'right')
location_map2.plot_width = 700
location_map2.plot_height = 500
location_map2.sizing_mode = 'scale_width'


# Clustering

coord_to_station = dict()  # to find the station after knowing which cluster its coordinate belongs to
for i in risky_stations:
    coord_to_station[i.coord] = i

X = np.array([i.coord for i in risky_stations])
db = DBSCAN(eps=0.1, min_samples=5, metric='haversine', n_jobs=-1).fit(X)

labels = db.labels_
unique_labels = set(labels)
num_clusters = len(unique_labels) - (1 if -1 in labels else 0)
print('Number of clusters:'+str(num_clusters))

cluster_pallet = linear_palette(Turbo256, len(unique_labels))
label_to_stations = dict()  # to find the list of stations knowing the cluster label
for i in unique_labels:
    if i != -1:
        label_to_stations[i] = []

location_map3 = gmap(environ.get('API_KEY'), options2, title="Clusters", tools=tools, active_scroll="wheel_zoom")

for i in unique_labels:
    if i != -1:  # not noise
        class_member_mask = (labels == i)
        coord = X[class_member_mask]
        for xy in coord:
            location_map3.circle(x=xy[1], y=xy[0], size=15, color=cluster_pallet[i], fill_alpha=0.8)
            label_to_stations[i].append(coord_to_station[(xy[0], xy[1])])  # find the station from its coordinates and append it to the dictionary

location_map3.plot_width = 700
location_map3.plot_height = 500
location_map3.sizing_mode = 'scale_width'

# Risky rivers
warning_text2 = Div(text="""<p><b>{}</b> rivers with risky stations, the top 5 is tabulated below.</p>""".format(len(rivers_with_station(risky_stations))), width=600)
warning_text2.sizing_mode = 'scale_width'

risky_rivers = rivers_by_station_number(risky_stations, 5)
risky_rivers_source = ColumnDataSource(data=dict(name=[i[0] for i in risky_rivers], num=[i[1] for i in risky_rivers]))
risky_river_table_columns = [
        TableColumn(field="name", title="River Name"),
        TableColumn(field="num", title="Number of Risky Stations"),
    ]
risky_river_table = DataTable(source=risky_rivers_source, columns=risky_river_table_columns, width=500, height=200)
risky_river_table.sizing_mode = 'scale_width'

# Risky towns
risky_towns = []
key_station_in_cluster = []
mean_levels = []
for label, s in label_to_stations.items():
    cluster_levels = np.array([i.relative_water_level() for i in s])
    mean_levels.append(cluster_levels.mean())
    key_station_in_cluster.append(s[np.argmax(cluster_levels)])
    for i in s:
        risky_towns.append(i.town)

risky_towns = set(risky_towns)  # to find the total number of risky towns
# sort the towns by the mean relative water level of the cluster it is in
key_station_in_cluster = sorted(key_station_in_cluster, key=lambda x: mean_levels[key_station_in_cluster.index(x)], reverse=True)
mean_levels = sorted(mean_levels, reverse=True)

risky_towns_source = ColumnDataSource(data=dict(key_stations = [i.name for i in key_station_in_cluster], key_towns=[i.town for i in key_station_in_cluster], levels=[round(i.relative_water_level(),2) for i in key_station_in_cluster], mean=[round(i,2) for i in mean_levels]))
warning_text3 = Div(text="""<p><b>{}</b> clusters found, the towns within these clusters (<b>{}</b> in total) have a risk of flooding. The table below lists the towns with the highest relative water level within each cluster in the order of decreasing risk (by calculating the mean relative water level of each cluster).</p>""".format(num_clusters, len(risky_towns)), width=600)
risky_town_table_columns = [
        TableColumn(field="key_towns", title="Towns with Highest Risk"),
        TableColumn(field="key_stations", title="Station Name"),
        TableColumn(field="levels", title="Relative Water Level"),
        TableColumn(field="mean", title="Mean Cluster Relative Water Level"),
    ]
risky_town_table = DataTable(source=risky_towns_source, columns=risky_town_table_columns, width=500, height=200)
risky_town_table.sizing_mode = 'scale_width'



## Layout

map_column = column(location_map, width=700, height=500)

# radio_button_group = RadioButtonGroup(labels=["Click on Map", "Search"], active=0)
# select_column = column(select_text, radio_button_group, selected_plot, width=600, height=500)
select_column = column(select_text, select_input, selected_plot, width=600, height=500)
select_column.sizing_mode = "fixed"

# def update_toggle():
#     global map_select
#     if radio_button_group.active == 1:
#         map_select = False
#         location_map.tools.pop()
#         r.data_source.selected.indices = []
#         select_column.children = [select_text, radio_button_group, select_input, selected_plot]
#     else:
#         map_select = True
#         location_map.add_tools(tap_tool)
#         r.data_source.selected.indices = []
#         select_column.children = [select_text, radio_button_group, selected_plot]
#
#
# radio_button_group.on_change('active', lambda attr, old, new: update_toggle())


highrisk_column = column(highrisk_title, highrisk_plots, width=800, height=650)
highrisk_column.sizing_mode = "fixed"

predict_column = column(predict_text, predict_tabs, width=500, height=650)
predict_column.sizing_mode = "fixed"

warning_column = column(warning_text, row(location_map2, location_map3), width=1300, height=550)
predict_column.sizing_mode = "fixed"

river_column = column(warning_text2, width=650, height=70)
predict_column.sizing_mode = "fixed"
town_column = column(warning_text3, width=650, height=70)
predict_column.sizing_mode = "fixed"

notice = Div(text="""<footer>&copy; Copyright 2020 Weixuan Zhang, Ghifari Pradana. CUED Part 1A Lent computing project.</footer>""", width=600)

l = layout([
    [location_map, select_column],
    [highrisk_column, predict_column],
    [warning_column],
    [river_column, town_column],
    [row(risky_river_table, risky_town_table, width=1300, height=200)],
    [notice]
])

curdoc().add_root(l)
curdoc().title = "Flood Warning System"
