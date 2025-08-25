from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
import os
import mysql.connector

app = Flask(__name__)
app.secret_key = "secretocarrito"
UPLOAD_FOLDER = "static/images/"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 


db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="tienda"
)

cursor = db.cursor(dictionary=True)


@app.route('/')
def index():
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    return render_template("index.html", productos=productos)

@app.route('/agregar', methods=["GET", "POST"])
def agregar():
    if request.method == "POST":
        nombre = request.form['nombre']
        precio = request.form['precio']
        imagen = request.files['imagen']


        if imagen:
            filename = secure_filename(imagen.filename)
            path_imagen = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            imagen.save(path_imagen)


            cursor.execute("INSERT INTO productos (nombre, precio, imagen) VALUES (%s, %s, %s)",
                           (nombre, precio, filename))
            db.commit()
            flash("Producto agregado con éxito")
            return redirect(url_for('index'))


    return render_template("agregar.html")

@app.route('/carrito/<int:id>')
def carrito(id):
    cursor.execute("SELECT * FROM productos WHERE id=%s", (id,))
    producto = cursor.fetchone()


    if "carrito" not in session:
        session['carrito'] = []


    session['carrito'].append(producto)
    session.modified = True


    return redirect(url_for('mostrar_carrito'))

@app.route('/mostrar_carrito')
def mostrar_carrito():
    carrito = session.get("carrito", [])
    total = sum([float(p['precio']) for p in carrito])
    return render_template("carrito.html", carrito=carrito, total=total)
    
@app.route('/factura')
def factura():
    carrito = session.get("carrito", [])
    total = sum([float(p['precio']) for p in carrito])

    session.pop("carrito", None)
    return render_template("factura.html", carrito=carrito, total=total)


if __name__ == "__main__":
    app.run(debug=True)




