from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
import json
import os


app = Flask(__name__)

app.config["MYSQL_USER"] = os.getenv('MYSQL_USER','root')
app.config["MYSQL_PASSWORD"] = os.getenv('MYSQL_PASSWORD','root')
app.config["MYSQL_DB"] = os.getenv('MYSQL_DB','crocosoft_test')
app.config["MYSQL_HOST"] =  os.getenv('MYSQL_HOST','localhost')

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
                time_update DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
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
    print(os.getenv('MYSQL_USER'))
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

# Create Customer
@app.route("/create_customer/",methods=['POST'])
def create_customer():
    data = json.loads(request.data)
    try:
        name = data['name']
        phone = data['phone']
        cursor = mysql.connection.cursor()
        query = f'INSERT INTO customer (name,phone) VALUES ("{name}","{phone}");'
        cursor.execute(query)
        mysql.connection.commit()
        return jsonify({
            'msg':"Customer created successfully"
        }) , 201
    except Exception as e:
        return jsonify({
            'error': f'Error: {e}',
        }) , 404


@app.route("/update_customer/<int:pk>", methods=["PUT"])
def update_customer(pk):
    data = json.loads(request.data)
    try:
        name = data['name']
        phone = data['phone']
        cursor = mysql.connection.cursor()
        query = f'UPDATE customer SET name="{name}",phone="{phone}" WHERE id={pk}'
        print(query)
        cursor.execute(query)
        mysql.connection.commit()
        return jsonify({
            'msg':f"Update User successfully"
        }) , 200
    except Exception as e:
        return jsonify({
            'error': f'Error: {e}',
        }) , 400

# Deleet Customer
@app.route("/customer_delete/<int:pk>", methods=["DELETE"])
def customer_delete(pk):
    try:
        cursor = mysql.connection.cursor()
        query = f'DELETE FROM customer WHERE id = {pk};'
        cursor.execute(query)
        mysql.connection.commit()
        return jsonify({
            'msg':f"deleted successfully"
        }) , 200
    except Exception as e:
        return jsonify({
            'error': f'Error: {e}',
        }) , 400
