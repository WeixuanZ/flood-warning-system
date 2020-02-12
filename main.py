import numpy as np

from bokeh.io import output_file, show
from bokeh.layouts import gridplot, layout
from bokeh.models import ColumnDataSource, GMapOptions, HoverTool, DatetimeTickFormatter, Span, BoxAnnotation
from bokeh.plotting import figure, curdoc

from floodsystem.plot import *
from floodsystem.flood import stations_highest_rel_level
from floodsystem.stationdata import build_station_list, update_water_levels
from floodsystem.predictor import predict

stations = build_station_list()

location_map = Map(stations).build()

update_water_levels(stations)
high_risk_stations = stations_highest_rel_level(stations, 5)
highrisk_plots = plot_water_levels_multiple(high_risk_stations, dt=10)

date, data = predict(stations[5].name, dataset_size=1000, lookback=2000, iteration=100, display=300,
                     use_pretrained=True, batch_size=256, epoch=20)
prediction_plot = plot_prediction(date, data)

l = layout([
    [location_map, highrisk_plots],
    [prediction_plot]
])

curdoc().add_root(l)
curdoc().title = "Flood Warning System"
