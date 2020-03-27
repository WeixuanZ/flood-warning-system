from bokeh.io import show

from floodsystem.plot import plot_prediction
from floodsystem.predictor import predict
from floodsystem.stationdata import build_station_list


def run():
    stations = build_station_list()

    # date, data, demo, prediction = predict('Cam', dataset_size=1000, lookback=2000, iteration=100, display=300, use_pretrained=True, batch_size=256, epoch=20)
    date, data = predict(
        stations[5].name,
        dataset_size=1000,
        lookback=2000,
        iteration=100,
        display=300,
        use_pretrained=True,
        batch_size=256,
        epoch=20,
    )

    p = plot_prediction(date, data)

    show(p)


if __name__ == "__main__":
    run()
