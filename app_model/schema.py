# CREATE
def create_user_table(conn):
    cur = conn.cursor()
    sql = '''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        role TEXT DEFAULT 'user',
        profile_picture BLOB,
        language TEXT DEFAULT 'English'
    );'''
    cur.execute(sql)
    conn.commit()

def create_login_history_table(conn):
    cur = conn.cursor()
    sql = '''CREATE TABLE IF NOT EXISTS login_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        success INTEGER NOT NULL,
        failed_attempts INTEGER DEFAULT 0,
        account_locked INTEGER DEFAULT 0      
    );'''
    cur.execute(sql)
    conn.commit()