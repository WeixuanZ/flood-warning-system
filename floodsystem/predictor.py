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


def fetch_levels(station_name, dt=100):
    stations = build_station_list()
    try:
        station = next(s for s in stations if s.name == station_name)
    except StopIteration:
        print("Station {} could not be found".format(station_name))
        return
    _, data = fetch_measure_levels(station.measure_id, dt=datetime.timedelta(days=dt))
    return np.array(data)


def data_prep(data, lookback=60):
    scaled_levels = scalar.fit_transform(data.reshape(-1, 1))
    x = np.array([scaled_levels[i - lookback:i, 0] for i in range(lookback, len(scaled_levels))])
    x = np.reshape(x, (x.shape[0], 1, x.shape[1]))  # samples, time steps, features
    y = np.array([scaled_levels[i, 0] for i in range(lookback, len(scaled_levels))])
    return x, y


def build_model(lookback=60):
    model = Sequential()
    model.add(LSTM(units=32, return_sequences=True, input_shape=(1, lookback), activation='tanh'))
    model.add(Dropout(0.2))
    model.add(LSTM(units=64, activation='tanh'))
    model.add(Dropout(0.2))
    model.add(Dense(1, activation='sigmoid'))

    model.compile(loss='mean_squared_error', optimizer='Adam')

    return model


def train_model(model, x, y, batch_size=128, epoch=1000, save_file='./floodsystem/cache/predictor_model.hdf5'):
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


def predict(station_name, dataset_size=100, lookback=60, iteration=10, use_pretrained=True):

    levels = fetch_levels(station_name, dataset_size)
    if use_pretrained:
        try:
            model = keras.models.load_model('./floodsystem/cache/predictor_model.hdf5')
        except:
            print('No pre-trained model found, training a model for {} now.'.format(station_name))
            x_train, y_train = data_prep(levels, lookback)
            model = train_model(build_model(lookback), x_train, y_train, epoch=100)
    else:
        print('Training a model for {} now.'.format(station_name))
        x_train, y_train = data_prep(levels, lookback)
        model = train_model(build_model(lookback), x_train, y_train, epoch=100)

    predictions = None
    levels = scalar.fit_transform(levels[-lookback:].reshape(-1, 1))
    levels = levels.reshape(1, 1, lookback)
    for i in range(iteration):
        prediction = model.predict(levels)
        levels = np.append(levels[:, :, -lookback+1:], prediction.reshape(1, 1, 1), axis=2)
        predictions = np.append(predictions, prediction, axis=0) if predictions is not None else prediction

    return fetch_levels(station_name, dataset_size)[-100:], scalar.inverse_transform(predictions)

