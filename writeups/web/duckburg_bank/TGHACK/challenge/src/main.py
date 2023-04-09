from flask import Flask, render_template, request, redirect
from base64 import b64encode

app = Flask(__name__)

flag1 = "TG23{everything_in_the_bank_is_mine}"
flag2 = "TG23{now_i_want_to_take_everything_with_me}"
flag3 = "TG23{this_is_the_most_valuable_file_in_duckburg}"


@app.get("/")
def root():
    return redirect("/login")

# Flag 1

@app.get("/login")
def login():
    return render_template("login.html", pw=b64encode(flag1.encode("utf-8")).decode("utf-8"))

@app.post("/login")
def login_post():
    username = request.form["username"]
    password = request.form["password"]
    if username == "scrooge" and password == flag1:
        res = redirect("/account")
        res.set_cookie("IS_ADMIN", "false")
        return res
    else:
        return redirect("/login")


# Flag 2

@app.get("/account")
def account():
    if "IS_ADMIN" in request.cookies.keys() and request.cookies.get("IS_ADMIN", None) == "true":
        return render_template("account.html", flag=flag2)
    else:
        return render_template("account.html", flag=None)

@app.post("/account")
def account_post():
    if "IS_ADMIN" in request.cookies.keys() and request.cookies.get("IS_ADMIN", None) == "true":
        return render_template("withdraw.html", flag=flag2)
    else:
        return redirect("/account")



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)