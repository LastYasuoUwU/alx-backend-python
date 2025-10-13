import sqlite3

class ExecuteQuery:
    def __init__(self, db_name, query, params=None):
        self.db_name = db_name
        self.query = query
        self.params = params or ()
        self.connection = None
        self.cursor = None
        self.results = None

    def __enter__(self):
        # Open database connection and cursor
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        
        # Execute query safely with parameters
        self.cursor.execute(self.query, self.params)
        self.results = self.cursor.fetchall()
        return self.results  # Returned to the 'as' variable in the with statement

    def __exit__(self, exc_type, exc_value, traceback):
        # Close cursor and connection
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        
        # Print any error (optional)
        if exc_type:
            print(f"An error occurred: {exc_value}")
        
        # Return False to let exceptions propagate
        return False


# --- Usage Example ---
if __name__ == "__main__":
    # Create a demo database
    with sqlite3.connect("example.db") as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
        conn.execute("DELETE FROM users")  # Clear table for demo
        conn.executemany("INSERT INTO users (name, age) VALUES (?, ?)", [
            ('Alice', 22),
            ('Bob', 30),
            ('Charlie', 28),
            ('Diana', 19)
        ])
        conn.commit()

    # Use our custom context manager to execute a query
    query = "SELECT * FROM users WHERE age > ?"
    params = (25,)

    with ExecuteQuery("example.db", query, params) as results:
        print("Users older than 25:")
        for row in results:
            print(row)
