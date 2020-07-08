#!/usr/bin/env python 

import os

from logger import LogLevel
import utils
THIS_FILE_NAME=os.path.basename(__file__)

SUPPORTED_MODULES=["bio", "dl"]

class JSONParser():
	__modules=None
	__bio_tools=None
	__dl_tools=None
	__cl_tools=None

	def __check_tools_for(self,args=None,values=None,evaluating=None,values_example=None):
		assert args is not None, "Missed the args at %s.__check_tools_for(self,args=None,values=None,evaluating=None,values_example=None)" % THIS_FILE_NAME
		assert values is not None, "Missed argument values in %s.__check_tools_for(self,args=None,values=None,evaluating=None,values_example=None)" % THIS_FILE_NAME
		assert evaluating is not None, "Missed argument evaluating in %s.__check_tools_for(self,args=None,values=None,evaluating=None,values_example=None)" % THIS_FILE_NAME
		assert values_example is not None, "Missed argument values_example in %s.__check_tools_for(self,args=None,values=None,evaluating=None,values_example=None)" % THIS_FILE_NAME

		import re
		import constants
		res=re.match(constants.RE_STRING_LISTS, values)
		assert res is not None, "Malformed expression for %s value in %s. Valid expressions (i.e. string list/array) are: %s, e.g.: %s" % (evaluating,args.config_file,constants.RE_STRING_LISTS,values_example)

		r=values.replace('[','').replace(']','').replace('\'','').split(',')
		return r

	def __check_bio_tools(self,args=None,cf=None):
		utils.check_args_n_cf(\
			args,cf,THIS_FILE_NAME,"__check_bio_tools(self,args=None,cf=None)")
		# assert "classes" in cf, "Missed the classes values in %s" % args.config_file

		values_example=\
			"['clustalo'], ['clustalo','muscle'], ['tool1.2','a new tool','Even tools like this 3.12-1_1']"

		return self.__check_tools_for(\
			args,cf["modules"]["bio"]["tools"],\
			"modules->bio->tools",\
			values_example)

		# import re
		# import constants
		# res=re.match(constants.RE_STRING_LISTS, cf["modules"]["bio"]["tools"])
		# assert res is not None, "Malformed expression for modules->bio->tools value in %s. Valid expressions (i.e. string list/array) are: %s, e.g.: ['clustalo'], ['clustalo','muscle'], ['tool1.2','a new tool','Even tools like this 3.12-1_1']

		# t=cf["modules"]["bio"]["tools"].replace('[','').replace(']','').split(',')
		# return t

	def __check_dl_tools(self,args=None,cf=None):
		utils.check_args_n_cf(\
			args,cf,THIS_FILE_NAME,"__check_dl_tools(self,args=None,cf=None)")

		values_example=\
			"['scikit'], ['scikit','keras'], ['tool1.2','a new tool','Even tools like this 3.12-1_1']"

		return self.__check_tools_for(\
			args,cf["modules"]["dl"]["tools"],\
			"modules->dl->tools",\
			values_example)

	def __check_cl_tools(self,args=None,cf=None):
		utils.check_args_n_cf(\
			args,cf,THIS_FILE_NAME,"__check_cl_tools(self,args=None,cf=None)")

		values_example=\
			"['scikit'], ['scikit','keras'], ['tool1.2','a new tool','Even tools like this 3.12-1_1']"

		return self.__check_tools_for(\
			args,cf["modules"]["cl"]["tools"],\
			"modules->cl->tools",\
			values_example)

	def __init__(self,args=None,**kwargs):
		assert args is not None, "Missed the args at %s.%s.__init__(args=None)" % (THIS_FILE_NAME,self.__class__)
		assert args.config_file is not None, "Please specify the configuration file"

		from json import load

		cfg=None
		with open(args.config_file, 'r') as f:
			cfg=load(f)

		assert cfg is not None, "Missed the configuration file at %s.%s.__init__(args=None)" % (THIS_FILE_NAME,self.__class__)

		super().__init__()

		assert "modules" in cfg, "Missed modules value in %s" % args.config_file

		modules=[]
		for key in cfg["modules"]:
			if key.upper()!="BIO" and key.upper()!="DL" and key.upper()!="CL":
				raise Exception("Wrong module '%s' in %s" % (key,args.config_file))
			modules.append(key)

		self.__modules=modules
		# has_bio_or_dl_tools="bio" in cfg["modules"] or "dl" in cfg["modules"]
		# assert has_bio_or_dl_tools, "Configuration file %s does not have bio or dl value" % args.config_file
		has_valid_tools="bio" in cfg["modules"] or "dl" in cfg["modules"] or "cl" in cfg["modules"]
		assert has_valid_tools, "Configuration file %s does not have bio, dl or cl value" % args.config_file

		# assert "bio" in cfg["modules"], "Missed modules->bio value in %s" % args.config_file
		if "bio" in cfg["modules"]:
			assert "tools" in cfg["modules"]["bio"], "Missed modules->bio->tools value in %s" % args.config_file
			self.__bio_tools=self.__check_bio_tools(args,cfg)

		# assert "dl" in cfg["modules"], "Missed modules->dl value in %s" % args.config_file
		if "dl" in cfg["modules"]:
			assert "tools" in cfg["modules"]["dl"], "Missed modules->dl->tools value in %s" % args.config_file
			self.__dl_tools=self.__check_dl_tools(args,cfg)

		if "cl" in cfg["modules"]:
			assert "tools" in cfg["modules"]["cl"], "Missed modules->cl->tools value in %s" % args.config_file
			self.__cl_tools=self.__check_cl_tools(args,cfg)

	@property
	def modules(self):
		return self.__modules

	@property
	def bio_tools(self):
		return self.__bio_tools

	@property
	def dl_tools(self):
		return self.__dl_tools

	@property
	def cl_tools(self):
		return self.__cl_tools