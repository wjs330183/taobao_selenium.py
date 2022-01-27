import tensorflow as tf
import os

from tensorflow.keras import datasets, layers, models
import matplotlib.pyplot as plt

# 下载并准备 CIFAR10 数据集
# (train_images, train_labels), (test_images, test_labels) = datasets.cifar10.load_data()

# Normalize pixel values to be between 0 and 1
# train_images, test_images = train_images / 255.0, test_images / 255.0
#
#
# #验证数据
# class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer',
#                'dog', 'frog', 'horse', 'ship', 'truck']
#
# plt.figure(figsize=(10, 10))
# for i in range(25):
#     plt.subplot(5, 5, i + 1)
#     plt.xticks([])
#     plt.yticks([])
#     plt.grid(False)
#     plt.imshow(train_images[i])
#     # The CIFAR labels happen to be arrays,
#     # which is why you need the extra index
#     plt.xlabel(class_names[train_labels[i][0]])
# plt.show()

#
#
# gpus = tf.config.experimental.list_physical_devices(device_type='GPU')
# print(os.environ['CUDA_VISIBLE_DEVICES'])

# sess = tf.compat.v1.Session(config=tf.compat.v1.ConfigProto(log_device_placement=True))


print(tf.config.list_physical_devices('GPU'))

