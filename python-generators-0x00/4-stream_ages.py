#!/usr/bin/env python3
"""
Memory-efficient aggregation using generators: stream ages and compute average.
"""

import seed


def stream_user_ages():
    """
    Generator that yields user ages one by one from the database without
    loading the entire dataset into memory.
    """
    connection = None
    cursor = None
    try:
        connection = seed.connect_to_prodev()
        if not connection:
            return
        cursor = connection.cursor()
        cursor.execute("SELECT age FROM user_data")
        # Loop 1: stream ages lazily
        for row in cursor:
            # row is a tuple like (age,)
            age = row[0]
            # Ensure int type for arithmetic
            yield int(age)
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def compute_and_print_average_age():
    """
    Consumes the stream_user_ages generator to compute and print the average age
    without loading all rows into memory. Uses at most one loop here.
    """
    total_age = 0
    count = 0
    # Loop 2: single pass aggregation
    for age in stream_user_ages():
        total_age += age
        count += 1

    if count == 0:
        print("Average age of users: 0")
        return

    average = total_age / count
    # Print as integer if whole number, else two decimals
    if float(average).is_integer():
        avg_str = str(int(average))
    else:
        avg_str = f"{average:.2f}"
    print(f"Average age of users: {avg_str}")


if __name__ == "__main__":
    compute_and_print_average_age()
