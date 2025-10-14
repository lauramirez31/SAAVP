from flask import Flask, render_template, request, redirect, url_for, flash, session



from flask_mysqldb import MySQL
import MySQLdb.cursors

from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os

import secrets
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText



#funcion para generar token de recuperacion
def generate_token(email):
    token =secrets.token_urlsafe(32)
    expiry = datetime.now() + timedelta(hours=1)
    cur = mysql.connection.cursor()
    cur.execute("UPDATE usuarios SET reset_token= %s, token_expiry = %s WHERE username = %s", (token, expiry, email))
    mysql.connection.commit()
    cur.close()
    return token

#enviar el correo con enlace de recuperacion

def enviar_correo_reset(email,token):
    enlace = url_for('reset', token = token, _external=True)
    cuerpo = f"""HOLA, Solicitaste recuperar tu contraseña. Haz click en el siguiente enlace:
    {enlace}
    Este enlace expirara en 1 hora
    Si no lo solisitaste, ignora este mensaje. """

    remitente ='david.lapras.cristian75@gmail.com'
    clave = 'dslm hlfh gfio dvxs'
    mensaje = MIMEText(cuerpo)
    mensaje['Subject'] = 'Recuperar contraseña'
    mensaje['From']= 'david.lapras.cristian75@gmail.com'
    mensaje ['To'] = email

    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login(remitente,clave)
    server.sendmail(remitente,email,mensaje.as_string())
    server.quit()



app= Flask(__name__)
app.secret_key = 'clave_secreta'

app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_USER'] = 'root' 
app.config['MYSQL_PASSWORD'] = '' 
app.config['MYSQL_DB'] = 'saavp' 

mysql =MySQL(app)


@app.route('/')
def index(): 
    return render_template('index.html')

@app.route('/login', methods =['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password_ingresada = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("""
        SELECT u.idUsuario, u.nombre, u.password, r.nombreRol
        FROM usuarios u
        JOIN usuario_rol ur ON u.idUsuario= ur.idUsuario
        JOIN roles r ON ur.idRol = r.idRol
        WHERE u.username =%s
        """, (username,))

        usuario = cur.fetchone()

        if usuario and check_password_hash (usuario[2], password_ingresada):
            session['usuario'] = usuario[1]
            session['ROL'] = usuario[3]
            flash(f"BIENVENDO {usuario [1]}")

            cur.execute("""
            INSERT INTO registro_login (idUsuario, fecha)
            VALUES (%s, NOW())
            """,(usuario[0],))
            mysql.connection.commit()

            cur.close()

            if usuario[3] == 'Admin':
                return redirect(url_for('dashboard'))
            elif usuario[3] == 'Usuario':
                return redirect(url_for('index'))
            else:
                flash("Rol no reconocido")
                return redirect(url_for('login'))
        else:
            flash("usuario o contraseña incorrecta")
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route ('/logout')
def logout():
    session.clear()
    flash("sesion cerrada correctamente")
    return redirect(url_for('login'))

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

            cur.execute("SELECT idUsuario FROM usuarios WHERE username =%s", (username,))
            nuevo_usuario = cur.fetchone()

            cur.execute("INSERT INTO usuario_rol(idUsuario, idRol) VALUES (%s, %s)", (nuevo_usuario[0], 2))
            mysql.connection.commit()

            flash ("Usuario Registrado Con exito")
            return redirect(url_for('login'))
        except:
            flash("Este correo ya esta registrado")
        finally:
            cur.close()

    return render_template('registro.html')

@app.route('/forgot',methods=['GET', 'POST'])
def forgot():
    if request.method == 'POST':
        email = request.form['email']

        cur = mysql.connection.cursor()
        cur.execute("SELECT idUsuario FROM usuarios WHERE username = %s", (email,))
        existe = cur.fetchone()
        cur.close()

        if not existe:
            flash("Este correo no esta registrado.")
            return redirect(url_for('forgot'))

        token = generate_token(email)
        enviar_correo_reset(email,token)

        flash ("Te ENVIAMOS UN CORREO CON EL ENLACE PARA RESETAR TO CONTRASEÑA >:(")
        return redirect(url_for('login'))
    return render_template('forgot.html')


@app.route('/reset/<token>', methods = ['GET', 'POST'])
def reset (token):
    cur = mysql.connection.cursor()
    cur.execute("SELECT idUsuario, token_expiry FROM usuarios WHERE reset_token = %s", (token,))
    usuario = cur.fetchone()
    cur.close()

    if not usuario or datetime.now() >usuario [1]:
        flash ("Token invalido O expirado :)")
        return redirect(url_for('forgot'))

    if request.method == 'POST':
        nuevo_password = request.form ['password']
        hash_nueva = generate_password_hash(nuevo_password)

        cur = mysql.connection.cursor()
        cur.execute("UPDATE usuarios SET password=%s, reset_token=NULL, token_expiry=NULL WHERE idUsuario=%s", (hash_nueva, usuario[0]))
        mysql.connection.commit()
        cur.close()

        flash ("Tu contraseña ha sido actualizada ;3")
        return redirect(url_for('login'))
    
    return render_template('reset.html')

@app.route('/dashboard')
def dashboard():
    if 'usuario' not in session:
        flash("DEBES INICIAR SESION PARA ACCEDER AL DASHBOARD .")
        return redirect(url_for('login'))
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("""
        SELECT u.idUsuario, u.nombre, u.apellido, u.username, r.nombreRol, ur.idRol
        FROM usuarios u
        LEFT JOIN usuario_rol ur ON u.idUsuario = ur.idUsuario
        LEFT JOIN roles r ON ur.idRol = r.idRol
        """)
    usuarios = cursor.fetchall()
    cursor.close()
    
    return render_template('dashboard.html', usuarios=usuarios)


@app.route('/actualizar/<int:id>', methods=['POST'])
def actualizar(id):
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    correo = request.form['correo']
    rol = request.form['rol']

    cursor = mysql.connection.cursor()
    cursor.execute("""UPDATE usuarios SET nombre =%s,apellido =%s, username=%s WHERE idUsuario=%s""",(nombre,apellido,correo,id))
    cursor.execute("SELECT * FROM usuario_rol WHERE idUsuario =%s", (id,))
    existe = cursor.fetchone()

    if existe:
        cursor.execute("UPDATE usuario_rol SET idRol =%s WHERE idUsuario=%s", (rol,id))
    else:
        cursor.execute("INSERT INTO usuario_rol(idUsuario, idRol) VALUES (%s, %s)", (id,rol))
    mysql.connection.commit()
    cursor.close()

    return redirect(url_for('dashboard'))


@app.route('/eliminar/<int:id>')
def eliminar(id):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM usuarios WHERE idUsuario=%s',(id,))
    mysql.connection.commit()
    cursor.close()
    flash ('USUARIO ELIMINADO')
    return redirect(url_for('dashboard'))




@app.route('/agregar_propiedad', methods=['GET', 'POST'])
def agregar_propiedad():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM categorias;")
    categorias = cursor.fetchall()
    cursor.execute("SELECT * FROM estado_inmueble;")
    estado = cursor.fetchall()
    cursor.close()

    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = request.form['precio']
        disponible = request.form['disponible']   
        estado = request.form['estado']         
        detalles = request.form['detalles']
        id_categoria = request.form['id_categoria']
        

        imagen = request.files['imagen']
        filename = None
        if imagen and imagen.filename != "":
            filename = secure_filename(imagen.filename)
            path_imagen = os.path.join(app.config['static/uploads'], filename)
            imagen.save(path_imagen)

        cursor = mysql.connection.cursor()
        cursor.execute("""
            INSERT INTO propiedad 
            (nombre, precio, disponible, imagen, tipo, detalles, id_categoria) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (nombre, precio, disponible, filename, estado, detalles, id_categoria))

        mysql.connection.commit()
        cursor.close()

        flash("Propiedad agregada con éxito")
        return redirect(url_for('agregar_propiedad'))

    return render_template("propiedades.html", categorias=categorias, estado=estado)


@app.route('/agendar', methods=['GET', 'POST'])
def agendar():
    if request.method == 'POST':
        titulo = request.form['titulo']
        descripcion = request.form['descripcion']
        fecha = request.form['fecha']
        hora = request.form['hora']

        # Tomamos el usuario logueado desde la sesión
        idUsuario = session.get('idUsuario')

        if not idUsuario:
            flash("Debes iniciar sesión para agendar una cita", "warning")
            return redirect(url_for('login'))

        cursor = mysql.connection.cursor()
        cursor.execute("""
            INSERT INTO citas (titulo, descripcion, fecha, hora, idUsuario)
            VALUES (%s, %s, %s, %s, %s)
        """, (titulo, descripcion, fecha, hora, idUsuario))
        mysql.connection.commit()
        cursor.close()

        flash("Cita agendada con éxito", "success")
        return redirect(url_for('mis_citas'))

    return render_template('agendar.html')


@app.route('/mis_citas')
def mis_citas():
    idUsuario = session.get('idUsuario')

    if not idUsuario:
        flash("Debes iniciar sesión para ver tus citas", "warning")
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor()
    cursor.execute("""
        SELECT titulo, descripcion, fecha, hora 
        FROM citas 
        WHERE idUsuario = %s
        ORDER BY fecha, hora
    """, (idUsuario,))
    citas = cursor.fetchall()
    cursor.close()

    return render_template('mis_citas.html', citas=citas)



if __name__ == '__main__':
    app.run(port=5000, debug=True)