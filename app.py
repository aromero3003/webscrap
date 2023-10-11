from flask import Flask
from flask import render_template, redirect
import pymysql
from dotenv import load_dotenv
from os import getenv

load_dotenv()

app = Flask(__name__)

# Configuraciones de la conexión
host = getenv("SQL_HOST")
port = int(getenv("SQL_PORT"))
database = getenv("DB_NAME")
user = getenv("DB_USER")
password = getenv("DB_PASSWORD")


@app.route('/')
def index():
    connection = pymysql.connect(
        host=host, port=port, database=database, user=user, password=password)
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM productos AS p INNER JOIN
        historial AS h ON p.id = h.prod_id WHERE
        h.datetime = (SELECT MAX(datetime) FROM historial
        WHERE historial.prod_id = p.id);""")
    productos = cursor.fetchall()
    connection.commit()
    return render_template('index.html', productos=productos)


@app.route('/product/<int:product_id>')
def product(product_id):
    connection = pymysql.connect(
        host=host, port=port, database=database, user=user, password=password)
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM productos WHERE id={product_id};")
    prod = cursor.fetchone()
    if prod is None:
        return redirect('/')

    cursor.execute(
        f"SELECT * FROM historial WHERE prod_id={prod[0]} ORDER BY datetime DESC;")
    # f"SELECT * FROM historial WHERE prod_id={prod[0]};")
    history = cursor.fetchall()
    connection.commit()
    return render_template('product.html', prod=prod, history=history)


if __name__ == "__main__":
    app.run(debug=True)
