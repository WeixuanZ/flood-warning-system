import os

os.environ["KERAS_BACKEND"] = "plaidml.keras.backend"

import numpy as np
import datetime
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
import keras
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout

from .datafetcher import fetch_measure_levels
from .stationdata import build_station_list

scalar = MinMaxScaler(feature_range=(0, 1))
np.random.seed(6)


# TODO: display time
def fetch_levels(station_name, dt):
    stations = build_station_list()
    try:
        station = next(s for s in stations if s.name == station_name)
    except StopIteration:
        print("Station {} could not be found".format(station_name))
        return
    _, data = fetch_measure_levels(station.measure_id, dt=datetime.timedelta(days=dt))
    return np.array(data)


def data_prep(data, lookback):
    scaled_levels = scalar.transform(data.reshape(-1, 1))
    x = np.array([scaled_levels[i - lookback:i, 0] for i in range(lookback, len(scaled_levels))])
    x = np.reshape(x, (x.shape[0], 1, x.shape[1]))  # samples, time steps, features
    y = np.array([scaled_levels[i, 0] for i in range(lookback, len(scaled_levels))])
    return x, y


def build_model(lookback):
    model = Sequential()
    model.add(LSTM(256, activation='relu', input_shape=(1, lookback), recurrent_dropout=0.1))
    model.add(Dense(512, activation='relu'))
    # model.add(Dense(256, activation='relu'))
    model.add(Dense(1, activation='tanh'))
    model.compile(optimizer='adam', loss='mse')

    return model


def train_model(model, x, y, batch_size, epoch, save_file='./floodsystem/cache/predictor_model.hdf5'):
    history = model.fit(x, y, batch_size=batch_size, epochs=epoch, verbose=1)
    plt.plot(history.history['loss'])
    plt.ylabel('loss')
    plt.show()
    try:
        model.save(save_file)
    except OSError:
        os.mkdir('./floodsystem/cache')
        model.save(save_file)
    return model


def predict(station_name, dataset_size=1000, lookback=2000, iteration=100, display=300, use_pretrained=True, batch_size=256, epoch=20):
    levels = fetch_levels(station_name, dataset_size)
    scalar.fit(levels.reshape(-1,1))  # fit the scalar on across the entire dataset
    if use_pretrained:
        try:
            model = keras.models.load_model('./floodsystem/cache/predictor_model.hdf5')
        except:
            print('No pre-trained model found, training a model for {} now.'.format(station_name))
            x_train, y_train = data_prep(levels, lookback)
            model = train_model(build_model(lookback), x_train, y_train, batch_size, epoch)
    else:
        print('Training a model for {} now.'.format(station_name))
        x_train, y_train = data_prep(levels, lookback)
        model = train_model(build_model(lookback), x_train, y_train, batch_size, epoch)

    # prediction of future <iteration> readings, based on the last <lookback> values
    predictions = None
    levels = scalar.transform(levels[-lookback:].reshape(-1, 1))
    levels = levels.reshape(1, 1, lookback)
    for i in range(iteration):
        prediction = model.predict(levels)
        levels = np.append(levels[:, :, -lookback+1:], prediction.reshape(1, 1, 1), axis=2)
        predictions = np.append(predictions, prediction, axis=0) if predictions is not None else prediction

    # demo of prediction of the last 100 data points, which is based on the <lookback> values before the final 100 points
    demo = None
    levels = fetch_levels(station_name, dataset_size)
    levels = scalar.transform(levels[-display-lookback:-display].reshape(-1, 1)).reshape(1, 1, lookback)
    for i in range(display):
        prediction = model.predict(levels)
        levels = np.append(levels[:, :, -lookback+1:], prediction.reshape(1, 1, 1), axis=2)
        demo = np.append(demo, prediction, axis=0) if demo is not None else prediction

    # return on last 100 data points, the demo values, and future predictions
    return fetch_levels(station_name, dataset_size)[-display:], scalar.inverse_transform(demo), scalar.inverse_transform(predictions)

