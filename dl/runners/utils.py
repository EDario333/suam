#!/usr/bin/env python 

def get_file_name_without_extension(fn=None):
	assert fn is not None, "The filename is missed at utils.get_file_name_without_extension(fn=None)"
	file_name = fn[fn.rfind('/') + 1:]
	file_name = file_name[0:file_name.find('.')]

	return file_name