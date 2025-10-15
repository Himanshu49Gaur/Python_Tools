import sys
import numpy as np
import sympy

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTextEdit, QGroupBox, QGridLayout, 
    QMessageBox, QComboBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class SimpsonsDualApp(QMainWindow):
    """
    A PyQt5 GUI application for approximating definite integrals using either
    Simpson's 1/3 Rule or Simpson's 3/8 Rule.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simpson's 1/3 & 3/8 Rules Solver")
        self.setGeometry(100, 100, 1300, 800)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.main_layout = QHBoxLayout(self.central_widget)

        self.create_input_widgets()
        self.create_output_widgets()
        self.populate_initial_explanation()

        self.setup_layout()

    def create_input_widgets(self):
        """Creates all the widgets for the user input panel."""
        # Method Selection
        self.method_group = QGroupBox("Select Integration Method")
        self.method_layout = QGridLayout(self.method_group)
        self.method_combo = QComboBox()
        self.method_combo.addItems(["Simpson's 1/3 Rule", "Simpson's 3/8 Rule"])
        self.method_combo.setFont(QFont("Arial", 10))
        self.method_layout.addWidget(self.method_combo, 0, 0)
        
        # Problem Input
        self.input_group = QGroupBox("Problem Definition")
        self.input_layout = QGridLayout(self.input_group)
        
        self.func_label = QLabel("Enter function f(x):")
        self.func_input = QLineEdit("1 / (1 + x**2)")
        
        self.lower_limit_label = QLabel("Lower Limit (a):")
        self.lower_limit_input = QLineEdit("0")
        
        self.upper_limit_label = QLabel("Upper Limit (b):")
        self.upper_limit_input = QLineEdit("6")
        
        self.intervals_label = QLabel("Intervals (n):")
        self.intervals_input = QLineEdit("6")

        self.input_layout.addWidget(self.func_label, 0, 0)
        self.input_layout.addWidget(self.func_input, 0, 1)
        self.input_layout.addWidget(self.lower_limit_label, 1, 0)
        self.input_layout.addWidget(self.lower_limit_input, 1, 1)
        self.input_layout.addWidget(self.upper_limit_label, 2, 0)
        self.input_layout.addWidget(self.upper_limit_input, 2, 1)
        self.input_layout.addWidget(self.intervals_label, 3, 0)
        self.input_layout.addWidget(self.intervals_input, 3, 1)
        
        self.solve_button = QPushButton("Calculate Integral")
        self.solve_button.setFont(QFont("Arial", 12, QFont.Bold))
        self.solve_button.clicked.connect(self.run_solver)
        
        self.clear_button = QPushButton("Clear & Reset Explanation")
        self.clear_button.clicked.connect(self.clear_all_fields)

    def create_output_widgets(self):
        """Creates the text area for displaying explanations and solutions."""
        self.output_group = QGroupBox("Explanation & Solution Steps")
        self.output_layout = QVBoxLayout(self.output_group)
        self.solution_display = QTextEdit()
        self.solution_display.setReadOnly(True)
        self.output_layout.addWidget(self.solution_display)

    def setup_layout(self):
        """Arranges all widgets in the main window layout."""
        input_panel = QWidget()
        input_layout = QVBoxLayout(input_panel)
        
        input_layout.addWidget(self.method_group)
        input_layout.addWidget(self.input_group)
        input_layout.addWidget(QLabel("Syntax Guide: Use 'x' and standard functions like exp(), sin(), etc."))

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.clear_button)
        button_layout.addWidget(self.solve_button)
        input_layout.addLayout(button_layout)
        
        input_panel.setFixedWidth(450)
        
        self.main_layout.addWidget(input_panel)
        self.main_layout.addWidget(self.output_group)

    def populate_initial_explanation(self):
        """Fills the output area with a detailed explanation of both methods."""
        self.solution_display.setFont(QFont("Arial", 11))
        explanation_html = """
        <h2 style='color:#003366;'>Simpson's Rules for Numerical Integration</h2>
        <p>Simpson's rules approximate integrals by fitting polynomials to the function. They are generally more accurate than the Trapezoidal rule.</p>
        <table width='100%' style='border-collapse: collapse;' border='1'>
            <tr style='background-color: #f0f8ff;'>
                <th style='padding: 8px; text-align: left;'><h3>Simpson's 1/3 Rule</h3></th>
                <th style='padding: 8px; text-align: left;'><h3>Simpson's 3/8 Rule</h3></th>
            </tr>
            <tr>
                <td style='padding: 8px; vertical-align: top;'>
                    <p><b>Core Idea:</b> Approximates the function over pairs of intervals using a <b>2nd-degree polynomial (a parabola)</b>.</p>
                    <p><b>Constraint:</b> The number of intervals 'n' <b>must be an even number</b>.</p>
                    <p><b>Formula:</b></p>
                    <p style='font-family: Courier New; font-size: 14px; background-color: #f0f0f0; padding: 10px; border-radius: 5px;'>
                        (h/3) [y₀ + 4y₁ + 2y₂ + 4y₃ + ... + 2yₙ₋₂ + 4yₙ₋₁ + yₙ]
                    </p>
                    <p><b>Coefficient Pattern:</b> 1, 4, 2, 4, 2, ... , 4, 1</p>
                </td>
                <td style='padding: 8px; vertical-align: top;'>
                    <p><b>Core Idea:</b> Approximates the function over groups of three intervals using a <b>3rd-degree polynomial (a cubic)</b>.</p>
                    <p><b>Constraint:</b> The number of intervals 'n' <b>must be a multiple of 3</b>.</p>
                    <p><b>Formula:</b></p>
                    <p style='font-family: Courier New; font-size: 14px; background-color: #f0f0f0; padding: 10px; border-radius: 5px;'>
                        (3h/8) [y₀ + 3y₁ + 3y₂ + 2y₃ + 3y₄ + ... + 2yₙ₋₃ + 3yₙ₋₂ + 3yₙ₋₁ + yₙ]
                    </p>
                    <p><b>Coefficient Pattern:</b> 1, 3, 3, 2, 3, 3, 2, ... , 3, 3, 1</p>
                </td>
            </tr>
        </table>
        """
        self.solution_display.setHtml(explanation_html)

    def clear_all_fields(self):
        """Clears all input fields and resets the explanation."""
        self.func_input.setText("1 / (1 + x**2)")
        self.lower_limit_input.setText("0")
        self.upper_limit_input.setText("6")
        self.intervals_input.setText("6")
        self.populate_initial_explanation()

    def show_message(self, title, message):
        msg_box = QMessageBox(); msg_box.setIcon(QMessageBox.Critical); msg_box.setText(message); msg_box.setWindowTitle(title); msg_box.exec_()

    def get_inputs_and_parse(self):
        """Reads UI inputs, validates them, and creates a numerical function."""
        method = self.method_combo.currentText()
        try:
            a, b, n = float(self.lower_limit_input.text()), float(self.upper_limit_input.text()), int(self.intervals_input.text())
            func_str = self.func_input.text()
            if not func_str: self.show_message("Input Error", "Function cannot be empty."); return None
        except ValueError: self.show_message("Input Error", "Limits and interval count must be valid numbers."); return None
        
        if method == "Simpson's 1/3 Rule" and n % 2 != 0:
            self.show_message("Input Error", "For Simpson's 1/3 Rule, 'n' must be an even number."); return None
        if method == "Simpson's 3/8 Rule" and n % 3 != 0:
            self.show_message("Input Error", "For Simpson's 3/8 Rule, 'n' must be a multiple of 3."); return None

        try:
            x_sym = sympy.symbols('x'); f_sym = sympy.sympify(func_str)
            f_numeric = sympy.lambdify(x_sym, f_sym, 'numpy'); _ = f_numeric(a)
        except Exception as e: self.show_message("Expression Error", f"Could not parse function: {e}"); return None
            
        return f_numeric, a, b, n, method

    def run_solver(self):
        """Dispatches to the correct solver based on user's choice."""
        self.solution_display.clear()
        self.solution_display.setFont(QFont("Courier New", 10))
        self.solution_display.setLineWrapMode(QTextEdit.NoWrap)
        
        parsed_data = self.get_inputs_and_parse()
        if parsed_data is None: self.populate_initial_explanation(); return
        
        _ , _ , _ , _ , method = parsed_data
        
        if method == "Simpson's 1/3 Rule":
            self.solve_simpson_1_3(parsed_data)
        else:
            self.solve_simpson_3_8(parsed_data)
    
    def solve_simpson_1_3(self, parsed_data):
        f, a, b, n, method = parsed_data
        self.solution_display.append(f"--- Solving with {method} ---\n")
        h = (b - a) / n
        self.solution_display.append(f"STEP 1: Calculate step size (h)\nh = (b - a) / n = ({b} - {a}) / {n} = {h:.6f}\n")
        
        x_vals = np.linspace(a, b, n + 1); y_vals = f(x_vals)
        self.solution_display.append("STEP 2: Evaluate f(x) at each point x_i")
        header = f"{'i':>4} | {'x_i':>15} | {'f(x_i)':>15}"; self.solution_display.append(header); self.solution_display.append("-" * len(header))
        for i, (x, y) in enumerate(zip(x_vals, y_vals)): self.solution_display.append(f"{i:>4} | {x:15.8f} | {y:15.8f}")
        
        self.solution_display.append("\nSTEP 3: Apply Simpson's 1/3 Rule formula")
        self.solution_display.append("   Integral ≈ (h/3) * [y₀ + 4(y₁ + y₃ + ...) + 2(y₂ + y₄ + ...) + yₙ]\n")

        y0, yn = y_vals[0], y_vals[-1]
        sum_odd = np.sum(y_vals[1:-1:2]); sum_even = np.sum(y_vals[2:-1:2])
        
        self.solution_display.append(f"   y₀ = {y0:.8f}"); self.solution_display.append(f"   yₙ = {yn:.8f}\n")
        self.solution_display.append(f"   4 * (Sum of odd terms) = 4 * {sum_odd:.8f} = {4*sum_odd:.8f}")
        self.solution_display.append(f"   2 * (Sum of even terms) = 2 * {sum_even:.8f} = {2*sum_even:.8f}\n")

        integral_val = (h / 3) * (y0 + 4 * sum_odd + 2 * sum_even + yn)
        self.solution_display.append("STEP 4: Final Calculation")
        self.solution_display.append(f"   Integral ≈ ({h:.6f}/3) * [{y0:.6f} + {4*sum_odd:.6f} + {2*sum_even:.6f} + {yn:.6f}]")
        self.solution_display.append(f"   Integral ≈ {h/3:.6f} * [{y0 + 4*sum_odd + 2*sum_even + yn:.6f}]")
        self.solution_display.append(f"\n--- FINAL RESULT ---\nApproximate Integral = {integral_val:.10f}")
        
    def solve_simpson_3_8(self, parsed_data):
        f, a, b, n, method = parsed_data
        self.solution_display.append(f"--- Solving with {method} ---\n")
        h = (b - a) / n
        self.solution_display.append(f"STEP 1: Calculate step size (h)\nh = (b - a) / n = ({b} - {a}) / {n} = {h:.6f}\n")

        x_vals = np.linspace(a, b, n + 1); y_vals = f(x_vals)
        self.solution_display.append("STEP 2: Evaluate f(x) at each point x_i")
        header = f"{'i':>4} | {'x_i':>15} | {'f(x_i)':>15}"; self.solution_display.append(header); self.solution_display.append("-" * len(header))
        for i, (x, y) in enumerate(zip(x_vals, y_vals)): self.solution_display.append(f"{i:>4} | {x:15.8f} | {y:15.8f}")

        self.solution_display.append("\nSTEP 3: Apply Simpson's 3/8 Rule formula")
        self.solution_display.append("   Integral ≈ (3h/8) * [y₀ + 3(y₁+y₂+y₄+y₅...) + 2(y₃+y₆+...) + yₙ]\n")

        y0, yn = y_vals[0], y_vals[-1]
        sum_mult_3, sum_mult_2 = 0, 0
        for i in range(1, n):
            if i % 3 == 0: sum_mult_2 += y_vals[i]
            else: sum_mult_3 += y_vals[i]
            
        self.solution_display.append(f"   y₀ = {y0:.8f}"); self.solution_display.append(f"   yₙ = {yn:.8f}\n")
        self.solution_display.append(f"   3 * (Sum of other terms) = 3 * {sum_mult_3:.8f} = {3*sum_mult_3:.8f}")
        self.solution_display.append(f"   2 * (Sum of y₃, y₆,... terms) = 2 * {sum_mult_2:.8f} = {2*sum_mult_2:.8f}\n")

        integral_val = (3 * h / 8) * (y0 + 3 * sum_mult_3 + 2 * sum_mult_2 + yn)
        self.solution_display.append("STEP 4: Final Calculation")
        self.solution_display.append(f"   Integral ≈ (3*{h:.6f}/8) * [{y0:.6f} + {3*sum_mult_3:.6f} + {2*sum_mult_2:.6f} + {yn:.6f}]")
        self.solution_display.append(f"   Integral ≈ {3*h/8:.6f} * [{y0 + 3*sum_mult_3 + 2*sum_mult_2 + yn:.6f}]")
        self.solution_display.append(f"\n--- FINAL RESULT ---\nApproximate Integral = {integral_val:.10f}")
