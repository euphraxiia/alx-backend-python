#!/usr/bin/env python3
"""
Lazy pagination function to fetch paginated data from user_data table.
"""

import seed


def paginate_users(page_size, offset):
    """
    Fetches a page of users from the database.
    
    Args:
        page_size (int): Number of rows to fetch per page
        offset (int): Offset for pagination
    
    Returns:
        list: List of dictionaries containing user data
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows


def lazy_paginate(page_size):
    """
    Generator function that implements lazy pagination, fetching pages only when needed.
    
    Args:
        page_size (int): Number of rows to fetch per page
    
    Yields:
        list: List of dictionaries containing user data for each page
    """
    offset = 0
    
    # Single loop to fetch and yield pages lazily
    while True:
        page = paginate_users(page_size, offset)
        
        # If no more data, stop
        if not page:
            break
        
        yield page
        offset += page_size


# Alias for test compatibility
lazy_pagination = lazy_paginate

