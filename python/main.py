import mysql.connector
import json
from flask import Flask, json
import os
import inspect

api = Flask(__name__)

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="hvz"
)

@api.route('/SQL_SELECT/querry')
def SQL_SELECT( query:str, params:tuple=None):
    """
    Executes a SELECT query on a MySQL database using prepared statements.

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

        # Get the column names from the cursor description
        column_names = [column[0] for column in cursor.description]

        # Close the cursor
        cursor.close()

        # Convert the results into a nested list format with column names as first row
        nested_result = [column_names] + [list(row) for row in result]

        # Return the nested list of results
        return nested_result

    except mysql.connector.Error as err:
        # Return the error message as a string
        return f"Error executing query: {err}"


def SQL_INSERT(query:str, params:tuple=None):
    """
    Executes an INSERT query on a MySQL database using prepared statements.

    ONLY WORKS WITH ONE ROW.

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

def SQL_UPDATE(query:str, params:tuple=None):
    """
    Executes an UPDATE query on a MySQL database using prepared statements.

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

def SQL_example():
    # Connect to the database


    #print(type(connection))

    # Define the SELECT query and parameters (if any)
    query = "SELECT * FROM players WHERE player_id = %s"
    params = (1,)

    # Execute the SELECT query and get the results
    result = SQL_SELECT(query, params)

    # Print the results
    print(result)

    # Close the database connection
    connection.close()

@api.route('/registerUser/<user_id>/<email>/<discord_id>/<phoneNumber>/<callsign>/<fname>/<lname>')
def registerUser(user_id:str, A_number:str, email:str, discord_id:str, 
                phoneNumber:str, callsign:str, fname:str, lname:str):
    '''
    adds a new player to a database. if there was an error return a string 
    discribing the error, if not it will return the json:
    {"rowsEffected":1}
    '''

    query = ("INSERT INTO players " +
    "(user_id, a_number, callsign, fname, lname email, discord_id, phone_number) " +
    "VALUES " +
    "(%s, %s, %s, %s, %s, %s, %s, %s);")

    params = (user_id, A_number, callsign, fname, lname, email, discord_id, phoneNumber)



    result = SQL_INSERT(query, params)

    #if there was an error, reutrn the text of the error
    if (type(result) == str):
        return result

    # if there was no error, 
    else:
        if (result != 1):
            return (f"ERROR: the qurry was only suposed to effect 1 row, "+
            f"but it effected {result}")
        
        else:
            return json.dump({"rowsEffected":result})



@api.route('/newGame/<gameName>/<startTime>/<game_email_key>')
def newGame(gameName:str, startTime:str, game_email_key:str):
    '''
    Adds a new game to a database. If there was an error return a string 
    discribing the error, if not it will return the json:
    {"rowsEffected":1}
    '''
    
    query = ("INSERT INTO games " +
    "(game_name, game_start_time, game_email_key) " +
    "VALUES " +
    "(%s, %s, %s);")

    params = (gameName, startTime, game_email_key)    
    

    result = SQL_INSERT(query, params)

    #if there was an error, reutrn the text of the error
    if (type(result) == str):
        return result

    # if there was no error, 
    else:
        if (result != 1):
            return (f"ERROR: the qurry was only suposed to effect 1 row, "+
            f"but it effected {result}")
        
        else:
            return json.dump({"rowsEffected":result})

@api.route('/registerUserInGame/<user_id>/<tag_code>/<gameName>')
@api.route('/registerUserInGame/<user_id>/<tag_code>/<gameName>/<stateName>')
def registerUserInGame(user_id:str, tag_code:str, gameName:str, stateName:str = "human"):
    '''
    Adds a new game to a database. If there was an error return a string 
    discribing the error, if not it will return the json:
    {"rowsEffected":1}
    '''

    # start by geting the player_id from the user_id
    query = (f"SELECT player_id FROM players WHERE user_id = %s")

    perams = (user_id,)
    

    results = SQL_SELECT (query, params)
    
    
    # Get the filename with extension
    filename = os.path.basename(__file__)

    # Extract the filename without extension (used in returning errors)
    filename_without_extension = os.path.splitext(filename)[0]

    # run a battery of tests on the result to make sure its in the propper format
    isValid = checkSingleSelectOutput(results)

    # if checkSingeSelectOutput, return its errorMsg
    if (isValid != True):
        return isValid
    
    # make sure that row is holding an int
    elif (is_int(result[1][0])):
        
        return (f"ERROR: {filename_without_extension}.{registerUser.__name__}() " + 
            f"expected {filename_without_extension}.SQL_SELECT() to return a player_id " + 
            f"(int) but it did not")

    # if no errors were called, set player_id to the result
    else:
        player_id = int(result[1][0])



    # now get the game_id from the gameName
    query = (f"SELECT game_id FROM games WHERE game_name = %s")

    perams = (gameName,)

    results = SQL_SELECT (query, params)

    # run a battery of tests on the result to make sure its in the propper format
    isValid = checkSingleSelectOutput(results)
    
    # if it returns true there were no errors, if not it returned an errorMsg,
    # return it to the user.
    if (isValid != True):
        return isValid
    
    # make sure that row is holding an int
    elif (is_int(result[1][0])):
        return (f"ERROR: {filename_without_extension}.{registerUser.__name__}() " + 
            f"expected {filename_without_extension}.SQL_SELECT() to return a player_id " + 
            f"(int) but it did not")

    # if there were no errors, set the game_id as the result
    else:
        game_id = int(result[1][0])


    

    # ok, last item we need to look up, the code_id

    query = (f"SELECT tag_code_id FROM codes WHERE tag_code = %s")

    perams = (gameName,)

    results = SQL_SELECT(query, params)

    # run a battery of tests on the result to make sure its in the propper format
    isValid = checkSingleSelectOutput(results)
    
    # if it returns true there were no errors, if not it returned an errorMsg,
    # return it to the user.
    if (isValid != True):
        return isValid
    
    # make sure that row is holding an int
    elif (is_int(result[1][0])):
        return (f"ERROR: {filename_without_extension}.{registerUser.__name__}() " + 
            f"expected {filename_without_extension}.SQL_SELECT() to return a player_id " + 
            f"(int) but it did not")

    # if there were no errors, set the game_id as the result
    else:
        code_id = int(result[1][0])


    # run the insert statment
    query = ("INSERT INTO players_games " +
    "(player_id, game_id, tag_code_id, states_id) " +
    "VALUES " +
    "(%s, %s, %s);")

    params = (player_id, game_id, code_id)    
    
    result = SQL_INSERT(connection, query, params)

    #if there was an error, reutrn the text of the error
    if (type(result) == str):
        return result

    # if there was no error, 
    else:
        if (result != 1):
            return (f"ERROR: the qurry was only suposed to effect 1 row, "+
            f"but it effected {result}")
        
        else:
            return json.dump({"rowsEffected":result})

def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def checkSingleSelectOutput(results):
    '''
    checks if a SELECT query designed to return a single result did so.

    if there is no error, it returns true, otherwise it returns the error as a str.
    '''
    
    # make sure SQL_SELECT returned a list
    if (type(results) != list):
        
        if (type(results) == str):
            return results
        else:

            filename = os.path.basename(__file__)

            # Extract the filename without extension
            filename_without_extension = os.path.splitext(filename)[0]
            
            return (f"ERROR: {filename_without_extension}." + 
                    f"{inspect.currentframe().f_back.f_code.co_name}() " + 
                    f"expected {filename_without_extension}.SQL_SELECT() to return a list " + 
                    f"but it rerned a '{type(results)}'")
    
    # make sure that list only has one row
    elif (len(results) != 2):
        return (f"ERROR: {filename_without_extension}." + 
                f"{inspect.currentframe().f_back.f_code.co_name}() " + 
                f"expected {filename_without_extension}.SQL_SELECT() to return 2 rows " + 
                f"but it rerned {len(results)}")

    # make sure that row is a list
    elif (type(results[1]) != list):
        return (f"ERROR: {filename_without_extension}." + 
                f"{inspect.currentframe().f_back.f_code.co_name}() " + 
                f"expected {filename_without_extension}.SQL_SELECT() to return a nested list " + 
                f"but it rerned a list containing a '{type(results[1])}'")
    
    # make sure that theres only one column
    elif (len(results[0][1]) != 1):
        return (f"ERROR: {filename_without_extension}." + 
                f"{inspect.currentframe().f_back.f_code.co_name}() " + 
                f"expected {filename_without_extension}.SQL_SELECT() to return 1 column " + 
                f"but it rerned {len(results[0])}")
    
    else:
        return True

if __name__ == "__main__":
    SQL_example()

# if __name__ == '__main__':
#     api.run()