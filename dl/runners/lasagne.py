#!/usr/bin/env python 

import os
import numpy as np

from . import AbstractRunner
THIS_FILE_NAME=os.path.basename(__file__)

class Lasagne(AbstractRunner):
	_nn=None

	# def _load_data(self):
	# 	super()._load_data()

	# def _clean_data(self):
	# 	super()._clean_data()

	# def _split_data(self):
	# 	super()._split_data()
	
	def train(self,**kwargs):
		x=self._df_training.loc[:,self._df_training.columns!="label"].to_numpy()
		t=self._df_training.loc[:,self._df_training.columns=="label"].transpose()
		y=np.empty(self._df_training.shape[0], dtype=np.float32)
		y[:]=t.values

		"""
		Multilayer perceptron model, with one hidden layer.
		input layer : 4 neuron, represents the features number
		hidden layer : 10 neuron, activation using ReLU
		output layer : 3 neuron, represents the classes number, Softmax Layer

		optimizer = stochastic gradient descent with no batch-size
		loss function = categorical cross entropy
		learning rate = 0.01
		epoch = 500
		"""
		import theano
		import theano.tensor as T
		# import numpy as np
		import lasagne

		#initiate theano variable
		input_val = T.fmatrix("inputs")
		target_val = T.ivector("targets")

		#build model
		input_layer  = lasagne.layers.InputLayer(shape=x.shape, input_var=input_val)
		hidden_layer = lasagne.layers.DenseLayer(input_layer, num_units=10,nonlinearity=lasagne.nonlinearities.rectify)   
		output_layer = lasagne.layers.DenseLayer(hidden_layer, num_units=3,nonlinearity=lasagne.nonlinearities.softmax)   
		output_val =  output_layer.get_output()

		#choose objective/loss function 
		objective = \
			lasagne.objectives.Objective(\
				output_layer,
				loss_function=lasagne.objectives.categorical_crossentropy)                
		loss = objective.get_loss(target=target_val)

		#choose optimizer
		all_params = lasagne.layers.get_all_params(output_layer)
		updates = lasagne.updates.sgd(loss, all_params, learning_rate=0.01)

		#compile theano function
		train_model = theano.function([input_val,target_val],loss,allow_input_downcast=True,updates=updates)
		test_model = theano.function([input_val],output_val,allow_input_downcast=True)

		#train
		for _ in range(500):   
			loss_val = train_model(x,y)
			prediction = np.argmax(test_model(x),axis=1)
			accuration = 100*np.mean(y == prediction)
			print("Epoch " + str(_+1) + "/" + str(500) + " - loss: " + str(loss_val) + " - accuration: " + str(accuration))

		self._nn=test_model

	def test(self,**kwargs):
		x=self._df_testing.loc[:,self._df_training.columns!="label"].to_numpy()
		t=self._df_testing.loc[:,self._df_testing.columns=="label"].transpose()
		y=np.empty(self._df_testing.shape[0], dtype=np.float32)
		y[:]=t.values

		#get prediction
		prediction = np.argmax(self._nn(x),axis=1)

		#get accuration
		accuration = 100*np.mean(y == prediction)

		test_accuracy = ("{0:." + str(self._cf_tool.precision_test_accuracy) + "f}").format(accuration)

		print("Test accuracy: %s%" % test_accuracy)
		print("Prediction: ")
		# print(classes)
		print("Target: ")
		# print(np.asarray(y,dtype="int32"))
		print(np.asarray(y))

	def run(self,**kwargs):
		predict=kwargs.pop("predict",None)
		assert predict is not None, "Missed the data to predict at %s.run(self,**kwargs)" % THIS_FILE_NAME		
		super().run(**kwargs)

		import pandas as pd
		data=pd.read_csv(predict)
		print("Prediction: ")
		prediction = np.argmax(self._nn(x),axis=1)
		print(self._nn.predict(data))

		# import numpy as np
