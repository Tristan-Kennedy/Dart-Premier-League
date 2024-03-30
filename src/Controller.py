from .JumbotronUI import *
from .ScorekeeperUI import *
from .Game import *
from .Database import *
from .StatsBoard import *
import sys

class Controller:
    def __init__(self):
        self.scorekeeper_ui = ScorekeeperUI()
        self.jumbotron_ui = JumbotronUI()
        self.stats_window = StatisticsWindow()
        self.database = Database()
        self.game = None

        self.scorekeeper_ui.settings.add_player_signal.connect(self.handle_add_player)
        self.scorekeeper_ui.settings.get_players_signal.connect(self.handle_get_players)
        self.scorekeeper_ui.settings.delete_player_signal.connect(self.handle_delete_player)
        self.scorekeeper_ui.settings.game_configure.connect(self.handle_configure_game)
        self.scorekeeper_ui.settings.open_config_dialog() # Open the configuration dialog before the rest as it initializes the game

        self.scorekeeper_ui.dartboard.dart_hit.connect(self.handle_dart_hit)
        self.scorekeeper_ui.dartboard.dart_knockout.connect(self.handle_knockout)
        self.scorekeeper_ui.settings.scoreboard_resize.connect(self.handle_scoreboard_resize)
        self.scorekeeper_ui.settings.undo_signal.connect(self.handle_undo)
        self.scorekeeper_ui.foul_signal.connect(self.handle_foul) #foul button
        self.scorekeeper_ui.bounceout_signal.connect(self.handle_bounceout) #bounceout button
        self.scorekeeper_ui.settings.playerstats_toggle.connect(self.handle_display_player_stats)
        self.scorekeeper_ui.show_leaderboard_signal.connect(self.handle_show_leaderboard)

        # If the game is still None at this point it did not initialize correctly and the program should exit.
        if(self.game == None):
            sys.exit()
            
        self.scorekeeper_ui.show()
        self.jumbotron_ui.show()

    def refresh_scoreboard(self):
        self.jumbotron_ui.scoreboard.refresh_scoreboard(self.game)

    def refresh_jumbotron_dartboard(self):
        self.jumbotron_ui.dartboard.clicked_points = self.scorekeeper_ui.dartboard.clicked_points
        self.jumbotron_ui.dartboard.update()

    def handle_dart_hit(self, multiplier, wedge_value):
        self.game.update_score(multiplier, wedge_value)
        self.refresh_scoreboard()
        self.refresh_jumbotron_dartboard()
    
    def handle_turn_switch(self):
        self.scorekeeper_ui.dartboard.clear_clicked_points()
        self.refresh_jumbotron_dartboard()

    def handle_undo(self):
        self.scorekeeper_ui.dartboard.undo_clicked_point()
        self.refresh_jumbotron_dartboard()
        self.game.undo()
        self.refresh_scoreboard()
        
    def handle_foul(self): #in the event of a foul, clear the dart dots from the board and move onto the next player
        self.game.foul()
        self.refresh_scoreboard()
        self.handle_turn_switch()
    
    def handle_bounceout(self): #in the event of a bounceout, the current turn scores 0
        self.game.bounceout()
        self.refresh_scoreboard()

    def handle_knockout(self, multiplier, wedge_value):
        self.game.update_score_knockout(multiplier, wedge_value)
        self.refresh_scoreboard()
        self.refresh_jumbotron_dartboard()

    def handle_scoreboard_resize(self, new_size):
        self.jumbotron_ui.resize(new_size, new_size * 1.5)

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
        date_of_match = config.get('date_of_match')
        location_of_match = config.get('location_of_match')
        official_name = config.get('official_name')

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
        self.game = Game(players, starting_score, best_of_legs, best_of_matches, date_of_match, location_of_match, official_name)

        self.game.game_end.connect(self.handle_game_end)
        self.game.turn_switch.connect(self.handle_turn_switch)

        self.refresh_scoreboard()
        self.handle_turn_switch()

    def handle_display_player_stats(self, visibility):
        self.stats_window.set_visibility(visibility)
        
    def handle_game_end(self):
        self.scorekeeper_ui.show_leaderboard_dialog()
        self.scorekeeper_ui.hide()

    def handle_show_leaderboard(self):
        self.jumbotron_ui.enable_leaderboard()