# Python Generators - Database Seeding

This project implements a database seeding script for setting up the ALX_prodev MySQL database with user data.

## Overview

The `seed.py` script provides functions to:
- Connect to MySQL database server
- Create the `ALX_prodev` database
- Create the `user_data` table with required fields
- Populate the database with data from `user_data.csv`

## Database Schema

### Database: ALX_prodev

### Table: user_data

| Field    | Type         | Constraints              |
|----------|--------------|--------------------------|
| user_id  | VARCHAR(36)  | PRIMARY KEY, INDEXED     |
| name     | VARCHAR(255) | NOT NULL                 |
| email    | VARCHAR(255) | NOT NULL                 |
| age      | DECIMAL(10,0)| NOT NULL                 |

## Requirements

- Python 3.x
- MySQL Server
- mysql-connector-python library

## Installation

1. Install MySQL server on your system
2. Install the required Python library:
```bash
pip3 install mysql-connector-python
```

3. Update database credentials in `seed.py` if needed (default: localhost, user: root, password: empty)

## Usage

### Running the seed script

```bash
python3 0-main.py
```

Or interactively:

```python
import seed

# Connect to MySQL server
connection = seed.connect_db()
if connection:
    # Create database
    seed.create_database(connection)
    connection.close()
    
    # Connect to ALX_prodev database
    connection = seed.connect_to_prodev()
    
    if connection:
        # Create table
        seed.create_table(connection)
        
        # Insert data from CSV
        seed.insert_data(connection, 'user_data.csv')
        
        connection.close()
```

## Functions

### `connect_db()`
Connects to the MySQL database server.
- **Returns:** MySQL connection object or None on failure

### `create_database(connection)`
Creates the `ALX_prodev` database if it doesn't exist.
- **Parameters:** `connection` - MySQL connection object

### `connect_to_prodev()`
Connects to the `ALX_prodev` database.
- **Returns:** MySQL connection object or None on failure

### `create_table(connection)`
Creates the `user_data` table with required fields if it doesn't exist.
- **Parameters:** `connection` - MySQL connection object

### `insert_data(connection, csv_file)`
Inserts data from the CSV file into the database, skipping duplicates.
- **Parameters:** 
  - `connection` - MySQL connection object
  - `csv_file` - Path to the CSV file containing user data

## CSV Format

The `user_data.csv` file should have the following format:
```csv
user_id,name,email,age
<uuid>,<name>,<email>,<age>
```

Example:
```csv
user_id,name,email,age
00234e50-34eb-4ce2-94ec-26e3fa749796,Dan Altenwerth Jr.,Molly59@gmail.com,67
```

## Notes

- The script checks for existing records before inserting to avoid duplicates
- UUIDs should be in standard UUID format (36 characters)
- Make sure MySQL server is running before executing the script

