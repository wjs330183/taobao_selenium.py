# 读取数据
import os
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, optimizers, datasets

(x, y), (x_val, y_val) = datasets.mnist.load_data()

x = tf.convert_to_tensor(x, dtype=tf.float32) / 255
y = tf.convert_to_tensor(y, dtype=tf.int32)
y = tf.one_hot(y, depth=10)
print("x.shape: {}, y.shape: {}".format(x.shape, y.shape))
train_dataset = tf.data.Dataset.from_tensor_slices((x, y))
train_dataset = train_dataset.batch(200)
model = keras.Sequential([
    layers.Dense(512, activation='relu'),
    layers.Dense(256, activation='relu'),
    layers.Dense(256)])

optimizer = optimizers.SGD(learning_rate=0.001)


(X_train, y_train) = (mnist.train.images, mnist.train.labels)
(X_test, y_test) = (mnist.test.images, mnist.test.labels)
X_train.shape  # (55000,784)
X_test.shape  # (10000,784)
model = Sequential()
model.add(Dense(input_dim=28 * 28, units=250, activation='sigmoid'))
model.add(Dense(units=250, activation='sigmoid'))
model.add(Dense(units=250, activation='sigmoid'))
model.add(Dense(units=10, activation='softmax'))
model.compile(loss='mse', optimizer=SGD(lr=0.1),
              metrics=['accuracy'])
model.fit(X_train, y_train, batch_size=100, epochs=10)
result1 = model.evaluate(X_train, y_train)
print('Train Accuracy:', result1[1])  # 0.133

result1 = model.evaluate(X_test, y_test)
print('Test Accuracy:', result1[1])  # 0.136

#
# #读取数据
# from tensorflow.examples.tutorials.mnist import input_data
# mnist = input_data.read_data_sets("MNIST_data/", one_hot=True) #实例化对象
#
# (X_train,y_train)=(mnist.train.images,mnist.train.labels)
# (X_test,y_test)=(mnist.test.images,mnist.test.labels)
# X_train.shape  #(55000,784)
# X_test.shape   #(10000,784)
# model=Sequential()
# model.add(Dense(input_dim=28*28,units=250,activation='sigmoid'))
# model.add(Dense(units=250,activation='sigmoid'))
# model.add(Dense(units=250,activation='sigmoid'))
# model.add(Dense(units=10,activation='softmax'))
# model.compile(loss='mse',optimizer=SGD(lr=0.1),
#               metrics=['accuracy'])
# model.fit(X_train,y_train,batch_size=100,epochs=10)
# result1=model.evaluate(X_train,y_train)
# print('Train Accuracy:',result1[1])   #0.133
#
# result1=model.evaluate(X_test,y_test)
# print('Test Accuracy:',result1[1])   #0.136
