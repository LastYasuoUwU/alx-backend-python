import sqlite3 
import functools
from datetime import datetime
import asyncio

def with_db_connection(func):
    """ 
    Decorator opens a database connection, passes it to the decorated function and ensure the connection is closed after use.
    """
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            timestimp = datetime.now().strftime("%Y-%m-%d %H:%M")
            print(f"[{timestimp}] Opening database connection...")
            await asyncio.sleep(4) #simulate opening connection to database
            print("Connection opened  ✅")
            result = await func(conn, *args, **kwargs)
            await asyncio.sleep(2) #simulate execution of the query
            print("Query execution finished ✅")
            return result
        finally:
            conn.close()
            print("Closing database connection.")
            await asyncio.sleep(4) #simulate closing connection to database
            print("Connection closed  ✅")
    return wrapper


@with_db_connection 
async def get_user_by_id(conn, user_id): 
    cursor = conn.cursor() 
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,)) 
    return cursor.fetchone() 

#### Fetch user by ID with automatic connection handling 
user = asyncio.run(get_user_by_id(user_id=1))
print(user)