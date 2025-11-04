import time
import sqlite3 
import functools

query_cache = {}

def with_db_connection(func):
    """
    Decorator that automatically handles opening and closing database connections.
    
    Opens a database connection, passes it to the function as the first argument,
    and closes it after the function completes.
    
    Args:
        func: The function to be decorated
        
    Returns:
        Wrapped function that handles database connection automatically
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Open database connection
        conn = sqlite3.connect('users.db')
        try:
            # Call the function with connection as first argument
            return func(conn, *args, **kwargs)
        finally:
            # Always close the connection, even if an error occurs
            conn.close()
    
    return wrapper

def cache_query(func):
    """
    Decorator that caches the results of database queries to avoid redundant calls.
    
    Caches query results based on the SQL query string. If the same query is executed
    again, the cached result is returned instead of executing the query again.
    
    Args:
        func: The function to be decorated
        
    Returns:
        Wrapped function that caches query results
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract the query string from kwargs or args
        query = kwargs.get('query') or (args[1] if len(args) > 1 else None)
        
        # Check if query result is in cache
        if query in query_cache:
            return query_cache[query]
        
        # Execute the function and cache the result
        result = func(*args, **kwargs)
        query_cache[query] = result
        return result
    
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

#### First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

#### Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")

