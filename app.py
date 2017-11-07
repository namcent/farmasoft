#!/usr/bin/env python
import csv
import operator
#timeout
import flask
import datetime
import flask_login
#fin timeout
from flask import Flask, render_template, redirect, url_for, flash, session, request
from flask_bootstrap import Bootstrap
from forms import LoginForm, RegistrarForm

app = Flask(__name__)
bootstrap = Bootstrap(app)

app.config['SECRET_KEY'] = 'muajajaja5867916263246'

#funciones
@app.route('/')
def index():
    return render_template('index.html')

@app.errorhandler(404)
def no_encontrado(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def error_interno(e):
    return render_template('500.html'), 500

#ingreso con login al sistema
@app.route('/ingresar', methods=['GET', 'POST'])
def ingresar():
    formulario = LoginForm()
    if formulario.validate_on_submit():
        with open('usuarios') as archivo:
            archivo_csv = csv.reader(archivo)
            registro = next(archivo_csv)
            while registro:
                if formulario.usuario.data == registro[0] and formulario.password.data == registro[1]:

                    session['username'] = formulario.usuario.data

                    rows = []
                    try:
                        csv_rows = CSVReader().read_csv()
                    except CSVException as e:
                        return render_template('error_en_csv.html', error=e)

                    headers = csv_rows[0]
                    for row in csv_rows:
                        rows.append(row)

                    return render_template('ingresado.html', rows=rows)
                registro = next(archivo_csv, None)
            else:
                flash('Revisá el nombre de usuario y la contraseña')
                return redirect(url_for('ingresar'))
    return render_template('login.html', formulario=formulario)

#registro de un nuevo usuario
@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    formulario = RegistrarForm()
    if formulario.validate_on_submit():
        if formulario.password.data == formulario.password_check.data:
            with open('usuarios', 'a+') as archivo:
                archivo_csv = csv.writer(archivo)
                registro = [formulario.usuario.data, formulario.password.data]
                archivo_csv.writerow(registro)
            flash('Usuario creado correctamente')
            return redirect(url_for('ingresar'))
        else:
            flash('Las passwords no coinciden. Por favor intente nuevamente.')
    return render_template('registrar.html', form=formulario)

#salir del sistema
@app.route('/logout', methods=['GET'])
def logout():
    if 'username' in session:
        session.pop('username')
        return render_template('logged_out.html')
    else:
        return redirect(url_for('index'))

#consulta de ultimas ventas
@app.route('/ultimas_ventas', methods=['GET'])
def ultimas_ventas():
    if "username"in session:
        rows = []

        try:
            csv_rows = CSVReader().read_csv()
        except CSVException as e:
            return render_template('error_en_csv.html', error=e)

        headers = csv_rows[0]
        for row in csv_rows[1:]:
            rows.append(row)

        return render_template('ultimas_ventas.html', rows=rows, headers=headers)
    else:
        return redirect(url_for('ingresar'))

#consulta por cliente
@app.route('/producto_por_cliente', methods=['GET'])
def producto_por_cliente():
    if "username"in session:
        rows = []
        options = set()

        cliente = request.args.get("cliente")

        try:
            csv_rows = CSVReader().read_csv()
        except CSVException as e:
            return render_template('error_en_csv.html', error=e)

        headers = csv_rows[0]
        cliente_index = Helper().get_col_index(headers, "cliente")

        for row in csv_rows[1:]:
            if cliente and cliente.lower() in row[cliente_index].lower():
                rows.append(row)

            options.add(row[cliente_index])

        if len(rows) > 0:
            resultados = True
        else:
            resultados = False

        return render_template('producto_por_cliente.html', rows=rows, resultados=resultados, cliente=cliente, headers=headers, options=options)
    else:
        return redirect(url_for('ingresar'))

#consulta por producto
@app.route('/clientes_por_producto', methods=['GET'])
def clientes_por_producto():
    if "username"in session:
        rows = []
        options = set()

        producto = request.args.get("producto")

        try:
            csv_rows = CSVReader().read_csv()
        except CSVException as e:
            return render_template('error_en_csv.html', error=e)

        headers = csv_rows[0]
        producto_index = Helper().get_col_index(headers, "producto")

        for row in csv_rows[1:]:
            if producto and producto.lower() in row[producto_index].lower():
                rows.append(row)

            options.add(row[producto_index])

        if len(rows) > 0:
            resultados = True
        else:
            resultados = False

        return render_template('clientes_por_producto.html', rows=rows, resultados=resultados, producto=producto, headers=headers, options=options)
    else:
        return redirect(url_for('ingresar'))

#consulta por dinero gastado por cada cliente
@app.route('/mejores_clientes', methods=['GET'])
def mejores_clientes():
    if "username"in session:
        mejores_clientes = {}

        try:
            rows = CSVReader().read_csv()
        except CSVException as e:
            return render_template('error_en_csv.html', error=e)

        headers = rows[0]
        cliente_index = Helper().get_col_index(headers, "cliente")
        cantidad_index = Helper().get_col_index(headers, "cantidad")
        precio_index = Helper().get_col_index(headers, "precio")

        for row in list(rows)[1:]:
            if row[cliente_index] not in mejores_clientes:
                mejores_clientes[row[cliente_index]] = float(row[cantidad_index]) * float(row[precio_index])
            else:
                mejores_clientes[row[cliente_index]] += float(row[cantidad_index]) * float(row[precio_index])

        mejores_clientes = reversed(sorted(mejores_clientes.items(), key=operator.itemgetter(1)))
        return render_template('mejores_clientes.html', mejores_clientes=mejores_clientes)
    else:
        return redirect(url_for('ingresar'))

#consulta por comparacion en cantidad de productos vendidos
@app.route('/productos_mas_vendidos', methods=['GET'])
def productos_mas_vendidos():
    if "username"in session:
        productos_mas_vendidos = {}

        try:
            rows = CSVReader().read_csv()
        except CSVException as e:
            return render_template('error_en_csv.html', error=e)

        headers = rows[0]
        producto_index = Helper().get_col_index(headers, "producto")
        cantidad_index = Helper().get_col_index(headers, "cantidad")

        for row in list(rows)[1:]:
            if row[1] not in productos_mas_vendidos:
                productos_mas_vendidos[row[producto_index]] = int(float(row[cantidad_index]))
            else:
                productos_mas_vendidos[row[producto_index]] += int(float(row[cantidad_index]))

        productos_mas_vendidos = reversed(sorted(productos_mas_vendidos.items(), key=operator.itemgetter(1)))
        return render_template('productos_mas_vendidos.html', productos_mas_vendidos=productos_mas_vendidos)
    else:
        return redirect(url_for('ingresar'))

#timeout de la sesion
@app.before_request
def before_request():
    flask.session.permanent = True
    app.permanent_session_lifetime = datetime.timedelta(minutes=5)
    flask.session.modified = True
    flask.g.user = flask_login.current_user

#clases para las excepciones del csv
class CSVException(Exception):
    pass


class CSVReader():

    def read_csv(self):

        try:
            csvfile = open('ventas.csv', 'r')
        except FileNotFoundError:
            raise CSVException("Archivo no encontrado")

        valid_cols = ["CODIGO","PRODUCTO","CLIENTE","CANTIDAD","PRECIO"]

        rows = list(csv.reader(csvfile))
        for col in rows[0]:
            if col not in valid_cols:
                raise CSVException("Columna invalida %s" % col)

        col_indexes = {}
        for col in valid_cols:
            col_indexes[col.lower()] = Helper().get_col_index(rows[0], col.lower())

        for row in rows[1:]:

            if len(row) != len(valid_cols):
                raise CSVException("La cantidad de campos es incorrecta")

            if not row[col_indexes["codigo"]]:
                raise CSVException("Columna de codigo vacia")

            try:
                cantidad = float(row[col_indexes["cantidad"]])
                if not cantidad.is_integer():
                    raise CSVException("La cantidad no es un entero %s" % cantidad)
            except:
                raise CSVException("La cantidad no es un entero")

            try:
                precio = float(row[col_indexes["precio"]])
            except:
                raise CSVException("El precio no es un decimal")

        return rows

class Helper():

    def get_col_index(self, headers, col):

        for i, header in enumerate(headers):
            if header.lower() == col:
                return i

if __name__ == "__main__":
    app.run(debug=True)