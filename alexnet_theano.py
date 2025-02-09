# -*- coding: utf-8 -*-

""" AlexNet.
Applying 'Alexnet' to Oxford's 17 Category Flower Dataset classification task.
References:
    - Alex Krizhevsky, Ilya Sutskever & Geoffrey E. Hinton. ImageNet
    Classification with Deep Convolutional Neural Networks. NIPS, 2012.
    - 17 Category Flower Dataset. Maria-Elena Nilsback and Andrew Zisserman.
Links:
    - [AlexNet Paper](http://papers.nips.cc/paper/4824-imagenet-classification-with-deep-convolutional-neural-networks.pdf)
    - [Flower Dataset (17)](http://www.robots.ox.ac.uk/~vgg/data/flowers/17/)
"""

from __future__ import division, print_function, absolute_import

import tflearn
from theano import tensor
#from tflearn.layers.conv import conv_2d, max_pool_2d
#from tflearn.layers.normalization import local_response_normalization
#from tflearn.layers.estimator import regression

# import tflearn.datasets.oxflower17 as oxflower17
# X, Y = oxflower17.load_data(one_hot=True, resize_pics=(227, 227))
def alexnet(width,height,lr):
	# Building 'AlexNet'
	network = input_data(shape=[None, width, height, 1])
	network = conv_2d(network, 96, 11, strides=4, activation='relu')
	network = max_pool_2d(network, 3, strides=2)
	network = local_response_normalization(network)
	network = conv_2d(network, 256, 5, activation='relu')
	network = max_pool_2d(network, 3, strides=2)
	network = local_response_normalization(network)
	network = conv_2d(network, 384, 3, activation='relu')
	network = conv_2d(network, 384, 3, activation='relu')
	network = conv_2d(network, 256, 3, activation='relu')
	network = max_pool_2d(network, 3, strides=2)
	network = local_response_normalization(network)
	network = fully_connected(network, 4096, activation='tanh')
	network = dropout(network, 0.5)
	network = fully_connected(network, 4096, activation='tanh')
	network = dropout(network, 0.5)
	network = fully_connected(network, 17, activation='softmax')
	network = regression(network, optimizer='momentum',
						 loss='categorical_crossentropy',
						 learning_rate=lr, name='targets')

	# Training
	model = tflearn.DNN(network, checkpoint_path='model_alexnet',
						max_checkpoints=1, tensorboard_verbose=2, tensorboard_dir='log')
	return model
	