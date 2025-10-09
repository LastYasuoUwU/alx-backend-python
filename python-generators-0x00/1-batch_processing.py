import mysql.connector

def stream_users_in_batches(batch_size):
    """A generator function that yields user data in batches of a specified size.

    Args:
        batch_size (int): The number of users to include in each batch.

    Yields:
        list: A list of user data dictionaries, each containing 'id','name' and 'mail'.
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
    batch=[]
    for row in cursor:
        batch.append(row)
        if len(batch) == batch_size:
            yield batch
            batch = []
                
    cursor.close()
    connection.close()
    

def batch_processing(batch_size):
    """Proccesses and print user data in batches.
    
    Args:
        batch_size (int): The number of users to include in each batch.
    """
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            print(user)