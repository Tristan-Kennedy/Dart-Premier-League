class Player:
    def __init__(self, name):
        self.name = name
        self.score = 501
        self.previous_score = 501
        self.legs_won = 0

class Game:
    def __init__(self, players):
        self.players = players
        self.current_player_index = 0
        self.starting_player_index = 0
        self.turns = 0
        self.game_states = []

    def get_current_player(self):
        return self.players[self.current_player_index]

    def reset_scores(self):
        for player in self.players:
            player.score = 501
    
    def store_game_state(self):
        game_state = {
            'scores': [player.score for player in self.players],
            'legs_won': [player.legs_won for player in self.players],
            'turns': self.turns,
            'current_player_index': self.current_player_index,
            'starting_player_index': self.starting_player_index
        }
        self.game_states.append(game_state)

    def undo(self):
        if not self.game_states:
            return

        game_state = self.game_states.pop()
        self.turns = game_state['turns']
        self.current_player_index = game_state['current_player_index']
        self.starting_player_index = game_state['starting_player_index']

        for player, score, legs_won in zip(self.players, game_state['scores'], game_state['legs_won']):
            player.score = score
            player.legs_won = legs_won


    def update_score(self, multiplier, wedge_value):
        self.store_game_state()

        current_player = self.get_current_player()
        current_player.score -= multiplier * wedge_value
        self.turns += 1

        bust = False
        if current_player.score == 0 and multiplier == 2:
            current_player.legs_won += 1
            self.reset_scores()
            self.turns = 0
            self.starting_player_index = (self.starting_player_index + 1) % len(self.players)
            self.current_player_index = self.starting_player_index
        elif current_player.score < 1 or current_player.score == 1:
            current_player.score = current_player.previous_score
            bust = True

        if self.turns >= 3 or bust:
            current_player.previous_score = current_player.score
            self.turns = 0
            self.current_player_index = (self.current_player_index + 1) % len(self.players)
