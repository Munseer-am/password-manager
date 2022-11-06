#! /usr/bin/env python
import os
from distutils.spawn import find_executable

class Main:
	def __init__(self):
		super(Main, self).__init__()
		self.home = os.path.expanduser("~")
