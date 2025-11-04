import sqlite3

class ExecuteQuery:
    """
    A reusable context manager that takes a query as input and executes it,
    managing both connection and query execution.
    """
    
    def __init__(self, query, params=None, db_name='users.db'):
        """
        Initialize the ExecuteQuery context manager.
        
        Args:
            query: SQL query string to execute
            params: Parameters for the query (tuple, list, or None)
            db_name: Name of the database file (default: 'users.db')
        """
        self.query = query
        self.params = params
        self.db_name = db_name
        self.conn = None
        self.results = None
    
    def __enter__(self):
        """
        Open the database connection, execute the query, and return the results.
        
        Returns:
            The query results
        """
        self.conn = sqlite3.connect(self.db_name)
        cursor = self.conn.cursor()
        
        # Execute query with parameters if provided
        if self.params is not None:
            cursor.execute(self.query, self.params)
        else:
            cursor.execute(self.query)
        
        # Fetch all results
        self.results = cursor.fetchall()
        return self.results
    
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

# Use the context manager with the query and parameter
with ExecuteQuery("SELECT * FROM users WHERE age > ?", (25,)) as results:
    print(results)

