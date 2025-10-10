import sqlite3
import functools

#### decorator to log SQL queries
def log_queries(func):
    """ 
    Create a decorator to log all SQL queries executed by a function.
    Learn to intercept function calls to enhance observability.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get('query', args[0] if args else None)
        print(f"Executing SQL Query: {query}")
        result = func(*args, **kwargs)
        print("Query execution finished ✅")
        return result
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