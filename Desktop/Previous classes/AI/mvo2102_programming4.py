

import numpy as np
import tensorflow as tf
from keras.datasets import cifar10
from keras import Sequential
from keras.layers import Dense, Flatten, Conv2D, MaxPooling2D, Dropout
from keras import optimizers


def load_cifar10():
    train, test = cifar10.load_data()
    xtrain, ytrain = train
    xtest, ytest = test

    ytrain_1hot = np.eye(10, dtype= int)[ytrain]
    ytrain_1hot = ytrain_1hot[:,0]
    ytest_1hot = np.eye(10)[ytest]
    ytest_1hot = ytest_1hot[:,0]

    xtrain = xtrain/255
    xtest = xtest/255

    return xtrain, ytrain_1hot, xtest, ytest_1hot


def build_multilayer_nn():
    """"
    [1.4890375181198121, 0.47689999999999999]
    """

    nn = Sequential()
    nn.add(Flatten(input_shape=(32,32,3)))
    hidden = Dense(units=100, activation="relu")
    nn.add(hidden)

    output = Dense(units=10, activation="softmax")
    nn.add(output)
    return nn


def train_multilayer_nn(model, xtrain, ytrain_1hot):
    sgd = optimizers.SGD(lr=0.01)
    model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy']) 
    model.fit(xtrain, ytrain_1hot, epochs=20, batch_size=32)
 

def build_convolution_nn():
    '''
    [0.76899708118438723, 0.72959999999999999]
    '''

    #create network
    nn = Sequential()
    #add two convolution layers, first one specifying input shape
    nn.add(Conv2D(32, (3, 3), activation='relu', padding="same", input_shape=(32, 32, 3)))
    nn.add(Conv2D(32, (3, 3), activation='relu', padding="same"))
    #add pooling layer to make 16x16x32
    nn.add(MaxPooling2D(pool_size=(2, 2)))
    #dropout .25 of the information
    nn.add(Dropout(0.25))
    #add two more convolution layers
    nn.add(Conv2D(32, (3, 3), activation='relu', padding="same"))
    nn.add(Conv2D(32, (3, 3), activation='relu', padding="same"))
    #add another pooling layer
    nn.add(MaxPooling2D(pool_size=(2, 2)))
    #add dropout layer of 0.5
    nn.add(Dropout(0.5))
    #flatten data from 8x8x32
    nn.add(Flatten(input_shape=(8, 8, 32)))
    #Add final hidden layers
    hidden1 = Dense(units=250, activation="relu")
    nn.add(hidden1)
    hidden2 = Dense(units=100, activation="relu")
    nn.add(hidden2)
    output = Dense(units=10, activation="softmax")
    nn.add(output)

    return nn
    

def train_convolution_nn(model, xtrain, ytrain_1hot):
    sgd = optimizers.SGD(lr=0.01)
    model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
    model.fit(xtrain, ytrain_1hot, epochs=20, batch_size=32)
    

def get_binary_cifar10():    
    train, test = cifar10.load_data()
    xtrain, ytrain = train
    xtest, ytest = test

    ytrain[(ytrain < 2) | (ytrain > 7)] = 0
    ytrain[(ytrain > 1) & (ytrain < 8)] = 1
    ytest[(ytest < 2) | (ytest > 7)] = 0
    ytest[(ytest > 1) & (ytest < 8)] = 1


    ytrain = ytrain[:,0]
    ytest = ytest[:,0]

    '''''
    ytrain_1hot = np.eye(10, dtype= int)[ytrain]
    ytrain_1hot = ytrain_1hot[:,0]
    ytest_1hot = np.eye(10)[ytest]
    ytest_1hot = ytest_1hot[:,0]
    '''
    xtrain = xtrain/255
    xtest = xtest/255

    return xtrain, ytrain, xtest, ytest


def build_binary_classifier():
    '''
    [0.15248513023853302, 0.94059999999999999]
    '''
    #create network
    nn = Sequential()
    #add two convolution layers, first one specifying input shape
    nn.add(Conv2D(32, (3, 3), activation='relu', padding="same", input_shape=(32, 32, 3)))
    nn.add(Conv2D(32, (3, 3), activation='relu', padding="same"))
    #add pooling layer to make 16x16x32
    nn.add(MaxPooling2D(pool_size=(2, 2)))
    #dropout .25 of the information
    nn.add(Dropout(0.25))
    #add two more convolution layers
    nn.add(Conv2D(32, (3, 3), activation='relu', padding="same"))
    nn.add(Conv2D(32, (3, 3), activation='relu', padding="same"))
    #add another pooling layer
    nn.add(MaxPooling2D(pool_size=(2, 2)))
    #add dropout layer of 0.5
    nn.add(Dropout(0.5))
    #flatten data from 8x8x32
    nn.add(Flatten(input_shape=(8, 8, 32)))
    #Add final hidden layers
    hidden1 = Dense(units=250, activation="relu")
    nn.add(hidden1)
    hidden2 = Dense(units=100, activation="relu")
    nn.add(hidden2)
    output = Dense(units=1, activation="sigmoid")
    nn.add(output)

    return nn


def train_binary_classifier(model, xtrain, ytrain):
    sgd = optimizers.SGD(lr=0.01)
    model.compile(loss='binary_crossentropy', optimizer=sgd, metrics=['accuracy'])
    model.fit(xtrain, ytrain, epochs=20, batch_size=32)

if __name__ == "__main__":
    xtrain, ytrain, xtest, ytest = get_binary_cifar10()

    nn = build_binary_classifier()
    train_binary_classifier(nn, xtrain, ytrain)

    x = nn.evaluate(xtest, ytest)
    print(x)
    nn.summary()



