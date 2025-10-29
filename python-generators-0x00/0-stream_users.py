#!/usr/bin/env python3
"""
Generator function to stream rows from user_data table one by one.
"""

import mysql.connector
from mysql.connector import Error


def stream_users():
    """
    Generator function that streams rows from the user_data table one by one.
    
    Yields:
        dict: Dictionary containing user_id, name, email, and age
    """
    connection = None
    cursor = None
    
    try:
        # Connect to ALX_prodev database
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='ALX_prodev',
            port=3306
        )
        
        if connection.is_connected():
            # Use dictionary cursor to return rows as dictionaries
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT user_id, name, email, age FROM user_data")
            
            # Single loop to yield rows one by one
            for row in cursor:
                yield row
    
    except Error as e:
        print(f"Error: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

