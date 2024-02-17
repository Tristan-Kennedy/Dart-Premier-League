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

    def get_current_player(self):
        return self.players[self.current_player_index]

    def reset_scores(self):
        for player in self.players:
            player.score = 501

    def update_score(self, score):
        current_player = self.get_current_player()
        current_player.score -= score
        self.turns += 1

        bust = False
        if current_player.score == 0:
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
