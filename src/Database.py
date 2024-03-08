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
                lastName TEXT NOT NULL
                );'''
        )

        # Create the 'throws' table
        cursor.execute(
            '''CREATE TABLE IF NOT EXISTS throws(
                throwID INTEGER PRIMARY KEY,
                points INTEGER,
                playerID INTEGER SECONDARY KEY
            );'''
        )

        conn.commit()
        conn.close()

    def addNewPlayer(self, fName, lName):
        conn = sq.connect('dartsDatabase.db')  # Defines the connection to the db file, creates the file if it doesn't exist  
        cursor = conn.cursor()  # Corrected: Added missing parentheses to make it a method call

        query = '''INSERT INTO players (firstName, lastName)
                    VALUES (?,?);'''
        
        cursor.execute(query, (fName, lName))

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

    def addThrow(self, points, playerID):
        conn = sq.connect('dartsDatabase.db')
        cursor = conn.cursor()

        query = '''INSERT INTO throws (points, playerID)
                    VALUES (?,?);'''
        
        cursor.execute(query, (points, playerID))

        conn.commit()
        conn.close()



    
    