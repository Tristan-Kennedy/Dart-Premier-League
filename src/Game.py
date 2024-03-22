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
    
    def get_playerID(self):
        return self.get_playerID


class Game(QObject):
    game_end = Signal()
    turn_switch = Signal()

    def __init__(self, players = [], starting_score = 501, best_of_legs = 14, best_of_matches = 4):
        super().__init__()
        self.players = players
        self.starting_score = starting_score
        self.best_of_legs = best_of_legs
        self.best_of_matches = best_of_matches
        self.current_player_index = 0
        self.starting_player_index = 0
        self.turns = 0
        self.game_states = []
        self.bust = False
        self.leg_end = False

    def on_leg_complete(self):
        for player in self.players:
            player.score = self.starting_score
            player.previous_score = self.starting_score
        self.turns = 0
        self.leg_end = True

    def on_match_complete(self):
        for player in self.players:
            player.legs_won = 0
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
            'leg_end': self.leg_end
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

        for player, score, legs_won, matches_won in zip(self.players, game_state['scores'], game_state['legs_won'], game_state['matches_won']):
            player.score = score
            player.legs_won = legs_won
            player.matches_won = matches_won

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
            self.turns = 0
            self.current_player_index = (self.current_player_index + 1) % len(self.players)
            self.turn_switch.emit()

        current_player = self.players[self.current_player_index]
        current_player.score -= multiplier * wedge_value
        self.turns += 1

        self.bust = False
        if current_player.score == 0 and multiplier == 2:
            current_player.legs_won += 1
            if current_player.legs_won >= self.best_of_legs:
                current_player.matches_won += 1
                if current_player.matches_won >= self.best_of_matches:
                    self.game_end.emit()
                self.on_match_complete()
            self.on_leg_complete()
        elif current_player.score < 1 or current_player.score == 1:
            current_player.score = current_player.previous_score
            self.bust = True