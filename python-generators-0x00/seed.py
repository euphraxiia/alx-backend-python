#!/usr/bin/env python3
"""
Database seeding script for ALX_prodev database.
Creates database, table, and populates with user data from CSV.
"""

import mysql.connector
from mysql.connector import Error
import csv
import os


def connect_db():
    """
    Connects to the MySQL database server.
    
    Returns:
        connection: MySQL connection object or None if connection fails
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            port=3306
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None


def create_database(connection):
    """
    Creates the database ALX_prodev if it does not exist.
    
    Args:
        connection: MySQL connection object
    """
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        cursor.close()
        print("Database ALX_prodev created successfully")
    except Error as e:
        print(f"Error creating database: {e}")


def connect_to_prodev():
    """
    Connects to the ALX_prodev database in MySQL.
    
    Returns:
        connection: MySQL connection object or None if connection fails
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='ALX_prodev',
            port=3306
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to ALX_prodev database: {e}")
        return None


def create_table(connection):
    """
    Creates a table user_data if it does not exist with the required fields.
    
    Args:
        connection: MySQL connection object
    """
    try:
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS user_data (
            user_id VARCHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL(10, 0) NOT NULL,
            INDEX idx_user_id (user_id)
        )
        """
        cursor.execute(create_table_query)
        connection.commit()
        cursor.close()
        print("Table user_data created successfully")
    except Error as e:
        print(f"Error creating table: {e}")


def insert_data(connection, data):
    """
    Inserts data from CSV file into the database if it does not exist.
    
    Args:
        connection: MySQL connection object
        data: Path to the CSV file containing user data
    """
    if not os.path.exists(data):
        print(f"Error: CSV file {data} not found")
        return
    
    try:
        cursor = connection.cursor()
        
        with open(data, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            
            for row in csv_reader:
                user_id = row.get('user_id', '').strip()
                name = row.get('name', '').strip()
                email = row.get('email', '').strip()
                age = row.get('age', '').strip()
                
                # Check if record already exists
                check_query = "SELECT user_id FROM user_data WHERE user_id = %s"
                cursor.execute(check_query, (user_id,))
                if cursor.fetchone():
                    continue  # Skip if already exists
                
                # Insert new record
                insert_query = """
                INSERT INTO user_data (user_id, name, email, age)
                VALUES (%s, %s, %s, %s)
                """
                cursor.execute(insert_query, (user_id, name, email, age))
        
        connection.commit()
        cursor.close()
        print(f"Data inserted successfully from {data}")
    except Error as e:
        print(f"Error inserting data: {e}")
    except Exception as e:
        print(f"Error reading CSV file: {e}")

