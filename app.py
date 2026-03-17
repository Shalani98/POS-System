import os

from flask import Flask, render_template, request, redirect, session, url_for, flash
import mysql.connector
from datetime import datetime

app = Flask(__name__)
app.secret_key = "your_secret_key"  # for login sessions

# MySQL connection
def get_db():
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST","localhost"),
        user=os.environ.get("DB_USER","root"),        # XAMPP default
        password=os.environ.get("DB_PASS",""),        # XAMPP default empty
        database=os.environ.get("DB_NAME","pos_system")
    )

# Admin login
@app.route("/", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM admin WHERE username=%s AND password=%s",
                       (username, password))
        admin = cursor.fetchone()
        conn.close()

        if admin:
            session["admin"] = username
            return redirect("/dashboard")
        else:
            flash("Invalid username or password")
            return redirect("/")

    return render_template("login.html")

# Dashboard - show products
@app.route("/dashboard")
def dashboard():
    if "admin" not in session:
        return redirect("/")
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    conn.close()
    return render_template("index.html", products=products)

# Add product
@app.route("/add", methods=["GET","POST"])
def add_product():
    if "admin" not in session:
        return redirect("/")
    if request.method == "POST":
        name = request.form["name"]
        price = request.form["price"]
        stock = request.form["stock"]

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO products(name, price, stock) VALUES(%s,%s,%s)",
                       (name, price, stock))
        conn.commit()
        conn.close()
        return redirect("/dashboard")
    return render_template("add_product.html")

# Sell product
@app.route("/sell/<int:id>")
def sell_product(id):
    if "admin" not in session:
        return redirect("/")
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT name, price, stock FROM products WHERE id=%s", (id,))
    product = cursor.fetchone()

    if not product:
        conn.close()
        return "Product not found"

    name, price, stock = product
    if stock <= 0:
        conn.close()
        return "Stock empty"

    cursor.execute("UPDATE products SET stock=stock-1 WHERE id=%s", (id,))
    cursor.execute("INSERT INTO sales(product_name, qty, total, date) VALUES(%s,%s,%s,%s)",
                   (name, 1, price, datetime.now()))
    conn.commit()
    conn.close()
    return redirect("/dashboard")

# Sales history
@app.route("/sales")
def sales_history():
    if "admin" not in session:
        return redirect("/")
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sales ORDER BY date DESC")
    sales = cursor.fetchall()
    conn.close()
    return render_template("sales.html", sales=sales)

# Logout
@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect("/")

if __name__ == "__main__":
    port=int(os.environ.get("PORT",5000))
    app.run(host="0.0.0.0",port=port,debug=True)