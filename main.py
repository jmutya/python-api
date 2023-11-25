from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS from flask_cors
import mysql.connector
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='api.log'
)
logger = logging.getLogger(__name__)

# Use CORS middleware to enable CORS support for all routes
CORS(app)  # Add this line to enable CORS

# Define the database connection parameters
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "brgy_information"
}

# Establish a database connection
conn = None
try:
    conn = mysql.connector.connect(**db_config)
    if conn.is_connected():
        logger.info("Connected to the database")
except mysql.connector.Error as e:
    logger.error(f"Database connection error: {e}")

# Create an endpoint for user registration
@app.route('/register', methods=['POST'])
def register_user():
    logger.info("Received registration request")
    data = request.get_json()
    name = data.get('name')
    password = data.get('password')

    if not all([name, password]):
        logger.error("Incomplete data received")
        return jsonify({"message": "Incomplete data"}), 400

    # Check if the user already exists
    cursor = conn.cursor()
    query = "SELECT * FROM test_user WHERE name = %s"
    values = (name,)

    cursor.execute(query, values)
    existing_user = cursor.fetchone()

    if existing_user:
        logger.info("User already exists")
        return jsonify({"message": "User already exists"}), 409

    # Insert the user data into the database
    query = "INSERT INTO test_user (name, password) VALUES (%s, %s)"
    try:
        cursor.execute(query, (name, password))
        conn.commit()
        logger.info("User registered successfully")
        return jsonify({"message": "Registration successful"}), 200
    except mysql.connector.Error as e:
        logger.error(f"Database error: {e}")
        return jsonify({"message": "Registration failed"}), 500
    finally:
        cursor.close()


@app.route('/add-user-profile', methods=['POST'])
def add_user_profile():
    logger.info("Received user profile creation request")
    data = request.get_json()
    F_Name = data.get('F_Name')
    L_Name = data.get('L_Name')
    Email = data.get('Email')
    Phone = data.get('Phone')

    if not all([F_Name, L_Name, Email, Phone]):
        logger.error("Incomplete data received")
        return jsonify({"message": "Incomplete data"}), 400

    cursor = conn.cursor()
    query = "INSERT INTO test_profiling (F_Name, L_Name, Email, Phone) VALUES (%s, %s, %s, %s)"

    try:
        cursor.execute(query, (F_Name, L_Name, Email, Phone))
        conn.commit()
        logger.info("Profile Added Successfully")
        return jsonify({"message": "Profile Added successful"}), 200
    except mysql.connector.Error as e:
        logger.error(f"Database error: {e}")
        return jsonify({"message": "Profile creation failed"}), 500
    finally:
        cursor.close()

#fetch profiles on admin
@app.route('/fetch-user-profiles', methods=['GET'])
def fetch_user_profiles():
    logger.info("Fetching user profiles")

    cursor = conn.cursor()
    query = "SELECT F_Name, L_Name, Email, Phone FROM test_profiling"

    try:
        cursor.execute(query)
        profiles = cursor.fetchall()
        column_names = [i[0] for i in cursor.description]

        # Convert the result to a list of dictionaries
        profile_list = []
        for profile in profiles:
            profile_dict = dict(zip(column_names, profile))
            profile_list.append(profile_dict)

        logger.info("Fetched user profiles successfully")
        return jsonify(profile_list), 200
    except mysql.connector.Error as e:
        logger.error(f"Database error: {e}")
        return jsonify({"message": "Failed to fetch user profiles"}), 500
    finally:
        cursor.close()

# Create an endpoint for user login
@app.route('/login', methods=['POST'])
def login_user():
    logger.info("Received login request")
    data = request.get_json()
    name = data.get('name')
    password = data.get('password')

    if not all([name, password]):
        logger.error("Incomplete data received")
        return jsonify({"message": "Incomplete data"}), 400

    # Check if the user exists and the password is correct
    cursor = conn.cursor()
    query = "SELECT * FROM test_user WHERE name = %s AND password = %s"
    values = (name, password)

    cursor.execute(query, values)
    user = cursor.fetchone()

    if user:
        logger.info("User logged in successfully")
        return jsonify({"message": "Login successful"}), 200
    else:
        logger.info("User login failed")
        return jsonify({"message": "Login failed. Invalid username or password"}), 401

#message insterted  to the database
@app.route('/message', methods=['POST'])
def insert_message():
    logger.info("Received message insertion request")
    data = request.get_json()
    title = data.get('title')
    body = data.get('body')
    name = data.get('name')

    if not all([title, body, name]):
        logger.error("Incomplete data received")
        return jsonify({"message": "Incomplete data"}), 400

    cursor = conn.cursor()
    query = "INSERT INTO test_message (title, body, name) VALUES (%s, %s, %s)"

    try:
        cursor.execute(query, (title, body, name))
        conn.commit()
        logger.info("Message inserted successfully")
        return jsonify({"message": "Message inserted successfully"}), 200
    except mysql.connector.Error as e:
        logger.error(f"Database error: {e}")
        return jsonify({"message": "Message insertion failed"}), 500
    finally:
        cursor.close()
#fetch message from database

@app.route('/fetch-messages', methods=['GET'])
def fetch_messages():
    logger.info("Fetching messages")

    cursor = conn.cursor()
    query = "SELECT title, body, name FROM test_message"

    try:
        cursor.execute(query)
        messages = cursor.fetchall()
        column_names = [i[0] for i in cursor.description]

        # Convert the result to a list of dictionaries
        message_list = []
        for message in messages:
            message_dict = dict(zip(column_names, message))
            message_list.append(message_dict)

        logger.info("Fetched messages successfully")
        return jsonify(message_list), 200
    except mysql.connector.Error as e:
        logger.error(f"Database error: {e}")
        return jsonify({"message": "Failed to fetch messages"}), 500
    finally:
        cursor.close()

#insert data to Updates/ post a updates
@app.route('/update_news', methods=['POST'])
def update_news():
    logger.info("Received message insertion request")
    data = request.get_json()
    headline = data.get('headline')
    body = data.get('body')

    if not all([headline, body]):
        logger.error("Incomplete data received")
        return jsonify({"message": "Incomplete data"}), 400

    cursor = conn.cursor()
    query = "INSERT INTO test_updates (headline, body) VALUES (%s, %s)"

    try:
        cursor.execute(query, (headline, body))
        conn.commit()
        logger.info("Message inserted successfully")
        return jsonify({"message": "Message inserted successfully"}), 200
    except mysql.connector.Error as e:
        logger.error(f"Database error: {e}")
        return jsonify({"message": "Message insertion failed"}), 500
    finally:
        cursor.close()

#fetch Updates
@app.route('/fetch_updates', methods=['GET'])
def fetch_updates():
    logger.info("Fetching messages")

    cursor = conn.cursor()
    query = "SELECT headline, body FROM test_updates"

    try:
        cursor.execute(query)
        messages = cursor.fetchall()
        column_names = [i[0] for i in cursor.description]

        # Convert the result to a list of dictionaries
        message_list = []
        for message in messages:
            message_dict = dict(zip(column_names, message))
            message_list.append(message_dict)

        logger.info("Fetched messages successfully")
        return jsonify(message_list), 200
    except mysql.connector.Error as e:
        logger.error(f"Database error: {e}")
        return jsonify({"message": "Failed to fetch messages"}), 500
    finally:
        cursor.close()


@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

# Close the database connection when the application exits
if conn and conn.is_connected():
    conn.close()
    logger.info("Database connection closed")
