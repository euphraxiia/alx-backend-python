#!/usr/bin/env python3
"""
Batch processing functions to fetch and process user data in batches.
"""

import mysql.connector
from mysql.connector import Error
import sys


def stream_users_in_batches(batch_size):
    """
    Generator function that fetches rows from user_data table in batches.
    
    Args:
        batch_size (int): Number of rows to fetch per batch
    
    Yields:
        list: List of dictionaries containing user data for each batch
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
            
            # Single loop to yield batches
            while True:
                batch = cursor.fetchmany(batch_size)
                if not batch:
                    break
                yield batch
    
    except Error as e:
        print(f"Error: {e}", file=sys.stderr)
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


def batch_processing(batch_size):
    """
    Generator function that processes batches to filter users over age 25.
    
    Args:
        batch_size (int): Number of rows to fetch per batch
    
    Yields:
        dict: Dictionary containing user data for users with age > 25
    """
    # Loop over batches
    for batch in stream_users_in_batches(batch_size):
        # Loop over users in batch to filter
        for user in batch:
            if user['age'] > 25:
                yield user

