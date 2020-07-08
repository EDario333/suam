#!/usr/bin/env python 

import os

# from . import LogLevel
from logger import LogLevel
import utils
THIS_FILE_NAME=os.path.basename(__file__)

SUPPORTED_TOOLS=["scikit", "keras", "tensorflow", "pytorch"]
# solvers aka optimizers??
AVAILABLE_OPTIMIZERS=["sgd","adam","lbfgs"]
AVAILABLE_LOSS_FUNCTIONS=["categorical cross entropy","cross entropy","sparse_categorical_crossentropy","categorical_crossentropy"]
AVAILABLE_ACTIVATION_FUNCTIONS=["relu","softmax"]

class JSONParser():
	__ds=None
	__label=None
	__classes=None
	__classes_codes=None
	__save_results=0
	__results_dir=None
	__test_set_target_accuracy=0.95
	__starting_percent_training=0.75
	__step_percent_training=0.01
	__starting_percent_features=0.75
	__step_percent_features=0.10
	__starting_percent_test=0.10
	__starting_percent_prediction=0.10
	__precision_test_accuracy=2
	__number_successful_tests=10
	__tools=None
	__log_level=LogLevel.ALL
	__log_file=None
	# in=input neurons
	# hn=hidden neurons
	# on=output neurons
	# op=optimizer
	# lf=loss function
	# lr=learning rate
	# ep=epoch
	__nn={"in": None,"hl":{"nn":None,"af":None},"ol":{"nn":None,"af":None},"op":None,"lf":None,"lr":None,"ep":None}

	# TO-DO: Please remove, be sure that does not need it anymore
	def __has_tool(self,cfg=None):
		# assert args is not None, "Missed the args at %s.__has_tool(args=None,cfg=None)" % THIS_FILE_NAME
		assert cfg is not None, "Missed the configuration file at %s.__has_tool(args=None,cfg=None)" % THIS_FILE_NAME

		# assert "tools" in cf, "Missed the tools in %s" % args.config_file

		# from adan import SUPPORTED_TOOLS

		tools=[ SUPPORTED_TOOLS[x] for x in range(len(SUPPORTED_TOOLS)-1) if SUPPORTED_TOOLS[x] in cfg["tools"] ]
		assert len(tools)>0, "Please specify at least one tool: %s" % SUPPORTED_TOOLS

		return tools

	def __check_classes(self,cf=None):
		# utils.check_args_n_cf(args,cf,THIS_FILE_NAME,"__check_classes(cf=None)")
		assert cf is not None, "Missed the cf argument at %s.%s__check_classes(self,cf=None)" % (THIS_FILE_NAME,self.__class__)
		# assert "classes" in cf, "Missed the classes value in %s" % args.config_file
		assert "classes" in cf, "Missed the classes value in %s" % cf

		if "classes" in cf:
			# from parsers.json import JSONParser
			import re
			import constants
			res=re.match(constants.RE_STRING_LISTS, cf["classes"])
			assert res is not None, "Malformed expression for classes in %s. Valid expressions (i.e. string list/array) are: %s, e.g.: ['Class 1'], ['Class1','Class 2'], ['Class 1.2','Class 2 with something','Even class with chars like _ or -'] and so on" % (args.config_file,constants.RE_STRING_LISTS)

			import numpy as np

			c=cf["classes"].replace('[','').replace(']','').split(',')
			cc=None

			if "classes-codes" in cf:
				res=re.match(constants.RE_NUMBER_LISTS, cf["classes-codes"])
				assert res is not None, "Malformed expression for classes-codes in %s. Valid expressions (i.e. list or array notation) are: %s, e.g.: [0], [0,1], [0.23,23.27,8] and so on" % (args.config_file,constants.RE_NUMBER_LISTS)

				cc=cf["classes-codes"].replace('[','').replace(']','').split(',')
				cc=np.array(cc,dtype=np.float64)
				assert len(c)==len(cc), "The classes codes length does not match with the classes length"
				# lst=[np.float64(itm) for itm in cc]
			
			return c,cc

		return None,None

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

		assert "label" in cfg, "Missed label value in %s" % cf
		self.__label=cfg["label"]

		assert "nn" in cfg, "Missed the network config (nn) in %s"%cf
		assert "in" in cfg["nn"], "Missed the input neurons (in) in neural network (nn) config at %s"%cf

		assert "hl" in cfg["nn"], "Missed the neural network (nn) hidden layer (hl) in config at %s"%cf
		assert "nn" in cfg["nn"]["hl"], "Missed the neurons number (nn) for the hidden layer in neural network (nn) config at %s"%cf
		assert "af" in cfg["nn"]["hl"], "Missed the activation function (af) for the hidden layer in neural network (nn) config at %s"%cf

		assert "ol" in cfg["nn"], "Missed the neural network (nn) output layer (ol) in config at %s"%cf
		assert "nn" in cfg["nn"]["ol"], "Missed the neurons number (nn) for the output layer in neural network (nn) config at %s"%cf
		assert "af" in cfg["nn"]["ol"], "Missed the activation function (af) for the output layer in neural network (nn) config at %s"%cf

		assert "op" in cfg["nn"], "Missed the optimizer (op) in neural network (nn) config at %s"%cf
		assert "lf" in cfg["nn"], "Missed the loss function (lf) in neural network (nn) config at %s"%cf
		assert "lr" in cfg["nn"], "Missed the learning rate (lr) in neural network (nn) config at %s"%cf
		assert "en" in cfg["nn"], "Missed the epoch number (en) in neural network (nn) config at %s"%cf

		try:
			self.__nn["in"]=int(cfg["nn"]["in"])
		except ValueError:
			raise Exception("Wrong value for input neurons (in) in neural network (nn) config at %s" % cf)

		try:
			self.__nn["hl"]["nn"]=list(cfg["nn"]["hl"]["nn"])
		except ValueError:
			raise Exception("Wrong value for hidden neurons (hn) in neural network (nn) config at %s" % cf)
		except TypeError:
			raise Exception("Wrong value for hidden neurons (hn) in neural network (nn) config at %s" % cf)

		assert cfg["nn"]["hl"]["af"] in AVAILABLE_ACTIVATION_FUNCTIONS,"Wrong value for neural network input layer activation function at %s. Valid values are %s"%(cf,AVAILABLE_ACTIVATION_FUNCTIONS)

		self.__nn["hl"]["af"]=cfg["nn"]["hl"]["af"]

		try:
			self.__nn["ol"]["nn"]=int(cfg["nn"]["ol"]["nn"])
		except ValueError:
			raise Exception("Wrong value for output neurons (on) in neural network (nn) config at %s" % cf)

		assert cfg["nn"]["ol"]["af"] in AVAILABLE_ACTIVATION_FUNCTIONS,"Wrong value for neural network output layer activation function at %s. Valid values are %s"%(cf,AVAILABLE_ACTIVATION_FUNCTIONS)

		self.__nn["ol"]["af"]=cfg["nn"]["ol"]["af"]

		assert cfg["nn"]["op"] in AVAILABLE_OPTIMIZERS,"Wrong value for optimizer (op) in neural network (nn) config at %s. Valid values are %s"%(cf, AVAILABLE_OPTIMIZERS)
		self.__nn["op"]=cfg["nn"]["op"]

		assert cfg["nn"]["lf"] in AVAILABLE_LOSS_FUNCTIONS,"Wrong value for loss function (lf) in neural network (nn) config at %s. Valid values are %s"%(cf, AVAILABLE_LOSS_FUNCTIONS)
		self.__nn["lf"]=cfg["nn"]["lf"]

		try:
			self.__nn["lr"]=float(cfg["nn"]["lr"])
		except ValueError:
			raise Exception("Wrong value for learning rate (lr) in neural network (nn) config at %s" % cf)

		try:
			self.__nn["en"]=int(cfg["nn"]["en"])
		except ValueError:
			raise Exception("Wrong value for epoch number (en) in neural network (nn) config at %s" % cf)

		# self.__tools=self.__has_tool(cfg)
		self.__classes, self.__classes_codes=self.__check_classes(cfg)

		if "save-results" in cfg:
			assert "results-dir" in cfg,"Missed results-dir value in %s" % args.config_file
			self.__save_results=True
			self.__results_dir=cfg["results-dir"]

		if "test-set-target-accuracy" in cfg:
			try:
				self.__test_set_target_accuracy=float(cfg["test-set-target-accuracy"])
			except ValueError:
				raise Exception("Wrong value for test-set-target-accuracy in %s" % args.config_file)

		if "starting-percent-training" in cfg:
			try:
				self.__starting_percent_training=float(cfg["starting-percent-training"])
			except ValueError:
				raise Exception("Wrong value for starting-percent-training in %s" % args.config_file)

		if "step-percent-training" in cfg:
			try:
				self.__step_percent_training=float(cfg["step-percent-training"])
			except ValueError:
				raise Exception("Wrong value for step-percent-training in %s" % args.config_file)

		if "starting-percent-features" in cfg:
			try:
				self.__starting_percent_features=float(cfg["starting-percent-features"])
			except ValueError:
				raise Exception("Wrong value for starting-percent-features in %s" % args.config_file)

		if "step-percent-features" in cfg:
			try:
				self.__step_percent_features=float(cfg["step-percent-features"])
			except ValueError:
				raise Exception("Wrong value for step-percent-features in %s" % args.config_file)

		if "starting-percent-test" in cfg:
			try:
				self.__starting_percent_test=float(cfg["starting-percent-test"])
			except ValueError:
				raise Exception("Wrong value for starting-percent-test in %s" % args.config_file)

		if "starting-percent-prediction" in cfg:
			try:
				self.__starting_percent_prediction=float(cfg["starting-percent-prediction"])
			except ValueError:
				raise Exception("Wrong value for starting-percent-prediction in %s" % args.config_file)

		if "precision-test-accuracy" in cfg:
			try:
				pta=int(cfg["precision-test-accuracy"])
				self.__precision_test_accuracy=utils.unsigned(pta)
			except ValueError:
				raise Exception("Wrong value for precision-test-accuracy in %s" % args.config_file)

		if "number-successful-tests" in cfg:
			try:
				nst=int(cfg["number-successful-tests"])
				self.__number_successful_tests=utils.unsigned(nst)
			except ValueError:
				raise Exception("Wrong value for number-successful-tests in %s" % args.config_file)

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
	def label(self):
		return self.__label

	@property
	def classes(self):
		return self.__classes

	@property
	def classes_codes(self):
		return self.__classes_codes

	@property
	def save_results(self):
		return self.__save_results

	@property
	def results_dir(self):
		return self.__results_dir

	@property
	def test_set_target_accuracy(self):
		return self.__test_set_target_accuracy

	@property
	def starting_percent_training(self):
	  return self.__starting_percent_training

	@property
	def step_percent_training(self):
	  return self.__step_percent_training

	@property
	def starting_percent_features(self):
	  return self.__starting_percent_features

	@property
	def step_percent_features(self):
	  return self.__step_percent_features

	@property
	def starting_percent_test(self):
		return self.__starting_percent_test

	@property
	def starting_percent_prediction(self):
		return self.__starting_percent_prediction

	@property
	def precision_test_accuracy(self):
		return self.__precision_test_accuracy

	@property
	def number_successful_tests(self):
		return self.__number_successful_tests

	@property
	def tools(self):
		return self.__tools

	@property
	def nn(self):
		return self.__nn

	@property
	def log_level(self):
		return self.__log_level

	@property
	def log_file(self):
		return self.__log_file