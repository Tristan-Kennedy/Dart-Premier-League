from .JumbotronUI import *
from .ScorekeeperUI import *
from .Game import *
from .Database import *
import sys

class Controller:
    def __init__(self):
        self.scorekeeper_ui = ScorekeeperUI()
        self.jumbotron_ui = JumbotronUI()
        self.jumbotron_ui.move(1000, 300)

        self.database = Database()

        self.scorekeeper_ui.settings.game_configure.connect(self.handle_configure_game)
        self.scorekeeper_ui.settings.open_config_dialog() # Open the configuration dialog before the rest as it initializes the game

        self.scorekeeper_ui.dartboard.dart_hit.connect(self.handle_dart_hit)
        self.scorekeeper_ui.settings.scoreboard_resize.connect(self.handle_scoreboard_resize)
        self.scorekeeper_ui.settings.undo_signal.connect(self.handle_undo)
        self.game.game_end.connect(self.handle_game_end)

        self.scorekeeper_ui.show()
        self.jumbotron_ui.show()

        self.refresh_scoreboard() # Call to initially display scoreboard

    def refresh_scoreboard(self):
        self.jumbotron_ui.scoreboard.refresh_scoreboard(self.game.players, self.game.current_player_index)

    def handle_dart_hit(self, multiplier, wedge_value):
        self.game.update_score(multiplier, wedge_value)
        self.refresh_scoreboard()

    def handle_undo(self):
        self.game.undo()
        self.refresh_scoreboard()

    def handle_scoreboard_resize(self, new_size):
        self.jumbotron_ui.resize(new_size * 2, new_size)

    def handle_configure_game(self, config):
        starting_score = config.get('starting_score', 501)
        best_of_legs = config.get('best_of_legs', 14)
        best_of_matches = config.get('best_of_matches', 4)

        player1 = Player("John", "Doe", starting_score)
        player2 = Player("Jane", "Doe", starting_score)

        # Check if the players are already in the database. If they are not, add them.
        if self.database.inDatabase(player1.fName, player1.lName) == False:
            self.database.addNewPlayer(player1.fName, player1.lName)
        
        if self.database.inDatabase(player2.fName, player2.lName) == False:
            self.database.addNewPlayer(player2.fName, player2.lName)

        players = [player1, player2]

        # Initialize game with new configuration
        self.game = Game(players, starting_score, best_of_legs, best_of_matches)
        self.refresh_scoreboard()
        
    def handle_game_end(self):
        print("Game Over.")
        sys.exit()

