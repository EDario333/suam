from abc import ABC, abstractmethod

import os
# from datetime import datetime

THIS_FILE_NAME=os.path.basename(__file__)

class AbstractRunner(ABC):
	_cf=None
	_cf_tool=None
	_cmd=None
	_verbose=False

	def __init__(self, cf=None, **kwargs):
		assert cf is not None, "Missed the cf argument at AbstractRunner.__init__(self,cf=None,**kwargs)"
		super().__init__()
		self._cf=cf

	def run(self,**kwargs):
		tool=kwargs.pop("tool",None)
		self.__parse_config_file(tool)

		import subprocess
		import sys

		# child=subprocess.Popen(\
		# 	str(cmd),\
		# 	stdout=subprocess.PIPE,\
		# 	stderr=subprocess.PIPE,\
		# 	universal_newlines=True,\
		# 	shell=(sys.platform!="win32"))

		# if verbose:
		# 	stdout=child.stdout.read()
		# 	if (len(stdout)>0):
		# 		print("\nStandard out is: %s\n" % stdout)
		# 	else:
		# 		print("\nStandard out is empty!\n")

		# 	stderr=child.stderr.read()
		# 	if (len(stderr)>0):
		# 		print("Standard error is: %s" % stderr)
		# 	else:
		# 		print("Standard error is empty")

		child=subprocess.Popen(\
			self._cmd,\
			stdout=sys.stdout,\
			stderr=sys.stderr,\
			universal_newlines=True,\
			shell=(sys.platform!="win32"))
		child.wait()

	def __parse_config_file(self,tool=None):
		assert tool is not None, "Missed the tool argument in %s.__parse_config_file(self,tool=None)" % THIS_FILE_NAME
		from json import load

		cfg=None
		dir_path = os.path.dirname(os.path.realpath(__file__))
		with open("%s/%s.json" % (dir_path,tool), 'r') as f:
			cfg=load(f)

		assert "bin-path" in cfg, "Missed the bin-path value in %s.json" % tool
		self._cf_tool=cfg
		self._cmd=self._cf_tool.pop(r"bin-path",None)

		for key,value in self._cf_tool.items():
			if key=="--verbose" or key=='-v':
				self._cmd+=" --verbose"
				self._verbose=True
			else:
				self._cmd+=r" %s %s" % (key,value)
		
		if self._verbose:
			print("Executing: %s\n" % self._cmd)

	# class Meta:
	# 	abstract=True

class BioRunner(AbstractRunner):
	def run(self,**kwargs):
		if self._cf.bio_tools is not None:
			from datetime import datetime
			started=datetime.now()

			print("Starting at: %s" % started.strftime("%Y-%m-%d %H:%M:%S"))

			if "clustalo" in self._cf.bio_tools:
				from . import clustalo
				clustalo.ClustaloRunner(self._cf).run(tool="clustalo")

			if "muscle" in self._cf.bio_tools:
				from . import muscle
				muscle.MuscleRunner(self._cf).run(tool="muscle")

			finished=datetime.now()
			print("Finished at: %s" % finished.strftime("%Y-%m-%d %H:%M:%S"))
			print("Total elapsed time: %s" % str(finished-started))