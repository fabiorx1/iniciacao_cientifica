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
#seção da escolha dos dados
os.environ['CUDA_VISIBLE_DEVICES']= '-1'
path='C:/Users/binho/Desktop/Pythono/Interface/datasets/cancer10k/treino'
path = Path(path)
labels = 'inferred'
itenes = list(path.rglob('*.*'))
features = len(itenes)
input_shape = (96,96,3)
#seção do tratamento de dados
generator = image.ImageDataGenerator(fill_mode='nearest')
batch_size = 20
input_size = (96,96)
timesteps = int(features/batch_size)
'''for x in range(0,len(itenes)):
   itenes[x] = Image.open(itenes[x])
   itenes[x] = itenes[x].resize(size=input_size)
   itenes[x] = np.asarray(itenes[x])
itenes = np.asarray(itenes)
y = itenes.shape
if(len(y)==3):
   itenes = np.reshape(itenes, (y[0],y[1],y[2],1))
generator.fit(itenes)'''
traingen = generator.flow_from_directory(path, target_size=input_size,batch_size=batch_size, shuffle=True)
#seção do modelo da arquitetura
model = models.Sequential()
model.add(layers.ZeroPadding2D(input_shape=input_shape, padding=1))
model.add(layers.Conv2D(filters=64,kernel_size=3,strides=1,dilation_rate=1,activation='relu'))
model.add(layers.ZeroPadding2D(1))
model.add(layers.Conv2D(filters=64,kernel_size=3,strides=1,dilation_rate=1,activation='relu'))
model.add(layers.MaxPooling2D(pool_size=2,strides=2))

model.add(layers.ZeroPadding2D(1))
model.add(layers.Conv2D(filters=128,kernel_size=3,strides=1,dilation_rate=1,activation='relu'))
model.add(layers.ZeroPadding2D(1))
model.add(layers.Conv2D(filters=128,kernel_size=3,strides=1,dilation_rate=1,activation='relu'))
model.add(layers.MaxPooling2D(pool_size=2,strides=2))

model.add(layers.ZeroPadding2D(1))
model.add(layers.Conv2D(filters=256,kernel_size=3,strides=1,dilation_rate=1,activation='relu'))
model.add(layers.ZeroPadding2D(1))
model.add(layers.Conv2D(filters=256,kernel_size=3,strides=1,dilation_rate=1,activation='relu'))
model.add(layers.ZeroPadding2D(1))
model.add(layers.Conv2D(filters=256,kernel_size=3,strides=1,dilation_rate=1,activation='relu'))
model.add(layers.MaxPooling2D(pool_size=2,strides=2))

model.add(layers.ZeroPadding2D(1))
model.add(layers.Conv2D(filters=512,kernel_size=3,strides=1,dilation_rate=1,activation='relu'))
model.add(layers.ZeroPadding2D(1))
model.add(layers.Conv2D(filters=512,kernel_size=3,strides=1,dilation_rate=1,activation='relu'))
model.add(layers.ZeroPadding2D(1))
model.add(layers.Conv2D(filters=512,kernel_size=3,strides=1,dilation_rate=1,activation='relu'))
model.add(layers.MaxPooling2D(pool_size=2,strides=2))

model.add(layers.ZeroPadding2D(1))
model.add(layers.Conv2D(filters=512,kernel_size=3,strides=1,dilation_rate=1,activation='relu'))
model.add(layers.ZeroPadding2D(1))
model.add(layers.Conv2D(filters=512,kernel_size=3,strides=1,dilation_rate=1,activation='relu'))
model.add(layers.ZeroPadding2D(1))
model.add(layers.Conv2D(filters=512,kernel_size=3,strides=1,dilation_rate=1,activation='relu'))
model.add(layers.MaxPooling2D(pool_size=2,strides=2))

model.add(layers.Flatten())
model.add(layers.Dense(units=4096,activation='relu'))
model.add(layers.Dropout(0.5))
model.add(layers.Dense(units=4096,activation='relu'))
model.add(layers.Dropout(0.5))
model.add(layers.Dense(units=2,activation='softmax'))
model.compile(optimizer='Adam',loss='categorical_crossentropy',metrics=['accuracy'])
history = model.fit(traingen, steps_per_epoch = timesteps, epochs = 5)
