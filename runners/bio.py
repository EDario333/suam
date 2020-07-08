#!/usr/bin/env python 

import os

# from . import AbstractRunner
THIS_FILE_NAME=os.path.basename(__file__)

class BioRunner(AbstractRunner):
	def run(self):
		if "clustalo" in self._cf.bio_tools:
			ClustaloRunner(self._cf).run()

		if "muscle" in self._cf.bio_tools:

class ClustaloRunner(AbstractRunner):
	def run(self):
		pass