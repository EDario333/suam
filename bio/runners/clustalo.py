#!/usr/bin/env python 

from . import AbstractRunner

class ClustaloRunner(AbstractRunner):
	def run(self,**kwargs):
		super().run(**kwargs)