import time
import sqlite3 
import functools

# Decorator to automatically provide database connection
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Create a connection to SQLite database
        conn = sqlite3.connect('users.db')
        try:
            # Pass the connection to the decorated function
            result = func(conn, *args, **kwargs)
            return result
        finally:
            # Always close the connection
            conn.close()
    return wrapper

# Decorator to retry function on failure
def retry_on_failure(retries=3, delay=2):
    """
    Decorator that retries a function if it raises an exception.
    
    Args:
        retries: Number of retry attempts (default: 3)
        delay: Delay in seconds between retries (default: 2)
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            while attempt < retries:
                try:
                    # Try to execute the function
                    result = func(*args, **kwargs)
                    return result
                except Exception as e:
                    attempt += 1
                    if attempt >= retries:
                        # If we've exhausted all retries, raise the exception
                        print(f"Failed after {retries} attempts. Error: {e}")
                        raise
                    else:
                        # Print retry message and wait before trying again
                        print(f"Attempt {attempt} failed: {e}. Retrying in {delay} seconds...")
                        time.sleep(delay)
        return wrapper
    return decorator

# Setup: Create a sample database and table
# def setup_database():
#     conn = sqlite3.connect('users.db')
#     cursor = conn.cursor()
    
#     # Drop table if it exists and create a fresh one
#     cursor.execute("DROP TABLE IF EXISTS users")
#     cursor.execute("""
#         CREATE TABLE users (
#             id INTEGER PRIMARY KEY,
#             name TEXT NOT NULL,
#             email TEXT NOT NULL
#         )
#     """)
    
#     # Insert sample data
#     cursor.execute("INSERT INTO users (name, email) VALUES ('Alice', 'alice@example.com')")
#     cursor.execute("INSERT INTO users (name, email) VALUES ('Bob', 'bob@example.com')")
#     cursor.execute("INSERT INTO users (name, email) VALUES ('Charlie', 'charlie@example.com')")
    
#     conn.commit()
#     conn.close()
#     print("Database setup complete!\n")

# Function decorated with both decorators
@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

# Main execution
if __name__ == "__main__":
    # Setup the database first
    # setup_database()
    
    # Attempt to fetch users with automatic retry on failure
    try:
        users = fetch_users_with_retry()
        print("Users fetched successfully:")
        for user in users:
            print(f"  ID: {user[0]}, Name: {user[1]}, Email: {user[2]}")
    except Exception as e:
        print(f"Operation failed completely: {e}")