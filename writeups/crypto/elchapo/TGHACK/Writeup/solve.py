from Crypto.PublicKey import ECC
from Crypto.Cipher import ChaCha20
from Crypto.Util.number import long_to_bytes as l2b, bytes_to_long as b2l
import hashlib
import os
import re

def decrypt(ciphertext, EKEY, P, nonce):
	Q = EKEY.pointQ
	d = int(EKEY.d)

	Y = d*P # d*P = d*e*G = e*Q = Y
	key = hashlib.sha256(l2b(int(Y.x))).digest()

	cipher = ChaCha20.new(key=key,nonce=nonce)
	plaintext = cipher.decrypt(ciphertext)

	return plaintext

if __name__ == '__main__':
	output = open('output.txt','rb').read()

	ct_regex = r'ct = ([0-9a-f]+)'
	nonce_regex = r'nonce = ([0-9a-f]+)'
	px_regex = r'P\.x = ([0-9]+)'
	py_regex = r'P\.y = ([0-9]+)'
	ecc_key = ECC.import_key(output[:246])
	print(re.findall(ct_regex, output.decode())[-1])
	ciphertext = bytes.fromhex(re.findall(ct_regex, output.decode())[-1])
	nonce = bytes.fromhex(re.findall(nonce_regex, output.decode())[-1])
	Px = int(re.findall(px_regex, output.decode())[-1])
	Py = int(re.findall(py_regex, output.decode())[-1])
	P = ECC.EccPoint(Px,Py,curve='P-256')

	flag = decrypt(ciphertext, ecc_key, P, nonce)
	print(flag)
