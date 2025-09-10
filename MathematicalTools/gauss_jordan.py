import sys
import numpy as np

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTableWidget, QTableWidgetItem,
    QSpinBox, QTextEdit, QGroupBox, QGridLayout, QHeaderView, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class GaussJordanApp(QMainWindow):
    """
    A PyQt5 GUI application for solving systems of linear equations
    using the Gauss-Jordan elimination method.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gauss-Jordan Elimination Solver")
        self.setGeometry(100, 100, 1200, 700)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.main_layout = QHBoxLayout(self.central_widget)

        self.create_input_widgets()
        self.create_output_widgets()

        self.setup_layout()

    def create_input_widgets(self):
        """Creates all the widgets for the user input panel."""
        self.size_label = QLabel("Number of Variables / Equations (n):")
        self.size_spinbox = QSpinBox()
        self.size_spinbox.setRange(2, 10)
        self.size_spinbox.setValue(3)
        self.size_spinbox.valueChanged.connect(self.update_ui_size)

        self.matrix_a_group = QGroupBox("Enter Coefficient Matrix [A]")
        self.matrix_a_layout = QVBoxLayout()
        self.matrix_a_table = QTableWidget()
        self.matrix_a_layout.addWidget(self.matrix_a_table)
        self.matrix_a_group.setLayout(self.matrix_a_layout)
        
        self.vector_b_group = QGroupBox("Enter Constant Vector [b]")
        self.vector_b_layout = QVBoxLayout()
        self.vector_b_table = QTableWidget()
        self.vector_b_layout.addWidget(self.vector_b_table)
        self.vector_b_group.setLayout(self.vector_b_layout)
        
        self.solve_button = QPushButton("Solve System")
        self.solve_button.setFont(QFont("Arial", 12, QFont.Bold))
        self.solve_button.clicked.connect(self.run_solver)
        
        self.clear_button = QPushButton("Clear All")
        self.clear_button.clicked.connect(self.clear_all_fields)

        self.update_ui_size()

    def create_output_widgets(self):
        """Creates the text area for displaying the solution steps."""
        self.output_group = QGroupBox("Solution Steps: Transforming [A|b] to [I|x]")
        self.output_layout = QVBoxLayout()
        self.solution_display = QTextEdit()
        self.solution_display.setReadOnly(True)
        self.solution_display.setFont(QFont("Courier New", 10))
        self.solution_display.setLineWrapMode(QTextEdit.NoWrap)
        self.output_layout.addWidget(self.solution_display)
        self.output_group.setLayout(self.output_layout)

    def setup_layout(self):
        """Arranges all widgets in the main window layout."""
        input_panel = QWidget()
        input_layout = QVBoxLayout(input_panel)
        
        size_layout = QHBoxLayout()
        size_layout.addWidget(self.size_label)
        size_layout.addWidget(self.size_spinbox)
        
        input_layout.addLayout(size_layout)
        input_layout.addWidget(self.matrix_a_group)
        input_layout.addWidget(self.vector_b_group)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.clear_button)
        button_layout.addWidget(self.solve_button)
        input_layout.addLayout(button_layout)
        
        input_panel.setFixedWidth(450)
        
        self.main_layout.addWidget(input_panel)
        self.main_layout.addWidget(self.output_group)

    def update_ui_size(self):
        """Resizes the UI tables when the system size changes."""
        n = self.size_spinbox.value()
        
        self.matrix_a_table.setRowCount(n)
        self.matrix_a_table.setColumnCount(n)
        self.matrix_a_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.matrix_a_table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.vector_b_table.setRowCount(n)
        self.vector_b_table.setColumnCount(1)
        self.vector_b_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.vector_b_table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.vector_b_table.setHorizontalHeaderLabels(["Value"])

        if n == 3:
             if self.matrix_a_table.item(0, 0) is None or self.matrix_a_table.item(0,0).text() == "":
                # Pre-fill with a classic example
                a_vals = [['2', '1', '-1'], ['-3', '-1', '2'], ['-2', '1', '2']]
                b_vals = [['8'], ['-11'], ['-3']]
                for r in range(3):
                    self.vector_b_table.setItem(r, 0, QTableWidgetItem(b_vals[r][0]))
                    for c in range(3):
                        self.matrix_a_table.setItem(r, c, QTableWidgetItem(a_vals[r][c]))

    def clear_all_fields(self):
        """Clears all input and output fields."""
        n = self.size_spinbox.value()
        for r in range(n):
            self.vector_b_table.setItem(r, 0, QTableWidgetItem(""))
            for c in range(n):
                self.matrix_a_table.setItem(r, c, QTableWidgetItem(""))
        self.solution_display.clear()

    def show_message(self, title, message):
        """Displays a standardized message box."""
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setText(message)
        msg_box.setWindowTitle(title)
        msg_box.exec_()

    @staticmethod
    def format_matrix(m, title="Matrix"):
        """Pretty-prints a NumPy matrix into a string for display."""
        header = f"--- {title} ---\n"
        if m.ndim == 1: # Handle 1D vector
            m = m.reshape(1, -1)
        
        body = ""
        for row in m:
            body += " | ".join([f"{val:8.4f}" for val in row]) + "\n"
        return header + body

    def get_inputs(self):
        """Reads UI inputs and returns them as NumPy arrays."""
        n = self.size_spinbox.value()
        try:
            matrix_a = np.zeros((n, n))
            vector_b = np.zeros((n, 1))
            for r in range(n):
                vector_b[r, 0] = float(self.vector_b_table.item(r, 0).text())
                for c in range(n):
                    matrix_a[r, c] = float(self.matrix_a_table.item(r, c).text())
        except (ValueError, AttributeError):
            self.show_message("Input Error", "All input fields must contain valid numbers.")
            return None, None
        return matrix_a, vector_b

    def run_solver(self):
        """Main function to trigger the Gauss-Jordan elimination."""
        self.solution_display.clear()
        
        A, b = self.get_inputs()
        if A is None: return

        n = len(b)
        # Create the augmented matrix
        M = np.hstack([A, b])
        
        self.solution_display.append("--- Starting Gauss-Jordan Elimination ---\n")
        self.solution_display.append(self.format_matrix(M, "Initial Augmented Matrix [A|b]"))

        for i in range(n):
            # --- Pivoting Step ---
            # Find the row with the largest pivot
            pivot_row = i
            for j in range(i + 1, n):
                if abs(M[j, i]) > abs(M[pivot_row, i]):
                    pivot_row = j
            
            # Swap the current row with the pivot row
            if pivot_row != i:
                M[[i, pivot_row]] = M[[pivot_row, i]]
                self.solution_display.append(f"\n-> Swap R{i+1} and R{pivot_row+1} for larger pivot")
                self.solution_display.append(self.format_matrix(M, f"After Swapping"))


            # --- Check for Zero Pivot ---
            pivot = M[i, i]
            if abs(pivot) < 1e-12:
                self.solution_display.append(f"\nERROR: Zero pivot element encountered at ({i+1},{i+1}).")
                self.solution_display.append("The system may not have a unique solution.")
                self.show_message("Solver Error", "Zero pivot encountered. Cannot solve the system.")
                return

            # --- Normalization ---
            # Divide the pivot row by the pivot element to make the pivot 1
            self.solution_display.append(f"\n-> Normalize Pivot Row {i+1}: R{i+1} = R{i+1} / {pivot:.4f}")
            M[i, :] = M[i, :] / pivot
            self.solution_display.append(self.format_matrix(M, f"After Normalizing R{i+1}"))
            QApplication.processEvents()

            # --- Elimination ---
            # Make other entries in the pivot column zero
            self.solution_display.append(f"\n-> Eliminate other entries in Column {i+1}")
            for j in range(n):
                if i != j:
                    factor = M[j, i]
                    self.solution_display.append(f"  - R{j+1} = R{j+1} - ({factor:.4f}) * R{i+1}")
                    M[j, :] = M[j, :] - factor * M[i, :]
            
            self.solution_display.append(self.format_matrix(M, f"After Elimination for Column {i+1}"))
            QApplication.processEvents()

        # Extract the solution
        solution = M[:, n]
        
        self.solution_display.append("\n--- ELIMINATION COMPLETE ---\n")
        self.solution_display.append(self.format_matrix(M, "Final Reduced Row Echelon Form [I|x]"))
        self.solution_display.append(self.format_matrix(solution.flatten(), "Final Solution Vector (x)"))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GaussJordanApp()
    window.show()
    sys.exit(app.exec_())
