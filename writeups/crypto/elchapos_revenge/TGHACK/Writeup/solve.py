import requests
import json
from base64 import b64encode as b64e
from urllib.parse import quote_plus as urienc
from mod_sqrt import tonelli
from Crypto.PublicKey import ECC
from Crypto.Util.number import long_to_bytes as l2b, bytes_to_long as b2l
from Crypto.Cipher import ChaCha20
import hashlib

HOSTNAME = 'localhost'
PORT = 3301

url = f'http://{HOSTNAME}:{PORT}'

key_json = json.loads(requests.get(f'{url}/key').content.decode())
key_prefix = b'-----BEGIN PRIVATE KEY-----'

payload = urienc(b64e(key_prefix + b'\x00'*500))
cipherstream_json = json.loads(requests.get(f'{url}/encrypt/{payload}').content.decode())


cipherstream = bytes.fromhex(cipherstream_json["ciphertext"])
enc_key = bytes.fromhex(key_json["ciphertext"])

XOR = lambda a,b:bytes(i^j for i,j in zip(a,b))

private_key = key_prefix + XOR(enc_key,cipherstream)[len(key_prefix):]


# next, let's get an encrypted flag with the associated data
flag_json = json.loads(requests.get(f'{url}/flag').content.decode())

ct = bytes.fromhex(flag_json['ciphertext'])
nonce = bytes.fromhex(flag_json['nonce'])
Px = int(flag_json['P.x'][2:], 16)


a = 0xffffffff00000001000000000000000000000000fffffffffffffffffffffffc
b = 0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b
p = 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff

# Py recoverable with tonelli shanks algorithm
Py = tonelli((Px**3 + a*Px + b ) % p, p)


# we have no gathered all the information we need to recover the flag :D

def decrypt(ciphertext, EKEY, P, nonce):
	Q = EKEY.pointQ
	d = int(EKEY.d)

	Y = d*P # d*P = d*e*G = e*Q = Y
	key = hashlib.sha256(l2b(int(Y.x))).digest()

	cipher = ChaCha20.new(key=key,nonce=nonce)
	plaintext = cipher.decrypt(ciphertext)

	return plaintext



KEY = ECC.import_key(private_key)
P = ECC.EccPoint(Px, Py, curve='P-256')

print(decrypt(ct, KEY, P, nonce))

