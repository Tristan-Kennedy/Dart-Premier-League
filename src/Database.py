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
                profile_path TEXT NOT NULL,
                threeDartAvg REAL,
                threeDartAvgTracker INTEGER, 
                numberOf180s INTEGER,
                gamesPlayed INTEGER,
                wins INTEGER,
                rank INTEGER
                );'''
        )

        # Create the 'throws' table
        cursor.execute(
            '''CREATE TABLE IF NOT EXISTS throws(
                throwID INTEGER PRIMARY KEY,
                points INTEGER,
                playerFirstName TEXT,
                playerLastName TEXT,
                location TEXT,
                date TEXT,
                playerID INTEGER SECONDARY KEY                
            );'''
        )

        # Create the 'games' table
        cursor.execute(
            '''CREATE TABLE IF NOT EXISTS games(
                gameID INTEGER PRIMARY KEY,
                player1ID INTEGER,
                player2ID INTEGER,
                date TEXT,
                location TEXT,
                officialName TEXT,
                bestOfLegs INTEGER,
                bestOfMatches INTEGER
            );'''
        )
        # Create the 'legs' table
        cursor.execute(
            '''CREATE TABLE IF NOT EXISTS legs(
                legID INTEGER PRIMARY KEY,
                player1ID INTEGER,
                player1FirstName TEXT,
                player1LastName TEXT,
                player1Score INTEGER,
                player2ID INTEGER,
                player2FirstName TEXT,
                player2LastName TEXT,
                player2Score INTEGER,
                winnerID INTEGER
            );'''
        )
        # Create the 'matches' table
        cursor.execute(
            '''CREATE TABLE IF NOT EXISTS matches(
                matchID INTEGER PRIMARY KEY,
                player1ID INTEGER,
                player1FirstName TEXT,
                player1LastName TEXT,
                player1LegsWon INTEGER,
                player2ID INTEGER,
                player2FirstName TEXT,
                player2LastName TEXT,
                player2LegsWon INTEGER,
                winnerID INTEGER
            );'''
        )
        conn.commit()
        conn.close()

    def addOrUpdatePlayer(self, fName, lName, country, profile_path, id=None, avg=0, avgTracker=0, oneEighties=0, gamesPlayed=0, wins=0, rank=None):
        conn = sq.connect('dartsDatabase.db')
        cursor = conn.cursor()
        if id is None:
            query = '''INSERT INTO players (firstName, lastName, country, profile_path, threeDartAvg, threeDartAvgTracker, numberOf180s, gamesPlayed, wins)
                        VALUES (?,?,?,?,?,?,?,?,?);'''
            cursor.execute(query, (fName, lName, country, profile_path, avg, avgTracker, oneEighties, gamesPlayed, wins))
        else:
            query = '''UPDATE players
                    SET firstName=?, lastName=?, country=?, profile_path=?, threeDartAvg=?, threeDartAvgTracker=?, numberOf180s=?, gamesPlayed=?, wins=?
                    WHERE playerID=?;'''
            cursor.execute(query, (fName, lName, country, profile_path, avg, avgTracker, oneEighties, gamesPlayed, wins, id))
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

    def addThrow(self, multiplier, wedge_value, playerID, playerFirstName, playerLastName, location, date):
        conn = sq.connect('dartsDatabase.db')
        cursor = conn.cursor()
        points = multiplier * wedge_value
        query = '''INSERT INTO throws (points, playerID, playerFirstName, playerLastName, location, date)
                    VALUES (?,?,?,?,?,?);'''
        cursor.execute(query, (points, playerID, playerFirstName, playerLastName, location, date))
        conn.commit()
        conn.close()

    def addGame(self, player1ID, player2ID, date, location, officialName, bestOfLegs, bestOfMatches):
        conn = sq.connect('dartsDatabase.db')
        cursor = conn.cursor()
        query = '''INSERT INTO games (player1ID, player2ID, date, location, officialName, bestOfLegs, bestOfMatches)
                    VALUES (?,?,?,?,?,?,?);'''
        cursor.execute(query, (player1ID, player2ID, date, location, officialName, bestOfLegs, bestOfMatches))
        conn.commit()
        conn.close()
    
    def addMatch(self, player1ID, player1FirstName, player1LastName, player1LegsWon, player2ID, player2FirstName, player2LastName, player2LegsWon, winnerID):
        conn = sq.connect('dartsDatabase.db')
        cursor = conn.cursor()
        query = '''INSERT INTO matches (player1ID, player1FirstName, player1LastName, player1LegsWon, player2ID, player2FirstName, player2LastName, player2LegsWon, winnerID)
                    VALUES (?,?,?,?,?,?,?,?,?);'''
        cursor.execute(query, (player1ID, player1FirstName, player1LastName, player1LegsWon, player2ID, player2FirstName, player2LastName, player2LegsWon, winnerID))
        conn.commit()
        conn.close()

    def addLeg(self, player1ID, player1FirstName, player1LastName, player1Score, player2ID, player2FirstName, player2LastName, player2Score, winnerID):
        conn = sq.connect('dartsDatabase.db')
        cursor = conn.cursor()
        query = '''INSERT INTO legs (player1ID, player1FirstName, player1LastName, player1Score, player2ID, player2FirstName, player2LastName, player2Score, winnerID)
                    VALUES (?,?,?,?,?,?,?,?,?);'''
        cursor.execute(query, (player1ID, player1FirstName, player1LastName, player1Score, player2ID, player2FirstName, player2LastName, player2Score, winnerID))
        conn.commit()
        conn.close()
    
    def updateThreeDartAvg(self, playerID, new_avg):
        conn = sq.connect('dartsDatabase.db')
        cursor = conn.cursor()

        # Fetch the current average and the tracker count
        cursor.execute('''
            SELECT threeDartAvg, threeDartAvgTracker FROM players
            WHERE playerID = ?;
            ''', (playerID,))
        result = cursor.fetchone()
        if result:
            current_avg, count = result
            # Calculate the new average
            if (count > 0)and (current_avg > 0) :  # Ensure there is at least one previous average to avoid division by zero
                updated_avg = ((current_avg * count) + new_avg) / count
            else:
                updated_avg = new_avg

            # Update the new average in the database
            cursor.execute('''
                UPDATE players
                SET threeDartAvg = ?
                WHERE playerID = ?;
            ''', (updated_avg, playerID))
            conn.commit()
        conn.close()

    def updateAvgTracker(self, playerID):
        conn = sq.connect('dartsDatabase.db')
        cursor = conn.cursor()
        query = '''UPDATE players
                    SET threeDartAvgTracker = threeDartAvgTracker + 1
                    WHERE playerID = ?;'''
        cursor.execute(query, (playerID,))
        conn.commit()
        conn.close()

    def updateGamesPlayed(self, playerID):
        conn = sq.connect('dartsDatabase.db')
        cursor = conn.cursor()
        # update the gamesPlayed column for the player by 1
        query = '''UPDATE players
                    SET gamesPlayed = gamesPlayed + 1
                    WHERE playerID = ?;'''
        cursor.execute(query, (playerID,))
        conn.commit()

    def updateWins(self, playerID):
        conn = sq.connect('dartsDatabase.db')
        cursor = conn.cursor()
        # update the wins column for the player by 1
        query = '''UPDATE players
                    SET wins = wins + 1
                    WHERE playerID = ?;'''
        cursor.execute(query, (playerID,))
        conn.commit()
        conn.close()

    def updatePlayerRanks(self):
        conn = sq.connect('dartsDatabase.db')
        cursor = conn.cursor()
        # Retrieve players ordered by wins in descending order
        cursor.execute('''
            SELECT playerID FROM players
            ORDER BY wins DESC
        ''')
        players = cursor.fetchall()

        # Update rank based on order in the result set
        rank = 1
        for player in players:
            # Update the rank of the player
            cursor.execute('''
                UPDATE players
                SET rank = ?
                WHERE playerID = ?;
            ''', (rank, player[0]))
            rank += 1
        
        conn.commit()
        conn.close()
    
    def updateOneEighties(self, num_one_eighties, playerID):
        conn = sq.connect('dartsDatabase.db')
        cursor = conn.cursor()
        query = '''UPDATE players
                    SET numberOf180s = numberOf180s + ?
                    WHERE playerID = ?;'''
        cursor.execute(query, (num_one_eighties, playerID))
        conn.commit()
        conn.close()


    

    
    