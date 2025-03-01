from flask import flash, session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

# Database configuration
db_config = {
    'host': 'mysql',
    'user': 'root',
    'password': 'rootpassword',
    'database': 'mydatabase'
}


# Helper function to get a database connection
def get_db_connection():
    conn = mysql.connector.connect(**db_config)
    return conn


# Function for user registration
def register_user(username, password):
    hashed_password = generate_password_hash(password)
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s)",
            (username, hashed_password)
        )
        conn.commit()
        flash('Account created! You can now log in.', 'success')
        return True
    except mysql.connector.Error as err:
        flash(f'Error creating account: {err}', 'danger')
        return False
    finally:
        cursor.close()
        conn.close()


# Function for user login
def login_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user and check_password_hash(user['password'], password):
        session['username'] = username
        flash('Logged in successfully!', 'success')
        return True
    else:
        flash('Invalid username or password!', 'danger')
        return False


# Function for user logout
def logout_user():
    session.pop('username', None)
    flash('You have been logged out.', 'info')


# Function to get user_id from username
def get_user_id(username):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT id FROM users WHERE username = %s",
                   (username,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user:
        return user['id']
    else:
        return None
