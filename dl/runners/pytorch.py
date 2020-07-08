#!/usr/bin/env python 

import torch
from torch.autograd import Variable

import os
import numpy as np

from . import AbstractRunner
THIS_FILE_NAME=os.path.basename(__file__)

class Pytorch(AbstractRunner):
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
		# import torch
		import torch.nn as nn
		import torch.nn.functional as F
		# from torch.autograd import Variable
		torch.manual_seed(1234)

		# Hyperparameters
		hl = 10
		lr = 0.01
		num_epoch = 500

		# Build model
		class Net(nn.Module):
			def __init__(self):
				super(Net, self).__init__()
				self.fc1 = nn.Linear(4, hl)
				self.fc2 = nn.Linear(hl, 3)

			def forward(self, x):
				x = F.relu(self.fc1(x))
				x = self.fc2(x)
				return x

		net = Net()

		# Choose optimizer and loss function
		criterion = nn.CrossEntropyLoss()
		optimizer = torch.optim.SGD(net.parameters(), lr=lr)

		# Train
		for epoch in range(num_epoch):
			X = Variable(torch.Tensor(x).float())
			Y = Variable(torch.Tensor(y).long())

			# Feedforward - backprop
			optimizer.zero_grad()
			out = net(X)
			loss = criterion(out, Y)
			loss.backward()
			optimizer.step()

			if (epoch) % 50 == 0:
				val=loss.data.item()
				# print ('Epoch [%d/%d] Loss: %.4f' 
				#            %(epoch+1, num_epoch, loss.data[0]))
				print("Epoch [%d/%d] Loss: %.4f" % (epoch+1, num_epoch, val))

		self._nn=net

	def test(self,**kwargs):
		# x=self._df_testing.loc[:,self._df_training.columns!="label"].to_numpy()
		x=self._df_testing.loc[:,self._df_testing.columns!="label"].to_numpy()
		t=self._df_testing.loc[:,self._df_testing.columns=="label"].transpose()
		y=np.empty(self._df_testing.shape[0], dtype=np.float32)
		y[:]=t.values

		# Get prediction
		X = Variable(torch.Tensor(x).float())
		Y = torch.Tensor(y).long()
		# out = net(X)
		out = self._nn(X)
		_, predicted = torch.max(out.data, 1)

		# Get accuration
		# print('Accuracy of the network %d %%' % (100 * torch.sum(Y==predicted) / 30))
		result=100 * torch.sum(Y==predicted)
		result=np.array(result)
		# result=np.true_divide(result,30)
		result=np.true_divide(result,len(y))

		test_accuracy = ("{0:." + str(self._cf_tool.precision_test_accuracy) + "f}").format(result)
		print("Accuracy of the network: {}%".format(test_accuracy))
		# print('Accuracy of the network %d%%' % result)

		print("Predicted: ")
		print(predicted)

		print("Expected: ")
		print(Y)

	def run(self,**kwargs):
		predict=kwargs.pop("predict",None)
		assert predict is not None, "Missed the data to predict at %s.run(self,**kwargs)" % THIS_FILE_NAME		
		super().run(**kwargs)

		import pandas as pd
		data=pd.read_csv(predict)

		# print("data")
		# print(data)
		# quit()
		x=data.loc[:,data.columns!="label"].to_numpy()
		# t=data.loc[:,data.columns=="label"].transpose()
		# y=np.empty(data.shape[0], dtype=np.float32)
		# y[:]=t.values

		# Get prediction
		X = Variable(torch.Tensor(x).float())
		# Y = torch.Tensor(y).long()
		# out = net(X)
		out = self._nn(X)
		# _, predicted = torch.max(out.data, 1)
		_, predicted = torch.max(out.data, 1)

		print("Prediction: ")
		print(predicted)