import sqlite3
from flask import session
from werkzeug.security import generate_password_hash, check_password_hash
#CREACION DE DB

def create_db():
    
    db = sqlite3.connect('Productos.db')
    return db

#CREACION TABLA
def create_table():
    conexion = create_db()
    cursor = conexion.cursor()
    
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS Productos (
                       id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
                       producto VARCHAR(30),
                       precio REAL,
                       stock INTEGER
                   )
                   ''')
    
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS Usuarios(
                       id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
                       nombre VARCHAR,
                       clave VARCHAR
                   )
                   ''')
    conexion.commit()
    conexion.close()

#CREAR USUARIO POR DEFECTO
def create_usuario(nombre,clave):
    conexion = create_db()
    cursor = conexion.cursor()
    
    try:
        clave_hash = generate_password_hash(clave)
        cursor.execute('''
                       INSERT INTO Usuarios (nombre, clave) VALUES(?,?)
                       ''',(nombre,clave_hash))
        conexion.commit()
        conexion.close()
                
    except Exception as e:
        print(f"Hubo un error: {e}")


#INICIAR SESION

def login(nombre):
    
    conexion = create_db()
    cursor = conexion.cursor()
    
    try:
        cursor.execute('SELECT id_usuario, clave FROM Usuarios WHERE nombre = ?',(nombre,))
    
        resultado_login = cursor.fetchone()
        return resultado_login
        
    except Exception as e:
        print(f"Hubo un error: {e}")
        
    conexion.close()
#INSERTAR PRODUCTOS

def insert_producto(producto, precio,stock):
    conexion = create_db()
    cursor = conexion.cursor()
    
    try:
        cursor.execute('''
                       INSERT INTO PRODUCTOS (producto, precio, stock) VALUES(?,?,?)
                       ''', (producto,precio,stock))
        
        conexion.commit()
        conexion.close()
        
    except Exception as e:
        print(f"Hub un error: {e}")
        
def mostrar_productos():
    
    conexion = create_db()
    cursor = conexion.cursor()
    
    try:
        cursor.execute('SELECT * FROM Productos')
        
        resultado = cursor.fetchall()
        return resultado
    except Exception as e:
        print(f"Hubo un error: {e}")
        
def eliminar_producto(id):
    
    conexion = create_db()
    
    cursor = conexion.cursor()
    
    try:
        cursor.execute('DELETE FROM Productos WHERE id_producto = ?',(id,))
        
        conexion.commit()
        conexion.close()
        
        print("☑️ Se Elimino correctamente un elemento")
    except Exception as e:
        print(f"Hubo un error: {e}")
        
def editar(id_producto, producto, precio, stock):
    
    conexion = create_db()
    cursor = conexion.cursor()
    
    try:
        cursor.execute('''UPDATE Productos SET producto = ?, precio = ?, stock = ?''', (producto,precio,stock))
        
        conexion.commit()
        conexion.close()
        
    except Exception as e:
        print(f"Hubo un error: {e}")