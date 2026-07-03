import bcrypt

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
def add_user(conn, name, hash):
    cur = conn.cursor()
    sql = 'INSERT INTO users (username, password_hash) VALUES (?, ?)'
    cur.execute(sql, (name, hash)); conn.commit()

# SELECT
def get_all_users(conn):
    cur = conn.cursor()
    cur.execute('SELECT * FROM users')
    return cur.fetchall()

def get_user(conn, name):
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE username = ?', (name,))
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

