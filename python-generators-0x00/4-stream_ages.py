def stream_user_ages():
    """
    Generator that yields user age one by one from the table user_data.    
    """
    seed = __import__('seed')
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT age FROM user_data")
    for row in cursor:
        yield row['age']
    connection.close()

if __name__ == "__main__":
    total_ages = 0
    count = 0
    for age in stream_user_ages():
        total_ages += age
        count += 1
    average_age = total_ages / count
    print(f"Average age of users: {average_age}")