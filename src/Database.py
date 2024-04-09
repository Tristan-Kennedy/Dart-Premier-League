import sqlite3 as sq

# Creates the database for use in the application.
# Methods to control the database are implemented in data

class Database:
    def __init__(self):
        self.createDatabase()

        
    def createDatabase(self):
        conn = sq.connect('dartsDatabase.db')  # Defines the connection to the db file, creates the file if it doesn't exist
        cursor = conn.cursor()  # Connects a new cursor to the database

        # Create the 'players' table
        cursor.execute(
            '''CREATE TABLE IF NOT EXISTS players(
                playerID INTEGER PRIMARY KEY,
                firstName TEXT NOT NULL,
                lastName TEXT NOT NULL,
                country TEXT NOT NULL,
                profile_path TEXT NOT NULL
                );'''
        )

        # Create the 'throws' table
        cursor.execute(
            '''CREATE TABLE IF NOT EXISTS throws(
                throwID INTEGER PRIMARY KEY,
                points INTEGER,
                legID INTEGER,
                gameID INTEGER,
                playerID INTEGER SECONDARY KEY
            );'''
        )

        conn.commit()
        conn.close()

    def addOrUpdatePlayer(self, fName, lName, country, profile_path, id=None):
        conn = sq.connect('dartsDatabase.db')
        cursor = conn.cursor()

        if id is None:
            query = '''INSERT INTO players (firstName, lastName, country, profile_path)
                        VALUES (?,?,?,?);'''
            cursor.execute(query, (fName, lName, country, profile_path))
        else:
            query = '''UPDATE players
                    SET firstName=?, lastName=?, country=?, profile_path=?
                    WHERE playerID=?;'''
            cursor.execute(query, (fName, lName, country, profile_path, id))

        conn.commit()
        conn.close()


    def removePlayer(self, playerID):
        conn = sq.connect('dartsDatabase.db')
        cursor = conn.cursor()
        
        query = '''DELETE FROM players 
                   WHERE playerID = ?;'''
        
        cursor.execute(query, (playerID,))

        conn.commit()
        conn.close()

    def get_all_players(self):
        conn = sq.connect('dartsDatabase.db')
        cursor = conn.cursor()

        query = 'SELECT * FROM players'

        cursor.execute(query)
        players = cursor.fetchall()

        conn.close()
        
        return players
    
    def get_player(self, id):
        conn = sq.connect('dartsDatabase.db')
        cursor = conn.cursor()

        query = 'SELECT * FROM players WHERE playerID = ?'

        cursor.execute(query, (id,))
        player = cursor.fetchone()

        conn.close()
        
        return player
    
    # A function to check if player is in database
    def inDatabase(self, fName, lName):
        conn = sq.connect('dartsDatabase.db')
        cursor = conn.cursor()

        query = '''SELECT * FROM players
                    WHERE firstName = ? AND lastName = ?;'''

        cursor.execute(query, (fName, lName))
        # fetch one player from the query
        player = cursor.fetchone()

        conn.close() 

        if player:   
            return True
        else:
            return False

    def addThrow(self, multiplier, wedge_value, playerID):
        conn = sq.connect('dartsDatabase.db')
        cursor = conn.cursor()

        points = multiplier * wedge_value

        query = '''INSERT INTO throws (points, playerID)
                    VALUES (?,?);'''
        
        cursor.execute(query, (points, playerID))

        conn.commit()
        conn.close()



    
    