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

@with_db_connection 
def get_user_by_id(conn, user_id): 
    cursor = conn.cursor() 
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,)) 
    return cursor.fetchone() 

#### Fetch user by ID with automatic connection handling 

user = get_user_by_id(user_id=1)
print(user)

