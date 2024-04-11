from PySide6.QtCore import QObject, Signal

class Player:
    def __init__(self, fname, lname, id, starting_score):
        self.fName = fname
        self.lName = lname
        self.playerID = id
        self.score = starting_score
        self.starting_score = starting_score
        self.previous_score = starting_score
        self.legs_won = 0
        self.matches_won = 0
        self.total_throws = 0
    
    def get_playerID(self):
        return self.get_playerID


class Game(QObject):
    game_end = Signal()
    turn_switch = Signal()
    leg_complete_signal = Signal(object)
    match_complete_signal = Signal(object)
    update_three_dart_avg_signal = Signal(object)
    update_wins_signal = Signal(int)
    update_rank_signal = Signal()

    def __init__(self, players=[], starting_score=501, best_of_legs=14, best_of_matches=4, date_of_match=None, location_of_match=None, official_name=None):
        super().__init__()
        self.players = players
        self.starting_score = starting_score
        self.best_of_legs = best_of_legs
        self.best_of_matches = best_of_matches
        self.date_of_match = date_of_match
        self.location_of_match = location_of_match
        self.official_name = official_name
        self.current_player_index = 0
        self.starting_player_index = 0
        self.turns = 0
        self.game_states = []
        self.bust = False
        self.leg_end = False
#############################
        self.turn_counter = 0
        self.turn_counter_current_player = [0, 0]
        self.total_turn_scores = 0
        self.total_turn_scores_current_player = [0, 0]
        self.avg_score_per_turn = 0
        self.avg_score_per_turn_current_player = 0
        self.avg_turn_score = 0
        self.num_180s = 0
        self.current_turn_score = 0
        self.lowest_turn_score = 999
        self.three_dart_avg = 0

    def on_leg_complete(self):
        # Data to be sent to the database
        DB_leg_data = {
            'playerID': self.players[self.current_player_index].playerID,
            'fName': self.players[self.current_player_index].fName,
            'lName': self.players[self.current_player_index].lName,
            'player1Score': self.players[self.current_player_index].score,
            'opponentID': self.players[1 - self.current_player_index].playerID,
            'opponentFName': self.players[1 - self.current_player_index].fName,
            'opponentLName': self.players[1 - self.current_player_index].lName,
            'oppScore': self.players[1 - self.current_player_index].score,
            'winnerID': self.players[self.current_player_index].playerID
        }
        self.leg_complete_signal.emit(DB_leg_data)
        for player in self.players:
            player.score = self.starting_score
            player.previous_score = self.starting_score
            player.total_throws = 0 #reset the number of darts thrown
        self.turns = 0
        self.leg_end = True

    def on_match_complete(self):
        # Data to be sent to the database
        DB_match_data = {
            'player1ID': self.players[self.current_player_index].playerID,
            'fName': self.players[self.current_player_index].fName,
            'lName': self.players[self.current_player_index].lName,
            'legs_won': self.players[self.current_player_index].legs_won,
            'opponentID': self.players[1-self.current_player_index].playerID,
            'opponentFName': self.players[1-self.current_player_index].fName,
            'opponentLName': self.players[1-self.current_player_index].lName,
            'oppLegsWon': self.players[1-self.current_player_index].legs_won,
            'winnerID': self.players[self.current_player_index].playerID
        }
        self.match_complete_signal.emit(DB_match_data)
        for player in self.players:
            player.legs_won = 0
            player.total_throws = 0 #reset the number of darts thrown
        self.starting_player_index = 1

    def store_game_state(self):
        game_state = {
            'scores': [player.score for player in self.players],
            'legs_won': [player.legs_won for player in self.players],
            'matches_won': [player.matches_won for player in self.players],
            'turns': self.turns,
            'current_player_index': self.current_player_index,
            'starting_player_index': self.starting_player_index,
            'bust': self.bust,
            'leg_end': self.leg_end,
            'throws': [player.total_throws for player in self.players]
        }
        self.game_states.append(game_state)

    def undo(self):
        if not self.game_states:
            return

        game_state = self.game_states.pop()
        self.turns = game_state['turns']
        self.current_player_index = game_state['current_player_index']
        self.starting_player_index = game_state['starting_player_index']
        self.bust = game_state['bust']
        self.leg_end = game_state['leg_end']
    

        for player, score, legs_won, matches_won, throws in zip(self.players, game_state['scores'], game_state['legs_won'], game_state['matches_won'], game_state['throws']):
            player.score = score
            player.legs_won = legs_won
            player.matches_won = matches_won
            player.total_throws = throws

    def update_score(self, multiplier, wedge_value):
        self.store_game_state()
        current_player = self.players[self.current_player_index]
        if self.leg_end:
            self.leg_end = False
            self.turn_switch.emit()
            self.starting_player_index = (self.starting_player_index + 1) % len(self.players)
            self.current_player_index = self.starting_player_index

        if self.bust or self.turns == 3:
            current_player.previous_score = current_player.score
            ################################
            self.turn_counter += 1
            self.total_turn_scores += self.current_turn_score
            self.avg_score_per_turn = self.total_turn_scores / self.turn_counter
            # data to be sent to the database
            self.turn_counter_current_player[self.current_player_index] += 1
            self.total_turn_scores_current_player[self.current_player_index] += self.current_turn_score
            self.avg_score_per_turn_current_player = self.total_turn_scores_current_player[self.current_player_index] / self.turn_counter_current_player[self.current_player_index]
            three_dart_avg_data = {
                'playerID': self.players[self.current_player_index].playerID, 
                'threeDartAvg' : self.avg_score_per_turn_current_player
                } 
            self.update_three_dart_avg_signal.emit(three_dart_avg_data)
            if self.lowest_turn_score > self.current_turn_score:
                self.lowest_turn_score = self.current_turn_score
            if self.current_turn_score == 180:
                self.num_180s += 1
            self.turns = 0
            self.current_player_index = (self.current_player_index + 1) % len(self.players)
            self.turn_switch.emit()

        current_player = self.players[self.current_player_index]
        current_player.score -= multiplier * wedge_value
        current_player.total_throws += 1 #update the number of darts thrown for that player
        ###############################################
        self.current_turn_score = current_player.previous_score - current_player.score # get current turn score
        self.turns += 1
        self.avg_turn_score = self.current_turn_score / self.turns  # average of this turn

        self.bust = False
        if current_player.score == 0 and multiplier == 2:
            current_player.legs_won += 1
            if current_player.legs_won >= self.best_of_legs:
                current_player.matches_won += 1
                if current_player.matches_won >= self.best_of_matches:
                    self.update_wins_signal.emit(self.players[self.current_player_index].playerID)
                    self.update_rank_signal.emit()
                    self.game_end.emit()
                self.on_match_complete()
            self.on_leg_complete()
        elif current_player.score < 1 or current_player.score == 1:
            current_player.score = current_player.previous_score
            self.bust = True

    def update_score_knockout(self, multiplier, wedge_value):
        self.store_game_state()
        current_player = self.players[self.current_player_index]
        current_player.score += multiplier * wedge_value

    def foul(self): #skip the current player's turn 
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        self.turns = 0
    
    def bounceout(self): #score doesn't update 
        self.update_score(0, 0) #maybe add a visual indicator that the dart did not stick to the board

