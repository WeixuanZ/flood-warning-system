import os
os.environ["KERAS_BACKEND"] = "plaidml.keras.backend"
import numpy as np
from sklearn.preprocessing import MinMaxcaler
import matplotlib.pyplot as plt

import keras
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout
from keras.optimizers import SGD, Adam

data = None

scaler = MinMaxcaler(feature_range=(0, 1))
data_scaled = scaler.fit_transform(data)


def data_prep(data, num)
    return np.array([data[i - num:i, 0] for i in range(num, len(data))]), np.array([data[i, 0] for i in range(num, len(data))])

x_train, y_train = data_prep(data, 10)
x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))  # samples, time steps, features

model = Sequential()
model.add(LSTM(units = 32, return_sequences = True, input_shape = (x_train.shape[1], 1), activation='tanh', recurrent_activation='sigmoid'))
model.add(Dropout(0.2))
model.add(LSTM(units = 64, activation='tanh', recurrent_activation='sigmoid'))
model.add(Dropout(0.2))
model.add(LSTM(units = 128, activation='tanh', recurrent_activation='sigmoid'))
model.add(Dropout(0.4))
model.add(Dense(1, activation='softmax'))

model.compile(loss='mean_squared_error', optimizer='Adam', metrics=['accuracy'])

def train_model(model,batch_size=128, epoch=1000, save_file='../model/detector_model.hdf5'):
	history = model.fit(x_train, y_train, batch_size=batch_size, epochs=epoch, verbose=1)

train_predict = model.predict()
train_predict = scaler.inverse_transform(trainPredict)