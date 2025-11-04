import sqlite3

class DatabaseConnection:
    """
    A class-based context manager for handling database connections.
    
    Automatically opens and closes database connections using the with statement.
    """
    
    def __init__(self, db_name='users.db'):
        """
        Initialize the DatabaseConnection context manager.
        
        Args:
            db_name: Name of the database file (default: 'users.db')
        """
        self.db_name = db_name
        self.conn = None
    
    def __enter__(self):
        """
        Open the database connection when entering the with statement.
        
        Returns:
            The database connection object
        """
        self.conn = sqlite3.connect(self.db_name)
        return self.conn
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Close the database connection when exiting the with statement.
        
        Args:
            exc_type: Exception type if an exception occurred
            exc_val: Exception value if an exception occurred
            exc_tb: Exception traceback if an exception occurred
            
        Returns:
            False to propagate exceptions, True to suppress them
        """
        if self.conn:
            self.conn.close()
        return False  # Don't suppress exceptions

# Use the context manager with the with statement
with DatabaseConnection() as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    
    # Print the results from the query
    print(results)

