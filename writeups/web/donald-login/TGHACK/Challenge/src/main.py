from flask import Flask, render_template, request, redirect
from base64 import b64encode, b64decode
from datetime import datetime
import random

app = Flask(__name__)

with open('flag.txt') as fh: 
    flag_g = fh.readline()

def get_encrypted_cookie():
    time_now = str(datetime.now().timestamp()).split('.')[0]
    math_1 = f'{str(random.getrandbits(2))} + {str(random.getrandbits(2))}'
    good_val = "Signed: R3lybyBHZWFybG9vc2U="
    
    encoded = b64encode(f'{b64encode(time_now.encode()).decode()}.{b64encode(math_1.encode()).decode()}.{b64encode(good_val.encode()).decode()}'.encode())[::-1]
    return encoded

def decrypt_cookie(cookie):

    rev = cookie[::-1]
    decoded = (b64decode(rev.encode())).decode()
    parts = decoded.split('.')
    a = (b64decode(parts[0].encode())).decode()
    b = (b64decode(parts[1].encode())).decode()
    c = (b64decode(parts[2].encode())).decode()

    values = {
        'time' : a, 
        'sum': eval(b),
        'good_val': c
    }

    return values

@app.get("/")
def root():
    return redirect("/login")

@app.get("/login")
def login():
    return render_template("login.html")

@app.post("/login")
def login_post():
    username = request.form["username"]
    password = request.form["password"]
    if username == "donald" and password == "duck":
        res = redirect("/admin")
        res.set_cookie("cookie", get_encrypted_cookie())
        return res
    else:
        return redirect("/login")
    
@app.get("/admin")
def account():
    if "cookie" in request.cookies.keys():
        cookie_values = decrypt_cookie(request.cookies.get("cookie", None))
        if int(cookie_values['time']) > datetime.now().timestamp() + 10.0:
            return render_template("admin.html", sum=cookie_values["sum"], flag=flag_g)
        else:
            return render_template("too_slow.html")

    return redirect("/login")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)