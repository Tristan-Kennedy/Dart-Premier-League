from PySide6.QtWidgets import QLineEdit, QWidget, QSlider, QVBoxLayout, QPushButton, QDialog, QFormLayout, QLabel, QSpinBox, QDialogButtonBox, QCheckBox, QComboBox, QDateEdit, QFileDialog
from PySide6.QtCore import Qt, Signal,  QDate
from PySide6.QtGui import QPixmap
import os
from shutil import copyfile

class Settings(QWidget):
    scoreboard_resize = Signal(int)
    undo_signal = Signal()
    game_configure = Signal(dict)
    gamestats_toggle = Signal(bool)
    playerstats_toggle = Signal(bool)
    gamestats_toggle = Signal(bool)
    add_player_signal = Signal(dict)
    get_players_signal = Signal()
    get_player_signal = Signal(int)
    delete_player_signal = Signal(int)

    def __init__(self):
        super().__init__()
        self.scoreLabels = []
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.all_players = []
        self.current_player_info = None
                
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

        starting_score_input = QComboBox()
        starting_score_input.addItems(["301", "501", "801"])
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

        league_management_button = QPushButton("League Management")
        league_management_button.clicked.connect(self.open_league_management_dialog)
        layout.addRow(league_management_button)

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
                'starting_score': int(starting_score_input.currentText()),
                'best_of_legs': best_of_legs_input.value(),
                'best_of_matches': best_of_matches_input.value(),
                'date_of_match': date_input.date().toString("yyyy-MM-dd"),
                'location_of_match': location_input.text(),
                'official_name': official_names_input.text(),
                'player1': self.player1_dropdown.currentText(),
                'player2': self.player2_dropdown.currentText()            
            })

    def open_league_management_dialog(self):
        dialog = QDialog()
        layout = QFormLayout()

        dialog.setLayout(layout)
        dialog.setWindowTitle("League Management")

        self.select_dropdown = QComboBox()
        self.get_players_signal.emit()
        self.select_dropdown.addItem("New Player")
        self.select_dropdown.addItems(self.all_players)

        layout.addRow(QLabel("Select a Player to Manage:"), self.select_dropdown)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addRow(button_box)

        result = dialog.exec()
        if result == QDialog.Accepted:
            player_name = self.select_dropdown.currentText()
            if player_name == "New Player":
                self.open_profile_dialog()
            else:
                player_id, _ = player_name.split(': ')
                self.get_player_signal.emit(int(player_id))
                self.open_profile_dialog(self.current_player_info)

    def open_profile_dialog(self, player_info = None):
        dialog = QDialog()
        layout = QFormLayout()
        self.image_path = None

        dialog.setLayout(layout)
        dialog.setWindowTitle("Profile")

        first_name_input = QLineEdit()
        last_name_input = QLineEdit()
        country_input = QLineEdit()

        self.profile_image_label = QLabel()
        self.profile_image_label.setFixedSize(200, 200)
        self.profile_image_label.setStyleSheet("border: 1px solid black;")

        upload_button = QPushButton("Upload Image")
        upload_button.clicked.connect(self.upload_image)

        layout.addRow(QLabel("Profile Image:"), self.profile_image_label)
        layout.addRow(upload_button)
        layout.addRow(QLabel("First Name:"), first_name_input)
        layout.addRow(QLabel("Last Name:"), last_name_input)
        layout.addRow(QLabel("Country:"), country_input)

        if player_info:
            first_name_input.setText(str(player_info[1]))
            last_name_input.setText(str(player_info[2]))
            country_input.setText(str(player_info[3]))
            self.profile_image_label.setPixmap(QPixmap(player_info[4]).scaled(200, 200))

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addRow(button_box)

        result = dialog.exec()
        if result == QDialog.Accepted:
            player_data = {
                'first_name': first_name_input.text(),
                'last_name': last_name_input.text(),
                'country': country_input.text(),
                'profile_path': self.image_path if self.image_path else (player_info[4] if player_info else ""),
            }
            if player_info:
                player_data['id'] = player_info[0]
            self.add_player_signal.emit(player_data)
            self.update_dropdowns()

    def upload_image(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Images (*.png *.jpg *.bmp)")
        if file_dialog.exec_():
            file_path = file_dialog.selectedFiles()[0]
            # Get the filename from the full path
            filename = os.path.basename(file_path)
            # Destination directory for storing profile pictures
            profile_pictures_dir = "profile_pictures"
            # Create the directory if it doesn't exist
            os.makedirs(profile_pictures_dir, exist_ok=True)
            # Destination path for copying the file
            destination_path = os.path.join(profile_pictures_dir, filename)
            # Copy the file to the destination path
            copyfile(file_path, destination_path)
            # Set the pixmap and update the label
            pixmap = QPixmap(destination_path)
            self.profile_image_label.setPixmap(pixmap.scaled(200, 200))
            # Set a member variable to store the image path
            self.image_path = destination_path

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