from abc import ABC, abstractmethod

import pandas as pd
import os

import parsers
THIS_FILE_NAME=os.path.basename(__file__)

class AbstractRunner(ABC):
	_cf=None
	# _data=None

	def __init__(self, cf=None, **kwargs):
		assert cf is not None, "Missed the cf argument at AbstractRunner.__init__(self,cf=None,**kwargs)"
		super().__init__()
		self._cf=cf

	@abstractmethod
	def run(self):
		raise NotImplementedError

	# class Meta:
	# 	abstract=True