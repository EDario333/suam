#!/usr/bin/env python 

import os

from logger import LogLevel
# import utils
THIS_FILE_NAME=os.path.basename(__file__)

SUPPORTED_TOOLS=["scikit", "keras", "tensorflow", "pytorch"]

class JSONParser():
	__ds=None
	__ni=None
	__cl=None
	__pl=None

	# __cc=None
	# __colors=None
	# __marker='o'

	# __classes_codes=None
	# __save_results=0
	# __results_dir=None
	# __test_set_target_accuracy=0.95
	# __starting_percent_training=0.75
	# __step_percent_training=0.01
	# __starting_percent_features=0.75
	# __step_percent_features=0.10
	# __starting_percent_test=0.10
	# __starting_percent_prediction=0.10
	# __precision_test_accuracy=2
	# __number_successful_tests=10
	# __tools=None
	__log_level=LogLevel.ALL
	__log_file=None

	def __init__(self,tool=None,**kwargs):
		assert tool is not None, "Missed the tool argument at %s.%s.__init__(tool=None)" % (THIS_FILE_NAME,self.__class__)
		# assert args.config_file is not None, "Please specify the configuration file"

		from json import load

		cfg=None
		dir_path = os.path.dirname(os.path.realpath(__file__))
		cf="%s/../runners/%s.json" % (dir_path, tool)
		with open(cf, 'r') as f:
			cfg=load(f)

		assert cfg is not None, "Missed the configuration file at %s.%s.__init__(args=None)" % (THIS_FILE_NAME,self.__class__)

		super().__init__()

		assert "datasource" in cfg, "Missed datasource value in %s.json" % cf
		self.__ds=cfg["datasource"]

		assert "times" in cfg, "Missed times value in %s.json" % cf

		try:
			self.__ni=int(cfg["times"])
		except ValueError:
			raise Exception("Wrong value for times in %s.json" % cf)

		assert "clusters" in cfg, "Missed clusters values in %s" % cf
		try:
			self.__cl=list(cfg["clusters"])
		except ValueError:
			raise Exception("Wrong value for clusters in %s.json" % cf)

		x=1
		for cluster in self.__cl:
			assert "name" in cluster,"Missed the name for cluster #%i in %s.json"%(x,cf)
			assert "center" in cluster,"Missed the center for cluster #%i in %s.json"%(x,cf)
			assert "color" in cluster,"Missed the color for cluster #%i in %s.json"%(x,cf)
			x+=1

		assert "plot" in cfg, "Missed the plot config in %s"%cf

		assert "title" in cfg["plot"],"Missed the title value for the plot config in %s"%cf

		assert 'x' in cfg["plot"],"Missed the 'x' axis config for the plot value in %s"%cf
		assert "label" in cfg["plot"]['x'],"Missed the 'x' axis label for plot value in %s"%cf

		assert 'y' in cfg["plot"],"Missed the 'y' axis config for the plot value in %s"%cf
		assert "label" in cfg["plot"]['y'],"Missed the 'y' axis label for plot value in %s"%cf
		
		assert "marker" in cfg["plot"],"Missed the marker value for the plot config in %s"%cf

		self.__pl=cfg["plot"]

		if "log-level" in cfg:
			log_level=cfg["log-level"].upper()
			if log_level=="NONE":
				self.__log_level=LogLevel.NONE
			elif log_level=="INFO":
				self.__log_level=LogLevel.INFO
			elif log_level=="WARNING":
				self.__log_level=LogLevel.WARNING
			elif log_level=="ERROR":
				self.__log_level=LogLevel.ERROR
			elif log_level=="ALL":
				self.__log_level=LogLevel.ALL

		if "log-file" in cfg:
			try:
				f = open(cfg["log-file"], 'w')
				f.close()
			except IOError as e:
				raise Exception(e.args[0])

			self.__log_file=cfg["log-file"]

	@property
	def datasource(self):
		return self.__ds

	@property
	def times(self):
		return self.__ni

	@property
	def clusters(self):
		return self.__cl

	@property
	def plot(self):
		return self.__pl

	# @property
	# def number_of_classes(self):
	# 	return self.__nc

	# @property
	# def colors(self):
	# 	return self.__colors

	# @property
	# def marker(self):
	# 	return self.__marker

	@property
	def log_level(self):
		return self.__log_level

	@property
	def log_file(self):
		return self.__log_file