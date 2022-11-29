#! /usr/bin/python3
import os
import platform
import shutil
import subprocess
from distutils.spawn import find_executable

home = os.path.expanduser("~")

def if_exists(path: str):
    return os.path.exists(path)


def is_installed(tool: str):
    return find_executable(tool)


def install(tool: str):
    if is_installed("apt") is not None:
        os.system(f"sudo apt install {tool} -y")
    elif is_installed("pacman") is not None:
        os.system(f"sudo pacman -Sy {tool}")
    elif is_installed("dnf") is not None:
        os.system("sudo dnf install {tool}")
    else:
        print("No Installation Candidate Found")


def install_tool(tool: str):
    if is_installed(tool) is None:
        print(f"Error: {tool} is not installed...")
        print(f"Installing {tool}...")
        install(tool)
    else:
        return True


def install_font():
    if if_exists("/usr/share/figlet/fonts/"):
        if not if_exists("/usr/share/figlet/fonts/Bloody.flf"):
            try:
                shutil.copyfile("Bloody.flf", "/usr/share/figlet/fonts/Bloody.flf")
            except PermissionError:
                os.system("sudo cp Bloody.flf /usr/share/figlet/fonts/")
    elif if_exists("/usr/share/figlet/"):
        if not if_exists("/usr/share/figlet/Bloody.flf"):
            try:
                shutil.copyfile("Bloody.flf", "/usr/share/figlet/Bloody.flf")
            except PermissionError:
                os.system("sudo cp Bloody.flf /usr/share/figlet/")


def main():
    install_tool("figlet")
    install_tool("lolcat")
    if if_exists("requirements.txt"):
        subprocess.call(["pip", "install", "-r", "requirements.txt"])
    else:
        print("Requirements File Missing")
    install_font()
    os.system("clear && figlet -c -f Bloody 'Munseer' | lolcat")
    if not if_exists("/usr/local/bin/manager"):
        print("Installing Script")
        os.system("sudo cp manager.py /usr/local/bin/manager && sudo chmod +rwx /usr/local/bin/manager")
        print("creating required directories".title())
        if not if_exists(f"{home}/.config/manager/"):
            os.mkdir(f"{home}/.config/manager/")
        if not if_exists(f"{home}/.config/manager/log/"):
            os.mkdir(f"{home}/.config/manager/log/")
        if not if_exists(f"{home}/.config/manager/backup/"):
            os.mkdir(f"{home}/.config/manager/backup/")
        print("Moving Files")
        if if_exists(f"{home}/.config/manager/config.py"):
            print("Found Existing Configurations")
        else:
            shutil.copyfile("lib/config.py", f"{home}/.config/manager/config.py")
        if not if_exists(f"{home}/.config/manager/db.sqlite3"):
            print("Found Existing Database")
        if not if_exists(f"{home}/.config/manager/menu.py"):
            shutil.copyfile("lib/menu.py", f"{home}/.config/manager/menu.py")
        if not if_exists(f"{home}/.config/manager/insults.py"):
            shutil.copyfile("lib/insults.py", f"{home}/.config/manager/insults.py")
        if if_exists(f"{home}/.config/manager/essentials.py"):
            confirm = input("do you want to update script[y/n]: ".title().lower())
            if confirm == "y":
                shutil.copyfile("lib/essentials.py", f"{home}/.config/manager/essentials.py")
        else:
            shutil.copyfile("lib/essentials.py", f"{home}/.config/manager/essentials.py")
        if not if_exists("/usr/local/bin/manager_repair"):
            os.system("sudo cp setup.py /usr/local/bin/manager_repair && sudo chmod +rwx /usr/local/bin/manager_repair")
        print("to run the script type `manager`".title())
    
