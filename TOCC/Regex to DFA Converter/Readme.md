# Regex to Deterministic Finite Automaton (DFA) Converter

This project is a web-based tool that provides a visual and educational walkthrough of converting a regular expression into a Deterministic Finite Automaton (DFA). It first converts the regex into an Epsilon-Nondeterministic Finite Automaton (ε-NFA) using Thompson's Construction and then converts the ε-NFA into a DFA using the Subset Construction algorithm.

The application is built with a Python Flask backend for the computational logic and a vanilla HTML/CSS/JavaScript frontend for the user interface and graph visualization.

## Features

- **Regex to ε-NFA:** Converts any given regular expression into an equivalent ε-NFA.
- **ε-NFA to DFA:** Transforms the generated ε-NFA into a DFA, eliminating ambiguity.
- **Interactive Visualization:** Uses the vis.js library to render clear, interactive graphs of both the NFA and DFA.
- **Step-by-Step Explanation:** Provides a detailed, multi-step log of the entire subset construction process, showing how each DFA state is derived from sets of NFA states.
- **Web-Based Interface:** A clean and simple single-page application that is easy to use.

## How It Works: The Conversion Process

The conversion from a regular expression to a DFA is a cornerstone of compiler design and theoretical computer science. This application automates the three key steps involved.

### Step 1: Infix to Postfix Conversion

To correctly handle operator precedence (* > concatenation > |), the input regular expression (infix notation) is first converted into postfix notation (also known as Reverse Polish Notation) using the Shunting-yard algorithm. An explicit concatenation operator (`.`) is added to the regex beforehand.

**Example:**  
The expression `(a|b)*a` is first converted to `(a|b)*.a` with an explicit concatenation operator. The final postfix form is `ab|*a..`.

### Step 2: Postfix to ε-NFA (Thompson's Construction)

The postfix expression is used to build an ε-NFA. This algorithm works by creating simple NFAs for individual characters and composing them into a larger NFA based on the operators.

- **Characters (a, b, ...):** A start state transitions to a final state on the character.
- **Concatenation (.):** The final state of the first NFA is connected to the start state of the second NFA via an ε-transition.
- **Union (|):** A new start state is created with ε-transitions to the start states of both NFAs. Their final states are connected to a new final state via ε-transitions.
- **Kleene Star (*):** A new start and final state are added. ε-transitions are added to create a "loop" around the original NFA, allowing it to be traversed zero or more times.

### Step 3: ε-NFA to DFA (Subset Construction)

This is the most complex part of the process. The algorithm creates a DFA where each state corresponds to a set of states from the ε-NFA.

- **Initial State:** The start state of the DFA is the ε-closure of the NFA's start state (all states reachable from it by only ε-transitions).
- **Explore Transitions:** For each DFA state and each symbol in the alphabet:
  1. Find all states reachable from the current set of NFA states on the given symbol (the move operation).
  2. Calculate the ε-closure of this new set of states.
- **Create New States:** If the resulting set of NFA states is not already a state in our DFA, create a new DFA state for it.
- **Repeat:** Continue until no new DFA states can be created.
- **Final States:** Any DFA state that contains the original NFA's final state is marked as a final state in the DFA.

## Project Structure

The application consists of two main files:

- **app.py:** A Python Flask backend server that handles all the computational logic. It exposes a single API endpoint (`/convert`) that accepts a regex and returns a JSON object with all the data needed for visualization.
- **index.html:** A self-contained frontend file. Includes HTML structure, CSS styling, and JavaScript for capturing user input, making API calls, and rendering graphs with vis.js.

## Setup and Installation

To run this project, have the backend server running and the frontend open in a browser.

### Prerequisites

- Python 3.x
- pip package manager

### Backend Setup

First, install the required Python libraries:
``pip install Flask Flask-Cors``



