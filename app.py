from flask import Flask, render_template, redirect, url_for, session, flash
from form import Form
from loginform import LoginForm
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "secret_key"

def init_db():
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute("""
                CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE,
                password TEXT,
                age INTEGER
                )
                """)
    conn.commit()
    conn.close()


@app.route("/")
def homepage():
    return render_template("homepage.html")


@app.route("/formpage", methods=["POST", "GET"])
def formpage():
    form = Form()
    if form.validate_on_submit():
        conn = sqlite3.connect('users.db')
        cur = conn.cursor()

        cur.execute(
            "SELECT 1 FROM users WHERE name = ?",
            (form.name.data,)
        )
        user = cur.fetchone()
        if user:
            conn.close()
            return render_template(
                "formpage.html",
                form=form,
                error="username already taken"
            )



        hashed_password = generate_password_hash(form.password.data)
        cur.execute(
            "INSERT INTO users (name, password, age) VALUES(?, ?, ?)",
            (form.name.data, hashed_password, form.age.data)
        )

        conn.commit()
        conn.close()
        return redirect( url_for("successregister"))
        

    return render_template("formpage.html", form=form)

@app.route("/successregisterpage")
def successregister():
    return render_template("successregisterpage.html")

@app.route("/successlogin")
def successlogin():
    if 'user' not in session:
        return redirect(url_for("login"))
    return render_template("successloginpage.html")



@app.route("/loginpage", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        conn = sqlite3.connect("users.db")
        cur = conn.cursor()
        cur.execute(
            "SELECT password FROM users WHERE name=?", (form.name.data,)
        )

        user = cur.fetchone()
        conn.close()


        if user and check_password_hash(user[0], form.password.data):
            session['user'] = form.name.data
            return redirect(url_for("successlogin"))
        else:
            flash("Invalid login details")
            return render_template("loginpage.html", form = form)


    return render_template("loginpage.html", form = form)

@app.route("/logout")
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))



if __name__ == '__main__':
    init_db()
    app.run(debug=True)