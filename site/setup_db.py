import sqlite3
import os
import sys
import stat

def create_or_open_database(db_path):
    """ Create a new SQLite database or open an existing one. """
    connection = sqlite3.connect(db_path)
    return connection

def setup_database(conn):
    """ Setup the database table if it doesn't exist. """
    cursor = conn.cursor()
    # Define the SQL statement for creating the table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            firstName TEXT,
            lastName TEXT,
            phoneNumber TEXT,
            item TEXT,
            transactionId TEXT,
            clientIP TEXT,
            submittedAt INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()

def insert_initial_transaction(conn, transaction_id):
    """ Insert the initial transaction ID if the table is empty. """
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM orders")
    if cursor.fetchone()[0] == 0:  # Check if the table is empty
        cursor.execute("INSERT INTO orders (transactionId) VALUES (?)", (transaction_id,))
        conn.commit()
        print("Initial transaction ID inserted successfully.")
    else:
        print("The table is not empty. Initial insertion skipped.")

def check_and_fix_permissions(db_path):
    """ Check and fix file permissions for www-data access. """
    # Set permissions to 664 to allow read/write for owner and group
    os.chmod(db_path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IWGRP)
    # Ensure the www-data user can access the file (assuming www-data is the group)
    os.chown(db_path, -1, os.getgid())  # Change group to the current user's group

def main(db_path, transaction_id):
    """ Main function to handle database initialization and setup. """
    conn = create_or_open_database(db_path)
    setup_database(conn)
    insert_initial_transaction(conn, transaction_id)
    check_and_fix_permissions(db_path)
    conn.close()
    print("Database setup complete.")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python setup_db.py <path_to_database> <initial_transaction_id>")
        sys.exit(1)

    db_path = sys.argv[1]
    initial_transaction_id = sys.argv[2]
    main(db_path, initial_transaction_id)

