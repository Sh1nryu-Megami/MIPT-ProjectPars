import psycopg2
from flask import Flask, jsonify, request
import b_const
from time import sleep

app = Flask(__name__)

def connect_to_database():
    conn = psycopg2.connect(
        dbname=b_const.dbname,
        user=b_const.user,
        password=b_const.password,
        host=b_const.host
    )
    return conn


@app.route('/select_about_dish/<selected_dish>')
def select_about_dish(selected_dish):
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute('SELECT dish_details, dish_grams, dish_price, dish_image FROM food_positions WHERE dish_name = %s',
                   (selected_dish,))
    return jsonify(cursor.fetchall())


@app.route('/select_all_entity/<selected_entity>')
def select_all_entity(selected_entity):
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute(
        """SELECT dish_type, dish_name, dish_grams, dish_price FROM food_positions
        WHERE LOWER(dish_details) NOT LIKE LOWER(%s)""",
        ('%' + selected_entity + '%',))
    return jsonify(cursor.fetchall())

@app.route('/select_entity/<selected_entity>/<selected_type>')
def select_entity(selected_entity, selected_type=None):
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute(
        """SELECT dish_type, dish_name, dish_grams, dish_price FROM food_positions 
        WHERE LOWER(dish_details) NOT LIKE LOWER(%s)
        AND dish_type = %s""",
        ('%' + selected_entity + '%', selected_type))
    return jsonify(cursor.fetchall())


@app.route('/select_selected_type/<selected_type>')
def select_selected_type(selected_type):
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute('SELECT dish_name FROM food_positions WHERE dish_type = %s ORDER BY id',
                   (selected_type,))
    return jsonify([row[0] for row in cursor.fetchall()])


@app.route('/select_all_dishes_types')
def select_all_dishes_types():
    conn = connect_to_database()
    cur = conn.cursor()
    cur.execute('SELECT DISTINCT dish_type FROM food_positions')
    return jsonify([row[0] for row in cur.fetchall()])


@app.route('/select_all_dishes_names')
def select_all_dishes_names():
    conn = connect_to_database()
    cur = conn.cursor()
    cur.execute('SELECT DISTINCT dish_name FROM food_positions')
    return jsonify([row[0] for row in cur.fetchall()])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
