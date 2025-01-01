# -*- coding: utf-8 -*-
"""transfer-learning-feature-extraction.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1HwMZfBhPKJYZqf3dcOAiwxNkQLK7rUpu
"""

!mkdir -p ~/.kaggle
!cp kaggle.json ~/.kaggle/

!kaggle datasets download -d salader/dogs-vs-cats

import zipfile
zip_ref = zipfile.ZipFile('/content/dogs-vs-cats.zip')
zip_ref.extractall('/content')
zip_ref.close()

import tensorflow
from tensorflow import keras
from keras import Sequential
from keras.layers import Dense, Flatten
from keras.applications.vgg16 import VGG16

conv_base = VGG16(
    weights = 'imagenet',
    include_top = False, # FC layers excluded
    input_shape = (150,150,3) # vgg expect 224x224x3  customize the input size
)

model = Sequential()

model.add(conv_base)
model.add(Flatten())
model.add(Dense(256, activation = 'relu'))
model.add(Dense(1,activation = 'sigmoid'))

conv_base.trainable = False

"""### Data Augmentation"""

from tensorflow.keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img

batch_size = 32

train_datagen  = ImageDataGenerator(
    rescale = 1./255,
    shear_range = 0.2,
    zoom_range = 0.2,
    horizontal_flip = True
)
test_datagen = ImageDataGenerator(rescale = 1./255) # on test data only apply normalization

train_generator  = train_datagen.flow_from_directory(
    '/content/train',
    target_size = (150,150),
    batch_size = batch_size,
    class_mode = 'binary'
)

validation_generator = test_datagen.flow_from_directory(
    '/content/test',
    target_size = (150,150),
    batch_size = batch_size,
    class_mode = 'binary'
)

model.compile(
    optimizer = 'adam',
    loss='binary_crossentropy',
    metrics=['accuracy'])

"""### Model Training"""

history = model.fit(
    train_generator,
    epochs = 10,
    validation_data=validation_generator
)

import matplotlib.pyplot as plt

plt.plot(history.history['accuracy'],color='red',label='train')
plt.plot(history.history['val_accuracy'],color='blue',label='validation')
plt.legend()
plt.show()

plt.plot(history.history['loss'],color='red',label='train_loss')
plt.plot(history.history['val_loss'],color='blue',label='validation_loss')
plt.legend()
plt.show()