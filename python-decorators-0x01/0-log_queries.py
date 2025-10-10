import sqlite3
import functools

#### decorator to log SQL queries
def log_queries(func):
    """ 
    decorator log_queries that logs the SQL query before executing it.
    """
    def wrapper(*args, **kwargs):
        print("Starting query execution...")
        return func(*args, **kwargs)
    return wrapper


# Function to initialize the database
# def init_database():
#     conn = sqlite3.connect('users.db')
#     cursor = conn.cursor()
    
#     # Create users table
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS users (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             name TEXT NOT NULL,
#             email TEXT NOT NULL
#         )
#     ''')
    
#     # Insert some sample data (optional)
#     cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", ("Alice", "alice@example.com"))
#     cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", ("Bob", "bob@example.com"))
    
#     conn.commit()
#     conn.close()

# Initialize the database first
# init_database()

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

#### fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users;")
print(f"users: {users}")
print("Query execution finished ✅")