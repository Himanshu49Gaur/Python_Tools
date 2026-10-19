class EnigmaMachine:
    """
    A simulator for the WWII 3-rotor Enigma machine.
    """
    ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    
    # Historical wiring configurations
    ROTORS = {
        "I":   {"wiring": "EKMFLGDQVZNTOWYHXUSPAIBRCJ", "notch": "Q"},
        "II":  {"wiring": "AJDKSIRUXBLHWTMCQGZNPYFVOE", "notch": "E"},
        "III": {"wiring": "BDFHJLCPRTXVZNYEIWGAKMUSQO", "notch": "V"}
    }
    REFLECTORS = {
        "B": "YRUHQSLDPXNGOKMIEBFZCWVJAT"
    }

    def __init__(self, rotor_types, reflector_type, ring_settings, initial_positions, plugboard_pairs):
        self.rotors = [self.ROTORS[r]["wiring"] for r in rotor_types]
        self.notches = [self.ROTORS[r]["notch"] for r in rotor_types]
        self.reflector = self.REFLECTORS[reflector_type]
        
        # Convert letters to 0-25 indices
        self.ring_settings = [self.ALPHABET.index(c) for c in ring_settings]
        self.positions = [self.ALPHABET.index(c) for c in initial_positions]
        self.plugboard = self._create_plugboard(plugboard_pairs)

    def _create_plugboard(self, pairs):
        """Creates a mapping for the plugboard swaps."""
        mapping = list(self.ALPHABET)
        for pair in pairs:
            a, b = pair[0], pair[1]
            mapping[self.ALPHABET.index(a)] = b
            mapping[self.ALPHABET.index(b)] = a
        return "".join(mapping)

    def _step_rotors(self):
        """Advances the rotors like an odometer before encrypting a character."""
        # Check if the middle rotor is at its notch (Double stepping anomaly of historical Enigma)
        step_middle = self.ALPHABET[self.positions[1]] == self.notches[1]
        step_left = step_middle
        
        # Check if the right rotor is at its notch
        if self.ALPHABET[self.positions[2]] == self.notches[2]:
            step_middle = True

        # Right rotor always steps
        self.positions[2] = (self.positions[2] + 1) % 26
        if step_middle:
            self.positions[1] = (self.positions[1] + 1) % 26
        if step_left:
            self.positions[0] = (self.positions[0] + 1) % 26

    def _pass_through_rotor(self, char_index, rotor_index, reverse=False):
        """Passes a signal through a single rotor."""
        wiring = self.rotors[rotor_index]
        pos = self.positions[rotor_index]
        ring = self.ring_settings[rotor_index]
        
        # Calculate the shift based on rotor position and ring setting
        shift = pos - ring
        
        if not reverse:
            # Forward pass (Right to Left)
            entry_char = self.ALPHABET[(char_index + shift) % 26]
            wired_char = wiring[self.ALPHABET.index(entry_char)]
            return (self.ALPHABET.index(wired_char) - shift) % 26
        else:
            # Reverse pass (Left to Right)
            entry_char = self.ALPHABET[(char_index + shift) % 26]
            wired_index = wiring.index(entry_char)
            return (wired_index - shift) % 26

    def process_character(self, char):
        """Encrypts/Decrypts a single character."""
        if char not in self.ALPHABET:
            return char
            
        self._step_rotors()

        # 1. Pass through Plugboard
        char = self.plugboard[self.ALPHABET.index(char)]
        char_index = self.ALPHABET.index(char)

        # 2. Pass through Rotors (Right to Left: 2 -> 1 -> 0)
        for i in [2, 1, 0]:
            char_index = self._pass_through_rotor(char_index, i, reverse=False)

        # 3. Pass through Reflector
        char_index = self.ALPHABET.index(self.reflector[char_index])

        # 4. Pass back through Rotors (Left to Right: 0 -> 1 -> 2)
        for i in [0, 1, 2]:
            char_index = self._pass_through_rotor(char_index, i, reverse=True)

        # 5. Pass back through Plugboard
        final_char = self.ALPHABET[char_index]
        return self.plugboard[self.ALPHABET.index(final_char)]

    def process_text(self, text):
        """Processes a full string."""
        text = text.upper()
        return "".join(self.process_character(c) for c in text)

# ==========================================
# Example Usage
# ==========================================
if __name__ == "__main__":
    # Settings must be EXACTLY the same for encryption and decryption
    rotors = ["I", "II", "III"]
    reflector = "B"
    ring_settings = "AAA"
    initial_positions = "CAT"
    plugboard_pairs = ["AB", "CD", "EF"] # A swaps with B, C with D, etc.

    # 1. Initialize machine for encryption
    enigma_encryptor = EnigmaMachine(
        rotors, reflector, ring_settings, initial_positions, plugboard_pairs
    )
    
    plaintext = "CYBERSECURITY AND DIGITAL FORENSICS"
    print(f"Plaintext:  {plaintext}")
    
    ciphertext = enigma_encryptor.process_text(plaintext)
    print(f"Ciphertext: {ciphertext}")

    # 2. Initialize a FRESH machine with the exact same settings for decryption
    enigma_decryptor = EnigmaMachine(
        rotors, reflector, ring_settings, initial_positions, plugboard_pairs
    )
    
    decrypted_text = enigma_decryptor.process_text(ciphertext)
    print(f"Decrypted:  {decrypted_text}")
    
    assert plaintext.replace(" ", "") == decrypted_text.replace(" ", "")
