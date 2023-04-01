import sys
import mysql.connector
import json
from flask import Flask, json, request
from flask import make_response
import os
import inspect
import importlib

api = Flask(__name__)


connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="hvz"
)


# this wont work if the user has multiple states. i would need to update the query 
@api.route('/getSingleUserData/<user_id>')
def getSingleUserData(user_id:str):
    '''
    returns all user data assoceated with a user_id

    returns a string if there was an error
    returns a json in the below format if everything went smothely 

    {"userData":nestedList}
    '''
    
    # the query to be sent to the SQL database
    query = (f"SELECT players.player_id, user_id, a_number, callsign, fname, lname, email, state " + 
             "FROM players " + 
             "LEFT JOIN players_games ON players.player_id = players_games.player_id " +
             "LEFT JOIN states ON players_games.state_id = states.state_id " +
            "WHERE user_id = %s;")

    # the peramiters. 
    # corisponds to %s in the query in order of appearance
    # i think this helps sidestep SQL injection attacks
    # alwasy use this mehtod for any kind of userInput data
    perams = (user_id,)
    
    results = SQL_SELECT (query, perams)
    

    # Get the filename with extension
    filename = os.path.basename(__file__)

    # Extract the filename without extension (used in returning errors)
    filename_without_extension = os.path.splitext(filename)[0]

    # if results is not a list there was an error
    if (type(results) != list):
        # if its a string, it contains an error msg
        if (type(results) == str):
            print(results)
            return results
        # if not, gerate our own.
        else:
            errorMsg = (f"ERROR: {filename_without_extension}.{getSingleUserData.__name__}() " + 
                f"expected {filename_without_extension}.SQL_SELECT() to return a list " + 
                f"but it returned a `{type(results)}`")
            print(errorMsg)
            return errorMsg
        
    # make sure there are only two rows, the data we want and a header.
    elif (len(results) != 2):
        errorMsg = (f"ERROR: {filename_without_extension}.{getSingleUserData.__name__}() " + 
            f"expected {filename_without_extension}.SQL_SELECT() to return two rows " + 
            f"but it returned {len(results)}")
        print(errorMsg)
        return errorMsg
    
    # make sure every row is a list
    for i in range(len(results)):
        row = results[i]

        if (type(row) != list):
            errorMsg = (f"ERROR: {filename_without_extension}.{getSingleUserData.__name__}() " + 
                f"expected {filename_without_extension}.SQL_SELECT() to " + 
                f"return a nested list, but row  {i} is a" + 
                f"'{type(row)}'")
            print(errorMsg)
            return errorMsg
    
    response = make_response({"userData":results})
    response.mimetype = 'application/json'
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
setattr(getSingleUserData, 'route', '/getSingleUserData/<user_id>')

@api.route('/getAllUserData')
def getAllUserData():
    '''
    returns all user data.

    returns a string if there was an error
    returns a json in the below format if everything went smothely 

    {"userData":nestedList}
    '''
    # the query to be sent to the SQL database
    query = (f"SELECT players.player_id, user_id, a_number, callsign, fname, lname, email, state " + 
             "FROM players " + 
             "LEFT JOIN players_games ON players.player_id = players_games.player_id " +
             "LEFT JOIN states ON players_games.state_id = states.state_id;")

    # send the query
    results = SQL_SELECT (query)
    

    # Get the filename with extension
    filename = os.path.basename(__file__)

    # Extract the filename without extension (used in returning errors)
    filename_without_extension = os.path.splitext(filename)[0]

    # if results is not a list there was an error
    resultsType = type(results)
    if (type(results)!= list):
        # if its a string, it contains an error msg
        if (type(results) == str):
            return results
        # if not, gerate our own.
        else:
            errorMsg = (f"ERROR: {filename_without_extension}.{getAllUserData.__name__}() " + 
                f"expected {filename_without_extension}.SQL_SELECT() to return a list " + 
                f"but it returned a `{str(type(results))}`")
            print(errorMsg)
            return errorMsg
    
    # make sure every row is a list
    for i in range(len(results)):
        row = results[i]

        if (type(row) != list):
            errorMsg = (f"ERROR: {filename_without_extension}.{getAllUserData.__name__}() " + 
                f"expected {filename_without_extension}.SQL_SELECT() to " + 
                f"return a nested list, but row  {i} is a" + 
                f"'{type(row)}'")
            print(errorMsg)
            return errorMsg
    


    response = make_response({"userData":results})
    response.mimetype = 'application/json'
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
setattr(getAllUserData, 'route', '/getAllUserData')




@api.route('/SQL_SELECT/<querry>')
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
SQL_SELECT.route = '/SQL_SELECT/<querry>'

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
    

@api.route('/registerUser/<user_id>/<a_number>/<email>/<fname>/<callsign>/<lname>/<discord_id>/<phoneNumber>')
@api.route('/registerUser/<user_id>/<a_number>/<email>/<fname>/<callsign>/<lname>')
def registerUser(user_id:str, a_number:str, email:str, callsign:str, fname:str, lname:str, discord_id:str = None, phoneNumber:str = None):
    '''
    adds a new player to a database. if there was an error return a string 
    discribing the error, if not it will return the json:
    {"rowsEffected":1}
    '''

    query = ("INSERT INTO players " +
    "(user_id, a_number, callsign, fname, lname email, discord_id, phone_number) " +
    "VALUES " +
    "(%s, %s, %s, %s, %s, %s, %s, %s);")

    discord_id = 'NULL' if discord_id is None else discord_id
    phoneNumber = 'NULL' if phoneNumber is None else phoneNumber

    params = (user_id, a_number, callsign, fname, lname, email, discord_id, phoneNumber)



    result = SQL_INSERT(query, params)

    #if there was an error, reutrn the text of the error
    if (type(result) == str):
        return result

    # if there was no error, 
    else:
        if (result != 1):
            errorMsg = (f"ERROR: the qurry was only suposed to effect 1 row, "+
            f"but it effected {result}")
            print(errorMsg)
            return errorMsg
        
        else:
            return json.dump({"rowsEffected":result})
setattr(registerUser, 'route', '/registerUser/<user_id>/<a_number>/<email>/<fname>/<callsign>/<lname>')


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
            errorMsg = (f"ERROR: the qurry was only suposed to effect 1 row, "+
            f"but it effected {result}")
            print(errorMsg)
            return errorMsg
        
        else:
            return json.dump({"rowsEffected":result})
setattr(newGame, 'route', '/newGame/<gameName>/<startTime>/<game_email_key>')

# this wont work if the user has multiple states. i would need to update the query 
@api.route('/registerUserInGame/<user_id>/<gameName>')
@api.route('/registerUserInGame/<user_id>/<gameName>/<stateName>')
def registerUserInGame(user_id:str,  gameName:str, stateName:str = "human"):
    '''
    Adds a new game to a database. If there was an error return a string 
    discribing the error, if not it will return the json:
    {"rowsEffected":1}
    '''

    # start by geting the player_id from the user_id
    query = (f"SELECT player_id FROM players WHERE user_id = %s;")

    # the peramiters. 
    # corisponds to %s in the query in order of appearance
    # i think this helps sidestep SQL injection attacks
    # alwasy use this mehtod for any kind of userInput data
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
        errorMsg = (f"ERROR: {filename_without_extension}.{registerUserInGame.__name__}() " + 
            f"expected {filename_without_extension}.SQL_SELECT() to return a player_id " + 
            f"(int) but it did not")
        print(errorMsg)
        return errorMsg

    # if no errors were called, set player_id to the result
    else:
        player_id = int(results[1][0])



    # now get the game_id from the gameName
    query = (f"SELECT game_id FROM games WHERE game_name = %s;")

    # the peramiters. 
    # corisponds to %s in the query in order of appearance
    # i think this helps sidestep SQL injection attacks
    # alwasy use this mehtod for any kind of userInput data
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
        errorMsg = (f"ERROR: {filename_without_extension}.{registerUserInGame.__name__}() " + 
            f"expected {filename_without_extension}.SQL_SELECT() to return a player_id " + 
            f"(int) but it did not")
        print(errorMsg)
        return errorMsg

    # if there were no errors, set the game_id as the result
    else:
        game_id = int(results[1][0])


    # look up, the code_id based on code

    query = (f"SELECT tag_code_id FROM codes WHERE tag_code = %s;")

    # the peramiters. 
    # corisponds to %s in the query in order of appearance
    # i think this helps sidestep SQL injection attacks
    # alwasy use this mehtod for any kind of userInput data
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
        errorMsg = (f"ERROR: {filename_without_extension}.{registerUserInGame.__name__}() " + 
            f"expected {filename_without_extension}.SQL_SELECT() to return a player_id " + 
            f"(int) but it did not")
        print(errorMsg)
        return errorMsg

    # if there were no errors, set the game_id as the result
    else:
        code_id = int(results[1][0])
    


    # ok, last item we need to look up, the state_id, usualy based off `zombie``.
    query = (f"SELECT state_id FROM states WHERE state = %s;")

    # the peramiters. 
    # corisponds to %s in the query in order of appearance
    # i think this helps sidestep SQL injection attacks
    # alwasy use this mehtod for any kind of userInput data
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
        
        errorMsg = (f"ERROR: {filename_without_extension}.{registerUserInGame.__name__}() " + 
            f"expected {filename_without_extension}.SQL_SELECT() to return a player_id " + 
            f"(int) but it did not")
        print(errorMsg)
        return errorMsg

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
            errorMsg = (f"ERROR: the qurry was only suposed to effect 1 row, "+
            f"but it effected {results}")
            print(errorMsg)
            return errorMsg
        
        else:
            response = make_response({"rowsEffected":results})
            response.mimetype = 'application/json'
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
setattr(registerUserInGame, 'route', '/registerUserInGame/<user_id>/<gameName>')

# NOT DONE
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


    game_id = getActiveGameID()
    
    # NOT DONE
    query = ("SELECT gameName FROM tag_registry " +
             "LEFT JOIN games ON tag_registry.game_id = games.game_id " + 
             "WHERE game_id = %s;")

    # the peramiters. 
    # corisponds to %s in the query in order of appearance
    # i think this helps sidestep SQL injection attacks
    # alwasy use this mehtod for any kind of userInput data
    perams = (game_id, )
    
    results = SQL_SELECT (query, perams)
    

    # Get the filename with extension
    filename = os.path.basename(__file__)

    # Extract the filename without extension (used in returning errors)
    filename_without_extension = os.path.splitext(filename)[0]

    # if results is not a list there was an error
    if (type(results) != list):
        # if its a string, it contains an error msg
        if (type(results) == str):
            return results
        # if not, gerate our own.
        else:
            errorMsg = (f"ERROR: {filename_without_extension}.{getTags.__name__}() " + 
                f"expected {filename_without_extension}.SQL_SELECT() to return a list " + 
                f"but it returned a `{type(results)}`")
            print(errorMsg)
            return errorMsg
    # make sure every row is a list
    for i in range(len(results)):
        row = results[i]

        if (type(row) != list):
            errorMsg = (f"ERROR: {filename_without_extension}.{getTags.__name__}() " + 
                f"expected {filename_without_extension}.SQL_SELECT() to " + 
                f"return a nested list, but row  {i} is a" + 
                f"'{type(row)}'")
            print(errorMsg)
            return errorMsg
        
    response = make_response({"tags":results})
    response.mimetype = 'application/json'
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
setattr(getTags, 'route', '/getTags')

@api.route('/getActiveGameID')
def getActiveGameID():
    '''
    returns the game_id of the active game.

    if theres an error it returns the errorMsg as a stirng
    
    if theres no error it returns a json object in the below format:
    
    {"activeGameID":int}
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
        
        errorMsg = (f"ERROR: {filename_without_extension}.{getTags.__name__}() " + 
            f"expected {filename_without_extension}.SQL_SELECT() to return a player_id " + 
            f"(int) but it did not")
        print(errorMsg)
        return errorMsg
    # if there were no errors, set the game_id as the result
    else:
        game_id = int(results[1][0])
    

    response = make_response({"activeGameID":game_id})
    response.mimetype = 'application/json'
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
setattr(getActiveGameID, 'route', '/getActiveGameID')

@api.route('/new2FAKey') 
def new2FAKey():
    '''
    returns a new 2FAKey

    returns a json object with the below format:

    {"2FAKey":int}
    '''
    from pyotp import random_base32

    response = make_response({"2FAKey":random_base32()})
    response.mimetype = 'application/json'
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
setattr(new2FAKey, 'route', '/new2FAKey')

@api.route('/check2FAKey/<user_id>/<code>') 
def check2FAKey(user_id, code):
    
    '''
    given a user_id and a code, checks a given 2FA code.

    if there was an error, returns the error msg as a string

    if no error returns a json object with the below format:
    
    {"validCode":bool}
    '''

    query = (f"SELECT twoFA_key FROM players WHERE user_id = %s;")

    # the peramiters. 
    # corisponds to %s in the query in order of appearance
    # i think this helps sidestep SQL injection attacks
    # alwasy use this mehtod for any kind of userInput data
    perams = (user_id,)
    
    results = SQL_SELECT (query, perams)
    

    # Get the filename with extension
    filename = os.path.basename(__file__)

    # Extract the filename without extension (used in returning errors)
    filename_without_extension = os.path.splitext(filename)[0]

    # if results is not a list there was an error
    if (type(results) != list):
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

    

    response = make_response({"validCode":authenticated})
    response.mimetype = 'application/json'
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
setattr(check2FAKey, 'route', '/check2FAKey/<user_id>/<code>')

@api.route('/generateQRCode/<url>') 
def generateQRCode(url):
    '''
    given a url, generates a QR code and saves it to ../images

    returns a json object with the below format:

    {"QRPath":string}
    '''
    
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

    json = {"QRPath":filepath}

    response = make_response({"QRPath":filepath})
    response.mimetype = 'application/json'
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
generateQRCode.route = '/generateQRCode/<url>'


@api.route('/getTagPageInfo/<user_id>') 
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
        errorMsg = (f"ERROR: {filename_without_extension}.{getTagPageInfo.__name__}() " + 
            f"expected {filename_without_extension}.SQL_SELECT() to return a player_id " + 
            f"(int) but it did not")
        print(errorMsg)
        return errorMsg

    # if there were no errors, set the game_id as the result
    else:
        game_id = int(results[1][0])
    
    # check the user Registration
    # check if there is a active game, if there is, get the game_id.
    query = (f"SELECT state_id FROM players_games WHERE player_id = %s AND game_id = %s;")

    # the peramiters. 
    # corisponds to %s in the query in order of appearance
    # i think this helps sidestep SQL injection attacks
    # alwasy use this mehtod for any kind of userInput data
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

    # the peramiters. 
    # corisponds to %s in the query in order of appearance
    # i think this helps sidestep SQL injection attacks
    # alwasy use this mehtod for any kind of userInput data
    perams = (player_id, game_id)

    results = SQL_SELECT (query, perams)

    
    # if it returns true there were no errors, if not it returned an errorMsg,
    # return it to the user.
    if (type(results) != list):
        errorMsg = (f"ERROR: {filename_without_extension}.{getTagPageInfo.__name__}() " + 
            f"expected {filename_without_extension}.SQL_SELECT() to return a nested list " + 
            f"but it returned a '{type(results)}'")
        
        print(errorMsg)
        return errorMsg

    for i  in range(len(results)):
        row = results[i]

        if type(row) != list:
            errorMsg = (f"ERROR: {filename_without_extension}.{getTagPageInfo.__name__}() " + 
                f"expected {filename_without_extension}.SQL_SELECT() to return a nested list " + 
                f"but it returned a list containing a '{type(row)}'")
            print(errorMsg)
            return errorMsg


    response = make_response({"results": results})
    response.mimetype = 'application/json'
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
setattr(getTagPageInfo, 'route', '/getTagPageInfo/<user_id>')

@api.route('/getPlayer_id/<user_id>') # Tested 
def getPlayer_id(user_id:str):
    '''
    returns a player_id for a given user_id.

    if there was an error, returns the error as a string

    if no error, returns a json object in the below format

    {"player_id":results}
    '''
    query = (f"SELECT player_id FROM players WHERE user_id = %s;")

    # the peramiters. 
    # corisponds to %s in the query in order of appearance
    # i think this helps sidestep SQL injection attacks
    # alwasy use this mehtod for any kind of userInput data
    perams = (user_id,)
    
    results = SQL_SELECT (query, perams)
    

    # Get the filename with extension
    filename = os.path.basename(__file__)

    # Extract the filename without extension (used in returning errors)
    filename_without_extension = os.path.splitext(filename)[0]

    # if results is not a list there was an error
    if (type(results) != list):
        # if its a string, it contains an error msg
        if (type(results) == str):
            return results
        # if not, gerate our own.
        else:
            errorMsg = (f"ERROR: {filename_without_extension}.{getPlayer_id.__name__}() " + 
                f"expected {filename_without_extension}.SQL_SELECT() to return a list " + 
                f"but it returned a `{type(results)}`")
            print(errorMsg)
            return errorMsg
        
    # make sure there are only two rows, the data we want and a header.
    elif (len(results) != 2):
        errorMsg = (f"ERROR: {filename_without_extension}.{getPlayer_id.__name__}() " + 
            f"expected {filename_without_extension}.SQL_SELECT() to return two rows " + 
            f"but it returned {len(results)}")
        print(errorMsg)
        return errorMsg
    
    # make sure every row is a list
    for i in range(len(results)):
        row = results[i]

        if (type(row) != list):
            return (f"ERROR: {filename_without_extension}.{getPlayer_id.__name__}() " + 
                f"expected {filename_without_extension}.SQL_SELECT() to " + 
                f"return a nested list, but row  {i} is a" + 
                f"'{type(row)}'")
    
    response = make_response({"player_id":results[1][0]})
    response.mimetype = 'application/json'
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
setattr(getPlayer_id, 'route', '/getPlayer_id/<user_id>')


@api.route('/getPlayerName/<user_id>')
def getPlayerName(user_id:str):
    '''
    Returns a playerName for a given user_id. includes callsign if posible.

    If there was an error, returns the error as a string

    If no error, returns a json object in the below format

    {"playerName":results}
    '''
    query = (f"SELECT IF(callsign IS NULL, CONCAT(fname, ' ',lname), CONCAT(fname, ' \\\'', callsign, '\\\' ', lname )) AS playerName FROM players WHERE user_id = %s;")

    # the peramiters. 
    # corisponds to %s in the query in order of appearance
    # i think this helps sidestep SQL injection attacks
    # alwasy use this mehtod for any kind of userInput data
    perams = (user_id,)
    
    results = SQL_SELECT (query, perams)
    

    # Get the filename with extension
    filename = os.path.basename(__file__)

    # Extract the filename without extension (used in returning errors)
    filename_without_extension = os.path.splitext(filename)[0]

    # if results is not a list there was an error
    if (type(results) != list):
        # if its a string, it contains an error msg
        if (type(results) == str):
            return results
        # if not, gerate our own.
        else:
            errorMsg =(f"ERROR: {filename_without_extension}.{getPlayer_id.__name__}() " + 
                f"expected {filename_without_extension}.SQL_SELECT() to return a list " + 
                f"but it returned a `{type(results)}`")
            print(errorMsg) 
            return errorMsg
        
    # make sure there are only two rows, the data we want and a header.
    elif (len(results) != 2):
        errorMsg = (f"ERROR: {filename_without_extension}.{getPlayer_id.__name__}() " + 
            f"expected {filename_without_extension}.SQL_SELECT() to return two rows " + 
            f"but it returned {len(results)}")
        print(errorMsg)
        return errorMsg
    
    # make sure every row is a list
    for i in range(len(results)):
        row = results[i]

        if (type(row) != list):
            errorMsg = (f"ERROR: {filename_without_extension}.{getPlayer_id.__name__}() " + 
                f"expected {filename_without_extension}.SQL_SELECT() to " + 
                f"return a nested list, but row  {i} is a" + 
                f"'{type(row)}'")
            print(errorMsg)
            return errorMsg
    
    response = make_response({"playerName":results[1][0]})
    response.mimetype = 'application/json'
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
setattr(getPlayerName, 'route', '/getPlayerName/<user_id>')

@api.route('/toggleGamePause')
def toggleGamePause():
    '''
    togles the pause state of the active game.

    if there was an error, ereturns the errormsg as a string

    if no error returns the below json object

    {"pauseRowsEffected":1}
    '''

    # Get the filename with extension
    filename = os.path.basename(__file__)

    # Extract the filename without extension (used in returning errors)
    filename_without_extension = os.path.splitext(filename)[0]
    
    game_id = getActiveGameID()

    # determine the curent state of the of the game 
    query = "SELECT is_safe_active FROM games WHERE game_id = %s"
    perams = (game_id, )

    results = SQL_SELECT(query, perams)

    isValid = checkSingleOutputSelect(results)

    if (isValid != True):
        return isValid
    
    elif (results[1][0] != 'y' and results[1][0] != 'n'):
        errorMsg = (
            f"ERROR: {filename_without_extension}.{registerUserInGame.__name__}() " + 
            f"expected {filename_without_extension}.SQL_SELECT() to return a game_id " + 
            f"(int) but it did not."
        )

        print(errorMsg)
        return errorMsg
    
    else:
        currentState = results[1][0]

    if (currentState == 'n'):
        newState = 'y'
    else:
        newState = 'n'

    query = ("UPDATE games SET is_save_active = %s WHERE game_id = %s")

    perams = (newState, game_id)

    results = SQL_UPDATE(query, perams)

    # if there was an error, reutrn the text of the error
    if (type(results) == str):
        return results

    # if there was no error, return the json.
    else:
        # make sure the json contians 1. otherwise theres a problem.
        if (results != 1):
            errorMsg = (f"ERROR: the qurry was only suposed to effect 1 row, "+
            f"but it effected {results}")
            print(errorMsg)
            return errorMsg
        
        else:
            response = make_response({"rowsEffected":results})
            response.mimetype = 'application/json'
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
setattr(toggleGamePause, 'route', '/toggleGamePause')

@api.route('/setActiveGame/<game_id>')
def setActiveGame(game_id:str):
    '''
    sets the active game to the game spesified

    if there was an error, returns the errorMsg as a string

    if there was no error returns the below json object.

    {"updateDeactivateRowsEffected":int, "updateActivateRowsEffected":1}
    '''
    # set the current active game as inactive
    query = "UPDATE games SET is_game_active = 'n'"

    results = SQL_UPDATE(query)

    output = {}

    # if there was an error, reutrn the text of the error
    if (type(results) == str):
        return results

    else:
        output["updateDeactivateRowsEffected"] = results

    
    # now update the spesified game to be the active one

    query = "UPDATE games SET is_game_active = 'y' WHERE game_id = %s"

    perams = (game_id, )

    results = SQL_UPDATE(query, perams)

    # if there was an error, reutrn the text of the error
    if (type(results) == str):
        return results

    # if there was no error, return the json.
    else:
        # make sure the json contians 1. otherwise theres a problem.
        if (results != 1):
            errorMsg = (f"ERROR: the qurry was only suposed to effect 1 row, "+
            f"but it effected {results}")
            print(errorMsg)
            return errorMsg
        
        else:
            output["updateActivateRowsEffected"] = results
        
    response = make_response(output)
    response.mimetype = 'application/json'
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
setattr(setActiveGame, 'route', '/setActiveGame/<game_id>')



@api.route('/getAllGameData')
def getAllGameData():
    '''
    returns all relivent data about all game

    if there is an error, returns the errorMsg as a string

    if no error, returns a json object in the below format:
    
    {"gameData":nestedList}
    '''

    query = "SELECT * FROM games"

    results = SQL_SELECT(query)


    # Get the filename with extension
    filename = os.path.basename(__file__)

    # Extract the filename without extension (used in returning errors)
    filename_without_extension = os.path.splitext(filename)[0]

    if (type(results) != list):
        pass
    elif(type(results[0]) != list):
        errorMsg = (f"ERROR: {filename_without_extension}.{getAllGameData.__name__}() " + 
                f"expected {filename_without_extension}.SQL_SELECT() to return a nested list " + 
                f"but it returned a '{type(results)}'")
        print(errorMsg)
        return(errorMsg)
    
    for i in range(len(results)):

        row = results[i]

        if (type(row) != list):

            errorMsg = (f"ERROR: {filename_without_extension}.{getAllGameData.__name__}() " + 
                    f"expected {filename_without_extension}.SQL_SELECT() to return a nested list " + 
                    f"but it returned a list containing a '{type(results)} at index {i}'")
            print(errorMsg)
            return errorMsg
    
    response = make_response({"gameData":results})
    response.mimetype = 'application/json'
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
setattr(getAllGameData, 'route', '/getAllGameData')





@api.route('/tagPlayer/<human_user_id>')
def tagPlayer(human_user_id):
    '''
    tags a player

    if there is an error it reurns the error as an errorMsg string

    if there is no error it returns the below json object

    {"insertRowsEffected":1, "updateRowsEffected":1}
    '''
    # get the player_id
    human_player_id = getPlayer_id(human_user_id)

    # get the current time
    time = get_current_time()

    # the the active game_id
    game_id = getActiveGameID()['active_game_id']

    # the query to send to MySQL
    query = "INSERT INTO tag_registry (human_id, time, game_id) VALUES (%s, %s, %s)"

    # the peramiters. 
    # corisponds to %s in the query in order of appearance
    # i think this helps sidestep SQL injection attacks
    # alwasy use this mehtod for any kind of userInput data
    perams = (human_player_id, time, game_id)

    # send the query
    results = SQL_INSERT(query, perams)

    
    #if there was an error, reutrn the text of the error
    if (type(results) == str):
        return results

    # if there was no error, 

    # make sure only one row was affected.
    if (results != 1):
        errorMsg = (f"ERROR: the qurry was only suposed to effect 1 row, "+
        f"but it effected {results}")
        print(errorMsg)
        return errorMsg
    
    
    # create an output var
    output = {}

    # save the results 
    output["insertRowsEffected"] = results

    query = ("UPDATE players_games SET state_id = (SELECT state_id FROM states WHERE state LIKE 'zombie') WHERE player_id = %s AND game_id = %s")

    perams = (human_player_id, game_id)

    results = SQL_UPDATE(query, perams)

    #if there was an error, reutrn the text of the error
    if (type(results) == str):
        return results

    # if there was no error, 

    # make sure only one row was affected.
    if (results != 1):
        errorMsg = (f"ERROR: the qurry was only suposed to effect 1 row, "+
        f"but it effected {results}")
        print(errorMsg)
        return errorMsg
    
    output["updateRowsEffected"] = results

    response = make_response(output)
    response.mimetype = 'application/json'
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
setattr(tagPlayer, 'route', '/tagPlayer/<human_user_id>')

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
    filename = os.path.basename(__file__)

    # Extract the filename without extension
    filename_without_extension = os.path.splitext(filename)[0]

    # make sure SQL_SELECT returned a list
    if (type(results) != list):
        
        if (type(results) == str):
            return results
        else:
            
            errorMsg = (f"ERROR: {filename_without_extension}." + 
                    f"{inspect.currentframe().f_back.f_code.co_name}() " + 
                    f"expected {filename_without_extension}.SQL_SELECT() to return a list " + 
                    f"but it rerned a '{type(results)}'")
            print(errorMsg)
            return errorMsg
    
    # make sure that list only has one row
    elif (len(results) != 2):

        errorMsg = (f"ERROR: {filename_without_extension}." + 
                f"{inspect.currentframe().f_back.f_code.co_name}() " + 
                f"expected {filename_without_extension}.SQL_SELECT() to return 2 rows " + 
                f"but it rerned {len(results)}")
        print(errorMsg)
        return errorMsg

    # make sure that row is a list
    elif (type(results[1]) != list):
        errorMsg = (f"ERROR: {filename_without_extension}." + 
                f"{inspect.currentframe().f_back.f_code.co_name}() " + 
                f"expected {filename_without_extension}.SQL_SELECT() to return a nested list " + 
                f"but it rerned a list containing a '{type(results[1])}'")
        print(errorMsg)
        return errorMsg
    
    # make sure that theres only one column
    elif (len(results[0][1]) != 1):
        errorMsg = (f"ERROR: {filename_without_extension}." + 
                f"{inspect.currentframe().f_back.f_code.co_name}() " + 
                f"expected {filename_without_extension}.SQL_SELECT() to return 1 column " + 
                f"but it rerned {len(results[0])}")
        
        print(errorMsg)
        
        return errorMsg
    
    else:
        return True

def get_current_time():
    from datetime import datetime
    # Get the current date and time
    now = datetime.now()

    # Format the date and time as a string in the desired format
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")

    # Return the formatted string
    return current_time

def resetFilePath():
    '''
    changed the working directory to the directory of the file this is in.
    '''
    import os
    
    # change working directory to current directory.
    path = os.path.dirname(os.path.abspath(__file__))
    os.chdir(path)

import inspect
import importlib
from flask import url_for
import main

@api.route('/help')
def help():
    # Get all functions defined in the app
    funcs = inspect.getmembers(main, predicate=inspect.isfunction)
    funcs_data = []
    for func_name, func in funcs:
        # Ignore the help function itself and any functions without a route attribute

        hasRoute = hasattr(func, 'route')

        if ((func_name != 'help') and (hasRoute == True)):

            # Try to get the URL for the function
            url = func.route
            
            # Get the function's docstring
            docstring = inspect.getdoc(func)
            # Add the function data to the list of functions
            funcs_data.append((func_name, url, docstring))
    
    # Generate the HTML response
    html = '<html> \n<body>\n  <div style="width:800px;margin:auto;">\n\n   <style>\n    .indent{display:inline-block;margin:0 0 0 20px;font-size: 16px;}\n   </style>'
    for func_name, url, docstring in funcs_data:
        html += f'\n\n   <br>\n   <br>\n   <p style = "font-size: 20px;"><b><u>{func_name}()</u></b></p>\n   <p class = "indent"><b>Description:</b> \n   <br>{replace_newlines(replace_lt_gt(docstring))}\n   <br>\n   <br>\n   <b>URL:</b> <br>\n   {replace_lt_gt(url)}</p>'
    html += '\n\n  </div>\n  </body>\n</html>'
    return html
        
def replace_lt_gt(string:str):
    """
    Replaces '<' with '&lt;' and '>' with '&gt;' in a given string.

    Args:
        string (str): The string to search and replace.

    Returns:
        str: The modified string with '<' replaced by '&lt;' and '>' replaced by '&gt;'.
    """
    return string.replace('<', '&lt;').replace('>', '&gt;')

def replace_newlines(text):
    """
    Replaces the string '\n' with the string '\\n' in the input text.

    Parameters:
        text (str): The input text to be processed.

    Returns:
        str: The processed text with '\n' replaced by '\\n'.
    """
    return text.replace('\n', '\\n')

# if __name__ == "__main__":
#     print(help())

# THIS LINE MUST BE UNCOMMENTED IN ORDER FOR THE PROGRAM TO WORK 
# AS AN API!
if __name__ == '__main__':
    api.run()