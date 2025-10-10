import sqlite3 
import functools
from datetime import datetime
import time

def with_db_connection(func):
    """
    Decorator opens a database connection, passes it to the decorated function 
    and ensures the connection is closed after use.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] Opening database connection...")
        time.sleep(2)  # Simulate connection delay
        
        conn = sqlite3.connect('users.db')
        print("Connection opened ✅")
        
        try:
            result = func(conn, *args, **kwargs)
            return result
        finally:
            conn.close()
            print("Closing database connection...")
            time.sleep(1)  # Simulate closing delay
            print("Database connection closed ✅")
    return wrapper


def transactional(func):
    """
    Decorator ensures a function running a database operation is wrapped in a transaction.
    If the function raises an error, rollback; otherwise, commit the transaction.
    """
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{timestamp}] Starting a new transaction...")
            conn.execute("BEGIN;")
            result = func(conn, *args, **kwargs)
            conn.commit()
            print("Transaction committed ✅")
            return result
        except Exception as e:
            conn.rollback()
            print(f"Transaction rolled back due to error: {e}")
            raise
    return wrapper


@with_db_connection 
@transactional 
def update_user_email(conn, user_id, new_email): 
    cursor = conn.cursor() 
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id)) 

#### Update user's email with automatic transaction handling 
update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')