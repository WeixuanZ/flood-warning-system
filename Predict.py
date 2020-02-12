import numpy as np
# import datetime
# import pandas as pd

from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource, DatetimeTickFormatter
from bokeh.plotting import figure


from floodsystem.predictor import predict
from floodsystem.stationdata import build_station_list

stations = build_station_list()

# date, data, demo, prediction = predict('Cam', dataset_size=1000, lookback=2000, iteration=100, display=300, use_pretrained=True, batch_size=256, epoch=20)
date, data = predict(stations[5].name, dataset_size=1000, lookback=2000, iteration=100, display=300, use_pretrained=True, batch_size=256, epoch=20)

output_file("prediction.html")
p = figure(plot_width = 600, plot_height = 600,
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
p.xaxis.major_label_orientation = np.pi/4
show(p)

