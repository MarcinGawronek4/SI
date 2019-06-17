# -*- coding: utf-8 -*-
from id3 import Id3Estimator, export_graphviz
from sklearn.model_selection import train_test_split
import pandas as ps
import numpy as np
from keras.preprocessing import image
from keras.models import load_model
import os
import random

def BuildTree():
    # nazwy cech
    feature_names = ["pair", "empty_plate", "talking", "mood", "asked", "hurry", "bill"]

    Yfeature_names = ["pair", "empty_plate", "talking", "mood", "asked", "hurry"]

    # wczytaj dataset z pliku dane.csv
    dataset = ps.read_csv("bill.csv", header=None, names=feature_names, sep=";")

    X = dataset.drop('bill', axis=1)
    Y = dataset['bill']

    # tworzenie drzewa decyzyjnego
    clf = Id3Estimator()

    # Podział na dane treningowe i dane testowe
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.20)
    # fit - synonim do "find patterns in data"
    clf.fit(X_train, Y_train)
    export_graphviz(clf.tree_, "test.dot", feature_names)
    model = load_model('third_try.h5')

    while True:
        path = random.choice(os.listdir("C://Users/Kinia/Desktop/sztuczna2/SI-master/test"))
        print(path)

        img_pred = image.load_img("test/" + path, target_size=(100, 100))
        img_pred = image.img_to_array(img_pred)
        img_pred = np.expand_dims(img_pred, axis=0)

        rslt = model.predict(img_pred)
        print(rslt)
        if rslt[0][0] == 1:
            prediction = 1
            break
        else:
            prediction = 0

        print(prediction)
    return [prediction, clf];


def PredictBill(k):
    clf = k[1]
    prediction = k[0]
    clientInfo = [
        [np.random.randint(2), prediction, np.random.randint(2), np.random.randint(99), np.random.randint(2),
         np.random.randint(2)]]
    print(clientInfo)
    result = clf.predict(clientInfo)
    print("Czy wydac rachunek: ", result)
    return result


# bill = BuildTree()
# if PredictBill(bill) == 1:
#     print("udalo sie")
# else:
#     print("no przyps")
