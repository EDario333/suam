#!/usr/bin/env python 

import os
import numpy as np

from . import AbstractRunner
THIS_FILE_NAME=os.path.basename(__file__)

class Scikit(AbstractRunner):
	_nn=None

	def _load_data(self):
		super()._load_data()

	def _clean_data(self):
		super()._clean_data()

	def _split_data(self):
		super()._split_data()
	
	def train(self,**kwargs):
		x=self._df_training.loc[:,self._df_training.columns!="label"].to_numpy()
		t=self._df_training.loc[:,self._df_training.columns=="label"].transpose()
		y=np.empty(self._df_training.shape[0], dtype=np.float32)
		y[:]=t.values

		"""
		Multilayer perceptron model
		"""
		from sklearn.neural_network import MLPClassifier
		# self._nn = MLPClassifier(hidden_layer_sizes=(10),solver='sgd',learning_rate_init=0.01,max_iter=500)

		self._nn = MLPClassifier(hidden_layer_sizes=self._cf_tool.nn["hl"]["nn"],solver=self._cf_tool.nn["op"],learning_rate_init=self._cf_tool.nn["lr"],max_iter=self._cf_tool.nn["en"])
		self._nn.fit(x, y)

	def test(self,**kwargs):
		x=self._df_testing.loc[:,self._df_training.columns!="label"].to_numpy()
		t=self._df_testing.loc[:,self._df_testing.columns=="label"].transpose()
		y=np.empty(self._df_testing.shape[0], dtype=np.float32)
		y[:]=t.values

		test_accuracy = ("{0:." + str(self._cf_tool.precision_test_accuracy) + "f}").format((self._nn.score(x,y)*100))
		print("Test accuracy: {}%".format(test_accuracy))

		classes=self._nn.predict(x)
		print("Test prediction: ")
		print(classes)
		print("Target: ")
		# print(np.asarray(y,dtype="int32"))
		print(np.asarray(y))


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
		print("Prediction: ")
		print(self._nn.predict(data))