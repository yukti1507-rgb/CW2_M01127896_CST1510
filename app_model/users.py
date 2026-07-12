import bcrypt
from datetime import datetime, timedelta
from app_model.db import get_connection


# PASSWORD HASHING
def generate_hash(psw):
    byte_psw = psw.encode('utf-8')
    salt = bcrypt.gensalt(rounds=12)
    hash = bcrypt.hashpw(byte_psw, salt)
    return hash.decode('utf-8')

def is_valid_hash(psw, hash):
    hash_ = hash.encode('utf-8')
    byte_psw = psw.encode('utf-8')
    is_valid = bcrypt.checkpw(byte_psw, hash_)
    return is_valid

# USER CRUD
# INSERT (parameterized — prevents SQL injection)
def add_user(conn, username, email, password_hash):
    cur = conn.cursor()
    sql = 'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)'
    cur.execute(sql, (username, email, password_hash)); conn.commit()

# User table indexes
USER_ID = 0
USERNAME = 1
EMAIL = 2
PASSWORD_HASH = 3
ROLE = 4
PROFILE_PICTURE = 5
LANGUAGE = 6

# SELECT
def get_all_users(conn):
    cur = conn.cursor()
    cur.execute('SELECT * FROM users')
    return cur.fetchall()

def get_user(conn, username):
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE username = ?', (username,))
    return cur.fetchone()

def get_email(conn, email):
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE email = ?', (email,))
    return cur.fetchone()

# UPDATE
def update_user(conn, old_name, new_name):
    cur = conn.cursor()
    cur.execute('UPDATE users SET username = ? WHERE username = ?', (new_name, old_name))
    conn.commit()

# DELETE
def delete_user(conn, user_name):
    cur = conn.cursor()
    cur.execute('DELETE FROM users WHERE username = ?', (user_name,))
    conn.commit()

# REGISTER/LOGIN
def register_user_terminal():
    name = input('Enter your name: > ')
    password = input('Enter your password: > ')
    password2 = input("Confirm your password: >")

    letters_only = ""
    for char in name:
        if char.isalpha():
            letters_only += char

    if name == "admin":
        print("This username is reserved. Please choose another.")
        return
    if password != password2:
        print("Passwords do not match.")
        return
    if len(password) < 8:
        print("Password must be at least 8 characters long.")
        return
    if not any(c.isupper() for c in password):
        print("Password must contain at least one uppercase letter.")
        return
    if not any(c.islower() for c in password):
        print("Password must contain at least one lowercase letter.")
        return
    if not any(c.isdigit() for c in password):
        print("Password must contain at least one number.")
        return
    if not any(c in "!@#$%^&*()-_=+[]{}|;:'\",.<>?/`~" for c in password):
        print("Password must contain at least one special character.")
        return
    if name.lower() in password.lower():
        print("Password cannot contain your username.")
        return
    if letters_only.lower() in password.lower():
        print("Password cannot be similar to username.")
        return
    if "password" in password.lower():
        print("Password cannot contain the word 'password'.")
        return
        
    hash_password = generate_hash(password)
    with open('DATA/users.txt', 'a') as f:
        f.write(f'{name},{hash_password}\n')
    print('User successfully registered!')

def login_user_terminal():
    name = input('Enter your name: > ')
    password = input('Enter your password: > ')
    with open('DATA/users.txt', 'r') as f:
        users = f.readlines()
    for user in users:
        user_name, user_hash = user.strip().split(',')
        if name == user_name and is_valid_hash(password, user_hash):
            return True
    return False

#Login history table indexs

LOGIN_ID = 0
LOGIN_USER_ID = 1
LOGIN_TIME = 2
LOGIN_SUCCESS = 3
LOGIN_FAILED_ATTEMPTS = 4
LOGIN_ACCOUNT_LOCKED = 5
LOGIN_LOCKED_UNTIL = 6

def save_login_attempt(conn, user_id, success, failed_attempts, account_locked, locked_until):
    cur = conn.cursor()
    sql = 'INSERT INTO login_history (user_id, success, failed_attempts, account_locked, locked_until) VALUES (?, ?, ?, ?, ?)'
    param = (user_id, success, failed_attempts, account_locked, locked_until)
    cur.execute(sql, param)
    conn.commit()

