import sys
import numpy as np

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTableWidget, QTableWidgetItem,
    QSpinBox, QTextEdit, QGroupBox, QGridLayout, QHeaderView, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class RankNullityApp(QMainWindow):
    """
    A PyQt5 GUI application for calculating the Rank and Nullity of a matrix.
    The process shows the step-by-step reduction to Row Echelon Form.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Rank and Nullity Calculator")
        self.setGeometry(100, 100, 1200, 700)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.main_layout = QHBoxLayout(self.central_widget)

        self.create_input_widgets()
        self.create_output_widgets()

        self.setup_layout()

    def create_input_widgets(self):
        """Creates all the widgets for the user input panel."""
        self.size_group = QGroupBox("Matrix Dimensions")
        self.size_layout = QGridLayout(self.size_group)
        
        self.rows_label = QLabel("Number of Rows (m):")
        self.rows_spinbox = QSpinBox()
        self.rows_spinbox.setRange(1, 10)
        self.rows_spinbox.setValue(3)
        self.rows_spinbox.valueChanged.connect(self.update_ui_size)

        self.cols_label = QLabel("Number of Columns (n):")
        self.cols_spinbox = QSpinBox()
        self.cols_spinbox.setRange(1, 10)
        self.cols_spinbox.setValue(4)
        self.cols_spinbox.valueChanged.connect(self.update_ui_size)
        
        self.size_layout.addWidget(self.rows_label, 0, 0)
        self.size_layout.addWidget(self.rows_spinbox, 0, 1)
        self.size_layout.addWidget(self.cols_label, 1, 0)
        self.size_layout.addWidget(self.cols_spinbox, 1, 1)

        self.matrix_group = QGroupBox("Enter Matrix [A]")
        self.matrix_layout = QVBoxLayout(self.matrix_group)
        self.matrix_table = QTableWidget()
        self.matrix_layout.addWidget(self.matrix_table)
        
        self.calc_button = QPushButton("Calculate Rank & Nullity")
        self.calc_button.setFont(QFont("Arial", 12, QFont.Bold))
        self.calc_button.clicked.connect(self.run_calculator)
        
        self.clear_button = QPushButton("Clear All")
        self.clear_button.clicked.connect(self.clear_all_fields)

        self.update_ui_size()

    def create_output_widgets(self):
        """Creates the text area for displaying the solution steps."""
        self.output_group = QGroupBox("Calculation Steps & Results")
        self.output_layout = QVBoxLayout(self.output_group)
        self.solution_display = QTextEdit()
        self.solution_display.setReadOnly(True)
        self.solution_display.setFont(QFont("Courier New", 10))
        self.solution_display.setLineWrapMode(QTextEdit.NoWrap)
        self.output_layout.addWidget(self.solution_display)

    def setup_layout(self):
        """Arranges all widgets in the main window layout."""
        input_panel = QWidget()
        input_layout = QVBoxLayout(input_panel)
        
        input_layout.addWidget(self.size_group)
        input_layout.addWidget(self.matrix_group)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.clear_button)
        button_layout.addWidget(self.calc_button)
        input_layout.addLayout(button_layout)
        
        input_panel.setFixedWidth(450)
        
        self.main_layout.addWidget(input_panel)
        self.main_layout.addWidget(self.output_group)

    def update_ui_size(self):
        """Resizes the UI tables when the matrix dimensions change."""
        rows = self.rows_spinbox.value()
        cols = self.cols_spinbox.value()
        
        self.matrix_table.setRowCount(rows)
        self.matrix_table.setColumnCount(cols)
        self.matrix_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.matrix_table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        if rows == 3 and cols == 4:
            if self.matrix_table.item(0, 0) is None or self.matrix_table.item(0,0).text() == "":
                # Pre-fill with a classic example
                vals = [['1', '2', '1', '1'], ['2', '4', '2', '2'], ['1', '2', '3', '4']]
                for r in range(rows):
                    for c in range(cols):
                        self.matrix_table.setItem(r, c, QTableWidgetItem(vals[r][c]))

    def clear_all_fields(self):
        """Clears all input and output fields."""
        rows = self.rows_spinbox.value()
        cols = self.cols_spinbox.value()
        for r in range(rows):
            for c in range(cols):
                self.matrix_table.setItem(r, c, QTableWidgetItem(""))
        self.solution_display.clear()

    def show_message(self, title, message):
        """Displays a standardized message box."""
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setText(message)
        msg_box.setWindowTitle(title)
        msg_box.exec_()

    @staticmethod
    def format_matrix(m, title="Matrix", precision=4):
        """Pretty-prints a NumPy matrix into a string for display."""
        header = f"--- {title} ---\n"
        body = ""
        for row in m:
            body += " | ".join([f"{val:{7+precision}.{precision}f}" for val in row]) + "\n"
        return header + body

    def get_inputs(self):
        """Reads UI inputs and returns them as a NumPy array."""
        rows = self.rows_spinbox.value()
        cols = self.cols_spinbox.value()
        try:
            matrix = np.zeros((rows, cols))
            for r in range(rows):
                for c in range(cols):
                    matrix[r, c] = float(self.matrix_table.item(r, c).text())
        except (ValueError, AttributeError):
            self.show_message("Input Error", "All matrix cells must contain valid numbers.")
            return None
        return matrix

    def run_calculator(self):
        """Main function to perform row reduction and find rank and nullity."""
        self.solution_display.clear()
        
        M = self.get_inputs()
        if M is None: return

        self.solution_display.append("--- Starting Rank & Nullity Calculation ---\n")
        self.solution_display.append(self.format_matrix(M, "Original Matrix [A]"))

        num_rows, num_cols = M.shape
        M_ref = M.copy().astype(float) # Use a copy for row reduction
        
        self.solution_display.append("\n--- Reducing to Row Echelon Form (REF) ---\n")
        
        pivot_row = 0
        for j in range(num_cols): # Iterate through columns
            if pivot_row >= num_rows:
                break

            # Find a non-zero pivot in the current column
            i = pivot_row
            while i < num_rows and abs(M_ref[i, j]) < 1e-12:
                i += 1

            if i < num_rows: # A pivot was found
                # Swap the pivot row with the current row
                if i != pivot_row:
                    self.solution_display.append(f"-> Swap R{pivot_row + 1} and R{i + 1} to get non-zero pivot.")
                    M_ref[[pivot_row, i]] = M_ref[[i, pivot_row]]
                    self.solution_display.append(self.format_matrix(M_ref, f"After Swapping"))
                
                # Eliminate entries below the pivot
                pivot_val = M_ref[pivot_row, j]
                self.solution_display.append(f"-> Using pivot at R{pivot_row+1}, C{j+1}. Eliminating entries below it.")
                for i in range(pivot_row + 1, num_rows):
                    factor = M_ref[i, j] / pivot_val
                    if abs(factor) > 1e-12:
                        self.solution_display.append(f"  - R{i+1} = R{i+1} - ({factor:.4f}) * R{pivot_row+1}")
                        M_ref[i, :] -= factor * M_ref[pivot_row, :]
                
                self.solution_display.append(self.format_matrix(M_ref, f"After Elimination for Column {j+1}"))
                QApplication.processEvents()

                pivot_row += 1

        self.solution_display.append("\n--- ROW REDUCTION COMPLETE ---\n")
        self.solution_display.append(self.format_matrix(M_ref, "Final Row Echelon Form"))
        
        # Calculate Rank by counting non-zero rows
        rank = 0
        for row in M_ref:
            if np.any(np.abs(row) > 1e-12):
                rank += 1
        
        # Calculate Nullity using the Rank-Nullity Theorem
        nullity = num_cols - rank
        
        self.solution_display.append("\n--- RESULTS ---\n")
        self.solution_display.append(f"Number of columns (n) = {num_cols}\n")
        self.solution_display.append(f"Rank(A) = {rank}")
        self.solution_display.append("  - The rank is the number of non-zero rows in the Row Echelon Form.")
        self.solution_display.append("  - It represents the dimension of the column space (the number of linearly independent columns).\n")
        
        self.solution_display.append(f"Nullity(A) = {nullity}")
        self.solution_display.append("  - Calculated using the Rank-Nullity Theorem: Rank(A) + Nullity(A) = n.")
        self.solution_display.append("  - It represents the dimension of the null space (the number of vectors 'x' for which Ax = 0).")
