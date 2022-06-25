from string import *
import random

def gen():
	sym = "*&^%$#?;:/[]{}()"
	all = sym + ascii_lowercase + ascii_uppercase + digits
	len = 20
	randomzing = random.sample(all, len)
	password = "".join(randomzing)
	print(f"Your Password is ready: {password}")
