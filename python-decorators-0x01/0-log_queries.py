import sqlite3
import functools

#### decorator to log SQL queries
def log_queries(func):
    """ 
    decorator log_queries that logs the SQL query before executing it.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = args[0] if args else kwargs.get('query', '')
        print(f"Executing SQL Query: {query}")
        return func(*args, **kwargs)
    return wrapper


# Function to initialize the database
def init_database():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL
        )
    ''')
    
    # Insert some sample data (optional)
    cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", ("Alice", "alice@example.com"))
    cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", ("Bob", "bob@example.com"))
    
    conn.commit()
    conn.close()


@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


# Initialize the database first
init_database()

#### fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users;")
print(users)