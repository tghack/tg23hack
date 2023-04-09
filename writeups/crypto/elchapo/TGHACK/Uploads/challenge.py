from Crypto.PublicKey import ECC
from Crypto.Cipher import ChaCha20
from Crypto.Util.number import long_to_bytes as l2b, bytes_to_long as b2l
import hashlib
import os

def encrypt(plaintext, EKEY):
	Q = EKEY.pointQ
	G = ECC.EccPoint(
		0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296,
		0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5,
		curve="P-256"
	)

	e = b2l(os.urandom(32))
	P = e*G
	Y = e*Q
	key = hashlib.sha256(l2b(int(Y.x))).digest()
	nonce = os.urandom(8)
	cipher = ChaCha20.new(key=key,nonce=nonce)
	ciphertext = cipher.encrypt(plaintext)

	return ciphertext, nonce, int(P.x), int(P.y)

if __name__ == '__main__':
	FLAG = open('flag.txt','rb').read()
	ecc_key = ECC.generate(curve='P-256')
	print(ecc_key.export_key(format='PEM'))

	ct, nonce, Px, Py = encrypt(FLAG, ecc_key)
	print('ct =',ct.hex())
	print('nonce =',nonce.hex())
	print('P.x =',Px)
	print('P.y =',Py)

