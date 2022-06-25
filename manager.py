#!/usr/bin/env python
import os
import sqlite3
import argparse
import config
import time
import threading
from modules import pass_gen
from modules import capture
from modules import encoder
from modules import logo
from modules import log
from modules import insert
from modules import fetch

start = time.time()
os.system("cp config.py ./modules")
os.system("clear")

logo.logo()

parser = argparse.ArgumentParser()
parser.add_argument("-new", help="Enter Keyword to unlock database inserting", type=str)
parser.add_argument("-a", help="Enter the name of the application", type=str)
parser.add_argument("-u", help="Enter the username of the application", type=str)
parser.add_argument("-e", help="Enter Email/phone of the application", type=str)
parser.add_argument("-p", help="Enter the password of application", type=str)

args = parser.parse_args()

class Main(object):
	def __init__(self):
		super(Main, self).__init__()
		key_con = sqlite3.connect(config.database_file_path)
		cur = key_con.cursor()
		cur.execute("SELECT * FROM KEY")
		keys = cur.fetchall()
		for key in keys:
			access_key = "".join(key)
		if args.new:
			insert.insert(str(args.a).capitalize(), args.u, args.e, args.p)
		else:
			self.security(access_key)

	def security(self, key):
		i = 0
		inp = str(input("\nEnter the password to unlock file: ")).strip()
		hash = encoder.encode(inp)
		while hash != key:
			i += 1
			print("Access Denied!")
			inp = str(input("\nTry again: ")).strip()
			hash = encoder.encode(inp)
		else:
			print("Access Granted!")

	def main(self):
		thread = threading.Thread(target=capture.capture, args=(config.log_dir,))
		thread.daemon = True
		thread.start()
		app = str(input("Enter the name of the application: ")).strip()
		log.txt_log(app, x, __file__)
		fetch(app)
		log.log(app, x, __file__)
		pas = str(input("Do you need a new password: ")).strip().lower()
		if pas in ("y", "yes"):
			pass_gen.gen()
		else:
			pass

if __name__ == '__main__':
	Main()
		
end = time.time()
print(f"Executing time: {end-start}")
time.sleep(3)
os.system("clear")
