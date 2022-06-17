from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
import json
import os


app = Flask(__name__)

app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "crocosoft_test"
app.config["MYSQL_HOST"] = "localhost"

mysql = MySQL(app)

@app.before_first_request
def create_tables():
    try:
        #create tables once for the first app run
        cursor = mysql.connection.cursor()
        cursor.execute('''
            CREATE TABLE type_vehicle(
                id TINYINT NOT NULL AUTO_INCREMENT,
                name VARCHAR(50),
                PRIMARY KEY (id));
            CREATE TABLE vehicle(
                id INT NOT NULL AUTO_INCREMENT,
                model VARCHAR(50),
                type_id TINYINT,
                available BOOLEAN,
                day_cost INT,
                color VARCHAR(50),
                time_create DATETIME DEFAULT CURRENT_TIMESTAMP,
                time_update DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (type_id) REFERENCES type_vehicle(id),
                PRIMARY KEY (id));
            CREATE TABLE customer(
                id INT NOT NULL AUTO_INCREMENT,
                name VARCHAR(100),
                phone VARCHAR(20),
                PRIMARY KEY (id));
            CREATE TABLE booking(
                id INT NOT NULL AUTO_INCREMENT,
                vehicle_id INT,
                customer_id INT,
                start_day DATE,
                end_day DATE, 
                FOREIGN KEY (vehicle_id) REFERENCES vehicle(id),
                FOREIGN KEY (customer_id) REFERENCES customer(id),
                PRIMARY KEY (id),
                CONSTRAINT check_return_date CHECK(end_day >= start_day AND DATEDIFF(end_day,start_day) <= 7));
        ''')
    except:
        #tables already created
        return True

#Get customer with ID
@app.route("/get_customer/<int:pk>", methods=["GET"])
def get_customer(pk):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute(f'''SELECT * FROM customer WHERE id = {pk}''')
        result = cursor.fetchall()[0]
        return jsonify({
            'data': result,
        }) , 200
    except Exception as e:
        return jsonify({
            'error': f'Error: {e}',
        }) , 404
