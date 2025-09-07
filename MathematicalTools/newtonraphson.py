import sys
import numpy as np
import sympy

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QSpinBox, QTextEdit, QGroupBox, QGridLayout, QHeaderView, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class NewtonRaphsonApp(QMainWindow):
    """
    A PyQt5 GUI application for solving systems of non-linear equations
    using the Newton-Raphson method.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Newton-Raphson Method Solver")
        self.setGeometry(100, 100, 1100, 800)

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
        self.size_spinbox.setRange(1, 10)
        self.size_spinbox.setValue(2)
        self.size_spinbox.valueChanged.connect(self.update_ui_size)

        self.equations_group = QGroupBox("Enter Non-Linear Equations f(x) = 0")
        self.equations_layout = QVBoxLayout()
        self.equations_table = QTableWidget()
        self.equations_layout.addWidget(self.equations_table)
        self.equations_group.setLayout(self.equations_layout)
        
        # Add a helper label for function syntax
        syntax_label = QLabel("Use variables x1, x2, ... and standard Python/Numpy functions like exp(), sin(), cos(), etc.")
        syntax_label.setWordWrap(True)
        self.equations_layout.addWidget(syntax_label)

        self.guess_group = QGroupBox("Enter Initial Guess Vector [x₀]")
        self.guess_layout = QVBoxLayout()
        self.guess_table = QTableWidget()
        self.guess_table.setFixedHeight(60)
        self.guess_layout.addWidget(self.guess_table)
        self.guess_group.setLayout(self.guess_layout)
        
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
        
        self.solve_button = QPushButton("Solve System")
        self.solve_button.setFont(QFont("Arial", 12, QFont.Bold))
        self.solve_button.clicked.connect(self.run_solver)
        
        self.clear_button = QPushButton("Clear All")
        self.clear_button.clicked.connect(self.clear_all_fields)

        self.update_ui_size() # Set initial size for tables

    def create_output_widgets(self):
        """Creates the text area for displaying the solution steps."""
        self.output_group = QGroupBox("Solution Steps & Matrices")
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
        input_layout.addWidget(self.equations_group)
        input_layout.addWidget(self.guess_group)
        input_layout.addWidget(self.params_group)

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
        
        self.equations_table.setRowCount(n)
        self.equations_table.setColumnCount(1)
        self.equations_table.setHorizontalHeaderLabels(["f(x)"])
        self.equations_table.setVerticalHeaderLabels([f"f{i+1}" for i in range(n)])
        self.equations_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        self.guess_table.setRowCount(1)
        self.guess_table.setColumnCount(n)
        self.guess_table.setHorizontalHeaderLabels([f"x{i+1}" for i in range(n)])
        self.guess_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Pre-fill with example for n=2
        if n == 2:
            if self.equations_table.item(0, 0) is None or self.equations_table.item(0,0).text() == "":
                self.equations_table.setItem(0, 0, QTableWidgetItem("x1**2 + x2**2 - 4"))
                self.equations_table.setItem(1, 0, QTableWidgetItem("exp(x1) + x2 - 3"))
                self.guess_table.setItem(0, 0, QTableWidgetItem("1"))
                self.guess_table.setItem(0, 1, QTableWidgetItem("1"))

    def clear_all_fields(self):
        """Clears all input and output fields."""
        n = self.size_spinbox.value()
        for r in range(n):
            self.equations_table.setItem(r, 0, QTableWidgetItem(""))
        for c in range(n):
            self.guess_table.setItem(c, 0, QTableWidgetItem(""))
            
        self.tol_input.setText("0.0001")
        self.max_iter_input.setText("50")
        self.solution_display.clear()

    def show_message(self, title, message, level="critical"):
        """Displays a standardized message box."""
        msg_box = QMessageBox()
        if level == "critical":
            msg_box.setIcon(QMessageBox.Critical)
        else:
            msg_box.setIcon(QMessageBox.Information)
        msg_box.setText(message)
        msg_box.setWindowTitle(title)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()
    
    @staticmethod
    def format_matrix(m, title="Matrix"):
        """Pretty-prints a NumPy matrix or vector into a string."""
        header = f"--- {title} ---\n"
        if m.ndim == 1: # It's a vector
            body = "[" + ", ".join([f"{val:10.6f}" for val in m]) + "]"
        else: # It's a matrix
            body = "\n".join(["[" + ", ".join([f"{val:10.6f}" for val in row]) + "]" for row in m])
        return header + body + "\n"

    def get_inputs_and_parse(self):
        """Reads UI inputs and uses Sympy to create numerical functions."""
        n = self.size_spinbox.value()
        
        # 1. Create Sympy symbols x1, x2, ...
        symbols = sympy.symbols(f'x1:{n+1}')
        
        # 2. Read equations and initial guess
        try:
            eq_strings = [self.equations_table.item(i, 0).text() for i in range(n)]
            x0 = np.array([float(self.guess_table.item(0, i).text()) for i in range(n)])
            tol = float(self.tol_input.text())
            max_iter = int(self.max_iter_input.text())
        except (ValueError, AttributeError):
            self.show_message("Input Error", "All input fields must contain valid numbers/expressions.")
            return None
            
        # 3. Use Sympy to parse strings, create Jacobian, and 'lambdify' them
        try:
            F_symbolic = [sympy.sympify(eq) for eq in eq_strings]
            J_symbolic = sympy.Matrix(F_symbolic).jacobian(symbols)
            
            # Convert symbolic expressions to fast numerical functions
            F_numeric = sympy.lambdify(symbols, F_symbolic, 'numpy')
            J_numeric = sympy.lambdify(symbols, J_symbolic, 'numpy')
            
            # Test run functions to catch errors early
            _ = F_numeric(*x0)
            _ = J_numeric(*x0)
            
        except Exception as e:
            self.show_message("Expression Error", f"Could not parse the equations. Check syntax.\nError: {e}")
            return None
            
        return F_numeric, J_numeric, x0, tol, max_iter, symbols, J_symbolic

    def run_solver(self):
        """Main function to trigger the Newton-Raphson method."""
        self.solution_display.clear()
        
        parsed_data = self.get_inputs_and_parse()
        if parsed_data is None: return
        
        F_numeric, J_numeric, x, tol, max_iter, symbols, J_symbolic = parsed_data
        
        self.solution_display.append("--- Starting Newton-Raphson Solver ---\n")
        self.solution_display.append(f"Symbolic Jacobian Matrix J(x):\n{str(J_symbolic)}\n")

        for k in range(max_iter):
            self.solution_display.append(f"================ Iteration {k+1} ================\n")
            
            # Evaluate F and J at the current point x
            F_val = np.array(F_numeric(*x))
            J_val = np.array(J_numeric(*x))
            
            self.solution_display.append(self.format_matrix(x, title=f"Current Guess x_({k})"))
            self.solution_display.append(self.format_matrix(F_val, title=f"Function Value Vector F(x_({k}))"))
            self.solution_display.append(self.format_matrix(J_val, title=f"Jacobian Matrix J(x_({k}))"))
            
            # Solve the linear system J(x) * dx = -F(x) for dx
            try:
                # We solve for delta_x, which is the step to the next point
                delta_x = np.linalg.solve(J_val, -F_val)
            except np.linalg.LinAlgError:
                self.show_message("Solver Error", "Jacobian matrix is singular. Cannot proceed.")
                self.solution_display.append("\nERROR: Jacobian matrix is singular. Solution failed.")
                return
            
            # Update the solution: x_new = x + delta_x
            x_new = x + delta_x
            
            # Calculate error and log results
            error = np.linalg.norm(delta_x, np.inf)
            self.solution_display.append(self.format_matrix(delta_x, title=f"Step Vector delta_x_({k})"))
            self.solution_display.append(f"Error (max change in x) = {error:.8f}\n")
            
            QApplication.processEvents()

            # Update x for the next iteration
            x = x_new
            
            # Check for convergence
            if error < tol:
                self.solution_display.append("\n--- CONVERGENCE REACHED ---\n")
                self.solution_display.append(f"Solution found after {k+1} iterations.")
                self.solution_display.append(self.format_matrix(x, "Final Solution Vector (x)"))
                return

        self.solution_display.append("\n--- FAILED TO CONVERGE ---\n")
        self.solution_display.append(f"The solution did not converge within {max_iter} iterations.")
        self.solution_display.append(self.format_matrix(x, "Last Calculated Solution (x)"))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = NewtonRaphsonApp()
    window.show()
    sys.exit(app.exec_())
