import tensorflow as tf
import numpy as np
from keras import layers
from keras import models
from keras.preprocessing import image
from pathlib import Path
import csv
from PIL import Image
from keras.utils import to_categorical
import os
#os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
path='C:/Users/binho/Desktop/Pythono/Interface/datasets/tonalidades/treino'
path = Path(path)
labels = 'inferred'
itenes = list(path.rglob('*.*'))
features = len(itenes)
input_shape = (128, 128, 3)
generator = image.ImageDataGenerator(fill_mode='nearest', featurewise_std_normalization=True)
batch_size = 20
input_size = (128,128)
timesteps = int(features/batch_size)
for x in range(0,len(itenes)):
   if(x%100==0): print(x)
   itenes[x] = Image.open(itenes[x])
   itenes[x] = itenes[x].resize(size=input_size)
   itenes[x] = np.asarray(itenes[x])
itenes = np.asarray(itenes)
y = itenes.shape
if(len(y)==3):
   itenes = np.reshape(itenes, (y[0],y[1],y[2],1))
generator.fit(itenes)
traingen = generator.flow_from_directory(path, target_size=input_size,batch_size=batch_size, shuffle=True)
#seção do modelo

model = models.Sequential()
model.add(layers.Flatten())
model.add(layers.Dense(units=512,activation='relu'))
model.add(layers.Dense(units=2,activation='sigmoid'))
model.compile(optimizer='SGD',loss='binary_crossentropy',metrics=['accuracy'])
history = model.fit(traingen, steps_per_epoch = timesteps,epochs = 7)