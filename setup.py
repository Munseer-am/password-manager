#! /usr/bin/python3
import os
import sys
import json
import platform
import shutil
import subprocess
from distutils.spawn import find_executable

home = os.path.expanduser("~")

def check_existence_of(path: str):
    return os.path.exists(path)


def is_installed(tool: str):
    return find_executable(tool)


def install(tool: str):
    package_managers = {
        "apt": f"sudo apt install {tool} -y",
        "pacman": f"sudo pacman -Sy {tool}",
        "dnf": f"sudo dnf install {tool}"
    }
    for key, value in package_managers.items():
        installed_package_manager = is_installed(key)
        if installed_package_manager is not None:
            command = package_managers[key].format(tool=tool)
            subprocess.run(command, shell=True, check=True)
            break
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
    if check_existence_of("/usr/share/figlet/fonts/"):
        if not check_existence_of("/usr/share/figlet/fonts/Bloody.flf"):
            try:
                shutil.copyfile("Bloody.flf", "/usr/share/figlet/fonts/Bloody.flf")
            except PermissionError:
                os.system("sudo cp Bloody.flf /usr/share/figlet/fonts/")
    elif check_existence_of("/usr/share/figlet/"):
        if not check_existence_of("/usr/share/figlet/Bloody.flf"):
            try:
                shutil.copyfile("Bloody.flf", "/usr/share/figlet/Bloody.flf")
            except PermissionError:
                os.system("sudo cp Bloody.flf /usr/share/figlet/")

def main():
    data = {
        f"{home}/.config/manager/insults.py": "lib/insults.py",
        f"{home}/.config/manager/essentials.py": "lib/essentials.py",
        f"{home}/.config/manager/menu.py": "lib/menu.py"
    }
    dirs = [f"{home}/.config/manager/", f"{home}/.config/manager/backup/", f"{home}/.config/manager/log/"]
    install_tool("figlet")
    install_tool("lolcat")
    if check_existence_of("requirements.txt"):
        subprocess.call(["pip", "install", "-r", "requirements.txt"])
    else:
        print("Requirements File Missing")
    install_font()
    os.system("clear && figlet -c -f Bloody 'Munseer' | lolcat")
    if not check_existence_of("/usr/local/bin/manager"):
        print("Installing Script")
        os.system("sudo cp manager.py /usr/local/bin/manager && sudo chmod +rwx /usr/local/bin/manager")
        print("creating required directories".title())
        for dir in dirs:
            if not check_existence_of(dir):
                os.mkdir(dir)
        print("Moving Files")
        for key, value in data.items():
            if not check_existence_of(key):
                shutil.copyfile(value, key)
        if not check_existence_of("/usr/local/bin/manager_repair"):
            os.system("sudo cp setup.py /usr/local/bin/manager_repair && sudo chmod +x /usr/local/bin/manager_repair")
        print("to run the script type `manager`".title())
    else:
        try:
            for key, value in data.items():
                if not check_existence_of(key):
                    shutil.copyfile(value, key)
            print("script already installed".title())
        except FileNotFoundError:
            os.system("sudo rm /usr/local/bin/manager")
            main()

try:
    base_dir = os.path.basename(os.getcwd())
    if platform.system() != "Linux":
        print("only linux is supported".title())
    else:
        if base_dir != "password-manager":
            print("""Run script in the "password-manager" directory""")
        else:
            main()
except Exception as e:
    with open("error.log", "a") as f:
        f.write(f"\n{str(e)}")
        f.close()
    print(e)
    quit()
