#!/usr/bin/env python 

import os
import numpy as np

from . import AbstractRunner
THIS_FILE_NAME=os.path.basename(__file__)
# AVAILABLE_LOSS_FUNCTIONS=["sparse_categorical_crossentropy","categorical_crossentropy"]

class Keras(AbstractRunner):
	_nn=None

	# def _load_data(self):
	# 	super()._load_data()

	# def _clean_data(self):
	# 	super()._clean_data()

	# def _split_data(self):
	# 	super()._split_data()
	
	# def train_from_example(self,**kwargs):
	# 	x=self._df_training.loc[:,self._df_training.columns!="label"].to_numpy()
	# 	t=self._df_training.loc[:,self._df_training.columns=="label"].transpose()
	# 	y=np.empty(self._df_training.shape[0], dtype=np.float32)
	# 	y[:]=t.values

	# 	"""
	# 	Multilayer perceptron model
	# 	"""
	# 	from keras.models import Sequential
	# 	from keras.layers import Dense, Activation
	# 	from keras.utils import np_utils

	# 	# Change target format
	# 	y=np_utils.to_categorical(y)

	# 	# import tensorflow as tf
	# 	# y = tf.keras.utils.to_categorical(y)

	# 	# Build model
	# 	self._nn=Sequential()
	# 	self._nn.add(Dense(output_dim=10, input_dim=4))
	# 	self._nn.add(Activation("relu"))
	# 	# self._nn.add(Dense(output_dim=3))
	# 	self._nn.add(Dense(units=3))
	# 	self._nn.add(Activation("softmax"))

	# 	# Choose optimizer and loss function
	# 	self._nn.compile(loss='categorical_crossentropy', optimizer='sgd', metrics=['accuracy'])

	# 	# Train
	# 	self._nn.fit(x, y, epochs=500, batch_size=120)
	# 	quit()

	def train(self,**kwargs):
		x=self._df_training.loc[:,self._df_training.columns!="label"].to_numpy()
		t=self._df_training.loc[:,self._df_training.columns=="label"].transpose()
		y=np.empty(self._df_training.shape[0], dtype=np.float32)
		y[:]=t.values

		"""
		Multilayer perceptron model
		"""
		from keras.models import Sequential
		from keras.layers import Dense, Activation

		# Build model
		self._nn=Sequential()
		# self._nn.add(Dense(output_dim=10, input_dim=4))
		# self._nn.add(Activation("relu"))
		# self._nn.add(Dense(units=3))
		# self._nn.add(Activation("softmax"))

		nl=len(self._cf_tool.nn["hl"]["nn"])
		for i in range(nl):
			self._nn.add(Dense(input_dim=self._cf_tool.nn["in"],units=self._cf_tool.nn["hl"]["nn"][i]))

		self._nn.add(Activation(self._cf_tool.nn["hl"]["af"]))

		self._nn.add(Dense(units=self._cf_tool.nn["ol"]["nn"]))
		self._nn.add(Activation(self._cf_tool.nn["ol"]["af"]))

		# Choose optimizer and loss function
		# self._nn.compile(loss="sparse_categorical_crossentropy", optimizer=self._cf_tool.nn["op"], metrics=["accuracy"])
		self._nn.compile(loss=self._cf_tool.nn["lf"], optimizer=self._cf_tool.nn["op"], metrics=["accuracy"])

		# Train
		self._nn.fit(x, y, epochs=self._cf_tool.nn["en"], batch_size=120)
	
	def test(self,**kwargs):
		x=self._df_testing.loc[:,self._df_training.columns!="label"].to_numpy()
		t=self._df_testing.loc[:,self._df_testing.columns=="label"].transpose()
		y=np.empty(self._df_testing.shape[0], dtype=np.float32)
		y[:]=t.values

		classes = self._nn.predict_classes(x, batch_size=120)
		# print(classes)
		# quit()

		# Get accuration
		# accuration = np.sum(classes == y)/30.0 * 100
		# accuration = np.sum(classes == y)/len(y)*100
		accuration = (np.sum(classes == y)/len(y))*100

		# print("Test Accuration: " + str(accuration) + '%')
		# print("Test Accuration: " + str(accuration))
		test_accuracy = ("{0:." + str(self._cf_tool.precision_test_accuracy) + "f}").format(accuration)
		print("Test accuracy: {}%".format(test_accuracy))

		print("Test prediction: ")
		print(classes)
		print("Target: ")
		print(np.asarray(y,dtype="int32"))

	# def predict(self,**kwargs):
	# 	print("ALGO 3")

		# from sklearn.model_selection import train_test_split
		# x_train, x_test, y_train, y_test = train_test_split(\
		# 	self._data[:,:4],\
		# 	self._data[:,4],\
		# 	test_size=0.2)

		# print("algo")

	def run(self,**kwargs):
		predict=kwargs.pop("predict",None)
		assert predict is not None, "Missed the data to predict at %s.run(self,**kwargs)" % THIS_FILE_NAME		
		super().run(**kwargs)

		import pandas as pd
		data=pd.read_csv(predict)

		classes = self._nn.predict_classes(data, batch_size=120)
		print("Prediction: ")
		print(classes)