from flask import Flask, render_template,request,redirect,url_for,flash
#importamos el modulo de flask
from flask_mysqldb import MySQL #im portamos modullo de mysql
app=Flask(__name__) #parametro
#creamos variables de conexion al servidor de mysql
app.config['MYSQL_HOST']='Localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='mbdpy'
mysql=MySQL(app)
#creamos ruta prncipal
@app.route("/")
def index():
    cu=mysql.connection.cursor()
    cu.execute('select * from clientes') #construimos la consulta
    datos=cu.fetchall()#ejecutamos para obtener todos los datos
    #print(datos) #imprime los datos de la consulta
    return render_template('index.html',clientes=datos)
#Crear ruta agrar clientes
@app.route("/add_clientes",methods=['POST']) #ruta de acceso al archivo adiciomnar contacto
def add_contact():
    if request.method=='POST':
        cc=request.form['Cedula']
        n=request.form['Nombres']
        tel=request.form['Telefono']
        em=request.form['Email']
        #mbdpyBASE DE DATOS
        cur=mysql.connection.cursor()# El cursor me permite ejecutar las consultas de mysql
        cur.execute('insert into clientes(id_cte,Nom_cte,Tel_cte,em_cte) values(%s,%s,%s,%s)',
        (cc,n,tel,em))
        mysql.connection.commit()
        return redirect(url_for('index')) #me redirecciona a la funcion de la ruta 7
#crear ruta consukta dato actualizar
@app.route('/edit/<string:id>')#ruta de acceso al archivo editar clientes
def get_contact(id):
    cur=mysql.connection.cursor()
    cur.execute('SELECT * from clientes WHERE id_cte={0}'.format(id))
    dato=cur.fetchall()#devuelve la consulta en un arreglo
    return render_template('Editacli.html',client=dato[0])
@app.route('/actualiza/<string:id>',methods=['POST'])#RUTA DE ACCESO AL ARCHIVO EDITAR CLIENTES
def set_contact(id):

    if request.method=='POST':
        cc=request.form['Cedula']
        n=request.form['Nombres']
        tel=request.form['Telefono']
        em=request.form['Email']
        cur=mysql.connection.cursor()
        cur.execute("""UPDATE clientes
                        SET id_cte=%s,
                        Nom_cte=%s,
                        Tel_cte=%s,
                        em_cte=%S
                        WHERE id_cte=%s""",(cc,n,tel,em,id))
        mysql.connection.commit()
        return redirect(url_for('index'))
#Crear ruta Eliminiar clientes
@app.route("/delete/<string:id>")#ruta de acceso al archivo editar clientes
def delete_contact(id):
    cur=mysql.connection.cursor()
    cur.execute('DELETE from clientes WHERE id_cte={0}'.format(id))
    mysql.connection.commit()
    return redirect(url_for('index'))

if __name__=="__main__":
      app.run(port =5000,debug=True)      
             
                    



