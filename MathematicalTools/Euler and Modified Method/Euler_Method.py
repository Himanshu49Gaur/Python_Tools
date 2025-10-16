import sys
import numpy as np
import sympy

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTextEdit, QGroupBox, QGridLayout, 
    QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class ModifiedEulerApp(QMainWindow):
    """
    A PyQt5 GUI application for solving first-order ODEs using the
    Modified Euler (Heun's) Method, with detailed step-by-step explanations.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Modified Euler Method Solver")
        self.setGeometry(100, 100, 1200, 700)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.main_layout = QHBoxLayout(self.central_widget)

        self.create_input_widgets()
        self.create_output_widgets()

        self.setup_layout()

    def create_input_widgets(self):
        """Creates all the widgets for the user input panel."""
        self.input_group = QGroupBox("Problem Definition")
        self.input_layout = QGridLayout(self.input_group)
        
        self.func_label = QLabel("dy/dx = f(x, y):")
        self.func_input = QLineEdit("x**2 - y")
        
        self.x0_label = QLabel("Initial x (x₀):")
        self.x0_input = QLineEdit("0")
        
        self.y0_label = QLabel("Initial y (y₀):")
        self.y0_input = QLineEdit("1")

        self.input_layout.addWidget(self.func_label, 0, 0)
        self.input_layout.addWidget(self.func_input, 0, 1)
        self.input_layout.addWidget(self.x0_label, 1, 0)
        self.input_layout.addWidget(self.x0_input, 1, 1)
        self.input_layout.addWidget(self.y0_label, 2, 0)
        self.input_layout.addWidget(self.y0_input, 2, 1)

        self.params_group = QGroupBox("Solver Parameters")
        self.params_layout = QGridLayout(self.params_group)
        self.xtarget_label = QLabel("Target x:")
        self.xtarget_input = QLineEdit("0.5")
        self.h_label = QLabel("Step Size (h):")
        self.h_input = QLineEdit("0.1")
        self.params_layout.addWidget(self.xtarget_label, 0, 0)
        self.params_layout.addWidget(self.xtarget_input, 0, 1)
        self.params_layout.addWidget(self.h_label, 1, 0)
        self.params_layout.addWidget(self.h_input, 1, 1)
        
        self.solve_button = QPushButton("Solve with Modified Euler's Method")
        self.solve_button.setFont(QFont("Arial", 12, QFont.Bold))
        self.solve_button.clicked.connect(self.run_solver)
        
        self.clear_button = QPushButton("Clear All")
        self.clear_button.clicked.connect(self.clear_all_fields)

    def create_output_widgets(self):
        """Creates the text area for displaying the solution steps."""
        self.output_group = QGroupBox("Detailed Solution Steps")
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
        
        input_layout.addWidget(self.input_group)
        input_layout.addWidget(self.params_group)
        input_layout.addWidget(QLabel("Syntax Guide: Use 'x' and 'y' as variables.\nSupported functions: sin, cos, exp, log, sqrt..."))

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.clear_button)
        button_layout.addWidget(self.solve_button)
        input_layout.addLayout(button_layout)
        
        input_panel.setFixedWidth(450)
        
        self.main_layout.addWidget(input_panel)
        self.main_layout.addWidget(self.output_group)

    def clear_all_fields(self):
        """Clears all input and output fields."""
        self.func_input.clear()
        self.x0_input.clear()
        self.y0_input.clear()
        self.xtarget_input.clear()
        self.h_input.clear()
        self.solution_display.clear()

    def show_message(self, title, message):
        """Displays a standardized message box."""
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setText(message)
        msg_box.setWindowTitle(title)
        msg_box.exec_()

    def get_inputs_and_parse(self):
        """Reads UI inputs, validates them, and creates a numerical function using SymPy."""
        try:
            x0 = float(self.x0_input.text())
            y0 = float(self.y0_input.text())
            x_target = float(self.xtarget_input.text())
            h = float(self.h_input.text())
            func_str = self.func_input.text()
            if not func_str:
                self.show_message("Input Error", "Function cannot be empty.")
                return None
        except ValueError:
            self.show_message("Input Error", "All input fields must contain valid numbers.")
            return None
        
        try:
            x_sym, y_sym = sympy.symbols('x y')
            f_sym = sympy.sympify(func_str)
            f_numeric = sympy.lambdify((x_sym, y_sym), f_sym, 'numpy')
            _ = f_numeric(x0, y0) # Test run
        except Exception as e:
            self.show_message("Expression Error", f"Could not parse function. Check syntax.\nError: {e}")
            return None
            
        return f_numeric, x0, y0, x_target, h

    def run_solver(self):
        """Main function to trigger the Modified Euler method and display detailed steps."""
        self.solution_display.clear()
        
        parsed_data = self.get_inputs_and_parse()
        if parsed_data is None: return
        
        f, x0, y0, x_target, h = parsed_data
        
        self.solution_display.append("--- Starting Modified Euler (Heun's) Method ---\n")
        
        x_current = x0
        y_current = y0
        
        num_steps = int(round((x_target - x0) / h))
        
        self.solution_display.append(f"Solving dy/dx = {self.func_input.text()}")
        self.solution_display.append(f"From x = {x0} to x = {x_target} with step size h = {h}.")
        self.solution_display.append(f"Total number of steps required: {num_steps}\n")

        for i in range(num_steps):
            self.solution_display.append(f"{'='*25} STEP {i+1} {'='*25}")
            self.solution_display.append(f"Current point (x_n, y_n) = ({x_current:.6f}, {y_current:.6f})\n")

            # --- Predictor Step ---
            self.solution_display.append("1. Predictor Step (using standard Euler):")
            self.solution_display.append("   - Calculate initial slope:")
            self.solution_display.append("     slope_start = f(x_n, y_n)")
            slope_start = f(x_current, y_current)
            self.solution_display.append(f"     slope_start = f({x_current:.4f}, {y_current:.4f}) = {slope_start:.6f}\n")

            self.solution_display.append("   - Predict the next y value (y*_{n+1}):")
            self.solution_display.append("     y*_{n+1} = y_n + h * slope_start")
            y_predicted = y_current + h * slope_start
            self.solution_display.append(f"     y*_{i+1} = {y_current:.6f} + {h:.4f} * {slope_start:.6f} = {y_predicted:.8f}\n")

            # --- Corrector Step ---
            self.solution_display.append("2. Corrector Step:")
            x_next = x_current + h
            self.solution_display.append(f"   - Calculate slope at the predicted end point (x_{i+1}, y*_{i+1}):")
            self.solution_display.append(f"     slope_end = f(x_n + h, y*_{n+1})")
            slope_end = f(x_next, y_predicted)
            self.solution_display.append(f"     slope_end = f({x_next:.4f}, {y_predicted:.6f}) = {slope_end:.6f}\n")

            self.solution_display.append("   - Average the slopes:")
            self.solution_display.append(f"     avg_slope = (slope_start + slope_end) / 2")
            avg_slope = (slope_start + slope_end) / 2
            self.solution_display.append(f"     avg_slope = ({slope_start:.6f} + {slope_end:.6f}) / 2 = {avg_slope:.6f}\n")

            self.solution_display.append("   - Correct y_{n+1} using the average slope:")
            self.solution_display.append("     y_{n+1} = y_n + h * avg_slope")
            y_next = y_current + h * avg_slope
            self.solution_display.append(f"     y_{i+1} = {y_current:.6f} + {h:.4f} * {avg_score:.6f} = {y_next:.8f}")
            
            self.solution_display.append(f"\n   The next point is ({x_next:.6f}, {y_next:.8f})")
            self.solution_display.append("-" * 60)
            QApplication.processEvents()

            # Update variables for the next iteration
            y_current = y_next
            x_current = x_next
        
        self.solution_display.append("\n--- CALCULATION COMPLETE ---\n")
        self.solution_display.append(f"The approximate value of y at x = {x_target:.4f} is: {y_current:.8f}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ModifiedEulerApp()
    window.show()
    sys.exit(app.exec_())
