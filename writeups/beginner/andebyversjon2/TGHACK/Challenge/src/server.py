from flask import Flask, render_template, request

app = Flask(__name__, template_folder="template", static_folder="static")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/robots.txt")
def robots():
    return "User-agent: *\nDisallow: /offlimits"

@app.route("/offlimits")
def flag():
    return "TG23{there_are_hidden_ducks_on_the_website}"


@app.route("/static/ducks/")
def root():
    name = request.args.get("name")
    if not name:
        return 404

    path = "./static/ducks/" + name
    with open(path, "rb") as f:
        data = f.read()
    return data



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)