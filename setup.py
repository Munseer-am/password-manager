#! /usr/bin/env python
import os
from distutils.spawn import find_executable

class Main:
	def __init__(self):
		super(Main, self).__init__()
		self.home = os.path.expanduser("~")
		self.base_dir = os.getcwd()
		print(self.base_dir)

	def is_installed(self, tool: str):
		return find_executable(tool)

	def exists(self, path: str):
		return os.path.exists(path)

	def install(self, tool: str):
		if is_installed("apt") is not None:
			os.system(f"sudo apt install {tool} -y")
		elif is_installed("pacman") is not None:
			os.system(f"sudo pacman -Sy {tool}")
		elif is_installed("dnf") is not None:
			os.system(f"sudo dnf install {tool}")
		else:
			print("No installation canditate found")

	def install_tool(self, tool: str):
		if is_installed(tool) is None:
			print(f"Error: {tool} is not installed...")
			print(f"Installing {tool}...")
			self.install(tool)

if __name__ == "__main__":
	Main()
