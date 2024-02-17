class Controller:
    def __init__(self, game, scoreboard_view, dartboard_view):
        self.game = game
        self.scoreboard_view = scoreboard_view
        self.dartboard_view = dartboard_view

        self.dartboard_view.dart_hit.connect(self.handle_dart_hit)

        self.scoreboard_view.refresh_scoreboard(self.game.players, self.game.current_player_index)
        self.dartboard_view.show()
        self.scoreboard_view.show()

    def handle_dart_hit(self, score):
        self.game.update_score(score)
        self.scoreboard_view.refresh_scoreboard(self.game.players, self.game.current_player_index)