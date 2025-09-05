import sys
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QSpinBox, QTextEdit, QGroupBox, QGridLayout, QHeaderView, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class GaussJacobiApp(QMainWindow):
    """
    A PyQt5 GUI application for solving systems of linear equations
    using the Gauss-Jacobi iterative method.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gauss-Jacobi Method Solver")
        self.setGeometry(100, 100, 900, 700) # x, y, width, height

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.main_layout = QHBoxLayout(self.central_widget)

        self.create_input_widgets()
        self.create_output_widgets()

        self.setup_layout()

    def create_input_widgets(self):
        """Creates all the widgets for the user input panel."""
        # --- System Size ---
        self.size_label = QLabel("Number of Variables (n):")
        self.size_spinbox = QSpinBox()
        self.size_spinbox.setRange(2, 20) # System size from 2x2 to 20x20
        self.size_spinbox.setValue(3)
        self.size_spinbox.valueChanged.connect(self.update_matrix_size)

        # --- Augmented Matrix [A|b] Input ---
        self.matrix_group = QGroupBox("Enter Augmented Matrix [A|b]")
        self.matrix_layout = QVBoxLayout()
        self.matrix_table = QTableWidget()
        self.matrix_layout.addWidget(self.matrix_table)
        self.matrix_group.setLayout(self.matrix_layout)

        # --- Initial Guess Input ---
        self.guess_group = QGroupBox("Enter Initial Guess Vector [x₀]")
        self.guess_layout = QVBoxLayout()
        self.guess_table = QTableWidget()
        self.guess_table.setFixedHeight(60)
        self.guess_layout.addWidget(self.guess_table)
        self.guess_group.setLayout(self.guess_layout)
        
        # --- Parameters Input ---
        self.params_group = QGroupBox("Parameters")
        self.params_layout = QGridLayout()
        self.tol_label = QLabel("Tolerance (e.g., 0.0001):")
        self.tol_input = QLineEdit("0.0001")
        self.max_iter_label = QLabel("Max Iterations (e.g., 100):")
        self.max_iter_input = QLineEdit("100")
        self.params_layout.addWidget(self.tol_label, 0, 0)
        self.params_layout.addWidget(self.tol_input, 0, 1)
        self.params_layout.addWidget(self.max_iter_label, 1, 0)
        self.params_layout.addWidget(self.max_iter_input, 1, 1)
        self.params_group.setLayout(self.params_layout)
        
        # --- Control Buttons ---
        self.solve_button = QPushButton("Solve System")
        self.solve_button.setFont(QFont("Arial", 12, QFont.Bold))
        self.solve_button.clicked.connect(self.run_solver)
        
        self.clear_button = QPushButton("Clear All")
        self.clear_button.clicked.connect(self.clear_all_fields)

        # Set initial size for tables
        self.update_matrix_size()

    def create_output_widgets(self):
        """Creates the text area for displaying the solution steps."""
        self.output_group = QGroupBox("Solution Steps")
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
        
        # Size selection layout
        size_layout = QHBoxLayout()
        size_layout.addWidget(self.size_label)
        size_layout.addWidget(self.size_spinbox)
        
        input_layout.addLayout(size_layout)
        input_layout.addWidget(self.matrix_group)
        input_layout.addWidget(self.guess_group)
        input_layout.addWidget(self.params_group)

        # Buttons layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.clear_button)
        button_layout.addWidget(self.solve_button)
        input_layout.addLayout(button_layout)
        
        input_panel.setFixedWidth(400)
        
        self.main_layout.addWidget(input_panel)
        self.main_layout.addWidget(self.output_group)

    def update_matrix_size(self):
        """Resizes the matrix and vector tables when the system size changes."""
        n = self.size_spinbox.value()
        
        # --- Update Matrix Table [A|b] ---
        self.matrix_table.setRowCount(n)
        self.matrix_table.setColumnCount(n + 1)
        labels_a = [f"x{i+1}" for i in range(n)]
        labels_b = ["b"]
        self.matrix_table.setHorizontalHeaderLabels(labels_a + labels_b)
        self.matrix_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.matrix_table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        # --- Update Guess Table [x0] ---
        self.guess_table.setRowCount(1)
        self.guess_table.setColumnCount(n)
        self.guess_table.setHorizontalHeaderLabels(labels_a)
        self.guess_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.guess_table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Populate with zeros for clarity
        for r in range(n):
            for c in range(n + 1):
                if self.matrix_table.item(r, c) is None:
                    self.matrix_table.setItem(r, c, QTableWidgetItem("0"))
        for c in range(n):
            if self.guess_table.item(0, c) is None:
                self.guess_table.setItem(0, c, QTableWidgetItem("0"))

    def clear_all_fields(self):
        """Clears all input and output fields."""
        self.update_matrix_size() # This also resets tables to 0
        self.tol_input.setText("0.0001")
        self.max_iter_input.setText("100")
        self.solution_display.clear()

    def show_error_message(self, title, message):
        """Displays a standardized error message box."""
        QMessageBox.critical(self, title, message)
    
    def get_inputs_from_ui(self):
        """Reads and validates all user inputs from the GUI."""
        n = self.size_spinbox.value()
        
        # --- Read Augmented Matrix ---
        try:
            augmented_matrix = np.zeros((n, n + 1))
            for i in range(n):
                for j in range(n + 1):
                    augmented_matrix[i, j] = float(self.matrix_table.item(i, j).text())
            
            A = augmented_matrix[:, :-1]
            b = augmented_matrix[:, -1]
        except (ValueError, AttributeError):
            self.show_error_message("Input Error", "The matrix [A|b] contains invalid or empty cells. Please enter numbers only.")
            return None
        
        # --- Read Initial Guess ---
        try:
            x0 = np.zeros(n)
            for i in range(n):
                x0[i] = float(self.guess_table.item(0, i).text())
        except (ValueError, AttributeError):
            self.show_error_message("Input Error", "The initial guess vector contains invalid or empty cells. Please enter numbers only.")
            return None
            
        # --- Read Parameters ---
        try:
            tol = float(self.tol_input.text())
            max_iter = int(self.max_iter_input.text())
            if tol <= 0 or max_iter <= 0:
                raise ValueError
        except ValueError:
            self.show_error_message("Parameter Error", "Tolerance and Max Iterations must be positive numbers.")
            return None
            
        return A, b, x0, tol, max_iter

    @staticmethod
    def check_diagonal_dominance(A):
        """Checks if the matrix A is strictly diagonally dominant."""
        n = len(A)
        for i in range(n):
            off_diagonal_sum = sum(abs(A[i, j]) for j in range(n) if i != j)
            if abs(A[i, i]) <= off_diagonal_sum:
                return False
        return True

    def run_solver(self):
        """Main function to trigger the Gauss-Jacobi method."""
        self.solution_display.clear()
        
        # 1. Get and validate inputs
        inputs = self.get_inputs_from_ui()
        if inputs is None:
            return # Stop if inputs are invalid
        A, b, x0, tol, max_iter = inputs
        
        self.solution_display.append("--- Starting Gauss-Jacobi Solver ---")
        self.solution_display.append(f"System Size: {len(b)}x{len(b)}")
        self.solution_display.append(f"Tolerance: {tol}, Max Iterations: {max_iter}\n")

        # 2. Check for diagonal dominance and inform the user
        if self.check_diagonal_dominance(A):
            self.solution_display.append("INFO: Matrix is strictly diagonally dominant. Convergence is likely.\n")
        else:
            self.solution_display.append("WARNING: Matrix is NOT strictly diagonally dominant. Method may not converge.\n")
        
        # 3. Run the iterative solver and display step-by-step results
        n = len(b)
        x = x0.copy()
        
        for k in range(max_iter):
            # Log the current state before calculation
            iteration_log = f"--- Iteration {k+1} ---\n"
            iteration_log += f"Current solution x({k}) = {np.array2string(x, precision=6, floatmode='fixed')}\n"
            
            x_new = np.zeros(n)
            
            # Perform the calculation for each variable
            for i in range(n):
                diagonal_element = A[i, i]
                if abs(diagonal_element) < 1e-12:
                    self.solution_display.append(f"ERROR: Diagonal element at A[{i},{i}] is zero. Cannot proceed.")
                    return

                off_diagonal_sum = sum(A[i, j] * x[j] for j in range(n) if i != j)
                x_new[i] = (b[i] - off_diagonal_sum) / diagonal_element
            
            # Calculate error and log results of this iteration
            error = np.linalg.norm(x_new - x, np.inf)
            iteration_log += f"New solution     x({k+1}) = {np.array2string(x_new, precision=6, floatmode='fixed')}\n"
            iteration_log += f"Error (max change) = {error:.8f}\n"
            self.solution_display.append(iteration_log)
            QApplication.processEvents() # Update the GUI to show the new text

            # Check for convergence
            if error < tol:
                self.solution_display.append("\n--- CONVERGENCE REACHED ---")
                self.solution_display.append(f"Solution found after {k+1} iterations.")
                final_solution_str = "\n".join([f"  x{i+1} = {val:.8f}" for i, val in enumerate(x_new)])
                self.solution_display.append(f"Final Solution (x):\n{final_solution_str}")
                return

            # Update x for the next iteration
            x = x_new.copy()

        # If loop finishes, it failed to converge
        self.solution_display.append("\n--- FAILED TO CONVERGE ---")
        self.solution_display.append(f"The solution did not converge within {max_iter} iterations.")
        last_solution_str = "\n".join([f"  x{i+1} = {val:.8f}" for i, val in enumerate(x)])
        self.solution_display.append(f"Last calculated solution:\n{last_solution_str}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GaussJacobiApp()
    window.show()
    sys.exit(app.exec_())
