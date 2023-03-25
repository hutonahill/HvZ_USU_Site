import mysql.connector

def SQL_SELECT(connection:mysql.connector.connection.MySQLConnection, query:str, params:tuple=None):
    """
    Executes a SELECT query on a MySQL database using prepared statements.

    :param connection: a MySQL database connection object
    :param query: a SELECT query string with placeholders for parameters
    :param params: a tuple of parameters for the query (optional)
    :return: a nested list of query results, or a string error message
    """
    try:
        # Create a prepared cursor object
        cursor = connection.cursor(prepared=True)

        # Execute the SELECT query using the cursor object
        cursor.execute(query, params)

        # Fetch all the results from the cursor
        result = cursor.fetchall()

        # Close the cursor
        cursor.close()

        # Convert the results into a nested list format
        nested_result = [list(row) for row in result]

        # Return the nested list of results
        return nested_result

    except mysql.connector.Error as err:
        # Return the error message as a string
        return f"Error executing query: {err}"

def SQL_INSERT(connection:mysql.connector.connection.MySQLConnection, query:str, params:tuple=None):
    """
    Executes an INSERT query on a MySQL database using prepared statements.

    ONLY WORKS WITH ONE ROW.

    :param connection: a MySQL database connection object
    :param query: an INSERT query string with placeholders for parameters
    :param params: a tuple of parameters for the query (optional)
    :return: the number of affected rows, or a string error message
    """
    try:
        # Create a prepared cursor object
        cursor = connection.cursor(prepared=True)

        # Execute the INSERT query using the cursor object
        cursor.execute(query, params)

        # Get the number of affected rows
        num_affected_rows = cursor.rowcount

        # Commit the transaction
        connection.commit()

        # Close the cursor
        cursor.close()

        # Return the number of affected rows
        return num_affected_rows

    except mysql.connector.Error as err:
        # Rollback the transaction
        connection.rollback()

        # Return the error message as a string
        return f"Error executing query: {err}"

def SQL_UPDATE(connection:mysql.connector.connection.MySQLConnection, query:str, params:tuple=None):
    """
    Executes an UPDATE query on a MySQL database using prepared statements.

    :param connection: a MySQL database connection object
    :param query: an UPDATE query string with placeholders for parameters
    :param params: a tuple of parameters for the query (optional)
    :return: the number of affected rows, or a string error message
    """
    try:
        # Create a prepared cursor object
        cursor = connection.cursor(prepared=True)

        # Execute the UPDATE query using the cursor object
        cursor.execute(query, params)

        # Get the number of affected rows
        num_affected_rows = cursor.rowcount

        # Commit the transaction
        connection.commit()

        # Close the cursor
        cursor.close()

        # Return the number of affected rows
        return num_affected_rows

    except mysql.connector.Error as err:
        # Rollback the transaction
        connection.rollback()

        # Return the error message as a string
        return f"Error executing query: {err}"

def main():
    # Connect to the database
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="hvz"
    )

    print(type(connection))

    # Define the SELECT query and parameters (if any)
    query = "SELECT * FROM players WHERE player_id = %s"
    params = (1,)

    # Execute the SELECT query and get the results
    result = SQL_SELECT(connection, query, params)

    # Print the results
    print(result)

    # Close the database connection
    connection.close()

if __name__ == "__main__":
    main()