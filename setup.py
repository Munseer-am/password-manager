#! /usr/bin/env python
import os
from distutils.spawn import find_executable


class Main:
	def __init__(self):
		super(Main, self).__init__()
		self.home = os.path.expanduser("~")
		self.base_dir = os.getcwd()

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

	def install_font(self):
		if self.exists("/usr/share/figlet/fonts"):
			if self.exists("/usr/share/figlet/fonts/Bloody.flf") != True:
				try:
					shutil.copy("Bloody.flf", "/usr/share/figlet/fonts/Bloody.flf")
				except PermissionError:
					os.system("sudo cp Bloody.flf /usr/share/figlet/fonts/")
		else:
			try:
				shutil.copy("Bloody.flf", "/usr/share/figlet/fonts/Bloody.flf")
			except PermissionError:
				os.system("sudo cp Bloody.flf /usr/share/figlet/")

	def main(self):
		pass

if __name__ == "__main__":
	Main().install_font()
