from flask import Flask, render_template, make_response, send_file
from Crypto.PublicKey import ECC
from Crypto.Cipher import ChaCha20
from Crypto.Util.number import long_to_bytes as l2b, bytes_to_long as b2l
import hashlib
import os
import re
import random
from base64 import b64encode as b64e, b64decode as b64d

app = Flask(__name__)
FLAG = open("flag.txt",'rb').read()
KEY = ECC.generate(curve='P-256')


def encrypt(plaintext, EKEY):
	Q = EKEY.pointQ
	G = ECC.EccPoint(
		0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296,
		0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5,
		curve="P-256"
	)

	nonce = hashlib.sha256(plaintext[:16] + EKEY.export_key(format='PEM').encode()).digest()[:8]
	random.seed(b2l(nonce))

	e = random.getrandbits(32)
	P = e*G
	Y = e*Q
	key = hashlib.sha256(l2b(int(Y.x))).digest()
	nonce = hashlib.md5(plaintext[:16]).digest()[:8]
	cipher = ChaCha20.new(key=key,nonce=nonce)
	ciphertext = cipher.encrypt(plaintext)

	return ciphertext, nonce, int(P.x), int(P.y)

@app.route('/')
def index():
	return render_template('./index.html')

@app.route('/encrypt/<plaintext>')
def get_enc(plaintext):
	pt = b64d(plaintext)
	ct, nonce, px, py = encrypt(pt, KEY)

	res = {
		"ciphertext":ct.hex(),
		"nonce":nonce.hex(),
		"P.x":hex(px)
	}

	return res

@app.route('/key/')
def get_key():
	ct, nonce, px, py = encrypt(KEY.export_key(format='PEM').encode(), KEY)
	res = {
		"ciphertext":ct.hex(),
		"nonce":nonce.hex(),
		"P.x":hex(px)
	}
	return res

@app.route('/flag/')
def get_flag():
	ct, nonce, px, py = encrypt(FLAG, KEY)
	res = {
		"ciphertext":ct.hex(),
		"nonce":nonce.hex(),
		"P.x":hex(px)
	}
	return res



if __name__ == "__main__":
	port = int(os.environ.get('PORT', 3301))
	app.run(debug=False, host='0.0.0.0', port=port)