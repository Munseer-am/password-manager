#! /usr/bin/env python
import os
import platform
import shutil
import subprocess
from distutils.spawn import find_executable


class Main:
	def __init__(self):
		super(Main, self).__init__()
		self.home = os.path.expanduser("~")
		self.base_dir = os.path.basename(os.getcwd())
		if platform.system() == "Linux":
			if self.base_dir != "password-manager":
				print("""Run in the "password-manager" directory """)
			else:
				self.main()
		else:
			print("Only Linux Is Supported")
		

	def is_installed(self, tool: str):
		return find_executable(tool)

	def exists(self, path: str):
		return os.path.exists(path)

	def install(self, tool: str):
		if self.is_installed("apt") is not None:
			os.system(f"sudo apt install {tool} -y")
		elif self.is_installed("pacman") is not None:
			os.system(f"sudo pacman -Sy {tool}")
		elif self.is_installed("dnf") is not None:
			os.system(f"sudo dnf install {tool}")
		else:
			print("No installation canditate found")

	def install_tool(self, tool: str):
		if self.is_installed(tool) is None:
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
			if self.exists("/usr/share/figlet/Bloody.flf") != True:
				try:
					shutil.copy("Bloody.flf", "/usr/share/figlet/fonts/Bloody.flf")
				except PermissionError:
					os.system("sudo cp Bloody.flf /usr/share/figlet/")

	def main(self):
		self.install_tool("figlet")
		self.install_tool("lolcat")
		if self.exists("requirements.txt"):
			subprocess.call(["pip", "install", "-r", "requirements.txt"])
		else:
			print("Requirements File Missing")
		self.install_font()
		os.system("clear && figlet -c -f Bloody 'Munseer' | lolcat")
		if self.exists("/usr/local/bin/manager") != True:
			print("Installing Script")
			os.system("sudo cp manager.py /usr/local/bin/manager && sudo chmod +rwx /usr/local/bin/manager")
			print("Creating required directories")
			if self.exists(f"{self.home}/.config/manager") != True:
				os.mkdir(f"{self.home}/.config/manager/")
			if self.exists(f"{self.home}/.config/manager/log/") != True:
				os.mkdir(f"{self.home}/.config/manager/log/")
			if self.exists(f"{self.home}/.config/manager/backup/") != True:
				os.mkdir(f"{self.home}/.config/manager/backup/")
			print("Moving Files")
			if self.exists(f"{self.home}/.config/manager/config.py"):
				print("Found Existing Configuration")
			else:
				shutil.copy("lib/config.py", f"{self.home}/.config/manager/config.py")
			if self.exists(f"{self.home}/.config/manager/db.sqlite3"):
				print("Found Existing Database")
			if self.exists(f"{self.home}/.config/manager/menu.py") != True:
				shutil.copy("lib/menu.py", f"{self.home}/.config/manager/menu.py")
			if self.exists(f"{self.home}/.config/manager/insults.py") != True:
				shutil.copy("lib/insults.py", f"{self.home}/.config/manager/insults.py")
			if self.exists("/usr/local/bin/manager_repair") != True:
				os.system("sudo cp setup.py /usr/local/bin/manager_repair && sudo chmod +rwx /usr/local/bin/manager_repair")
			print("TO RUN THE SCRIPT TYPE `manager`")
		else:
			if self.exists(f"{self.home}/.config/manager/config.py") != 1:
				shutil.copy("lib/config.py", f"{self.home}/.config/manager/config.py")
			if self.exists(f"{self.home}/.config/manager/menu.py") != True:
				shutil.copy("lib/menu.py", f"{self.home}/.config/manager/menu.py")
			if self.exists(f"{self.home}/.config/manager/insults.py") != True:
				shutil.copy("lib/insults.py", f"{self.home}/.config/manager/insults.py")
			if self.exists("/usr/local/bin/manager_repair") != True:
				os.system("sudo cp setup.py /usr/local/bin/manager_repair && sudo chmod +rwx /usr/local/bin/manager_repair")
			print("Script Already Installed")


if __name__ == "__main__":
	Main()
