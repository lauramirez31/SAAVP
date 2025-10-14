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
    clave = 'bmze wpye rxfi duke'
    mensaje = MIMEText(cuerpo)
    mensaje['Subject'] = 'Recuperar contraseña'
    mensaje['From']= 'david.lapras.cristian75@gmail.com'
    mensaje ['To'] = email

    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login(remitente,clave)
    server.sendmail(remitente,email,mensaje.as_string())
    server.quit()

def enviar_correo_cita(email, nombre, fecha, hora, motivo):
    cuerpo = f"""
    Hola {nombre},

    Tu cita ha sido agendada exitosamente.

    Detalles de tu cita:
    - Motivo: {motivo}
    - Fecha: {fecha}
    - Hora: {hora}

    Por favor llega puntual o responde a este correo si necesitas reprogramarla.

    ¡Gracias por confiar en nosotros!
    """

    remitente = 'david.lapras.cristian75@gmail.com'
    clave = 'bmze wpye rxfi duke'  
    mensaje = MIMEText(cuerpo)
    mensaje['Subject'] = 'Confirmación de cita'
    mensaje['From'] = remitente
    mensaje['To'] = email

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(remitente, clave)
    server.sendmail(remitente, email, mensaje.as_string())
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
            session['idUsuario'] = usuario[0]
            session['usuario'] = usuario[1]
            session['rol'] = usuario[3]
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


@app.route('/dashboard_propiedades')
def dashboard_propiedades():

    if 'usuario' not in session:
        flash("Debes iniciar sesión para acceder al dashboard.")
        return redirect(url_for('login'))

  

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute("""
        SELECT p.id_propiedad, p.nombre, p.precio, p.disponible, p.imagen,
               p.tipo, p.detalles, p.id_categoria, c.nombre AS categoria_nombre
        FROM propiedad p
        LEFT JOIN categorias c ON p.id_categoria = c.id_categoria
    """)
    propiedades = cursor.fetchall()

    cursor.execute("SELECT * FROM categorias")
    categorias = cursor.fetchall()

    cursor.execute("SELECT * FROM tipo_inmueble")
    tipos = cursor.fetchall()

    cursor.close()
    return render_template('dashboard_propiedades.html', propiedades=propiedades, categorias=categorias, tipos=tipos)

@app.route('/actualizar_propiedad/<int:id>', methods=['POST'])
def actualizar_propiedad(id):
    if 'usuario' not in session or session.get('rol') != 'Admin':
        flash("Acceso no autorizado.")
        return redirect(url_for('login'))

    nombre = request.form['nombre']
    precio = request.form['precio']
    disponible = request.form['disponible']
    id_categoria = request.form['id_categoria']
    tipo = request.form['tipo']
    detalles = request.form['detalles']
    imagen = request.files.get('imagen')

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

   
    if imagen and imagen.filename != '':
        filename = imagen.filename
        ruta = os.path.join('static/uploads', filename)
        imagen.save(ruta)
        cursor.execute("""
            UPDATE propiedad SET nombre=%s, precio=%s, disponible=%s,
            id_categoria=%s, tipo=%s, detalles=%s, imagen=%s
            WHERE id_propiedad=%s
        """, (nombre, precio, disponible, id_categoria, tipo, detalles, filename, id))
    else:
      
        cursor.execute("""
            UPDATE propiedad SET nombre=%s, precio=%s, disponible=%s,
            id_categoria=%s, tipo=%s, detalles=%s
            WHERE id_propiedad=%s
        """, (nombre, precio, disponible, id_categoria, tipo, detalles, id))

    mysql.connection.commit()
    cursor.close()
    flash("Propiedad actualizada correctamente.")
    return redirect(url_for('dashboard_propiedades'))

@app.route('/eliminar_propiedad/<int:id>')
def eliminar_propiedad(id):
    if 'usuario' not in session or session.get('rol') != 'Admin':
        flash("Acceso no autorizado.")
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("DELETE FROM propiedad WHERE id_propiedad = %s", [id])
    mysql.connection.commit()
    cursor.close()
    flash("Propiedad eliminada correctamente.")
    return redirect(url_for('dashboard_propiedades'))


@app.route('/catalogo')
def catalogo():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM propiedad")
    propiedad = cursor.fetchall()
    cursor.close()
    return render_template('catalogo.html', propiedad=propiedad)





@app.route('/agregar_propiedad', methods=['GET', 'POST'])
def agregar_propiedad():

    idUsuario = session.get('idUsuario')

    print("ID de sesión:", idUsuario)  # Depuración: imprime el ID de sesión en la consola
   
    if 'usuario' not in session:
        flash("Debes iniciar sesión para agregar una propiedad.")
        return redirect(url_for('login'))
    
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM categorias;")
    categorias = cursor.fetchall()
    cursor.execute("SELECT * FROM tipo_inmueble;")
    estado = cursor.fetchall()
    cursor.close()

    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = request.form['precio']
        disponible = request.form['disponible']   
        categoria = request.form['categoria']         
        detalles = request.form['detalles']
        tipo = request.form['tipo']
        idUsuario = session.get('idUsuario')


        imagen = request.files['imagen']
        filename = None
        if imagen and imagen.filename != "":
            filename = secure_filename(imagen.filename)
            imagen.save( os.path.join('static/uploads', filename))
        

        cursor = mysql.connection.cursor()
        cursor.execute("""
            INSERT INTO propiedad 
            (nombre, precio, disponible, imagen, tipo, detalles, id_categoria, idUsuario) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (nombre, precio, disponible, filename, tipo, detalles, categoria, idUsuario))

        mysql.connection.commit()
        cursor.close()

        flash("Propiedad agregada con éxito")
        return redirect(url_for('index'))

    return render_template("propiedades.html", categorias=categorias, estado=estado)


@app.route('/agendar', methods=['GET', 'POST'])
def agendar():
    id_propiedad = request.args.get('id') 
    idUsuario = session.get('idUsuario')   

    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        motivo = request.form['motivo']
        fecha = request.form['fecha']
        hora = request.form['hora']
        correo = request.form['correo']
        metodo =  request.form['metodo']
        

  
        cursor = mysql.connection.cursor()
        cursor.execute("""
            INSERT INTO citas (nombre, apellido, motivo, fecha, hora, correo, metodo, id_propiedad, idUsuario)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (nombre, apellido,motivo, fecha, hora, correo, metodo, id_propiedad, idUsuario))
        mysql.connection.commit()
        cursor.close()

        try:
            enviar_correo_cita(correo, nombre, fecha, hora, motivo)
        except Exception as e:
            print("Error al enviar el correo:", e)

        flash("Cita agendada con éxito")
        return redirect(url_for('catalogo'))

    return render_template('agendar.html', id_propiedad=id_propiedad)



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