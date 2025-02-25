# service.py
import database

def get_user_name(user_id):
    conn = database.connect()
    user = conn.query("SELECT name FROM users WHERE id=?", user_id)
    return user.name
