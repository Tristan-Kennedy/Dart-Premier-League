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
        self.game = None

        self.database = Database()

        self.scorekeeper_ui.settings.add_player_signal.connect(self.handle_add_player)
        self.scorekeeper_ui.settings.get_players_signal.connect(self.handle_get_players)
        self.scorekeeper_ui.settings.delete_player_signal.connect(self.handle_delete_player)
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

    def handle_add_player(self, player):
        self.database.addNewPlayer(player.get('first_name'), player.get('last_name'))
        self.handle_get_players() # Call after adding to get the new player in the dropdowns
    
    def handle_get_players(self):
        players = self.database.get_all_players()
        # Convert each tuple into a string
        players = ['{}: {} {}'.format(id, first_name, last_name) for id, first_name, last_name in players]
        self.scorekeeper_ui.settings.all_players = players
    
    def handle_delete_player(self, player_id):
        self.database.removePlayer(player_id)
        self.handle_get_players() # Call after deleting to remove player in the dropdowns

    def handle_configure_game(self, config):
        starting_score = config.get('starting_score', 501)
        best_of_legs = config.get('best_of_legs', 14)
        best_of_matches = config.get('best_of_matches', 4)
        player1 = config.get('player1')
        player2 = config.get('player2')

        player1_id, player1_name = config.get('player1').split(': ')
        player1_id = int(player1_id)
        player1_first_name, player1_last_name = player1_name.split(' ')

        player2_id, player2_name = config.get('player2').split(': ')
        player2_id = int(player2_id)
        player2_first_name, player2_last_name = player2_name.split(' ')

        player1 = Player(player1_first_name, player1_last_name, player1_id, starting_score)
        player2 = Player(player2_first_name, player2_last_name, player2_id, starting_score)

        players = [player1, player2]

        # Initialize game with new configuration
        self.game = Game(players, starting_score, best_of_legs, best_of_matches)
        self.refresh_scoreboard()
        
    def handle_game_end(self):
        print("Game Over.")
        sys.exit()

