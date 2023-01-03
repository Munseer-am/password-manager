#! /usr/bin/env python
import argparse
import pyfiglet
import os
import datetime
import time
import sys
from rich.console import Console

try:
    sys.path.insert(0, f"{os.path.expanduser('~')}/.config/manager/")
    from essentials import Main, is_not_configured, uninstall_script
except ImportError:
    os.system("sudo rm /usr/local/bin/manager")
    os.system("manager_repair")
    exit()

console = Console()
console.clear()
os.system("figlet -c -f Bloody 'Manager' | lolcat")
x = str(datetime.datetime.now().strftime("%H:%M:%S %b %d %Y"))
console.print(x.replace(":", "[blink]:[/blink]"))

parser = argparse.ArgumentParser()
parser.add_argument("-r", "--reset", help="reset the password of script", action="store_true")
parser.add_argument("-U", "--uninstall", help="Delete script file from /usr/local/bin/", action="store_true")
parser.add_argument("--REMOVE", help="Delete all files and directories related to password manager",
                    action="store_true")
args = parser.parse_args()

start = time.time()


class Main(Main):
    def __init__(self):
        super(Main, self).__init__()
        configured = not is_not_configured()
        if configured:
            options = {
                "reset": self.reset,
                "REMOVE": self.delete,
                "uninstall": uninstall_script,
            }
            for key, value in options.items():
                if getattr(args, key):
                    value()
                    break
            else:
                self.security()
        else:
            self.set_details()



try:
    if __name__ == "__main__":
        Main()
    end = time.time()
    print(f"Execution Time: {end-start}")
    time.sleep(4)
    console.clear()
except KeyboardInterrupt:
    console.clear()
    exit(0)
