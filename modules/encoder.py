import hashlib

def encode(word):
	enc = hashlib.md5(word.encode()).hexdigest()
	return enc
