from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import re

# --- Infix to Postfix Conversion (Shunting-yard algorithm) ---
# This part handles operator precedence for the regex.
# Precedence: Kleene Star > Concatenation > Union

def add_concatenation_operator(regex):
    """
    Explicitly adds the '.' concatenation operator to the regex string.
    This is crucial for the shunting-yard algorithm to work correctly.
    Example: 'ab|c*' becomes 'a.b|c*'
    """
    output = ''
    for i in range(len(regex)):
        output += regex[i]
        if i + 1 < len(regex):
            # A char/group followed by another char/group needs a '.'
            left = regex[i]
            right = regex[i+1]
            if left not in '(|' and right not in ')|*':
                output += '.'
    return output
