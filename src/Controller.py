class Controller:
    def __init__(self, game, jumbotron_ui, scorekeeper_ui):
        self.game = game
        self.jumbotron_ui = jumbotron_ui
        self.scorekeeper_ui = scorekeeper_ui

        self.scorekeeper_ui.dartboard.dart_hit.connect(self.handle_dart_hit)
        self.scorekeeper_ui.settings.scoreboard_resize.connect(self.handle_scoreboard_resize)

        self.scorekeeper_ui.show()
        self.jumbotron_ui.show()

        self.jumbotron_ui.scoreboard.refresh_scoreboard(self.game.players, self.game.current_player_index) # Call to initially display scoreboard

    def handle_dart_hit(self, score):
        self.game.update_score(score)
        self.jumbotron_ui.scoreboard.refresh_scoreboard(self.game.players, self.game.current_player_index) # Call to update scoreboard after each dart hit

    def handle_scoreboard_resize(self, new_size):
        self.jumbotron_ui.resize(new_size * 2, new_size)
        
