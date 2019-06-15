from id3 import Id3Estimator, export_graphviz
from sklearn.model_selection import train_test_split
import pandas as ps
import numpy as np
from sklearn.preprocessing import LabelEncoder

def BuildTree():
    feature_names = ["danie", "na ciepło", "z mięsem", "na słodko", "kwaśne", "alkoholowe", "czekoladowe", "wybor"]

    dataset = ps.read_csv("recommend.csv", header=None, names=feature_names, sep=";")
 
    X = dataset.drop('wybor', axis=1)
    Y = dataset['wybor']

    clf = Id3Estimator()

    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.20)
    clf.fit(X_train, Y_train)
    
    export_graphviz(clf.tree_, "lol.dot", feature_names)
    return clf

def PredictMeal(clf, prediction):
    abc=[]
    clientInfo = [
        [np.random.randint(11,14), np.random.randint(0,10),  np.random.randint(0,10), np.random.randint(0,10), np.random.randint(0,10),
         np.random.randint(0,10), np.random.randint(0,10)]]
        print(clientInfo)
    result = clf.predict(clientInfo)
    print("Czy wydac rachunek: ", result)
    return result

meal = BuildTree()
print(PredictMeal(meal, 10))