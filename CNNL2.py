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



#jednolizenie danych itd.

img_width, img_height = 100, 100

train_data_dir = 'plate-and-food/train'
validation_data_dir = 'plate-and-food/valid'
nb_train_samples = 700
nb_validation_samples = 100
epochs = 6
batch_size = 14

if K.image_data_format() == 'channels_first':
    input_shape = (3, img_width, img_height)
else:
    input_shape = (img_width, img_height, 3)

train_datagen = ImageDataGenerator(
    rescale = 1. / 255,
    shear_range = 0.2,
    zoom_range = 0.2,
    horizontal_flip = True)

test_datagen = ImageDataGenerator(rescale = 1. / 255)

train_generator = train_datagen.flow_from_directory(
    train_data_dir,
    target_size = (img_width, img_height),
    batch_size = batch_size,
    class_mode = 'binary')

validation_generator = test_datagen.flow_from_directory(
    validation_data_dir,
    target_size = (img_width, img_height),
    batch_size = batch_size,
    class_mode = 'binary')


model = load_model('third_try.h5')
# summarize model.
model.summary()



path = random.choice(os.listdir("C:\\Users/Kinia/Desktop/sztuczna/plate-and-food/test"))
print(path)

img_pred = image.load_img("plate-and-food/test/" + path, target_size = (100, 100))
img_pred = image.img_to_array(img_pred)
img_pred =  np.expand_dims(img_pred, axis = 0)


rslt = model.predict(img_pred)
print (rslt)
if rslt[0][0] == 1:
    prediction = "plate"
else:
    prediction = "food"

print (prediction)