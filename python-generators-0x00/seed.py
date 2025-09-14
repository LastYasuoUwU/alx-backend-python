import mysql.connector
import csv
import uuid

# ----------------------------
# 1. Connect to MySQL server
# ----------------------------
def connect_db():
    return mysql.connector.connect(
        host="localhost",   # change if needed
        user="root",        # your MySQL username
        password="M@shiSou9ek" # your MySQL password
    )

# ----------------------------
# 2. Create database ALX_prodev
# ----------------------------
def create_database(connection):
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
    cursor.close()

# ----------------------------
# 3. Connect directly to ALX_prodev
# ----------------------------
def connect_to_prodev():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="M@shiSou9ek",
        database="ALX_prodev"
    )

# ----------------------------
# 4. Create table user_data
# ----------------------------
def create_table(connection):
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_data (
            user_id CHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL UNIQUE,
            age DECIMAL(3,0) NOT NULL,
            INDEX idx_user_id (user_id)
        )
    """)
    connection.commit()
    cursor.close()

# ----------------------------
# 5. Insert data into table
# ----------------------------
def insert_data(connection, data):
    cursor = connection.cursor()
    try:
        cursor.execute("""
            INSERT INTO user_data (user_id, name, email, age)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
            name=VALUES(name), age=VALUES(age)
        """, data)
        connection.commit()
    except Exception as e:
        print("Insert failed:", e)
    finally:
        cursor.close()

# ----------------------------
# 6. Generator to stream rows
# ----------------------------
def stream_rows(connection):
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")
    for row in cursor:
        yield row  # yield one row at a time
    cursor.close()

# ----------------------------
# 7. Main seeding logic
# ----------------------------
def main():
    # Step 1: connect to MySQL server
    conn = connect_db()
    create_database(conn)
    conn.close()

    # Step 2: connect to ALX_prodev
    conn = connect_to_prodev()
    create_table(conn)

    # Step 3: read CSV and insert data
    with open("user_data.csv", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            user_id = str(uuid.uuid4())  # generate UUID
            insert_data(conn, (user_id, row["name"], row["email"], row["age"]))

    # Step 4: stream rows with generator
    print("Streaming rows one by one:")
    for row in stream_rows(conn):
        print(row)

    conn.close()


if __name__ == "__main__":
    main()
