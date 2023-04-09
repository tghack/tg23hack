from flask import Flask, render_template, request, redirect, session, flash, jsonify
import sqlite3

app = Flask(__name__, template_folder="template", static_folder="static")
app.secret_key = 'very-secret-key'


@app.route("/")
def index():
    return render_template("index.html")

# Flagg 1 (kommer som en alert når man trykker på en av linkene på hovedsiden)
@app.route('/get_info')
def get_info():
    info = {'message': 'The password is: TG23{remember_to_vaccinate_kids}'}
    return jsonify(info)

# Flagg 2 (ligger i databasen. Logg inn med brukernavn: generic-duck og passord: flagg 1, endre parameter i url fra 1 til 3)
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Get form data
        username = request.form["username"]
        password = request.form["password"]

        # Connect to DB
        connection = sqlite3.connect("user_data.db")
        cursor = connection.cursor()

        # Check if username and password are correct
        query = "SELECT user_id, username, password FROM users WHERE username=? and password=?"
        cursor.execute(query, (username, password,))
        results = cursor.fetchall()
        
        if len(results) == 0:
            flash('Login unsuccessful. Please try again.')
            return render_template("login.html")
        else:
            session["logged_in"] = True
            user_id = int(results[0][0])
            return redirect(f"/home/{user_id}")
    # Show login form
    return render_template("login.html")

@app.route("/home/<int:id>")
def home(id):
    if not session.get("logged_in"):
        return redirect(("/login"))
    else:
        conn = sqlite3.connect('user_data.db')
        c = conn.cursor()   
        c.execute("SELECT * FROM user_information WHERE user_id=?", (id,))
        row = c.fetchall()
        bilde = f"/static/{id}.png"
        things = {"Gate addresse": row[0][1], "Medlemskap på treningssenter": row[0][2], "Bibliotekskort": row[0][3], "Flagg": row[0][4]}
        return render_template('home.html', things=things, username=row[0][5], profil_bilde=bilde)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect('/')

# Flagg 3 (sql injection: skriv ' or '1'='1 i input feltet)
@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        search_query = request.form["search"]

        if search_query:
            # Trying to stop users from messing with the db
            if "drop" in search_query.lower() or "table" in search_query.lower() or "insert" in search_query.lower() or "schema" in search_query.lower():
                return render_template("search.html")
            
            conn = sqlite3.connect('articles.db')
            c = conn.cursor()

            try:
                c.execute(f"SELECT * FROM articles WHERE title='{search_query}'")
                articles = c.fetchall()
            except Exception as e:
                print("An error occurred while fetching articles:", e)
                articles = []

        conn.close()

        return render_template("search.html", articles=articles, search_query=search_query)
    return render_template("search.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)