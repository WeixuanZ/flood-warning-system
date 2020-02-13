import numpy as np

from bokeh.io import output_file, show
from bokeh.layouts import gridplot, layout, column
from bokeh.models import ColumnDataSource, Select, Div, TextInput, Tabs, Panel
from bokeh.plotting import curdoc

from floodsystem.plot import *
from floodsystem.flood import stations_highest_rel_level
from floodsystem.stationdata import build_station_list, update_water_levels
from floodsystem.datafetcher import fetch_measure_levels
from floodsystem.predictor import predict


# Fetching data

stations = build_station_list()
update_water_levels(stations)
highrisk_stations = stations_highest_rel_level(stations, 6)


# Map

location_map = Map(stations).build()
location_map.plot_width = 700
location_map.plot_height = 500
location_map.sizing_mode = 'scale_width'


# High risk stations

highrisk_title = Div(text="""<h3>High Risk Stations</h3><p>The six stations with the highest relative water levels are shown below.</p> """)
highrisk_plots = plot_water_levels_multiple(highrisk_stations, dt=10, width=250, height=250)
highrisk_plots.sizing_mode = 'scale_width'


# Selected station plot

select_input = TextInput(value="Cam", title="Name of station to search for:")
select_text = Div(text="<p>Select a station either by clicking on the map, or using the search field below, to display its historical level.</p>")

# data for plot of selected station
source = ColumnDataSource(data=dict(dates=[], levels=[]))


def make_dataset(station_name):
    try:
        selected_station = next(s for s in stations if s.name == station_name)
        dates, levels = fetch_measure_levels(selected_station.measure_id, dt=timedelta(days=30))
        return ColumnDataSource(data=dict(dates=dates, levels=levels))
    except StopIteration:
        print("Station {} could not be found".format(select_input.value))
        return ColumnDataSource(data=dict(dates=[], levels=[]))


def update_select():
    selected_station_name = select_input.value
    print(selected_station_name)
    new_data = make_dataset(selected_station_name)
    source.data.update(new_data.data)


select_input.on_change('value', lambda attr, old, new: update_select())
update_select()

selected_plot = plot_water_levels_dynamic(source)
selected_plot.plot_height = 350
selected_plot.plot_width = 600
selected_plot.sizing_mode = 'scale_width'


# Prediction

predict_text = Div(text="""<p>Choose one of the high risk stations to see the prediction by a recurrent neural network.</p>""")

predict_date = []
predict_level = []
predict_plots = []
for station in highrisk_stations:
    date, level = predict(station.name, dataset_size=1000, lookback=2000, iteration=100, display=300,
                         use_pretrained=False, batch_size=256, epoch=20)
    predict_plot = plot_prediction(date, level)
    predict_plot.plot_width = 400
    predict_plot.plot_height = 400
    predict_plot.sizing_mode = 'scale_width'
    predict_plots.append(Panel(child=predict_plot, title=station.name))

predict_tabs = Tabs(tabs=predict_plots)



# Layout
map_column = column(location_map, width=700, height=500)

select_column = column(select_text, select_input, selected_plot, width=600, height=500)
select_column.sizing_mode = "fixed"

highrisk_column = column(highrisk_title, highrisk_plots, width=800, height=600)
highrisk_column.sizing_mode = "fixed"

predict_column = column(predict_text, predict_tabs, width=500, height=600)
predict_column.sizing_mode = "fixed"

l = layout([
    [location_map, select_column],
    [highrisk_column, predict_column]
])


curdoc().add_root(l)
curdoc().title = "Flood Warning System"
