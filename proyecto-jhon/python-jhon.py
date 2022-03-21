from flask import Flask, url_for, render_template, json, jsonify, request
from flask_mysqldb import MySQL
from datetime import datetime

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'restaurante2022'
conexion = MySQL(app)

@app.route("/api/categorias/all")
def listado_categorias():
    cursor = conexion.connection.cursor()
    listado_categorias = "SELECT * FROM res_categorias;"
    cursor.execute(listado_categorias)
    cursor.connection.commit()
    recordset = cursor.fetchall()
    registros = []
    for i in recordset:
        datos = {
            'cat_id' : i[0],
            'cat_nombre' : i[1],
            'cat_imagen' : i[2],
            'cat_descripcion' : i[3],
            'cat_hora' : str(i[4]),
            'cat_fecha' : str(i[5])
            }
        registros.append(datos)
    return jsonify({'resultado':registros})
@app.route("/api/categorias/<idc>", methods=['GET'])
def categorias_x_id(idc):
    cursor = conexion.connection.cursor()
    busca_id = "SELECT * FROM res_categorias WHERE cat_id = %s"
    cursor.execute(busca_id,(idc))
    conexion.connection.commit()
    recordset = cursor.fetchone()
    if len(recordset) > 0:
        datos = {
            'cat_id' :recordset[0],
            'cat_nombre' : recordset[1],
            'cat_imagen' : recordset[2],
            'cat_descripcion' : recordset[3],
            'cat_hora' : str(recordset[4]),
            'cat_fecha' : str(recordset[5])
            }
    return jsonify({'resultado':datos})
@app.route("/api/categorias/nombre", methods = ['POST'])
def categorias_x_nombre():
    if request.method == 'POST':
         cursor = conexion.connection.cursor()
         nombreCategorias = request.json['cat_nombre']
         cadenaBusq= "%" + nombreCategorias + "%"
         buscar_nombre = "SELECT * FROM res_categorias WHERE cat_nombre like %s"
         cursor.execute(buscar_nombre, (cadenaBusq,))
         conexion.connection.commit()
         recordset = cursor.fetchall()
         #if recordset[0]>0:
         registros = []
         for reg in recordset:
            datos = {
                'cat_id': reg[0],
                'cat_nombre': reg[1],
                'cat_imagen': reg[2],
                'cat_descripcion': reg[3],
                'cat_hora': str(reg[4]),
                'cat_fecha': str(reg[5])
                }
            registros.append(datos)
            return jsonify({"Resultado: ":registros})
@app.route("/api/categorias/insert", methods = ['POST'])
def insertar_categorias():
    cursor = conexion.connection.cursor()
    cat_nombre = request.json['cat_nombre']
    cat_imagen = request.json['cat_imagen']
    cat_descripcion = request.json['cat_descripcion']
    datosInsert = (cat_nombre,cat_imagen,cat_descripcion)
    InserCat = "Insert Into res_categorias(cat_nombre, cat_imagen, cat_descripcion)VALUES(%s, %s, %s);"
    cursor.execute(InserCat, datosInsert)
    conexion.connection.commit()
    return jsonify('INSERCION GUARDADA')
@app.route("/")
def homepage():
    return render_template('layout.html')
@app.route("/contactos")
def contactos():
    return render_template('contactos.html')
@app.route("/nosotros")
def qs():
    return render_template('qs.html')
@app.route("/productos")
def productos():
    return render_template('productos.html')
@app.route("/socios")
def socios():
    return render_template('socios.html')
if __name__=='__main__':
    app.run(debug=True, port=5000)
