from PySide6.QtWidgets import QWidget, QSlider, QVBoxLayout, QPushButton, QDialog, QFormLayout, QLabel, QSpinBox, QDialogButtonBox, QCheckBox
from PySide6.QtCore import Qt, Signal

class Settings(QWidget):
    scoreboard_resize = Signal(int)
    undo_signal = Signal()
    game_configure = Signal(dict)
    gamestats_toggle = Signal(bool)
    playerstats_toggle = Signal(bool)

    def __init__(self):
        super().__init__()
        self.scoreLabels = []
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
                
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(50)
        self.slider.setMaximum(500)
        self.slider.setValue(200)
        self.slider.valueChanged.connect(self.scoreboard_resize.emit)
        self.layout.addWidget(self.slider)

        self.undo_button = QPushButton('Undo')
        self.undo_button.clicked.connect(self.undo_signal.emit)  # Emit undo signal without any arguments
        self.layout.addWidget(self.undo_button)

        # Add a button for game configuration
        self.config_button = QPushButton("Configure Game Settings")
        self.config_button.clicked.connect(self.open_config_dialog)
        self.layout.addWidget(self.config_button)

        # Add gamestats toggle
        self.gamestats_checkbox = QCheckBox("Show Game Stats")
        self.gamestats_checkbox.setChecked(False)
        self.gamestats_checkbox.stateChanged.connect(self.toggle_gamestats)
        self.layout.addWidget(self.gamestats_checkbox)

        # Add playerstats toggle
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
        layout.addRow(QLabel("Best of Matches:"), best_of_matches_input)

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
                'best_of_matches': best_of_matches_input.value()
            })
    
    def toggle_gamestats(self, state):
        self.gamestats_toggle.emit(state == Qt.Checked)

    def toggle_playerstats(self, state):
        self.playerstats_toggle.emit(state == Qt.Checked)