import os

os.environ["KERAS_BACKEND"] = "plaidml.keras.backend"

import numpy as np
import datetime
from sklearn.preprocessing import MinMaxScaler
import keras
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout

from .datafetcher import fetch_measure_levels
from .stationdata import build_station_list

scalar = MinMaxScaler(feature_range=(0, 1))

def fetch_levels(station_name, dt=100):
    stations = build_station_list()
    try:
        station = next(s for s in stations if s.name == station_name)
    except StopIteration:
        print("Station {} could not be found".format(station_name))
        return
    _, data = fetch_measure_levels(station.measure_id, dt=datetime.timedelta(days=dt))
    return np.array(data)


def data_prep(data, sample_size=60):
    scaled_levels = scalar.fit_transform(data.reshape(-1, 1))
    x = np.array([scaled_levels[i - sample_size:i, 0] for i in range(sample_size, len(scaled_levels))])
    x = x.reshape(x.shape[0], 1, x.shape[1])  # samples, time steps, features
    print(x.shape)
    y = np.array([scaled_levels[i, 0] for i in range(sample_size, len(scaled_levels))])
    return x, y


def build_model(input_shape=60):
    model = Sequential()
    model.add(LSTM(units=32, return_sequences=True, input_shape=(input_shape,1), activation='tanh',
                   recurrent_activation='sigmoid'))
    model.add(Dropout(0.2))
    model.add(LSTM(units=64, activation='tanh', recurrent_activation='sigmoid'))
    model.add(Dropout(0.2))
    model.add(LSTM(units=128, activation='tanh', recurrent_activation='sigmoid'))
    model.add(Dropout(0.4))
    model.add(Dense(1, activation='softmax'))

    model.compile(loss='mean_squared_error', optimizer='Adam', metrics=['accuracy'])

    return model


def train_model(model, x, y, batch_size=128, epoch=1000, save_file='./model/predictor_model.hdf5'):
    model.fit(x, y, batch_size=batch_size, epochs=epoch, verbose=1)
    model.save(save_file)
    return model


def predict(station_name, dataset_size=100, sample_size=60, iteration=10, use_pretrained=True):
    if use_pretrained:
        try:
            model = keras.models.load_model('./model/predictor_model.hdf5')
        except:
            print('No pre-trained model found, training a model for {} now.'.format(station_name))
            levels = fetch_levels(station_name, dataset_size)
            x_train, y_train = data_prep(levels, sample_size)
            model = train_model(build_model(), x_train, y_train)
    else:
        print('Training a model for {} now.'.format(station_name))
        levels = fetch_levels(station_name, dataset_size)
        x_train, y_train = data_prep(levels, sample_size)
        model = train_model(build_model(), x_train, y_train)

    predictions = []
    levels = scalar.fit_transform(fetch_levels(station_name, sample_size).reshape(-1, 1))
    for i in range(iteration):
        prediction = model.predict(levels[-sample_size:])
        predictions.append(prediction)
        levels.append(prediction)

    return fetch_levels(station_name, sample_size), scalar.inverse_transform(predictions)



