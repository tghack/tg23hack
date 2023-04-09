from flask import Flask, render_template, make_response

app = Flask(__name__, template_folder="template", static_folder="static")

@app.route("/")
def index():
    # Render index.html
    resp = make_response(render_template("index.html"))

    # Setting cookie key and value
    resp.set_cookie('safari-cookie', 'TG23{chewy_cookies_are_the_best}')

    return resp 

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)