#!/usr/bin/env python 

from . import AbstractRunner

class MuscleRunner(AbstractRunner):
	def run(self,**kwargs):
		super().run(**kwargs)