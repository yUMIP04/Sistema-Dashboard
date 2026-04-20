from flask import Flask, render_template,request,redirect, url_for, session
from database import create_db, create_table,insert_producto, mostrar_productos, eliminar_producto, editar,create_usuario, login
import plotly .express as px
import pandas as pd
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import os
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

create_db()
create_table()

create_usuario("Victoria perez", "Yumi3012#20L")
lista_productos = mostrar_productos()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'inicio_sesion'



class Usuario(UserMixin):
    
    def __init__(self, id, nombre, contraseña):
        self.id = id
        self.nombre = nombre
        self.contraseña = contraseña

@login_manager.user_loader        
def loguear(id_usuario):
    
    conexion = create_db()
    cursor = conexion.cursor()
    
    cursor.execute('SELECT * FROM Usuarios WHERE id_usuario = ?', (id_usuario,))
    datos = cursor.fetchone()
    
    conexion.close()
    if datos:
        
        return Usuario(id=datos[0], nombre=datos[1], contraseña=datos[2] )
#INDEX

@app.route('/', methods=['GET', 'POST'])
def inicio_sesion():
    try:
        
        if request.method == 'POST':
            nombre = request.form.get('nombre')
            password = request.form.get('password')
            
            sesion_inicio = login(nombre)
            
            
            if sesion_inicio is not None:
                
                id_usuario = sesion_inicio[0]
                contraseña_hash = sesion_inicio[1]
                
                if check_password_hash(contraseña_hash, password):
                    
                    usuario_Obj = Usuario(id=id_usuario, nombre=nombre, contraseña=contraseña_hash)
                    
                    login_user(usuario_Obj)
                    print("☑️ Inicio de sesion exitoso!")
                    session['nombre'] = nombre
                    return redirect(url_for('index'))
                else:
                    print("Contraseña incorrecta")
    except Exception as e:
        print(f"Hubo un error: {e}")
    return render_template('inicio_sesion.html')


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def index():
    
    lista_productos = mostrar_productos()
    if request.method == 'POST':
        try:
            producto = request.form['producto']
            precio = request.form['precio']
            stock = request.form['stock']
            
            precio_float = float(precio)
            stock_int = int(stock)
            insert_producto(producto,precio_float,stock_int)
            lista_productos = mostrar_productos()
            
        except Exception as e:
            print(f"Hubo un error: {e}")
            
    try:
        BD = mostrar_productos()
        columnas = ['id', 'producto', 'precio', 'stock']
        sql_resultados = pd.DataFrame(BD, columns=columnas)

        sql_limpio = sql_resultados.dropna().drop_duplicates()

        fig = px.bar(sql_limpio, x='producto', y='precio', title="Precios por Producto")
        fig_stock = px.bar(sql_limpio, x='producto', y='stock', title="Stock de cada Producto")
        fig.write_html("static/Graficos.html")
        fig_stock.write_html("static/stocks.html")
        
        
        print("🥳Se genero con exito el html!")
        
    except Exception as e:
        print(f"Hubo un error: {e}")
    
    return render_template('index.html', lista_productos=lista_productos);



#ELIMINAR PRODUCTO
@app.route('/eliminar/<int:id>', methods=['GET', 'POST'])
def eliminar(id):
    if 'nombre' not in session:
        return redirect(url_for('inicio_sesion'))
    
    try:
        eliminar_producto(id)
        return redirect('/dashboard')
       
    except Exception as e:
        print(f"Hubo un error: {e}")
    

@app.route('/editar/<producto>/<int:id>', methods=['GET', 'POST'])

def editar_producto(producto ,id):
    producto = ""
    precio =""
    stock = ""
    if 'nombre' not in session:
        return redirect(url_for('inicio_sesion'))
    
    if request.method == "POST":
        try:
            
            producto = request.form['producto']
            precio = request.form['precio']
            stock = request.form['stock']
            
            precio_float = float(precio)
            stock_int = int(stock)
            editar(id, producto,precio_float,stock_int)
            
            return redirect(url_for('index'))
        except Exception as e:
            print(f"Hubo un error: {e}")
    return render_template('editar.html')
 
 
@app.route('/cerrar_sesion')
@login_required
def logout():
    
    logout_user()
    return redirect(url_for('inicio_sesion'))
if __name__ == '__main__':
    app.run(debug=False) 