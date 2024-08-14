import mysql.connector

# MySQL database connection configuration
config = {
    "host": "localhost",
    "user": "root",
    "password": "new_password",
    "database": "testSQLDB"
}

# Define the table name you want to check


try:
    # Establish a connection to the MySQL database
    connection = mysql.connector.connect(**config)

    # Create a cursor object to interact with the database
    cursor = connection.cursor()

    # Execute a query to retrieve all rows from the specified table
    query = f"select max(postalcode) from offices;"
    cursor.execute(query)

    # Fetch all rows from the result set
    rows = cursor.fetchall()
    
   
    for row in rows:
        print(row)


    # if len(rows) == 0:
    #     print(f"No rows found in the '{table_name}' table.")
    # else:
    #     print(f"Found {len(rows)} rows in the '{table_name}' table.")
        # You can iterate through 'rows' to process the data as needed

except mysql.connector.Error as err:
    print(f"Error: {err}")
finally:
    # Close the cursor and connection when done
    if cursor:
        cursor.close()
    if connection:
        connection.close()