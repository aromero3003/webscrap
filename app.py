from flask import Flask
from flask import render_template, request
import pymysql
from dotenv import load_dotenv
from os import getenv
# from flaskext.mysql import MySQL

load_dotenv()

app = Flask(__name__)

# mysql = MySQL()
# mysql.init_app(app)

# Configuraciones de la conexión
host = getenv("SQL_HOST")
port = int(getenv("SQL_PORT"))
database = getenv("DB_NAME")
user = getenv("DB_USER")
password = getenv("DB_PASSWORD")


@app.route('/')
def index():
    # sql_query = "select * from productos;"
    # conn = mysql.connect()
    # cursor = conn.cursor()
    # cursor.execute(sql_query)
    # cursor.commit()

    connection = pymysql.connect(
        host=host, port=port, database=database, user=user, password=password)
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM productos AS p INNER JOIN
        historial AS h ON p.url = h.product_url WHERE
        h.datetime = (SELECT MAX(datetime) FROM historial
        WHERE historial.product_url = p.url);""")
    productos = cursor.fetchall()
    # print(productos)
    connection.commit()
    return render_template('index.html', productos=productos)


@app.route('/product/<int:product_id>')
def product(product_id):
    connection = pymysql.connect(
        host=host, port=port, database=database, user=user, password=password)
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM productos WHERE id={product_id};")
    prod = cursor.fetchone()

    cursor.execute(
        f"SELECT * FROM historial WHERE product_url='{prod[2]}';")
    history = cursor.fetchall()
    connection.commit()
    return render_template('product.html', prod=prod, history=history)


if __name__ == "__main__":
    app.run(debug=True)
