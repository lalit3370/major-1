from keras import backend as K
from keras.preprocessing.image import ImageDataGenerator,load_img, img_to_array
from keras.models import Sequential, Model
from keras.layers import Conv2D, MaxPooling2D,GlobalAveragePooling2D
from keras.layers import Activation, Dropout, BatchNormalization, Flatten, Dense, AvgPool2D,MaxPool2D,Input,SeparableConv2D
from keras.models import Sequential, Model
from keras.callbacks import ModelCheckpoint, Callback, EarlyStopping
# from keras.applications.vgg16 import VGG16, preprocess_input
from keras.optimizers import Adam
from skimage.io import imread
import tensorflow as tf
import os
import numpy as np
import pandas as pd
import glob
import cv2
from pathlib import Path
import sys

from tensorflow.keras.applications.densenet import DenseNet169
denseNet169 = DenseNet169(input_shape = (224,224,3), 
                                include_top = False, 
                                weights = "imagenet")


for layer in denseNet169.layers:
    layer.trainable = False

x = Flatten()(denseNet169.output)
x = Dense(512, activation='relu')(x)
x = Dropout(0.2)(x)
x = Dense(256, activation='relu')(x)
x = Dense(128, activation='relu')(x)
x = Dropout(0.4)(x)
x = Dense(64, activation='relu')(x)
x = Dense(1 , activation='sigmoid')(x)

model = Model( denseNet169.input, x)
model.compile(optimizer='adam', loss="binary_crossentropy",metrics=['accuracy'])
data_dir = Path('./public')
model.load_weights("./denseNet169_weights.hdf5");
imgGrab = data_dir.glob(str(sys.argv[1]))
# imgGrab = data_dir.glob(str('COVID19(575).jpg'))

test_data = []
for img in imgGrab:
    # print('{"imagename":"'+str(img)+'"}')
    # sys.stdout.flush()
    img = cv2.imread(str(img))
    img = cv2.resize(img, (224,224))
    if img.shape[2] ==1:
        img = np.dstack([img, img, img])
    else:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = img.astype(np.float32)/255.
    test_data.append(img)
    
test_data = np.array(test_data)

densePred = model.predict(test_data, batch_size=16)
# label = test_generator.classes
predicted_class_indices=densePred
predicted_class_indices[predicted_class_indices>0.5]=1
predicted_class_indices[predicted_class_indices<=0.5]=0


outputDense169=[]
for i in range(predicted_class_indices.shape[0]):
    outputDense169.append(int(predicted_class_indices[i]))


# labels = (test_generator.class_indices)
# labels2 = dict((v,k) for k,v in labels.items())
# predictions = [labels2[k] for k in outputDense169]
# print(outputDense169)
print('{"status":"'+str(outputDense169[0])+'"}')
# print (labels)
# print (predictions)
# print(preds)