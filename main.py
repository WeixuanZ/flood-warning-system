import numpy as np

from bokeh.io import output_file, show
from bokeh.layouts import gridplot, layout, column
from bokeh.models import ColumnDataSource, Select, Div, TextInput, Button
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

select_input = TextInput(value="Cam", title="Name of station to search for:")
select_text = Div(text="<p>Select a station either by clicking on the map, or using the search field below, to display its historical level.</p>")

# Selected station plot
selected_station = stations[0]
try:
    selected_station = next(s for s in stations if s.name == select_input.value)
except StopIteration:
    print("Station {} could not be found".format(select_input.value))
dates, levels = fetch_measure_levels(selected_station.measure_id, dt=timedelta(days=30))
selected_plot = plot_water_levels(selected_station, dates, levels)
selected_plot.plot_height = 350
selected_plot.plot_width = 600
selected_plot.sizing_mode = 'scale_width'

predict_text = Div(text="""<p>Choose one of the high risk stations for prediction using a recurrent neural network.</p>""")
predict_select = Select(title="Station to predict:", value=highrisk_stations[0].name, options=[i.name for i in highrisk_stations])


class Source:
    date, data = predict(highrisk_stations[0].name, dataset_size=1000, lookback=2000, iteration=100, display=300,
                         use_pretrained=True, batch_size=256, epoch=20)


# Prediction
predict_plot = plot_prediction(Source.date, Source.data)
predict_plot.plot_width = 400
predict_plot.plot_height = 400
predict_plot.sizing_mode = 'scale_width'



# def update():
#     selection = predict_select.value
#     Source.data, Source.data = predict(selection, dataset_size=1000, lookback=2000, iteration=100, display=300,
#                          use_pretrained=True, batch_size=256, epoch=20)
#
#
# controls = [select_input, predict_select]
# for control in controls:
#     control.on_change('value', lambda attr, old, new: update())



map_column = column(location_map, width=700, height=500)

select_column = column(select_text, select_input, selected_plot, width=600, height=500)
select_column.sizing_mode = "fixed"

highrisk_column = column(highrisk_title, highrisk_plots, width=800, height=600)
highrisk_column.sizing_mode = "fixed"

predict_column = column(predict_text, predict_select, predict_plot, width=500, height=600)
predict_column.sizing_mode = "fixed"

l = layout([
    [location_map, select_column],
    [highrisk_column, predict_column]
])


# update()

curdoc().add_root(l)
curdoc().title = "Flood Warning System"
