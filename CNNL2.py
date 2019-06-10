# Importing the Keras libraries and packages

from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras import backend as K
import numpy as np
from keras.preprocessing import image
from keras.models import load_model
import os
import random






model = load_model('third_try.h5')
# summarize model.
model.summary()





k =1
prediction = 1
while prediction == 1:
    path = random.choice(os.listdir("C:\\Users/Kinia/Desktop/sztuczna/plate-and-food/test"))

    if k==1:
        img_pred = image.load_img("plate-and-food/test/20151127_120156.jpg", target_size = (100, 100))
        img_pred = image.img_to_array(img_pred)
        img_pred =  np.expand_dims(img_pred, axis = 0)

    elif k>1:
        img_pred = image.load_img("plate-and-food/test/" + path, target_size=(100, 100))
        img_pred = image.img_to_array(img_pred)
        img_pred = np.expand_dims(img_pred, axis=0)
    k = k+1
    print(k)
    rslt = model.predict(img_pred)
    print(prediction)
    if rslt[0][0] == 1:
        prediction = 0
    else:
        prediction = 1
    if prediction == 0:
        break



print (prediction)