import sqlite3

class DatabaseConnection:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None

    def __enter__(self):
        # Open database connection
        self.connection = sqlite3.connect(self.db_name)
        return self.connection.cursor()

    def __exit__(self, exc_type, exc_value, traceback):
        # Commit changes and close connection
        if self.connection:
            self.connection.commit()
            self.connection.close()
        # If exception occurred, print it (optional)
        if exc_type:
            print(f"An error occurred: {exc_value}")
        # Returning False means exceptions (if any) will not be suppressed
        return False


# --- Usage Example ---
if __name__ == "__main__":
    # Create sample database and table for demo
    with sqlite3.connect("example.db") as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)")
        conn.execute("INSERT INTO users (name) VALUES ('Alice'), ('Bob'), ('Charlie')")
        conn.commit()

    # Use our custom context manager
    with DatabaseConnection("example.db") as cursor:
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        print("Users from database:")
        for row in results:
            print(row)
