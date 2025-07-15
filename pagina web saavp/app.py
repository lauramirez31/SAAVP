from flask import Flask, render_template



from flask_mysqldb import MySQL



app= Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost' #servidor base de datos (localhost)
app.config['MYSQL_user'] = 'root' # usuario por defecto de phpmyadmin
app.config['MYSQL_PASSWORD'] = '' #se deja vacio sii no tiene contraseña
app.config['MYSQL_BD'] = 'saavp' #Nombre de tu base da datos con login y roles

mysql =MySQL(app)


@app.route('/')
def index(): 
    return render_template('index.html')

@app.route('/login')
def login():                    
    return render_template('login.html')

@app.route('/registro')
def registro():                    
    return render_template('registro.html')

if __name__ == '__main__':
    app.run(port=5000, debug=True)