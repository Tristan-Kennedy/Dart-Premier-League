from PySide6.QtWidgets import QLineEdit, QWidget, QSlider, QVBoxLayout, QPushButton, QDialog, QFormLayout, QLabel, QSpinBox, QDialogButtonBox, QCheckBox, QComboBox, QDateEdit
from PySide6.QtCore import Qt, Signal,  QDate

class Settings(QWidget):
    scoreboard_resize = Signal(int)
    undo_signal = Signal()
    game_configure = Signal(dict)
    gamestats_toggle = Signal(bool)
    playerstats_toggle = Signal(bool)
    gamestats_toggle = Signal(bool)
    add_player_signal = Signal(dict)
    get_players_signal = Signal()
    delete_player_signal = Signal(int)

    def __init__(self):
        super().__init__()
        self.scoreLabels = []
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.all_players = []
                
        # Slider for adjusting scoreboard size
        self.slider_label = QLabel("Scoreboard Size:")
        self.slider_label.setAlignment(Qt.AlignBottom)  # Align the label to the top
        self.layout.addWidget(self.slider_label)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(300)
        self.slider.setMaximum(800)
        self.slider.setValue(500)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setTickInterval(50)
        self.slider.valueChanged.connect(self.scoreboard_resize.emit)
        self.layout.addWidget(self.slider)

        # Undo button
        self.undo_button = QPushButton('Undo')
        self.undo_button.clicked.connect(self.undo_signal.emit)  # Emit undo signal without any arguments
        self.layout.addWidget(self.undo_button)

        # Button for game configuration
        self.config_button = QPushButton("Configure Game Settings")
        self.config_button.clicked.connect(self.open_config_dialog)
        self.layout.addWidget(self.config_button)

        # Gamestats toggle
        self.gamestats_checkbox = QCheckBox("Show Game Stats")
        self.gamestats_checkbox.setChecked(False)
        self.gamestats_checkbox.stateChanged.connect(self.toggle_gamestats)
        self.layout.addWidget(self.gamestats_checkbox)

        # Playerstats toggle
        self.playerstats_checkbox = QCheckBox("Show Player Stats")
        self.playerstats_checkbox.setChecked(False)
        self.playerstats_checkbox.stateChanged.connect(self.toggle_playerstats)
        self.layout.addWidget(self.playerstats_checkbox)

    def open_config_dialog(self):
        dialog = QDialog()
        layout = QFormLayout()

        starting_score_input = QSpinBox()
        starting_score_input.setRange(301, 801)
        starting_score_input.setSingleStep(100)
        layout.addRow(QLabel("Starting Score:"), starting_score_input)

        best_of_legs_input = QSpinBox()
        best_of_legs_input.setRange(1, 20)
        layout.addRow(QLabel("Best of Legs:"), best_of_legs_input)

        best_of_matches_input = QSpinBox()
        best_of_matches_input.setRange(1, 10)
        layout.addRow(QLabel("Best of Sets:"), best_of_matches_input)

        date_input = QDateEdit(QDate.currentDate())
        date_input.setCalendarPopup(True)
        layout.addRow(QLabel("Date of Match:"), date_input)

        location_input = QLineEdit()
        layout.addRow(QLabel("Location of Match:"), location_input)

        official_names_input = QLineEdit()
        layout.addRow(QLabel("Official Name:"), official_names_input)

        self.player1_dropdown = QComboBox()
        self.player2_dropdown = QComboBox()
        self.get_players_signal.emit()
        self.player1_dropdown.addItems(self.all_players)
        self.player2_dropdown.addItems(self.all_players)

        layout.addRow(QLabel("Player 1:"), self.player1_dropdown)
        layout.addRow(QLabel("Player 2:"), self.player2_dropdown)

        add_player_button = QPushButton("Add New Player")
        add_player_button.clicked.connect(self.open_add_player_dialog)
        layout.addRow(add_player_button)

        remove_player_button = QPushButton("Delete Player")
        remove_player_button.clicked.connect(self.open_remove_player_dialog)
        layout.addRow(remove_player_button)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addRow(button_box)

        dialog.setLayout(layout)
        dialog.setWindowTitle("Game Config.")

        result = dialog.exec()
        if result == QDialog.Accepted:
            self.game_configure.emit({
                'starting_score': starting_score_input.value(),
                'best_of_legs': best_of_legs_input.value(),
                'best_of_matches': best_of_matches_input.value(),
                'date_of_match': date_input.date().toString("yyyy-MM-dd"),
                'location_of_match': location_input.text(),
                'official_name': official_names_input.text(),
                'player1': self.player1_dropdown.currentText(),
                'player2': self.player2_dropdown.currentText()            
            })

    def open_add_player_dialog(self):
        dialog = QDialog()
        layout = QFormLayout()

        dialog.setLayout(layout)
        dialog.setWindowTitle("Add Player")

        first_name_input = QLineEdit()
        layout.addRow(QLabel("First Name:"), first_name_input)
        last_name_input = QLineEdit()
        layout.addRow(QLabel("Last Name:"), last_name_input)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addRow(button_box)

        result = dialog.exec()
        if result == QDialog.Accepted:
            self.add_player_signal.emit({
                'first_name': first_name_input.text(),
                'last_name': last_name_input.text()         
            })
            self.update_dropdowns()

    def open_remove_player_dialog(self):
        dialog = QDialog()
        layout = QFormLayout()

        dialog.setLayout(layout)
        dialog.setWindowTitle("Remove Player")

        self.remove_dropdown = QComboBox()
        self.get_players_signal.emit()
        self.remove_dropdown.addItems(self.all_players)

        layout.addRow(QLabel("Player to Delete:"), self.remove_dropdown)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addRow(button_box)

        result = dialog.exec()
        if result == QDialog.Accepted:
            player_id, _ = self.remove_dropdown.currentText().split(': ')
            self.delete_player_signal.emit(int(player_id))
            self.update_dropdowns()

    def update_dropdowns(self):
        # Clear the dropdowns
        self.player1_dropdown.clear()
        self.player2_dropdown.clear()

        # Add the updated players to the dropdowns
        self.player1_dropdown.addItems(self.all_players)
        self.player2_dropdown.addItems(self.all_players)
    
    def toggle_gamestats(self, state):
        self.gamestats_toggle.emit(state == 2)

    def toggle_playerstats(self, state):
        self.playerstats_toggle.emit(state == 2)