#! /usr/bin/env python
import argparse
import os
import datetime
import time
import sys
from rich.console import Console

try:
    sys.path.insert(0, f"{os.path.expanduser('~')}/.config/manager/")
    import essentials
    from config import config
except ImportError:
    os.system("sudo rm /usr/local/bin/manager")
    os.system("manager_repair")
    exit()

console = Console()
os.system("clear")
os.system("figlet -c -f Bloody 'Munseer' | lolcat")
x = str(datetime.datetime.now().strftime("%H:%M:%S %b %d %Y"))
console.print(x.replace(":", "[blink]:[/blink]"))

parser = argparse.ArgumentParser()
parser.add_argument("-r", "--reset", help="reset the password of script", action="store_true")
parser.add_argument("-U", "--uninstall", help="Delete script file from /usr/local/bin/", action="store_true")
parser.add_argument("--REMOVE", help="Delete all files and directories related to password manager",
                    action="store_true")
args = parser.parse_args()

start = time.time()


class Main(essentials.Main):
    def __init__(self):
        super(Main, self).__init__()
        if not essentials.is_not_configured():
            if args.reset:
                self.reset()
            elif args.REMOVE:
                self.delete()
            elif args.uninstall:
                essentials.uninstall_script()
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
    os.system("clear")
except KeyboardInterrupt:
    os.system("clear")
    exit(0)
