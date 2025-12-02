class DFA:
    def __init__(self):
        # States represent the remainder when divided by 3: q0=0, q1=1, q2=2
        self.states = {'q0', 'q1', 'q2'}
        self.start_state = 'q0'
        self.accept_states = {'q0'}
        # Transition function: (current_state, input_symbol) -> next_state
        self.transitions = {
            ('q0', '0'): 'q0', ('q0', '1'): 'q1',
            ('q1', '0'): 'q2', ('q1', '1'): 'q0',
            ('q2', '0'): 'q1', ('q2', '1'): 'q2'
        }
        self.current_state = self.start_state

    def process_string(self, input_string):
        self.current_state = self.start_state
        print(f"Starting at {self.current_state}")
        
        for char in input_string:
            if char not in ['0', '1']:
                raise ValueError("Invalid Alphabet")
            
            prev = self.current_state
            self.current_state = self.transitions[(self.current_state, char)]
            print(f"Input: {char} | {prev} -> {self.current_state}")
            
        return self.current_state in self.accept_states

# Test Cases
dfa = DFA()
test_strings = ["11", "110", "1001"] # 3 (accept), 6 (accept), 9 (accept)
