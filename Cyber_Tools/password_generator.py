import sys
import random
import string
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QSpinBox, QProgressBar, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor
import os

class PasswordGeneratorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Advanced Strong Password Generator")
        self.setGeometry(300, 300, 500, 420)

        main_layout = QVBoxLayout()

        # Password length
        length_layout = QHBoxLayout()
        length_label = QLabel("Password Length (8–13):")
        self.length_spin = QSpinBox()
        self.length_spin.setRange(8, 13)
        self.length_spin.setValue(8)
        length_layout.addWidget(length_label)
        length_layout.addWidget(self.length_spin)

        # Number count
        num_layout = QHBoxLayout()
        num_label = QLabel("How many numbers (min 1):")
        self.num_spin = QSpinBox()
        self.num_spin.setRange(1, 13)
        self.num_spin.setValue(1)
        num_layout.addWidget(num_label)
        num_layout.addWidget(self.num_spin)

        # Custom numbers
        custom_num_layout = QHBoxLayout()
        custom_num_label = QLabel("Choose your numbers:")
        self.custom_num_input = QLineEdit()
        self.custom_num_input.setPlaceholderText("e.g. 123456")
        custom_num_layout.addWidget(custom_num_label)
        custom_num_layout.addWidget(self.custom_num_input)

        # Special character count
        spec_layout = QHBoxLayout()
        spec_label = QLabel("Special Characters (min 1):")
        self.spec_spin = QSpinBox()
        self.spec_spin.setRange(1, 10)
        self.spec_spin.setValue(1)
        spec_layout.addWidget(spec_label)
        spec_layout.addWidget(self.spec_spin)

        # Strength Bar
        self.strength_bar = QProgressBar()
        self.strength_bar.setRange(0, 100)
        self.strength_bar.setValue(0)
        self.strength_bar.setFormat("Strength: %p%")

        # Generate button
        self.generate_btn = QPushButton("Generate Password")
        self.generate_btn.clicked.connect(self.generate_password)

        # Password Output
        self.output = QLineEdit()
        self.output.setReadOnly(True)

        # Copy button
        self.copy_btn = QPushButton("Copy to Clipboard")
        self.copy_btn.clicked.connect(self.copy_to_clipboard)

        # Compare user password input
        compare_layout = QHBoxLayout()
        self.compare_input = QLineEdit()
        self.compare_input.setPlaceholderText("Enter your password to compare")
        self.compare_btn = QPushButton("Compare")
        self.compare_btn.clicked.connect(self.compare_passwords)
        compare_layout.addWidget(self.compare_input)
        compare_layout.addWidget(self.compare_btn)

        # Save history button
        self.history_btn = QPushButton("Save to Password History")
        self.history_btn.clicked.connect(self.save_history)

        # Add widgets to main layout
        main_layout.addLayout(length_layout)
        main_layout.addLayout(num_layout)
        main_layout.addLayout(custom_num_layout)
        main_layout.addLayout(spec_layout)
        main_layout.addWidget(self.strength_bar)
        main_layout.addWidget(self.generate_btn)
        main_layout.addWidget(self.output)
        main_layout.addWidget(self.copy_btn)
        main_layout.addLayout(compare_layout)
        main_layout.addWidget(self.history_btn)

        self.setLayout(main_layout)

    def generate_password(self):
        length = self.length_spin.value()
        num_count = self.num_spin.value()
        spec_count = self.spec_spin.value()

        custom_numbers = self.custom_num_input.text().strip()
        if not custom_numbers:
            custom_numbers = string.digits

        if num_count + spec_count > length:
            self.output.setText("Error: Length too small!")
            return

        letters = string.ascii_letters
        specials = "!@#$%^&*()-_=+?/<>"

        password = []
        password += random.choices(custom_numbers, k=num_count)
        password += random.choices(specials, k=spec_count)
        password += random.choices(letters, k=length - (num_count + spec_count))

        random.shuffle(password)
        final_password = ''.join(password)
        self.output.setText(final_password)

        score = self.calculate_strength(final_password)
        self.update_strength_color(score)
        self.strength_bar.setValue(score)

    def calculate_strength(self, password):
        score = 0
        if any(c.islower() for c in password): score += 20
        if any(c.isupper() for c in password): score += 20
        if any(c.isdigit() for c in password): score += 20
        if any(c in "!@#$%^&*()-_=+?/<>" for c in password): score += 20
        if len(password) >= 12: score += 20
        return score

    def update_strength_color(self, score):
        pal = self.strength_bar.palette()
        if score < 40:
            pal.setColor(QPalette.Highlight, QColor(Qt.red))
        elif score < 80:
            pal.setColor(QPalette.Highlight, QColor(Qt.yellow))
        else:
            pal.setColor(QPalette.Highlight, QColor(Qt.green))
        self.strength_bar.setPalette(pal)

    def copy_to_clipboard(self):
        QApplication.clipboard().setText(self.output.text())
        QMessageBox.information(self, "Copied", "Password copied to clipboard!")

    def save_history(self):
        pwd = self.output.text()
        if not pwd:
            QMessageBox.warning(self, "Error", "Generate a password first!")
            return

        with open("password_history.txt", "a") as file:
            file.write(pwd + "\n")

        QMessageBox.information(self, "Saved", "Password saved to history file.")

    def compare_passwords(self):
        user_pwd = self.compare_input.text()
        if not user_pwd:
            QMessageBox.warning(self, "Error", "Enter a password to compare!")
            return

        score = self.calculate_strength(user_pwd)
        msg = f"Your Password Strength: {score}%"
        QMessageBox.information(self, "Comparison Result", msg)
