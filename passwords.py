import hashlib
import os
import binascii


def encode_password(password):
	salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
	hash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000)
	hash = binascii.hexlify(hash)
	hash = (salt + hash).decode('ascii')
	
	return hash


def verify_password(password, hash):
	salt = hash[:64].encode('ascii')
	old_hash = hash[64:]
	new_hash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000)
	new_hash = binascii.hexlify(new_hash)
	new_hash = new_hash.decode('ascii')

	return old_hash == new_hash