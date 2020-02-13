import numpy as np

from bokeh.layouts import gridplot, layout, column
from bokeh.models import ColumnDataSource, Select, Div, TextInput, Tabs, Panel, RadioButtonGroup, GMapOptions, HoverTool, TapTool
from bokeh.plotting import curdoc, gmap


from floodsystem.plot import *
from floodsystem.flood import stations_highest_rel_level
from floodsystem.stationdata import build_station_list, update_water_levels
from floodsystem.datafetcher import fetch_measure_levels
from floodsystem.predictor import predict

map_select = True

# Fetching data

stations = build_station_list()
update_water_levels(stations)
highrisk_stations = stations_highest_rel_level(stations, 6)


# Map

locations = [i.coord for i in stations]
origin = (52.2070, 0.1131)
options = GMapOptions(lat=origin[0], lng=origin[1], map_type="roadmap", zoom=11)
tools = "crosshair,pan,wheel_zoom,reset,save"
location_map = gmap(environ.get('API_KEY'), options, title="Station locations", tools=tools, active_scroll="wheel_zoom")
map_source = ColumnDataSource(data=dict(lat=[i[0] for i in locations], lng=[i[1] for i in locations],
                                            name=[i.name for i in stations],
                                            river=[i.river for i in stations],
                                            town=[i.town for i in stations],
                                            typical_low=[i.typical_range[0] if i.typical_range is not None else 'nan' for i in stations],
                                            typical_high=[i.typical_range[1] if i.typical_range is not None else 'nan' for i in stations],
                                            latest_level=[i.latest_level if i.latest_level is not None else 'nan' for i in stations],
                                            relative_level=[i.relative_water_level() if i.relative_water_level() is not None else 'nan' for i in stations],
                                            color=[map_palette(i) for i in stations]))
r = location_map.circle(x="lng", y="lat", size=15, fill_color='color', fill_alpha=0.8, source=map_source)
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


def update_map_select(attr, old, new):
    if map_select is True:
        inds = new
        selected_station_name = map_source.data['name'][inds[0]]
        print(selected_station_name)
        new_data = make_dataset(selected_station_name)
        source.data.update(new_data.data)


r.data_source.selected.on_change('indices', update_map_select)


selected_plot = plot_water_levels_dynamic(source)
selected_plot.plot_height = 320
selected_plot.plot_width = 600
selected_plot.sizing_mode = 'scale_width'


# Prediction

predict_text = Div(text="""<p>Choose one of the high risk stations to see the prediction by a recurrent neural network.</p>""")

predict_date = []
predict_level = []
predict_plots = []
for station in highrisk_stations:
    date, level = predict(station.name, dataset_size=1000, lookback=200, iteration=100, display=300,
                         use_pretrained=True, batch_size=256, epoch=20)
    predict_plot = plot_prediction(date, level)
    predict_plot.plot_width = 400
    predict_plot.plot_height = 400
    predict_plot.sizing_mode = 'scale_width'
    predict_plots.append(Panel(child=predict_plot, title=station.name))

predict_tabs = Tabs(tabs=predict_plots)



# Layout
map_column = column(location_map, width=700, height=500)

radio_button_group = RadioButtonGroup(labels=["Click on Map", "Search"], active=0)
select_column = column(select_text, radio_button_group, selected_plot, width=600, height=500)
select_column.sizing_mode = "fixed"


def update_toggle():
    global map_select
    if radio_button_group.active == 1:
        map_select = False
        location_map.tools.pop()
        select_column.children = [select_text, radio_button_group, select_input, selected_plot]
    else:
        map_select = True
        location_map.add_tools(tap_tool)
        select_column.children = [select_text, radio_button_group, selected_plot]


radio_button_group.on_change('active', lambda attr, old, new: update_toggle())


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
