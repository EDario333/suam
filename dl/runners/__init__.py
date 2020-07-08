from abc import ABC, abstractmethod

import pandas as pd
import os

import parsers
THIS_FILE_NAME=os.path.basename(__file__)

from .utils import get_file_name_without_extension

class AbstractRunner(ABC):
	_cf=None
	_cf_tool=None
	_data=None
	_df_training=None
	_df_testing=None
	_df_predict=None

	def _choose_random_features(self):
		import random

		df=pd.DataFrame(self._data)
		tsfe = len(df.columns)
		# ssfe = int(tsfe * args.starting_percent_features)
		ssfe = int(tsfe * self._cf_tool.starting_percent_features)

		series = []
		processed = []
		new_df = pd.DataFrame()

		# x = random.randint(0, ssfe-1)
		x = 0

		while len(new_df.columns) < ssfe:
			while x in processed:
				# x = random.randint(0, ssfe-1)
				x += 1
			processed.append(x)
			serie = df[df.columns[x]]
			new_df = pd.concat([new_df, serie], 'columns')
			# x = random.randint(0, ssfe-1)
			x += 1

		#file_name = args.data_set[args.data_set.rfind('/') + 1:]
		#file_name = file_name[0:file_name.find('.')]

		df_randomized = pd.concat([new_df, pd.Series(data=self._data[::,-1],name='label')], 'columns')

		filename = utils.get_file_name_without_extension(self._cf_tool.datasource)
		filename += '-' + str(ssfe) + 'features-all-data.csv'
		# new_df.to_csv(filename, index=False)
		df_randomized.to_csv(filename, index=False)

		# return new_df
		return df_randomized

	def _choose_random_data(self,df=None):
		# assert args is not None, 'The args are missed'
		assert df is not None, 'Please specify the randomized dataframe'

		# df = pd.DataFrame(df_randomized)
		tsda = len(df)

		tsfe = len(df.columns)
		ssfe = int(tsfe * self._cf_tool.starting_percent_features)

		sstr = int(tsda * self._cf_tool.starting_percent_training)
		self._df_training = df.sample(sstr)

		file_name_ = utils.get_file_name_without_extension(self._cf_tool.datasource)
		file_name = file_name_ + '-' + str(ssfe) + 'features-training-data-'
		file_name += str(sstr) + '-rows.csv'
		self._df_training.to_csv(file_name, index=False)

		self._df_testing = df[~df.isin(self._df_training).all(1)]
		file_name = file_name_ + '-' + str(ssfe) + 'features-test-data-'
		file_name += str(tsda-sstr) + '-rows.csv'
		self._df_testing.to_csv(file_name, index=False)

		n_rows_for_prediction = int(tsda * self._cf_tool.starting_percent_prediction) 
		self._df_predict = df.sample(n_rows_for_prediction)
		file_name = file_name_ + '-' + str(ssfe) + 'features-predict-data-'
		file_name += str(n_rows_for_prediction) + '-rows.csv'
		self._df_predict.to_csv(file_name, index=False)

		return self._df_training,self._df_testing,self._df_predict

	def __init__(self, cf=None, **kwargs):
		assert cf is not None, "Missed the cf argument at AbstractRunner.__init__(self,cf=None,**kwargs)"
		super().__init__()
		self._cf=cf

	def _load_data(self):
		self._data=pd.read_csv(self._cf_tool.datasource)

	def _clean_data(self):
		import numpy as np

		if self._cf_tool.classes is not None:
			top=range(len(self._cf_tool.classes))
			for x in top:
				itm=self._cf_tool.classes[x].replace('\'','')
				self._data.loc[self._data[self._cf_tool.label]==itm,self._cf_tool.label]=self._cf_tool.classes_codes[x]

		df = self._data.apply(pd.to_numeric)

		self._data = np.array(df,dtype="float64")

		return self._data
		# raise Exception(self._data)

	# @abstractmethod
	def _split_data(self):
		df=self._choose_random_features()
		self._choose_random_data(df)

	def _log(self,n_test, cf=None, train_x=None, predict_y=None):
		assert cf is not None, "Missed the cf argument at AbstractRunner._log(self,n_test, cf=None, train_x=None, predict_y=None)"
		assert train_x is not None, "Missed the train_x argument at AbstractRunner._log(self,n_test, cf=None, train_x=None, predict_y=None)"
		assert predict_y is not None, "Missed predict_y argument at AbstractRunner._log(self,n_test, cf=None, train_x=None, predict_y=None)"

		if cf.log_file is not None:
			import sys
			__stdout=sys.stdout

			try:
				sys.stdout = open(cf.log_file, 'w')
			except IOError as e:
				# raise Exception(e.args[0])
				raise Exception(e.args)

		from datetime import datetime

		print("[%s: %s]: Test #%i, trying with:\n" % (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), parsers.INFO, n_test))

		# Args from ADAN
		# print("Starting percent training: %f%c (rows = %i)" % (cf.starting_percent_training*100,'%',len(train_x)))
		# print('Step percent training: ' + str(args.step_percent_training) + '\n')
		# print('Starting percent features: ' + str(args.starting_percent_features) + ' (features = ' + str(len(ds_train_x.columns)) + ')')
		# print('Step percent features: ' + str(args.step_percent_features) + '\n')
		# #print('Starting percent test: ' + str(args.starting_percent_test) + '\n')
		# print('Starting percent prediction: ' + str(args.starting_percent_prediction) + ' (rows = ' + str(len(ds_predict_y)) + ')' + '\n')
		# print('Precision test accuracy: ' + str(args.precision_test_accuracy) + ' decimals')
		# print('Number of hidden layers: ' + str(args.hidden_layers_number))
		# print('Number of neurons for each hidden layer: ' + str(args.neurons_per_layer))
		# print('Limit of the train steps: ' + str(args.limit_train_steps))
		# print('Number of times that we require reach the tsta: ' + str(args.number_successful_tests))

		if cf.log_file is not None:
			try:
				sys.stdout.close()
			except IOError as e:
				# raise Exception(e.args[0])
				raise Exception(e.args)

	def _parse_config_file(self,tool=None):
		assert tool is not None, "Missed the tool argument in %s._parse_config_file(self,tool=None)" % THIS_FILE_NAME
		from ..parsers.json import JSONParser
		self._cf_tool=JSONParser(tool)

	@abstractmethod
	def run(self,**kwargs):
		tool=kwargs.pop("tool",None)
		assert tool is not None, "Missed the tool argument in %s.run(self,**kwargs)" % THIS_FILE_NAME

		self._parse_config_file(tool)
		self._load_data()
		self._clean_data()
		self._split_data()
		self.train()
		self.test()
		# self.predict()

	@abstractmethod
	def train(self,**kwargs):
		pass

	@abstractmethod
	def test(self,**kwargs):
		pass

	# @abstractmethod
	# def predict(self,**kwargs):
	# 	pass

	class Meta:
		abstract=True

class DLRunner():
	_cf=None
	# def _split_data(self):
	# 	pass

	def __init__(self, cf=None, **kwargs):
		assert cf is not None, "Missed the cf argument at DLRunner.__init__(self,cf=None,**kwargs)"
		super().__init__()
		self._cf=cf

	def run(self,**kwargs):
		predict=kwargs.pop("predict",None)
		assert predict is not None, "Missed the data to predict at %s.run(self,**kwargs)" % THIS_FILE_NAME

		if self._cf.dl_tools is not None:
			from datetime import datetime
			started=datetime.now()

			print("Starting at: %s" % started.strftime("%Y-%m-%d %H:%M:%S"))

			if "scikit" in self._cf.dl_tools:
				from . import scikit
				scikit.Scikit(self._cf).run(tool="scikit",predict=predict)
				# scikit.Scikit(self._cf).run(tool="scikit")
			elif "keras" in self._cf.dl_tools:
				from . import keras
				keras.Keras(self._cf).run(tool="keras",predict=predict)
			elif "lasagne" in self._cf.dl_tools:
				from . import lasagne
				lasagne.Lasagne(self._cf).run(tool="lasagne",predict=predict)
			elif "pytorch" in self._cf.dl_tools:
				from . import pytorch
				pytorch.Pytorch(self._cf).run(tool="pytorch",predict=predict)

			finished=datetime.now()
			print("Finished at: %s" % finished.strftime("%Y-%m-%d %H:%M:%S"))
			print("Total elapsed time: %s" % str(finished-started))