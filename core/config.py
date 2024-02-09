import os
import json
import keyring
from core import b64_decode

class Config:
	def __init__(self):
		super(Config, self).__init__()
		self.user_home: str = os.path.expanduser("~")
		self.conf_dir: str = os.path.join(self.user_home, ".config")
		self.__services = [b'TWFuYWdlcg==', b'VG9rZW4=']
		self.__services = [b64_decode(service) for service in self.__services]
		self.files: dict = {
			"config_dir": os.path.join(self.conf_dir, "manager"),
			"logs": os.path.join(self.conf_dir, "manager", 'log'),
			"backups": os.path.join(self.conf_dir, "manager", 'backup'),
			"config": os.path.join(self.conf_dir, "manager", 'config.json')
		}

	def checkConfig(self) -> bool:
		for _, file in self.files.items():
			if not os.path.exists(file):
				raise Exception("ConfigError")
				break
		return True

	def storeToken(self, token: bytes) -> None:
		self.__services.append(token.decode())
		self.__addToKeyring(*self.__services)

	def getToken(self) -> bytes:
		return self.__retriveFromKeyring(*self.__services).encode()

	def deleteToken(self) -> None:
		try:
			keyring.delete_password(*self.__services)
		except keyring.errors.PasswordDeleteError:
			print("No such token")

	def __addToKeyring(self, *args) -> None:
		kr = keyring.get_keyring()
		kr.set_password(*args)

	def __retriveFromKeyring(self, *args) -> str:
		kr = keyring.get_keyring()
		return kr.get_password(*args)

	def readConfig(self) -> dict:
		try:
			with open(self.files['config'], "r") as f:
				content: dict = json.load(f)
				f.close()
			return content
		except FileNotFoundError:
			self.checkConfig()

	def writeConfig(self, conf: dict):
		try:
			with open(self.files['config'], "w") as f:
				json.dump(conf, f, indent=4)
				f.close()
		except FileNotFoundError:
			self.checkConfig()
