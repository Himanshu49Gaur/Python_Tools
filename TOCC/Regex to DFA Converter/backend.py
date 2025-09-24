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

def infix_to_postfix(regex):
    """
    Converts an infix regular expression to a postfix (RPN) expression.
    This makes it easier to evaluate and build the NFA.
    """
    precedence = {'|': 1, '.': 2, '*': 3}
    postfix = ''
    stack = []
    
    formatted_regex = add_concatenation_operator(regex)

    for char in formatted_regex:
        if char.isalnum() or char == 'ε':
            postfix += char
        elif char == '(':
            stack.append(char)
        elif char == ')':
            while stack and stack[-1] != '(':
                postfix += stack.pop()
            stack.pop()  # Pop '('
        else: # Operator
            while stack and stack[-1] != '(' and precedence.get(stack[-1], 0) >= precedence.get(char, 0):
                postfix += stack.pop()
            stack.append(char)

    while stack:
        postfix += stack.pop()
        
    return postfix, formatted_regex

# --- Thompson's Construction: Postfix to ε-NFA ---

class NFAState:
    _id = 0
    def __init__(self):
        self.id = NFAState._id
        NFAState._id += 1
        self.transitions = {} # symbol -> set of states

class EpsilonNFA:
    def __init__(self, start_state, final_state):
        self.start_state = start_state
        self.final_state = final_state

def postfix_to_nfa(postfix):
    """
    Builds an ε-NFA from a postfix regex using Thompson's Construction.
    """
    NFAState._id = 0 # Reset state counter for each run
    stack = []
    
    explanation_steps = []

    for char in postfix:
        if char.isalnum() or char == 'ε':
            # Base case: create a simple NFA for a character
            start = NFAState()
            final = NFAState()
            start.transitions[char] = {final}
            stack.append(EpsilonNFA(start, final))
        elif char == '*':
            # Kleene Star: loop the NFA
            nfa = stack.pop()
            start = NFAState()
            final = NFAState()
            start.transitions['ε'] = {nfa.start_state, final}
            nfa.final_state.transitions['ε'] = {nfa.start_state, final}
            stack.append(EpsilonNFA(start, final))
        elif char == '.':
            # Concatenation: connect two NFAs sequentially
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            nfa1.final_state.transitions['ε'] = {nfa2.start_state}
            stack.append(EpsilonNFA(nfa1.start_state, nfa2.final_state))
        elif char == '|':
            # Union: create a new start and final state with branches
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            start = NFAState()
            final = NFAState()
            start.transitions['ε'] = {nfa1.start_state, nfa2.start_state}
            nfa1.final_state.transitions['ε'] = {final}
            nfa2.final_state.transitions['ε'] = {final}
            stack.append(EpsilonNFA(start, final))

    return stack.pop()


# --- ε-NFA to DFA Conversion (Subset Construction) ---

def get_all_nfa_states(nfa):
    """Traverses the NFA to get all unique state objects."""
    all_states = set()
    q = [nfa.start_state]
    visited = {nfa.start_state}
    while q:
        current = q.pop(0)
        all_states.add(current)
        for symbol, next_states in current.transitions.items():
            for state in next_states:
                if state not in visited:
                    visited.add(state)
                    q.append(state)
    return list(all_states)
    
def epsilon_closure(states, all_nfa_states_map):
    """
    Calculates the ε-closure for a set of NFA states.
    This is the set of all states reachable via ε-transitions.
    """
    closure = set(states)
    stack = list(states)
    while stack:
        state_id = stack.pop()
        state_obj = all_nfa_states_map.get(state_id)
        if state_obj:
            epsilon_transitions = state_obj.transitions.get('ε', set())
            for next_state in epsilon_transitions:
                if next_state.id not in closure:
                    closure.add(next_state.id)
                    stack.append(next_state.id)
    return frozenset(closure)

def move(states, symbol, all_nfa_states_map):
    """
    Calculates the set of states reachable from a set of states on a given symbol.
    """
    reachable = set()
    for state_id in states:
        state_obj = all_nfa_states_map.get(state_id)
        if state_obj:
            transitions = state_obj.transitions.get(symbol, set())
            for next_state in transitions:
                reachable.add(next_state.id)
    return frozenset(reachable)

def nfa_to_dfa(nfa, alphabet):
    """
    Converts an ε-NFA to a DFA using the subset construction algorithm.
    """
    all_nfa_states = get_all_nfa_states(nfa)
    all_nfa_states_map = {s.id: s for s in all_nfa_states}
    nfa_final_state_id = nfa.final_state.id

    dfa_states = []
    dfa_transitions = {}
    
    # The key is the frozenset of NFA state IDs, the value is the DFA state ID
    dfa_state_map = {} 
    
    # Start state of DFA is the ε-closure of the NFA's start state
    start_state_nfa_ids = epsilon_closure({nfa.start_state.id}, all_nfa_states_map)
    
    unmarked_states = [start_state_nfa_ids]
    dfa_state_map[start_state_nfa_ids] = 0
    dfa_states.append({'id': 0, 'nfa_states': sorted(list(start_state_nfa_ids))})
    
    dfa_id_counter = 1
    
    conversion_steps = []

    while unmarked_states:
        current_nfa_ids = unmarked_states.pop(0)
        current_dfa_id = dfa_state_map[current_nfa_ids]
        
        step_explanation = f"Processing DFA state {current_dfa_id} which corresponds to NFA states {sorted(list(current_nfa_ids))}:"
        step_transitions = []
        
        for symbol in alphabet:
            move_result = move(current_nfa_ids, symbol, all_nfa_states_map)
            
            if not move_result:
                step_transitions.append(f"  - On symbol '{symbol}', move({sorted(list(current_nfa_ids))}, '{symbol}') is empty. No transition.")
                continue
                
            closure_result = epsilon_closure(move_result, all_nfa_states_map)
            
            if closure_result not in dfa_state_map:
                dfa_state_map[closure_result] = dfa_id_counter
                unmarked_states.append(closure_result)
                dfa_states.append({'id': dfa_id_counter, 'nfa_states': sorted(list(closure_result))})
                dfa_id_counter += 1
            
            target_dfa_id = dfa_state_map[closure_result]
            dfa_transitions.setdefault(current_dfa_id, {})[symbol] = target_dfa_id

            # Explanation for the step
            trans_exp = (f"  - On symbol '{symbol}':\n"
                         f"    1. move({sorted(list(current_nfa_ids))}, '{symbol}') = {sorted(list(move_result))}\n"
                         f"    2. ε-closure({sorted(list(move_result))}) = {sorted(list(closure_result))}\n"
                         f"    3. This corresponds to DFA state {target_dfa_id}. Created transition {current_dfa_id} -> {target_dfa_id}.")
            step_transitions.append(trans_exp)
        
        conversion_steps.append({'title': step_explanation, 'transitions': step_transitions})

    # Determine final states of the DFA
    dfa_final_states = [
        state['id'] for state in dfa_states 
        if nfa_final_state_id in state['nfa_states']
    ]

    return dfa_states, dfa_transitions, dfa_final_states, conversion_steps


# --- Flask App ---
app = Flask(__name__)
CORS(app) # Allow frontend to call backend

@app.route('/convert', methods=['POST'])
def convert_regex():
    try:
        data = request.get_json()
        regex = data['regex']
        if not regex:
            return jsonify({'error': 'Regex cannot be empty'}), 400

        # Step 1: Infix to Postfix
        postfix, formatted_regex = infix_to_postfix(regex)
        alphabet = sorted(list(set(re.sub(r'[^a-zA-Z0-9]', '', regex))))

        # Step 2: Postfix to ε-NFA
        nfa = postfix_to_nfa(postfix)
        
        # Format NFA for vis.js
        all_nfa_states = get_all_nfa_states(nfa)
        nfa_nodes = [{'id': s.id, 'label': str(s.id)} for s in all_nfa_states]
        nfa_edges = []
        for s in all_nfa_states:
            for symbol, next_states in s.transitions.items():
                for ns in next_states:
                    nfa_edges.append({'from': s.id, 'to': ns.id, 'label': symbol})

        # Step 3: ε-NFA to DFA
        dfa_states_data, dfa_transitions_data, dfa_final_states_ids, conversion_steps = nfa_to_dfa(nfa, alphabet)

        # Format DFA for vis.js
        dfa_nodes = [{'id': s['id'], 'label': f"{s['id']}\n{{{','.join(map(str, s['nfa_states']))}}}"} for s in dfa_states_data]
        dfa_edges = []
        for from_id, transitions in dfa_transitions_data.items():
            for symbol, to_id in transitions.items():
                dfa_edges.append({'from': from_id, 'to': to_id, 'label': symbol})

        return jsonify({
            'regex': regex,
            'formatted_regex': formatted_regex,
            'postfix': postfix,
            'alphabet': ''.join(alphabet),
            'nfa': {
                'nodes': nfa_nodes,
                'edges': nfa_edges,
                'start_state': nfa.start_state.id,
                'final_state': nfa.final_state.id
            },
            'dfa': {
                'nodes': dfa_nodes,
                'edges': dfa_edges,
                'start_state': 0,
                'final_states': dfa_final_states_ids,
                'conversion_steps': conversion_steps
            }
        })
    except Exception as e:
        return jsonify({'error': f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)

