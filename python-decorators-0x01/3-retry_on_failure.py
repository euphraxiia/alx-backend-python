import time
import sqlite3 
import functools

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

def retry_on_failure(retries=3, delay=2):
    """
    Decorator that retries database operations if they fail due to transient errors.
    
    Args:
        retries: Number of times to retry the function (default: 3)
        delay: Delay in seconds between retries (default: 2)
        
    Returns:
        Decorator function
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            
            # Try to execute the function up to 'retries' times
            for attempt in range(retries):
                try:
                    # Execute the function
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    # If not the last attempt, wait before retrying
                    if attempt < retries - 1:
                        time.sleep(delay)
                    # Otherwise, raise the last exception
                    else:
                        raise last_exception
            
            # This should never be reached, but just in case
            if last_exception:
                raise last_exception
        
        return wrapper
    return decorator

@with_db_connection
@retry_on_failure(retries=3, delay=1)

def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

#### attempt to fetch users with automatic retry on failure

users = fetch_users_with_retry()
print(users)

