from flask import Flask
from flask import render_template, request, redirect
from flaskext.mysql import MySQL
from datetime import datetime

app=Flask(__name__)
mysql = MySQL()

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'sitio'
mysql.init_app(app)

@app.route('/')
def index():
    return render_template('sitio/index.html')

@app.route('/libros')
def libros():
    return render_template('sitio/libros.html')

@app.route('/nosotros')
def nosotros():
    return render_template('sitio/nosotros.html')

@app.route('/admin')
def admin_index():
    return render_template('admin/index.html')

@app.route('/admin/login')
def login():
    return render_template('admin/login.html')
    
@app.route('/admin/libros')
def admin_libros():
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM libros")
    libros = cursor.fetchall()
    conexion.commit()
    print(libros)
    return render_template('admin/libros.html', libros=libros)

@app.route('/admin/cerrar')
def admin_cerrar():
    return render_template('admin/cerrar.html')

@app.route('/admin/libros/guardar' , methods=['POST'])
def admin_libros_guardar():
    titulo=request.form['txtNombre']
    url=request.form['txtURL']
    archivo=request.files['txtImagen']

    tiempo = datetime.now()
    horaActual = tiempo.strftime("%Y%H%M%S")

    if archivo.filename != '':
        nuevoNombre = horaActual+"_"+archivo.filename
        archivo.save("templates/sitio/img" + nuevoNombre)

    sql="INSERT INTO libros (id, nombre, imagen, url) VALUES (NULL, %s, %s, %s);"
    datos=(titulo,archivo.filename,url)
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql,datos)
    conexion.commit()
    print(titulo,url,archivo)
    return redirect('/admin/libros')

@app.route('/admin/libros/borrar', methods=['POST'])
def admin_libros_eliminar():
    _id=request.form['txtID']

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM libros WHERE id = %s",(_id))
    conexion.commit()

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM libros WHERE id = %s",(_id))
    conexion.commit()
    return redirect('/admin/libros')


if __name__ == '__main__':
    app.run(debug=True)
