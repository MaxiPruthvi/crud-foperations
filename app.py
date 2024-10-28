from flask import Flask, render_template, request, jsonify
import mysql.connector

app = Flask(__name__)

# External MySQL database configuration
db_config = {
    'user': 'sql12741212',                  # External database username
    'password': 'cveWJQsc1v',               # External database password
    'host': 'sql12.freemysqlhosting.net',   # Host for the external database
    'database': 'sql12741212',              # Database name
    'port': 3306                            # Port number for MySQL
}

# Function to create a connection to the database
def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/employees', methods=['GET', 'POST'])
def employees():
    if request.method == 'POST':
        data = request.get_json()
        name = data['name']
        role = data['role']
        country = data['country']
        department = data['department']
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO employees (name, role, country, department) VALUES (%s, %s, %s, %s)', 
                (name, role, country, department)
            )
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({'status': 'success'}), 201
        except Exception as e:
            print(f"Error: {e}")  # Print the error to the console
            return jsonify({'status': 'error', 'message': str(e)}), 500
    
    if request.method == 'GET':
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM employees')
        employees = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(employees)

@app.route('/employees/<int:id>', methods=['PUT', 'DELETE'])
def employee(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if request.method == 'PUT':
        data = request.get_json()
        name = data['name']
        role = data['role']
        country = data['country']
        department = data['department']
        
        cursor.execute(
            'UPDATE employees SET name = %s, role = %s, country = %s, department = %s WHERE id = %s', 
            (name, role, country, department, id)
        )
        conn.commit()
        cursor.close()
        return jsonify({'status': 'success'})
    
    if request.method == 'DELETE':
        cursor.execute('DELETE FROM employees WHERE id = %s', (id,))
        conn.commit()
        cursor.close()
        return jsonify({'status': 'deleted'})
    
    conn.close()

if __name__ == '__main__':
    app.run(debug=True)
