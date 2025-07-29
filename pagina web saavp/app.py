from flask import Flask, render_template, request, redirect, url_for, flash



from flask_mysqldb import MySQL

from werkzeug.security import generate_password_hash



app= Flask(__name__)
app.secret_key = 'clave_secreta'

app.config['MYSQL_HOST'] = 'localhost' #servidor base de datos (localhost)
app.config['MYSQL_USER'] = 'root' # usuario por defecto de phpmyadmin
app.config['MYSQL_PASSWORD'] = '' #se deja vacio sii no tiene contraseña
app.config['MYSQL_DB'] = 'saavp' #Nombre de tu base da datos con login y roles

mysql =MySQL(app)


@app.route('/')
def index(): 
    return render_template('index.html')

@app.route('/login')
def login():                    
    return render_template('login.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form ['nombre']
        apellido = request.form ['apellido']
        username = request.form ['username']
        password = request.form ['password']
        hash = generate_password_hash(password)

        cur = mysql.connection.cursor()
        try :
            cur.execute("""INSERT INTO usuarios(nombre, apellido, username, password) VALUES (%s, %s, %s, %s)""", (nombre, apellido, username, hash))
            mysql.connection.commit()
            flash ("Usuario Registrado Con exito")
            return redirect(url_for('login'))
        except:
            flash("Este correo ya esta registrado")
        finally:
            cur.close()

    return render_template('registro.html')

if __name__ == '__main__':
    app.run(port=5000, debug=True)