import clipboard
import hashlib
import os
import random
import sys
from cryptography.fernet import Fernet
from shutil import copyfile
from string import ascii_lowercase, ascii_uppercase, digits
from rich.prompt import Prompt
from rich.console import Console

console = Console()

try:
    sys.path.insert(0, f"{os.path.expanduser('~')}/.config/manager/")
    from config import config
    from insults import insult
except ImportError:
    os.system("sudo rm /usr/local/bin/manager")
    os.system("manager_repair")
    sys.exit(0)

home = os.path.expanduser("~")


def generate_password():
    sym = "!@#$%^&*(){}[]:;"
    all_chars = ascii_uppercase + ascii_lowercase + digits + sym
    r = random.sample(all_chars, 20)
    return "".join(r)


def sha256_encoder(word: str):
    return hashlib.sha3_256(word.encode("utf-8")).hexdigest()


def copy(word: str):
    clipboard.copy(word)
    clipboard.paste()


def is_not_configured():
    if config is not None:
        return False
    else:
        return True


def uninstall_script():
    pas = Prompt.ask("Enter password to delete", password=True)
    hashed = sha256_encoder(pas)
    if hashed != config["KEY"]:
        console.print("Invalid Password")
    else:
        os.system("sudo rm /usr/local/bin/manager")


def encrypt(key: bytes, password: str):
    enc = Fernet(key)
    return enc.encrypt(password.encode("utf-8"))


def decrypt(key: bytes, password: bytes):
    dec = Fernet(key)
    return dec.decrypt(password).decode("utf-8")


def backup(db: str, path: str, dst: str):
    copyfile(path, f"{dst}/{db}")


def security():
    inp = Prompt.ask("Enter password to unlock", password=True)
    enc = sha256_encoder(inp)
    i = 0
    while enc != config["KEY"]:
        i += 1
        if i >= 3:
            console.print("Access Denied!")
            break
        else:
            console.print(insult())
            inp = Prompt.ask("\nTry again", password=True)
            enc = sha256_encoder(inp)
    else:
        console.print("Access Granted!")
