import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error

load_dotenv()

app = Flask(__name__)

# Database connection details

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': os.getenv('DB_PASSWORD'),  # Using environment variable
    'database': 'my_database'
}

def connect_to_database():
    try:
        conn = mysql.connector.connect(**db_config)
        if conn.is_connected():
            print("Successfully connected to the database!")
            return conn
        else:
            print("Connection failed.")
            return None
    except Error as err:
        print(f"Error: {err}")
        return None
    
# Function to close the connection safely
def close_connection(conn):
    if conn is not None and conn.is_connected():
        conn.close()
        print("Connection closed.")
    else:
        print("No active connection to close.")
    

    
# Endpoint to get all users
@app.route('/api/users', methods=['GET'])
def get_users():
    try:
        conn = mysql.connector.connect(**db_config)
        # Perform database operations only if connection is successful
        if conn:
    # Your database operations here (e.g., queries, inserts)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users")
            users = cursor.fetchall()
            return jsonify(users), 200
            
        else:
            return f"Cannot perform database operations without a valid connection."
        
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            #Close the connection
            close_connection(conn)
            

# Endpoint to add a new user
@app.route('/api/users', methods=['POST'])
def add_user():
    data = request.json
    name = data.get('name')
    email = data.get('email')

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        query = "INSERT INTO users (name, email) VALUES (%s, %s)"
        cursor.execute(query, (name, email))
        conn.commit()
        return jsonify({"message": "User added successfully!"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# Endpoint to delete a user
@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        query = "DELETE FROM users WHERE id = %s"
        cursor.execute(query, (user_id,))
        conn.commit()
        return jsonify({"message": "User deleted successfully!"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == '__main__':
    app.run(debug=True)
