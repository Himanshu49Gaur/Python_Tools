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

class GaussSeidelApp(QMainWindow):
    """
    A PyQt5 GUI application for solving systems of linear or non-linear equations
    using the Gauss-Seidel Iteration method.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gauss-Seidel Iteration Solver")
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
        self.size_spinbox.setValue(3)
        self.size_spinbox.valueChanged.connect(self.update_ui_size)

        self.equations_group = QGroupBox("Enter Rearranged Equations x = g(x)")
        self.equations_layout = QVBoxLayout()
        self.equations_table = QTableWidget()
        self.equations_layout.addWidget(self.equations_table)
        self.equations_group.setLayout(self.equations_layout)
        
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

        self.update_ui_size()

    def create_output_widgets(self):
        """Creates the text area for displaying the solution steps."""
        self.output_group = QGroupBox("Solution Steps & Vectors")
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
        self.equations_table.setHorizontalHeaderLabels(["g(x)"])
        self.equations_table.setVerticalHeaderLabels([f"x{i+1} =" for i in range(n)])
        self.equations_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        self.guess_table.setRowCount(1)
        self.guess_table.setColumnCount(n)
        self.guess_table.setHorizontalHeaderLabels([f"x{i+1}" for i in range(n)])
        self.guess_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        if n == 3:
            if self.equations_table.item(0, 0) is None or self.equations_table.item(0,0).text() == "":
                self.equations_table.setItem(0, 0, QTableWidgetItem("(7 + x2 - x3) / 4"))
                self.equations_table.setItem(1, 0, QTableWidgetItem("(21 + 4*x1 + x3) / 8"))
                self.equations_table.setItem(2, 0, QTableWidgetItem("(15 - 2*x1 + x2) / 5"))
                self.guess_table.setItem(0, 0, QTableWidgetItem("0"))
                self.guess_table.setItem(0, 1, QTableWidgetItem("0"))
                self.guess_table.setItem(0, 2, QTableWidgetItem("0"))

    def clear_all_fields(self):
        """Clears all input and output fields."""
        n = self.size_spinbox.value()
        for r in range(n):
            self.equations_table.setItem(r, 0, QTableWidgetItem(""))
        for c in range(n):
            self.guess_table.setItem(0, c, QTableWidgetItem(""))
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
    
    @staticmethod
    def format_vector(v, title="Vector"):
        """Pretty-prints a NumPy vector into a string."""
        header = f"--- {title} ---\n"
        body = "[" + ", ".join([f"{val:10.6f}" for val in v]) + "]"
        return header + body + "\n"

    def get_inputs_and_parse(self):
        """Reads UI inputs and uses Sympy to create numerical functions."""
        n = self.size_spinbox.value()
        symbols = sympy.symbols(f'x1:{n+1}')
        
        try:
            eq_strings = [self.equations_table.item(i, 0).text() for i in range(n)]
            x0 = np.array([float(self.guess_table.item(0, i).text()) for i in range(n)])
            tol = float(self.tol_input.text())
            max_iter = int(self.max_iter_input.text())
        except (ValueError, AttributeError):
            self.show_message("Input Error", "All input fields must contain valid numbers/expressions.")
            return None
            
        try:
            G_symbolic = [sympy.sympify(eq) for eq in eq_strings]
            Jg_symbolic = sympy.Matrix(G_symbolic).jacobian(symbols)
            G_numeric_list = [sympy.lambdify(symbols, g, 'numpy') for g in G_symbolic]
            Jg_numeric = sympy.lambdify(symbols, Jg_symbolic, 'numpy')
            _ = [g(*x0) for g in G_numeric_list]
            _ = Jg_numeric(*x0)
        except Exception as e:
            self.show_message("Expression Error", f"Could not parse equations. Check syntax.\nError: {e}")
            return None
            
        return G_numeric_list, Jg_numeric, x0, tol, max_iter

    def run_solver(self):
        """Main function to trigger the Gauss-Seidel Iteration method."""
        self.solution_display.clear()
        
        parsed_data = self.get_inputs_and_parse()
        if parsed_data is None: return
        
        G_numeric_list, Jg_numeric, x, tol, max_iter = parsed_data
        
        self.solution_display.append("--- Starting Gauss-Seidel Iteration Solver ---\n")

        try:
            Jg_val = np.array(Jg_numeric(*x))
            eigenvalues = np.linalg.eigvals(Jg_val)
            spectral_radius = np.max(np.abs(eigenvalues))
            
            self.solution_display.append("--- Convergence Analysis at Initial Point ---")
            self.solution_display.append(f"Jacobian of g(x) at x₀: \n{Jg_val}\n")
            self.solution_display.append(f"Eigenvalues: {np.round(eigenvalues, 6)}")
            self.solution_display.append(f"Spectral Radius |ρ(Jg(x₀))| = {spectral_radius:.6f}\n")
            if spectral_radius < 1:
                self.solution_display.append("CONDITION MET (for Fixed-Point): ρ < 1. Iteration is likely to converge.\n")
            else:
                self.solution_display.append("WARNING (for Fixed-Point): ρ >= 1. Iteration may diverge.\n")
        except Exception as e:
            self.solution_display.append(f"Could not perform convergence analysis. Error: {e}\n")

        for k in range(max_iter):
            self.solution_display.append(f"================ Iteration {k+1} ================\n")
            x_old = x.copy()
            
            self.solution_display.append(self.format_vector(x_old, title=f"Vector at Start of Iteration x_({k})"))
            self.solution_display.append("--- Component-wise Calculation ---\n")
            
            # This is the core of Gauss-Seidel: use new values as soon as they are computed.
            # We will modify the vector 'x' in place.
            try:
                for i in range(len(x)):
                    # The function g uses the vector 'x', which contains already updated components from this iteration
                    current_args = tuple(x)
                    new_val = G_numeric_list[i](*current_args)
                    self.solution_display.append(f"  x{i+1}_new = g{i+1}{current_args} = {new_val:.8f}")
                    x[i] = new_val # Update in place
            
            except (ValueError, TypeError):
                 self.solution_display.append("\nERROR: Mathematical error during function evaluation (e.g., log of negative).")
                 self.show_message("Runtime Error", "A math error occurred. Check your functions and initial guess.")
                 return

            self.solution_display.append(self.format_vector(x, title=f"Vector at End of Iteration x_({k+1})"))

            error = np.linalg.norm(x - x_old, np.inf)
            self.solution_display.append(f"Error (max change) = {error:.8f}\n")
            QApplication.processEvents()
            
            if error < tol:
                self.solution_display.append("\n--- CONVERGENCE REACHED ---\n")
                self.solution_display.append(f"Solution found after {k+1} iterations.")
                self.solution_display.append(self.format_vector(x, "Final Solution Vector (x)"))
                return

        self.solution_display.append("\n--- FAILED TO CONVERGE ---\n")
        self.solution_display.append(f"The solution did not converge within {max_iter} iterations.")
        self.solution_display.append(self.format_vector(x, "Last Calculated Solution (x)"))
