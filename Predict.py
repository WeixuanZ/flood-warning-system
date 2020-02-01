import matplotlib.pyplot as plt
import numpy as np

from floodsystem.predictor import predict
from floodsystem.stationdata import build_station_list

stations = build_station_list()

# data, demo, prediction = predict('Cam', dataset_size=1000, lookback=2500, iteration=100, display=300, use_pretrained=False, batch_size=256, epoch=20)
data, demo, prediction = predict(stations[5].name, dataset_size=1000, lookback=2000, iteration=100, display=300, use_pretrained=False, batch_size=256, epoch=20)

plt.plot(np.arange(1, len(data) + 1, 1), data)
plt.plot(np.arange(1, len(data) + 1, 1), demo)
plt.plot(np.arange(len(data) + 1, len(data) + len(prediction) + 1, 1), prediction)
plt.show()
