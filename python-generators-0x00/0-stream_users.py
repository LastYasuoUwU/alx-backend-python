import mysql.connector

def stream_users():
    """
    Generator that streams rows from the user_data table one by one.
    Uses a single loop and the yield keyword.
    """
    # Connect to ALX_prodev database
    connection = mysql.connector.connect(
        host="localhost",
        user="root",          # change this to your MySQL username
        password="M@shiSou9ek",  # change this to your MySQL password
        database="ALX_prodev"
    )
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data;")

    # Single loop - yield one row at a time
    for row in cursor:
        yield row

    cursor.close()
    connection.close()



# Example usage
if __name__ == "__main__":
    for user in stream_users():
        print(user)
