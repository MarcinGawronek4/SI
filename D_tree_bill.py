# -*- coding: utf-8 -*-
from id3 import Id3Estimator, export_graphviz
from sklearn.model_selection import train_test_split
import pandas as ps
import numpy as np


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

    return clf


def PredictBill(clf,prediction):
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



