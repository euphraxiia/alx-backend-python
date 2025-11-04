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

def transactional(func):
    """
    Decorator that manages database transactions by automatically committing or rolling back changes.
    
    If the function raises an error, the transaction is rolled back.
    If the function completes successfully, the transaction is committed.
    
    Args:
        func: The function to be decorated
        
    Returns:
        Wrapped function that handles transactions automatically
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # The connection should be the first argument (conn)
        conn = args[0] if args else None
        
        try:
            # Execute the function
            result = func(*args, **kwargs)
            # If successful, commit the transaction
            conn.commit()
            return result
        except Exception as e:
            # If an error occurs, rollback the transaction
            conn.rollback()
            raise e
    
    return wrapper

@with_db_connection 
@transactional 
def update_user_email(conn, user_id, new_email): 
    cursor = conn.cursor() 
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id)) 

#### Update user's email with automatic transaction handling 

update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')

