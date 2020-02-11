import os

os.environ["KERAS_BACKEND"] = "plaidml.keras.backend"

import numpy as np
import datetime
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
import keras
from keras.models import Sequential
from keras.layers import Dense, LSTM

from .datafetcher import fetch_measure_levels
from .stationdata import build_station_list

scalar = MinMaxScaler(feature_range=(0, 1))
np.random.seed(6)  # for reproducibility


def fetch_levels(station_name, dt, return_date=False):
    stations = build_station_list()
    try:
        station = next(s for s in stations if s.name == station_name)
    except StopIteration:
        print("Station {} could not be found".format(station_name))
        return
    date, data = fetch_measure_levels(station.measure_id, dt=datetime.timedelta(days=dt))

    if return_date:
        return date[::-1], np.array(data)[::-1]
    else:
        return np.array(data)[::-1]


def data_prep(data, lookback, exclude=0):
    if exclude != 0:
        data = data[:-exclude]
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


def train_model(model, x, y, batch_size, epoch, save_file='./floodsystem/cache/predictor_model.hdf5', show_loss=False):
    history = model.fit(x, y, batch_size=batch_size, epochs=epoch, verbose=1)
    if show_loss:
        plt.plot(history.history['loss'])
        plt.ylabel('loss')
        plt.show()
    try:
        model.save(save_file)
    except OSError:
        os.mkdir('./floodsystem/cache')
        model.save(save_file)
    return model


def train_all(stations, dataset_size=1000, lookback=2000, batch_size=256, epoch=20):
    for i, station in enumerate(stations):
        print('Training for {} ({}/{})'.format(station.name, i, len(stations)))
        levels = fetch_levels(station.name, dataset_size)
        scalar.fit(levels.reshape(-1, 1))  # fit the scalar on across the entire dataset
        x_train, y_train = data_prep(levels, lookback)
        train_model(build_model(lookback), x_train, y_train, batch_size, epoch,
                    save_file='./floodsystem/cache/{}.hdf5'.format(station.name))


def predict(station_name, dataset_size=1000, lookback=2000, iteration=100, display=300, use_pretrained=True,
            batch_size=256, epoch=20):
    date, levels = fetch_levels(station_name, dataset_size, return_date=True)
    scalar.fit(levels.reshape(-1, 1))  # fit the scalar on across the entire dataset

    if use_pretrained:
        try:
            model = keras.models.load_model('./floodsystem/cache/{}.hdf5'.format(station_name))
        except:
            print('No pre-trained model for {} found, training a model for it now.'.format(station_name))
            x_train, y_train = data_prep(levels, lookback)
            model = train_model(build_model(lookback), x_train, y_train, batch_size, epoch,
                                save_file='./floodsystem/cache/{}.hdf5'.format(station_name))
    else:
        print('Training a model for {} now.'.format(station_name))
        x_train, y_train = data_prep(levels, lookback)
        model = train_model(build_model(lookback), x_train, y_train, batch_size, epoch,
                            save_file='./floodsystem/cache/{}.hdf5'.format(station_name))

    # prediction of future <iteration> readings, based on the last <lookback> values
    predictions = None
    pred_levels = scalar.transform(levels[-lookback:].reshape(-1, 1))
    pred_levels = pred_levels.reshape(1, 1, lookback)
    for i in range(iteration):
        prediction = model.predict(pred_levels)
        pred_levels = np.append(pred_levels[:, :, -lookback + 1:], prediction.reshape(1, 1, 1), axis=2)
        predictions = np.append(predictions, prediction, axis=0) if predictions is not None else prediction

    # demo of prediction of the last <display> data points, which is based on the <lookback> values before the final 100 points
    demo = None
    demo_levels = scalar.transform(levels[-display - lookback:-display].reshape(-1, 1)).reshape(1, 1, lookback)
    for i in range(display):
        prediction = model.predict(demo_levels)
        demo_levels = np.append(demo_levels[:, :, -lookback + 1:], prediction.reshape(1, 1, 1), axis=2)
        demo = np.append(demo, prediction, axis=0) if demo is not None else prediction

    # return on last <display> data points, the demo values, and future predictions
    date = (date[-display:], [date[-1] + datetime.timedelta(minutes=15) * i for i in range(iteration)])
    return date, levels[-display:], scalar.inverse_transform(
        demo), scalar.inverse_transform(predictions)
