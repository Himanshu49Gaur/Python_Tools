from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import re

# --- Infix to Postfix Conversion (Shunting-yard algorithm) ---
# This part handles operator precedence for the regex.
# Precedence: Kleene Star > Concatenation > Union
