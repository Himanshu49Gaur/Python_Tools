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

class SimpsonsApp(QMainWindow):
    """
    A PyQt5 GUI application for approximating definite integrals using
    Simpson's 1/3 Rule. It includes a built-in explanation and a
    step-by-step solver.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simpson's 1/3 Rule Solver & Explainer")
        self.setGeometry(100, 100, 1200, 750)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.main_layout = QHBoxLayout(self.central_widget)

        self.create_input_widgets()
        self.create_output_widgets()
        self.populate_initial_explanation()

        self.setup_layout()

    def create_input_widgets(self):
        """Creates all the widgets for the user input panel."""
        self.input_group = QGroupBox("Problem Definition")
        self.input_layout = QGridLayout(self.input_group)
        
        self.func_label = QLabel("Enter function f(x):")
        self.func_input = QLineEdit("exp(-x**2)")
        
        self.lower_limit_label = QLabel("Lower Limit (a):")
        self.lower_limit_input = QLineEdit("0")
        
        self.upper_limit_label = QLabel("Upper Limit (b):")
        self.upper_limit_input = QLineEdit("1")
        
        self.intervals_label = QLabel("Intervals (n, must be even):")
        self.intervals_input = QLineEdit("10")

        self.input_layout.addWidget(self.func_label, 0, 0)
        self.input_layout.addWidget(self.func_input, 0, 1)
        self.input_layout.addWidget(self.lower_limit_label, 1, 0)
        self.input_layout.addWidget(self.lower_limit_input, 1, 1)
        self.input_layout.addWidget(self.upper_limit_label, 2, 0)
        self.input_layout.addWidget(self.upper_limit_input, 2, 1)
        self.input_layout.addWidget(self.intervals_label, 3, 0)
        self.input_layout.addWidget(self.intervals_input, 3, 1)
        
        syntax_label = QLabel("Use 'x' as the variable and standard functions like exp(), sin(), cos(), log(), etc.")
        syntax_label.setWordWrap(True)
        
        self.solve_button = QPushButton("Calculate Integral")
        self.solve_button.setFont(QFont("Arial", 12, QFont.Bold))
        self.solve_button.clicked.connect(self.run_solver)
        
        self.clear_button = QPushButton("Clear Inputs & Reset")
        self.clear_button.clicked.connect(self.clear_all_fields)

    def create_output_widgets(self):
        """Creates the text area for displaying explanations and solutions."""
        self.output_group = QGroupBox("Explanation & Solution Steps")
        self.output_layout = QVBoxLayout(self.output_group)
        self.solution_display = QTextEdit()
        self.solution_display.setReadOnly(True)
        # We will use HTML for the initial explanation
        self.output_layout.addWidget(self.solution_display)

    def setup_layout(self):
        """Arranges all widgets in the main window layout."""
        input_panel = QWidget()
        input_layout = QVBoxLayout(input_panel)
        
        input_layout.addWidget(self.input_group)
        input_layout.addWidget(QLabel("Syntax Guide:"))
        input_layout.addWidget(QLabel("Use 'x' as the variable. Supported functions include: sin, cos, tan, exp, log, sqrt, etc."))

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.clear_button)
        button_layout.addWidget(self.solve_button)
        input_layout.addLayout(button_layout)
        
        input_panel.setFixedWidth(400)
        
        self.main_layout.addWidget(input_panel)
        self.main_layout.addWidget(self.output_group)

    def populate_initial_explanation(self):
        """Fills the output area with a detailed explanation of the method."""
        self.solution_display.setFont(QFont("Arial", 11))
        explanation_html = """
        <h2 style='color:#003366;'>Simpson's 1/3 Rule for Numerical Integration</h2>
        <p>
            Simpson's 1/3 Rule is a numerical method for approximating the value of a definite integral. It is generally more accurate than methods like the Trapezoidal Rule because it approximates the function not with straight lines, but with <b>quadratic polynomials (parabolas)</b>.
        </p>
        <hr>
        <h3 style='color:#003366;'>The Core Idea & Derivation</h3>
        <ol>
            <li><b>Divide and Conquer:</b> The integration interval [a, b] is divided into an <b>even number 'n'</b> of subintervals of equal width, <i>h</i>.</li>
            <li><b>Use Three Points:</b> The rule considers a pair of adjacent intervals at a time, for example from x<sub>0</sub> to x<sub>2</sub>. This region is defined by three points: (x<sub>0</sub>, f(x<sub>0</sub>)), (x<sub>1</sub>, f(x<sub>1</sub>)), and (x<sub>2</sub>, f(x<sub>2</sub>)).</li>
            <li><b>Fit a Parabola:</b> A unique parabola can be fitted perfectly through these three points. The idea is that this parabola is a better approximation of the original function <i>f(x)</i> over this small region than a straight line would be.</li>
            <li><b>Integrate the Parabola:</b> The integral of this simple quadratic function can be calculated exactly. The result of integrating the parabola from x<sub>0</sub> to x<sub>2</sub> is:
                <br><b>Area ≈ (h/3) [f(x<sub>0</sub>) + 4f(x<sub>1</sub>) + f(x<sub>2</sub>)]</b>
                <br>This small formula is the foundation of the rule.
            </li>
            <li><b>Sum the Areas:</b> To find the total integral from <i>a</i> to <i>b</i>, we simply sum the areas of the parabolas fitted over all pairs of intervals: [x<sub>0</sub>, x<sub>2</sub>], [x<sub>2</sub>, x<sub>4</sub>], ..., [x<sub>n-2</sub>, x<sub>n</sub>].
        </ol>
        <hr>
        <h3 style='color:#003366;'>The Final Formula</h3>
        <p>
            When we sum up the areas, the terms at the connection points (x<sub>2</sub>, x<sub>4</sub>, etc.) are counted in two adjacent parabolic segments. This results in the final generalized formula:
        </p>
        <p style='font-family: Courier New; font-size: 14px; background-color: #f0f0f0; padding: 10px; border-radius: 5px;'>
            <b>&int;<sub>a</sub><sup>b</sup> f(x) dx &nbsp;&approx;&nbsp; (h/3) [f(x<sub>0</sub>) + 4f(x<sub>1</sub>) + 2f(x<sub>2</sub>) + 4f(x<sub>3</sub>) + ... + 2f(x<sub>n-2</sub>) + 4f(x<sub>n-1</sub>) + f(x<sub>n</sub>)]</b>
        </p>
        <p>Where:</p>
        <ul>
            <li><b>n</b> is the total number of subintervals (<b>must be even</b>).</li>
            <li><b>h = (b - a) / n</b> is the width of each subinterval.</li>
            <li>The coefficients pattern is: <b>1, 4, 2, 4, 2, ..., 4, 1</b>.</li>
        </ul>
        """
        self.solution_display.setHtml(explanation_html)

    def clear_all_fields(self):
        """Clears all input fields and resets the explanation."""
        self.func_input.setText("exp(-x**2)")
        self.lower_limit_input.setText("0")
        self.upper_limit_input.setText("1")
        self.intervals_input.setText("10")
        self.populate_initial_explanation()

    def show_message(self, title, message):
        """Displays a standardized message box."""
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setText(message)
        msg_box.setWindowTitle(title)
        msg_box.exec_()

    def get_inputs_and_parse(self):
        """Reads UI inputs, validates them, and creates a numerical function."""
        try:
            a = float(self.lower_limit_input.text())
            b = float(self.upper_limit_input.text())
            n = int(self.intervals_input.text())
            func_str = self.func_input.text()
            if not func_str:
                self.show_message("Input Error", "Function cannot be empty.")
                return None
        except ValueError:
            self.show_message("Input Error", "Limits and interval count must be valid numbers.")
            return None
        
        if n % 2 != 0:
            self.show_message("Input Error", "The number of intervals (n) must be an even number for Simpson's 1/3 Rule.")
            return None

        try:
            x_sym = sympy.symbols('x')
            f_sym = sympy.sympify(func_str)
            f_numeric = sympy.lambdify(x_sym, f_sym, 'numpy')
            _ = f_numeric(a) # Test run
        except Exception as e:
            self.show_message("Expression Error", f"Could not parse function. Check syntax.\nError: {e}")
            return None
            
        return f_numeric, a, b, n

    def run_solver(self):
        """Main function to trigger the integration process."""
        self.solution_display.clear()
        self.solution_display.setFont(QFont("Courier New", 10))
        self.solution_display.setLineWrapMode(QTextEdit.NoWrap)
        
        parsed_data = self.get_inputs_and_parse()
        if parsed_data is None: 
            self.populate_initial_explanation() # Restore explanation on error
            return
        
        f, a, b, n = parsed_data
        
        self.solution_display.append(f"--- Solving Integral of f(x) = {self.func_input.text()} from {a} to {b} ---\n")
        
        # Step 1: Calculate h
        h = (b - a) / n
        self.solution_display.append(f"STEP 1: Calculate step size (h)")
        self.solution_display.append(f"h = (b - a) / n = ({b} - {a}) / {n} = {h:.6f}\n")
        
        # Step 2: Evaluate function at each point
        x_vals = np.linspace(a, b, n + 1)
        y_vals = f(x_vals)
        self.solution_display.append("STEP 2: Evaluate f(x) at each point x_i")
        header = f"{'i':>4} | {'x_i':>15} | {'f(x_i)':>15}"
        self.solution_display.append(header)
        self.solution_display.append("-" * len(header))
        for i, (x, y) in enumerate(zip(x_vals, y_vals)):
            self.solution_display.append(f"{i:>4} | {x:15.8f} | {y:15.8f}")
        QApplication.processEvents()

        # Step 3: Sum the terms according to the rule
        self.solution_display.append("\nSTEP 3: Apply Simpson's 1/3 Rule formula")
        self.solution_display.append("Integral ≈ (h/3) * [f(x₀) + 4Σf(x_odd) + 2Σf(x_even) + f(x_n)]\n")

        f0 = y_vals[0]
        fn = y_vals[-1]
        sum_odd = np.sum(y_vals[1:-1:2])
        sum_even = np.sum(y_vals[2:-1:2])
        
        self.solution_display.append(f"f(x₀) = {f0:.8f}")
        self.solution_display.append(f"f(xₙ) = f(x_{n}) = {fn:.8f}\n")
        self.solution_display.append(f"Sum of odd-indexed terms (multiplied by 4):")
        self.solution_display.append(f"  4 * ({' + '.join([f'{y:.4f}' for y in y_vals[1:-1:2]])}) = 4 * {sum_odd:.8f} = {4*sum_odd:.8f}\n")
        
        self.solution_display.append(f"Sum of even-indexed terms (multiplied by 2):")
        if len(y_vals[2:-1:2]) > 0:
            self.solution_display.append(f"  2 * ({' + '.join([f'{y:.4f}' for y in y_vals[2:-1:2]])}) = 2 * {sum_even:.8f} = {2*sum_even:.8f}\n")
        else:
            self.solution_display.append("  (No inner even terms for n < 4)\n")

        # Step 4: Final Calculation
        integral_val = (h / 3) * (f0 + 4 * sum_odd + 2 * sum_even + fn)
        
        self.solution_display.append("STEP 4: Combine all parts for the final result")
        self.solution_display.append(f"Integral ≈ ({h:.6f}/3) * [{f0:.6f} + {4*sum_odd:.6f} + {2*sum_even:.6f} + {fn:.6f}]")
        self.solution_display.append(f"Integral ≈ ({h/3:.6f}) * [{f0 + 4*sum_odd + 2*sum_even + fn:.6f}]")

        self.solution_display.append("\n--- FINAL RESULT ---\n")
        self.solution_display.append(f"The approximate value of the integral is: {integral_val:.10f}")
