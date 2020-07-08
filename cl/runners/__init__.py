from abc import ABC, abstractmethod

import pandas as pd
import os

import parsers
THIS_FILE_NAME=os.path.basename(__file__)

class AbstractRunner(ABC):
	_cf=None
	_cf_tool=None
	_data=None

	def __init__(self, cf=None, **kwargs):
		assert cf is not None, "Missed the cf argument at AbstractRunner.__init__(self,cf=None,**kwargs)"
		super().__init__()
		self._cf=cf

	def _load_data(self):
		self._data=pd.read_csv(self._cf_tool.datasource)

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

	class Meta:
		abstract=True

class CLRunner():
	_cf=None

	def __init__(self, cf=None, **kwargs):
		assert cf is not None, "Missed the cf argument at CLRunner.__init__(self,cf=None,**kwargs)"
		super().__init__()
		self._cf=cf

	def run(self,**kwargs):
		# predict=kwargs.pop("predict",None)
		# assert predict is not None, "Missed the data to predict at %s.run(self,**kwargs)" % THIS_FILE_NAME

		if self._cf.cl_tools is not None:
			from datetime import datetime
			started=datetime.now()

			print("Starting at: %s" % started.strftime("%Y-%m-%d %H:%M:%S"))

			if "scikit" in self._cf.cl_tools:
				from . import scikit
				scikit.Scikit(self._cf).run(tool="scikit")
			# elif "keras" in self._cf.dl_tools:
			# 	from . import keras
			# 	keras.Keras(self._cf).run(tool="keras",predict=predict)
			# elif "lasagne" in self._cf.dl_tools:
			# 	from . import lasagne
			# 	lasagne.Lasagne(self._cf).run(tool="lasagne",predict=predict)
			# elif "pytorch" in self._cf.dl_tools:
			# 	from . import pytorch
			# 	pytorch.Pytorch(self._cf).run(tool="pytorch",predict=predict)

			finished=datetime.now()
			print("Finished at: %s" % finished.strftime("%Y-%m-%d %H:%M:%S"))
			print("Total elapsed time: %s" % str(finished-started))

	@property
	def data(self):
		return self._data
