import time
import sqlite3 
import functools


query_cache = {}


def with_db_connection(func):
    """Decorator that provides a database connection to the wrapped function"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Create a connection to an in-memory SQLite database
        conn = sqlite3.connect(':memory:')
        
        # Create a sample users table for testing
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT,
                email TEXT
            )
        ''')
        cursor.execute("INSERT INTO users (name, email) VALUES ('Alice', 'alice@example.com')")
        cursor.execute("INSERT INTO users (name, email) VALUES ('Bob', 'bob@example.com')")
        cursor.execute("INSERT INTO users (name, email) VALUES ('Charlie', 'charlie@example.com')")
        conn.commit()
        
        try:
            # Call the original function with the connection
            result = func(conn, *args, **kwargs)
            return result
        finally:
            conn.close()
    
    return wrapper


def cache_query(func):
    """
    Decorator that caches database query results based on the SQL query string.
    
    How it works:
    1. Extracts the 'query' parameter from function arguments
    2. Checks if this query has been executed before (exists in cache)
    3. If cached: returns the stored result immediately
    4. If not cached: executes the query, stores result, then returns it
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Get the query string from kwargs
        query = kwargs.get('query')
        
        # Check if this query result is already in the cache
        if query in query_cache:
            print(f"📦 Cache HIT! Using cached result for query: {query[:50]}...")
            return query_cache[query]
        
        # If not in cache, execute the function
        print(f"🔍 Cache MISS! Executing query: {query[:50]}...")
        result = func(*args, **kwargs)
        
        # Store the result in cache for future use
        query_cache[query] = result
        print(f"💾 Result cached for future use!")
        
        return result
    
    return wrapper


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    """Fetch users from database with automatic caching"""
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


# Test the caching functionality
print("=" * 60)
print("FIRST CALL - Will execute the query and cache the result")
print("=" * 60)
start_time = time.time()
users = fetch_users_with_cache(query="SELECT * FROM users")
end_time = time.time()
print(f"Result: {users}")
print(f"Time taken: {(end_time - start_time) * 1000:.2f}ms\n")

print("=" * 60)
print("SECOND CALL - Will use the cached result (much faster!)")
print("=" * 60)
start_time = time.time()
users_again = fetch_users_with_cache(query="SELECT * FROM users")
end_time = time.time()
print(f"Result: {users_again}")
print(f"Time taken: {(end_time - start_time) * 1000:.2f}ms\n")

print("=" * 60)
print("DIFFERENT QUERY - Will execute and cache separately")
print("=" * 60)
start_time = time.time()
specific_user = fetch_users_with_cache(query="SELECT * FROM users WHERE name='Alice'")
end_time = time.time()
print(f"Result: {specific_user}")
print(f"Time taken: {(end_time - start_time) * 1000:.2f}ms\n")

print("=" * 60)
print("Current cache contents:")
print("=" * 60)
for query, result in query_cache.items():
    print(f"Query: {query}")
    print(f"Cached Result: {result}\n")