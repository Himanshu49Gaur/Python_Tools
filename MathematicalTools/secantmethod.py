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

class SecantApp(QMainWindow):
    """
    A PyQt5 GUI application for finding the root of a single non-linear equation
    using the Secant method.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Secant Method Root Finder")
        self.setGeometry(100, 100, 1000, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.main_layout = QHBoxLayout(self.central_widget)

        self.create_input_widgets()
        self.create_output_widgets()

        self.setup_layout()

    def create_input_widgets(self):
        """Creates all the widgets for the user input panel."""
        self.input_group = QGroupBox("Function and Initial Guesses")
        self.input_layout = QGridLayout()
        
        self.func_label = QLabel("Enter function f(x):")
        self.func_input = QLineEdit("cos(x) - x*exp(x)")
        
        self.x0_label = QLabel("First Initial Guess (x₀):")
        self.x0_input = QLineEdit("0")
        
        self.x1_label = QLabel("Second Initial Guess (x₁):")
        self.x1_input = QLineEdit("1")

        self.input_layout.addWidget(self.func_label, 0, 0)
        self.input_layout.addWidget(self.func_input, 0, 1)
        self.input_layout.addWidget(self.x0_label, 1, 0)
        self.input_layout.addWidget(self.x0_input, 1, 1)
        self.input_layout.addWidget(self.x1_label, 2, 0)
        self.input_layout.addWidget(self.x1_input, 2, 1)
        self.input_group.setLayout(self.input_layout)

        syntax_label = QLabel("Use 'x' as the variable and standard Python/Numpy functions like exp(), sin(), cos(), etc.")
        syntax_label.setWordWrap(True)
        
        self.params_group = QGroupBox("Parameters")
        self.params_layout = QGridLayout()
        self.tol_label = QLabel("Tolerance:")
        self.tol_input = QLineEdit("0.0001")
        self.max_iter_label = QLabel("Max Iterations:")
        self.max_iter_input = QLineEdit("50")
        self.params_layout.addWidget(self.tol_label, 0, 0)
        self.params_layout.addWidget(self.tol_input, 0, 1)
        self.params_layout.addWidget(self.max_iter_label, 1, 0)
        self.params_layout.addWidget(self.max_iter_input, 1, 1)
        self.params_group.setLayout(self.params_layout)
        
        self.solve_button = QPushButton("Find Root")
        self.solve_button.setFont(QFont("Arial", 12, QFont.Bold))
        self.solve_button.clicked.connect(self.run_solver)
        
        self.clear_button = QPushButton("Clear All")
        self.clear_button.clicked.connect(self.clear_all_fields)

        self.input_panel_layout = QVBoxLayout()
        self.input_panel_layout.addWidget(self.input_group)
        self.input_panel_layout.addWidget(syntax_label)
        self.input_panel_layout.addWidget(self.params_group)
        
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.clear_button)
        button_layout.addWidget(self.solve_button)
        self.input_panel_layout.addLayout(button_layout)

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
        input_panel.setLayout(self.input_panel_layout)
        input_panel.setFixedWidth(400)
        
        self.main_layout.addWidget(input_panel)
        self.main_layout.addWidget(self.output_group)

    def clear_all_fields(self):
        """Clears all input and output fields."""
        self.func_input.setText("")
        self.x0_input.setText("")
        self.x1_input.setText("")
        self.tol_input.setText("0.0001")
        self.max_iter_input.setText("50")
        self.solution_display.clear()

    def show_message(self, title, message, level="critical"):
        """Displays a standardized message box."""
        msg_box = QMessageBox()
        if level == "critical": msg_box.setIcon(QMessageBox.Critical)
        else: msg_box.setIcon(QMessageBox.Information)
        msg_box.setText(message)
        msg_box.setWindowTitle(title)
        msg_box.exec_()

    def get_inputs_and_parse(self):
        """Reads UI inputs and uses Sympy to create a numerical function."""
        try:
            x0 = float(self.x0_input.text())
            x1 = float(self.x1_input.text())
            tol = float(self.tol_input.text())
            max_iter = int(self.max_iter_input.text())
            func_str = self.func_input.text()
            if not func_str:
                self.show_message("Input Error", "Function cannot be empty.")
                return None
        except ValueError:
            self.show_message("Input Error", "All input fields must contain valid numbers.")
            return None
        
        try:
            x_sym = sympy.symbols('x')
            f_sym = sympy.sympify(func_str)
            f_numeric = sympy.lambdify(x_sym, f_sym, 'numpy')
            # Test run
            _ = f_numeric(x0)
        except Exception as e:
            self.show_message("Expression Error", f"Could not parse function. Check syntax.\nError: {e}")
            return None
            
        return f_numeric, x0, x1, tol, max_iter

    def run_solver(self):
        """Main function to trigger the Secant method."""
        self.solution_display.clear()
        
        parsed_data = self.get_inputs_and_parse()
        if parsed_data is None: return
        
        f, x_prev, x_curr, tol, max_iter = parsed_data
        
        self.solution_display.append("--- Starting Secant Method ---\n")
        header = f"{'Iter':>4} | {'x_n-1':>15} | {'x_n':>15} | {'f(x_n-1)':>15} | {'f(x_n)':>15} | {'x_n+1':>15} | {'Error':>15}"
        self.solution_display.append(header)
        self.solution_display.append("-" * len(header))

        for k in range(max_iter):
            try:
                f_prev = f(x_prev)
                f_curr = f(x_curr)

                if abs(f_curr - f_prev) < 1e-12: # Check for division by a very small number
                    self.solution_display.append("\nERROR: Denominator f(x_n) - f(x_n-1) is near zero. Method fails.")
                    self.show_message("Solver Error", "Denominator is near zero. The method cannot proceed, try different initial points.")
                    return
                
                # Secant method formula
                x_next = x_curr - f_curr * (x_curr - x_prev) / (f_curr - f_prev)
                
                error = abs(x_next - x_curr)
                
                log_line = f"{k+1:>4} | {x_prev:15.8f} | {x_curr:15.8f} | {f_prev:15.8f} | {f_curr:15.8f} | {x_next:15.8f} | {error:15.8f}"
                self.solution_display.append(log_line)
                QApplication.processEvents()

                if error < tol:
                    self.solution_display.append("\n--- CONVERGENCE REACHED ---\n")
                    self.solution_display.append(f"Root found after {k+1} iterations.")
                    self.solution_display.append(f"Approximate Root x = {x_next:.10f}")
                    return

                # Update points for the next iteration
                x_prev = x_curr
                x_curr = x_next
            
            except (ValueError, TypeError):
                 self.solution_display.append("\nERROR: Mathematical error during function evaluation (e.g., log of negative).")
                 self.show_message("Runtime Error", "A math error occurred. Check your function and initial guesses.")
                 return

        self.solution_display.append("\n--- FAILED TO CONVERGE ---\n")
        self.solution_display.append(f"The solution did not converge within {max_iter} iterations.")
        self.solution_display.append(f"Last calculated root x = {x_curr:.10f}")



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SecantApp()
    window.show()
    sys.exit(app.exec_())

