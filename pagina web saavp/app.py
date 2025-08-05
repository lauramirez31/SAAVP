from flask import Flask, render_template, request, redirect, url_for, flash, session



from flask_mysqldb import MySQL

from werkzeug.security import generate_password_hash, check_password_hash

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

app.config['MYSQL_HOST'] = 'localhost' #servidor base de datos (localhost)
app.config['MYSQL_USER'] = 'root' # usuario por defecto de phpmyadmin
app.config['MYSQL_PASSWORD'] = '' #se deja vacio sii no tiene contraseña
app.config['MYSQL_DB'] = 'saavp' #Nombre de tu base da datos con login y roles

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
        cur.execute("SELECT idUsuario, nombre, password FROM usuarios WHERE username = %s", (username,))
        usuario = cur.fetchone()
        cur.close

        if usuario and check_password_hash (usuario[2], password_ingresada):
            session ['usuario'] = usuario[1]
            flash(f"BIENVENDO {usuario [1]}")
            return redirect(url_for('index'))
        else:
            flash("usuario o contraseña incorrecta")                    
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


if __name__ == '__main__':
    app.run(port=5000, debug=True)