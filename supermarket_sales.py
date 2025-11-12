from flask import Flask, render_template, redirect, flash, request, url_for
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3

def init_db():
    connection = sqlite3.connect("supermarket.db")
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS supermarket(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    ''')
    connection.commit()
    connection.close()

init_db()

app = Flask(__name__)
app.secret_key = "my-very-secret-key"

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        connection = sqlite3.connect("supermarket.db")
        cursor = connection.cursor()
        cursor.execute("SELECT password FROM supermarket WHERE username = ?", (username,))
        result = cursor.fetchone()
        connection.close()

        if result and check_password_hash(result[0], password):
            flash("Login Successful", "success")
            return redirect(url_for("sales"))
        else:
            flash("Incorrect Credentials", "error")
            return redirect(url_for("home"))

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        confirm = request.form["confirm"]

        if password != confirm:
            flash("Password does not match", "error")
            return redirect(url_for("register"))

        hashed_password = generate_password_hash(password)

        try:
            connection = sqlite3.connect("supermarket.db")
            cursor = connection.cursor()
            cursor.execute("INSERT INTO supermarket(username, password) VALUES(?, ?)", (username, hashed_password))
            connection.commit()
            connection.close()

            flash("Registration Successful", "success")
            return redirect(url_for("home"))

        except sqlite3.IntegrityError:
            flash("Username already exists", "error")
            return redirect(url_for("register"))

    return render_template("register.html")

@app.route("/sales")
def sales():
    return render_template("sales.html")

@app.route("/sales_per_day")
def sales_per_day():
    return render_template("sales_per_day.html")

@app.route("/sales_region")
def sales_region():
    return render_template("sales_region.html")

@app.route("/monthly_sales")
def monthly_sales():
    return render_template("monthly_sales.html")

@app.route("/payment_method")
def payment_method():
    return render_template("payment_method.html")

@app.route("/quantity_sold_per_product")
def quantity_sold_per_product():
    return render_template("quantity_sold_per_product.html")

@app.route("/quantity_sold_per_weekday")
def quantity_sold_per_weekday():
    return render_template("quantity_sold_per_weekday.html")

@app.route("/revenue_per_month")
def revenue_per_month():
    return render_template("revenue_per_month.html")

@app.route("/revenue_per_product")
def revenue_per_product():
    return render_template("revenue_per_product.html")

if __name__ == "__main__":
    app.run(debug=True)