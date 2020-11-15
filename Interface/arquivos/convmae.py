import tensorflow as tf
import numpy as np
from keras import layers
from keras import models
from keras.preprocessing import image
from pathlib import Path
import csv
from PIL import Image
from keras.utils import to_categorical
path='C:/Users/binho/Desktop/Pythono/Interface/datasets/geometricas/treino'
path = Path(path)
labels = 'inferred'
itenes = list(path.rglob('*.*'))
features = len(itenes)
input_shape = (128, 128, 3)
generator = image.ImageDataGenerator(samplewise_std_normalization=True,fill_mode='constant')
batch_size = 20
input_size = (128,128)
timesteps = int(features/batch_size)
for x in range(0,len(itenes)):
   itenes[x] = Image.open(itenes[x])
   itenes[x] = itenes[x].resize(size=input_size)
   itenes[x] = np.asarray(itenes[x])
itenes = np.asarray(itenes)
y = itenes.shape
if(len(y)==3):
   itenes = np.reshape(itenes, (y[0],y[1],y[2],1))
generator.fit(itenes)
traingen = generator.flow_from_directory(path, target_size=input_size,batch_size=batch_size, shuffle=True)
model = models.Sequential()
model.add(layers.Conv2D(input_shape=input_shape,filters=32,kernel_size=5,strides=1,dilation_rate=1,activation='relu'))
model.add(layers.Conv2D(filters=32,kernel_size=5,strides=1,dilation_rate=1,activation='relu'))
model.add(layers.MaxPooling2D(pool_size=2,strides=1))
model.add(layers.Flatten())
model.add(layers.Dense(units=256,activation='relu'))
model.add(layers.Dense(units=2,activation='sigmoid'))
model.compile(optimizer='RMSprop',loss='mean_squared_error',metrics=['accuracy'])
history = model.fit(traingen, steps_per_epoch = timesteps,epochs = 12)




'''
registro = dense.history.history
registro.keys()

def plot(x,y,x_label,y_label,title,grid,modo):
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    if(grid): plt.grid()
    plt.plot(x, y, modo)
    plt.show()
'''
