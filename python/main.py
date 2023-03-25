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


    #print(type(connection))

    # Define the SELECT query and parameters (if any)
    query = "SELECT * FROM players WHERE player_id = %s;"
    params = (1,)

    # Execute the SELECT query and get the results
    result = SQL_SELECT(query, params)

    # Print the results
    print(result)
    

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
    query = (f"SELECT player_id FROM players WHERE user_id = %s;")

    perams = (user_id,)
    

    results = SQL_SELECT (query, perams)
    
    
    # Get the filename with extension
    filename = os.path.basename(__file__)

    # Extract the filename without extension (used in returning errors)
    filename_without_extension = os.path.splitext(filename)[0]

    # run a battery of tests on the result to make sure its in the propper format
    isValid = checkSingleOutputSelect(results)

    # if checkSingeSelectOutput, return its errorMsg
    if (isValid != True):
        return isValid
    
    # make sure that row is holding an int
    elif (is_int(results[1][0])):
        
        return (f"ERROR: {filename_without_extension}.{registerUserInGame.__name__}() " + 
            f"expected {filename_without_extension}.SQL_SELECT() to return a player_id " + 
            f"(int) but it did not")

    # if no errors were called, set player_id to the result
    else:
        player_id = int(results[1][0])



    # now get the game_id from the gameName
    query = (f"SELECT game_id FROM games WHERE game_name = %s;")

    perams = (gameName,)

    results = SQL_SELECT (query, perams)

    # run a battery of tests on the result to make sure its in the propper format
    isValid = checkSingleOutputSelect(results)
    
    # if it returns true there were no errors, if not it returned an errorMsg,
    # return it to the user.
    if (isValid != True):
        return isValid
    
    # make sure that row is holding an int
    elif (is_int(results[1][0])):
        return (f"ERROR: {filename_without_extension}.{registerUserInGame.__name__}() " + 
            f"expected {filename_without_extension}.SQL_SELECT() to return a player_id " + 
            f"(int) but it did not")

    # if there were no errors, set the game_id as the result
    else:
        game_id = int(results[1][0])




    # look up, the code_id based on code

    query = (f"SELECT tag_code_id FROM codes WHERE tag_code = %s;")

    perams = (gameName,)

    results = SQL_SELECT(query, perams)

    # run a battery of tests on the result to make sure its in the propper format
    isValid = checkSingleOutputSelect(results)
    
    # if it returns true there were no errors, if not it returned an errorMsg,
    # return it to the user.
    if (isValid != True):
        return isValid
    
    # make sure that row is holding an int
    elif (is_int(results[1][0])):
        return (f"ERROR: {filename_without_extension}.{registerUserInGame.__name__}() " + 
            f"expected {filename_without_extension}.SQL_SELECT() to return a player_id " + 
            f"(int) but it did not")

    # if there were no errors, set the game_id as the result
    else:
        code_id = int(results[1][0])
    


    # ok, last item we need to look up, the state_id, usualy based off `zombie``.
    query = (f"SELECT state_id FROM states WHERE state = %s;")

    perams = (stateName,)

    results = SQL_SELECT(query, perams)

    # run a battery of tests on the result to make sure its in the propper format
    isValid = checkSingleOutputSelect(results)
    
    # if it returns true there were no errors, if not it returned an errorMsg,
    # return it to the user.
    if (isValid != True):
        return isValid
    
    # make sure that row is holding an int
    elif (is_int(results[1][0])):
        return (f"ERROR: {filename_without_extension}.{registerUserInGame.__name__}() " + 
            f"expected {filename_without_extension}.SQL_SELECT() to return a player_id " + 
            f"(int) but it did not")

    # if there were no errors, set the game_id as the result
    else:
        state_id = int(results[1][0])

    # run the insert statment
    query = ("INSERT INTO players_games " +
    "(player_id, game_id, tag_code_id, states_id) " +
    "VALUES " +
    "(%s, %s, %s, %s);")

    params = (player_id, game_id, code_id, state_id)    
    
    results = SQL_INSERT(query, params)

    #if there was an error, reutrn the text of the error
    if (type(results) == str):
        return results

    # if there was no error, return the json.
    else:
        # make sure the json contians 1. otherwise theres a problem.
        if (results != 1):
            return (f"ERROR: the qurry was only suposed to effect 1 row, "+
            f"but it effected {results}")
        
        else:
            return json.dump({"rowsEffected":results})

@api.route('/getUserData/<user_id>')
def getUserData(user_id:str):
    '''
    returns all user data assoceated with a user_id

    returns a string if there was an error
    returns a json in the below format if everything went smothely 

    {"userData":nestedList}
    '''
    

    query = (f"SELECT * FROM players WHERE user_id = %s;")

    perams = (user_id,)
    
    results = SQL_SELECT (query, perams)
    

    # Get the filename with extension
    filename = os.path.basename(__file__)

    # Extract the filename without extension (used in returning errors)
    filename_without_extension = os.path.splitext(filename)[0]

    # if results is not a list there was an error
    if (type(results != list)):
        # if its a string, it contains an error msg
        if (type(results) == str):
            return results
        # if not, gerate our own.
        else:
            return (f"ERROR: {filename_without_extension}.{getUserData.__name__}() " + 
                f"expected {filename_without_extension}.SQL_SELECT() to return a list " + 
                f"but it returned a `{type(results)}`")
        
    # make sure there are only two rows, the data we want and a header.
    elif (len(results) != 2):
        return (f"ERROR: {filename_without_extension}.{getUserData.__name__}() " + 
            f"expected {filename_without_extension}.SQL_SELECT() to return two rows " + 
            f"but it returned {len(results)}")
    
    # make sure every row is a list
    for i in range(len(results)):
        row = results[i]

        if (type(row) != list):
            return (f"ERROR: {filename_without_extension}.{getUserData.__name__}() " + 
                f"expected {filename_without_extension}.SQL_SELECT() to " + 
                f"return a nested list, but row  {i} is a" + 
                f"'{type(row)}'")
    
    return json.dumps({"userData":results})

@api.route('/getUserData')
def getUserData():
    '''
    returns all user data.

    returns a string if there was an error
    returns a json in the below format if everything went smothely 

    {"userData":nestedList}
    '''
    
    query = (f"SELECT * FROM players;")

    
    results = SQL_SELECT (query)
    

    # Get the filename with extension
    filename = os.path.basename(__file__)

    # Extract the filename without extension (used in returning errors)
    filename_without_extension = os.path.splitext(filename)[0]

    # if results is not a list there was an error
    if (type(results != list)):
        # if its a string, it contains an error msg
        if (type(results) == str):
            return results
        # if not, gerate our own.
        else:
            return (f"ERROR: {filename_without_extension}.{getUserData.__name__}() " + 
                f"expected {filename_without_extension}.SQL_SELECT() to return a list " + 
                f"but it returned a `{type(results)}`")
    
    # make sure every row is a list
    for i in range(len(results)):
        row = results[i]

        if (type(row) != list):
            return (f"ERROR: {filename_without_extension}.{getUserData.__name__}() " + 
                f"expected {filename_without_extension}.SQL_SELECT() to " + 
                f"return a nested list, but row  {i} is a" + 
                f"'{type(row)}'")
    
    return json.dumps({"userData":results})

@api.route('/getTags')
def getTags():
    '''
    returns all tags.

    returns a string if there was an error
    returns a json in the below format if everything went smothely 

    {"tags":nestedList}
    '''

    # Get the filename with extension
    filename = os.path.basename(__file__)

    # Extract the filename without extension (used in returning errors)
    filename_without_extension = os.path.splitext(filename)[0]


    # first we get the active game
    # now get the game_id from the gameName
    query = (f"SELECT game_id FROM games WHERE is_game_active = y;")

    results = SQL_SELECT (query)

    # run a battery of tests on the result to make sure its in the propper format
    isValid = checkSingleOutputSelect(results)
    
    # if it returns true there were no errors, if not it returned an errorMsg,
    # return it to the user.
    if (isValid != True):
        return isValid
    # make sure that row is holding an int
    elif (is_int(results[1][0])):
        return (f"ERROR: {filename_without_extension}.{getTags.__name__}() " + 
            f"expected {filename_without_extension}.SQL_SELECT() to return a player_id " + 
            f"(int) but it did not")

    # if there were no errors, set the game_id as the result
    else:
        game_id = int(results[1][0])
    

    query = (f"SELECT * FROM tag_registry WHERE game_id = %s;")

    perams = (game_id, )
    
    results = SQL_SELECT (query)
    

    # Get the filename with extension
    filename = os.path.basename(__file__)

    # Extract the filename without extension (used in returning errors)
    filename_without_extension = os.path.splitext(filename)[0]

    # if results is not a list there was an error
    if (type(results != list)):
        # if its a string, it contains an error msg
        if (type(results) == str):
            return results
        # if not, gerate our own.
        else:
            return (f"ERROR: {filename_without_extension}.{getTags.__name__}() " + 
                f"expected {filename_without_extension}.SQL_SELECT() to return a list " + 
                f"but it returned a `{type(results)}`")
    
    # make sure every row is a list
    for i in range(len(results)):
        row = results[i]

        if (type(row) != list):
            return (f"ERROR: {filename_without_extension}.{getTags.__name__}() " + 
                f"expected {filename_without_extension}.SQL_SELECT() to " + 
                f"return a nested list, but row  {i} is a" + 
                f"'{type(row)}'")
    
    return json.dumps({"tags":results})

@api.route('/new2FAKey') 
def new2FAKey():
    from pyotp import random_base32

    return json.dump(random_base32())

@api.route('/check2FAKey/<user_id>/<code>') 
def check2FAKey(user_id, code):
    
    query = (f"SELECT twoFA_key FROM players WHERE user_id = %s;")

    perams = (user_id,)
    
    results = SQL_SELECT (query, perams)
    

    # Get the filename with extension
    filename = os.path.basename(__file__)

    # Extract the filename without extension (used in returning errors)
    filename_without_extension = os.path.splitext(filename)[0]

    # if results is not a list there was an error
    if (type(results != list)):
        # if its a string, it contains an error msg
        if (type(results) == str):
            return results
        # if not, gerate our own.
        else:
            return (f"ERROR: {filename_without_extension}.{check2FAKey.__name__}() " + 
                f"expected {filename_without_extension}.SQL_SELECT() to return a list " + 
                f"but it returned a `{type(results)}`")
        
    # make sure there are only two rows, the data we want and a header.
    elif (len(results) != 2):
        return (f"ERROR: {filename_without_extension}.{check2FAKey.__name__}() " + 
            f"expected {filename_without_extension}.SQL_SELECT() to return two rows " + 
            f"but it returned {len(results)}")
    
    # make sure every row is a list
    for i in range(len(results)):
        row = results[i]

        if (type(row) != list):
            return (f"ERROR: {filename_without_extension}.{check2FAKey.__name__}() " + 
                f"expected {filename_without_extension}.SQL_SELECT() to " + 
                f"return a nested list, but row  {i} is a" + 
                f"'{type(row)}'")
    
    secretKey = results[0][0]
    
    from pyotp import TOTP

    totp = TOTP(secretKey)
    authenticated = totp.verify(code)

    return authenticated

@api.route('/generateQRCode/<url>') 
def generateQRCode(url):
    import os
    import qrcode

    # create QR code object
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(url)
    qr.make(fit=True)

    # generate image from QR code
    img = qr.make_image(fill_color="black", back_color="white")

    # create directory if it doesn't exist
    directory = "../images"
    if not os.path.exists(directory):
        os.makedirs(directory)

    # save image to directory and return filepath
    filepath = os.path.join(directory, "qr_code.png")
    count = 1
    while os.path.exists(filepath):
        # append number to filename if filepath already exists
        filepath = os.path.join(directory, f"qr_code_{count}.png")
        count += 1
    img.save(filepath)
    return filepath


def getTagPageInfo(user_id:str):
    '''
    check if a tag page exists for a player and returns all the data asoceated 
    with it.

    reuturns true if a game is active and the player is un-registered
    returns false if there are no active games
    returns a stirng if an error occured
    returns a json with all relivent player, game, and state data in the below json format
    '''
    player_id = getPlayer_id(user_id)["player_id"]

    # Get the filename with extension
    filename = os.path.basename(__file__)

    # Extract the filename without extension (used in returning errors)
    filename_without_extension = os.path.splitext(filename)[0]

    # check if there is a active game, if there is, get the game_id.
    query = (f"SELECT game_id FROM games WHERE is_game_active = y;")

    results = SQL_SELECT (query)

    # run a battery of tests on the result to make sure its in the propper format
    isValid = checkSingleOutputSelect(results)
    
    # if it returns true there were no errors, if not it returned an errorMsg,
    # return it to the user.
    if (len(results) == 1):
        return False
    elif (isValid != True):
        return isValid
    # make sure that row is holding an int
    elif (is_int(results[1][0])):
        return (f"ERROR: {filename_without_extension}.{getTagPageInfo.__name__}() " + 
            f"expected {filename_without_extension}.SQL_SELECT() to return a player_id " + 
            f"(int) but it did not")

    # if there were no errors, set the game_id as the result
    else:
        game_id = int(results[1][0])
    
    # check the user Registration
    # check if there is a active game, if there is, get the game_id.
    query = (f"SELECT state_id FROM players_games WHERE player_id = %s AND game_id = %s;")

    perams = (player_id, game_id)

    results = SQL_SELECT (query, perams)

    # run a battery of tests on the result to make sure its in the propper format
    isValid = checkSingleOutputSelect(results)
    
    # if it returns true there were no errors, if not it returned an errorMsg,
    # return it to the user.
    
    if(len(results) == 1):
        return True
    
    elif (isValid != True):
        return isValid
    # make sure that row is holding an int
    elif (is_int(results[1][0])):
        return (f"ERROR: {filename_without_extension}.{getTagPageInfo.__name__}() " + 
            f"expected {filename_without_extension}.SQL_SELECT() to return a player_id " + 
            f"(int) but it did not")

    # if there were no errors, set the game_id as the result
    else:
        state_id = int(results[1][0])
    
    # now we have all our data and we know it exists we can query the player data, game data, and state data
    query = (f"SELECT * FROM players " + 
             "LEFT JOIN players_games ON players.player_id = players_games.player_id "+
             "LEFT JOIN games ON players_games.game_id = games.game_id "+
             "LEFT JOIN states ON players_games.state_id = states.state_id "+
             "WHERE players.player_id = %s AND players_games.game_id = %s;")

    perams = (player_id, game_id)

    results = SQL_SELECT (query, perams)

    
    # if it returns true there were no errors, if not it returned an errorMsg,
    # return it to the user.
    if (type(results) != list):
        return (f"ERROR: {filename_without_extension}.{getTagPageInfo.__name__}() " + 
            f"expected {filename_without_extension}.SQL_SELECT() to return a nested list " + 
            f"but it returned a '{type(results)}'")

    for i  in range(len(results)):
        row = results[i]

        if type(row) != list:
            return (f"ERROR: {filename_without_extension}.{getTagPageInfo.__name__}() " + 
                f"expected {filename_without_extension}.SQL_SELECT() to return a nested list " + 
                f"but it returned a list containing a '{type(results)}'")


    return json.dumps({"results": results})

        



    

@api.route('/getPlayer_id/<user_id>') 
def getPlayer_id(user_id:str):
    '''
    returns a player_id for a given user_id.

    if there was an error, returns the error as a string

    if no error, returns a json object in the below format

    {"player_id":results}
    '''
    query = (f"SELECT player_id FROM players WHERE user_id = %s;")

    perams = (user_id,)
    
    results = SQL_SELECT (query, perams)
    

    # Get the filename with extension
    filename = os.path.basename(__file__)

    # Extract the filename without extension (used in returning errors)
    filename_without_extension = os.path.splitext(filename)[0]

    # if results is not a list there was an error
    if (type(results != list)):
        # if its a string, it contains an error msg
        if (type(results) == str):
            return results
        # if not, gerate our own.
        else:
            return (f"ERROR: {filename_without_extension}.{getPlayer_id.__name__}() " + 
                f"expected {filename_without_extension}.SQL_SELECT() to return a list " + 
                f"but it returned a `{type(results)}`")
        
    # make sure there are only two rows, the data we want and a header.
    elif (len(results) != 2):
        return (f"ERROR: {filename_without_extension}.{getPlayer_id.__name__}() " + 
            f"expected {filename_without_extension}.SQL_SELECT() to return two rows " + 
            f"but it returned {len(results)}")
    
    # make sure every row is a list
    for i in range(len(results)):
        row = results[i]

        if (type(row) != list):
            return (f"ERROR: {filename_without_extension}.{getPlayer_id.__name__}() " + 
                f"expected {filename_without_extension}.SQL_SELECT() to " + 
                f"return a nested list, but row  {i} is a" + 
                f"'{type(row)}'")
    
    return json.dumps({"player_id":results[1][0]})


def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def checkSingleOutputSelect(results):
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

# THIS LINE MUST BE UNCOMMENTED IN ORDER FOR THE PROGRAM TO WORK 
# AS AN API!
# if __name__ == '__main__':
#     api.run()
#     connection.close()