class SimplifiedDES:
    """
    A structural replica of DES scaled down for educational purposes.
    - Block size: 8 bits (vs 64 in standard DES)
    - Key size: 10 bits (vs 56 in standard DES)
    - Rounds: 2 (vs 16 in standard DES)
    """
    # Key Generation Tables
    P10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
    P8  = [6, 3, 7, 4, 8, 5, 10, 9]

    # Block Permutation Tables
    IP    = [2, 6, 3, 1, 4, 8, 5, 7] # Initial Permutation
    IP_INV= [4, 1, 3, 5, 7, 2, 8, 6] # Final Permutation (Inverse IP)
    EP    = [4, 1, 2, 3, 2, 3, 4, 1] # Expansion Permutation
    P4    = [2, 4, 3, 1]             # P-Box

    # Substitution Boxes (S-Boxes)
    S0 = [
        [1, 0, 3, 2],
        [3, 2, 1, 0],
        [0, 2, 1, 3],
        [3, 1, 3, 2]
    ]
    S1 = [
        [0, 1, 2, 3],
        [2, 0, 1, 3],
        [3, 0, 1, 0],
        [2, 1, 0, 3]
    ]

    def __init__(self, key: int):
        # Generate the two 8-bit round subkeys from the 10-bit master key
        self.k1, self.k2 = self._generate_keys(key)

    def _permute(self, data: int, table: list, bit_length: int) -> int:
        """Permutes the bits of 'data' according to the 'table'."""
        result = 0
        for i, pos in enumerate(table):
            # Extract the bit at 'pos' (1-indexed from left) and place it at 'i'
            bit = (data >> (bit_length - pos)) & 1
            result |= (bit << (len(table) - 1 - i))
        return result

    def _left_shift(self, bits: int, shifts: int) -> int:
        """Performs a circular left shift on 5-bit halves."""
        # 5-bit mask is 11111 (31)
        shifted = ((bits << shifts) & 31) | (bits >> (5 - shifts))
        return shifted

    def _generate_keys(self, key: int):
        """Generates subkey 1 and subkey 2 for the two Feistel rounds."""
        p10_key = self._permute(key, self.P10, 10)
        
        # Split into two 5-bit halves
        left = (p10_key >> 5) & 31
        right = p10_key & 31
        
        # Shift 1 for K1
        left1 = self._left_shift(left, 1)
        right1 = self._left_shift(right, 1)
        k1 = self._permute((left1 << 5) | right1, self.P8, 10)
        
        # Shift 2 for K2
        left2 = self._left_shift(left1, 2)
        right2 = self._left_shift(right1, 2)
        k2 = self._permute((left2 << 5) | right2, self.P8, 10)
        
        return k1, k2

    def _sbox(self, data: int, sbox: list) -> int:
        """Looks up a 2-bit output from a 4-bit input using a DES S-Box."""
        # The outer bits (bit 1 and 4) determine the row
        row = ((data & 0b1000) >> 2) | (data & 0b0001)
        # The inner bits (bit 2 and 3) determine the column
        col = (data & 0b0110) >> 1
        return sbox[row][col]

    def _f_function(self, right_nibble: int, subkey: int) -> int:
        """The core DES round function."""
        # 1. Expand 4 bits to 8 bits
        expanded = self._permute(right_nibble, self.EP, 4)
        
        # 2. Key Mixing (XOR)
        mixed = expanded ^ subkey
        
        # 3. S-Boxes
        left_mixed = (mixed >> 4) & 15
        right_mixed = mixed & 15
        s0_out = self._sbox(left_mixed, self.S0)
        s1_out = self._sbox(right_mixed, self.S1)
        
        # 4. P-Box Permutation
        s_combined = (s0_out << 2) | s1_out
        return self._permute(s_combined, self.P4, 4)

    def _process_block(self, block: int, decrypt=False) -> int:
        """Runs the 8-bit block through the S-DES network."""
        keys = (self.k2, self.k1) if decrypt else (self.k1, self.k2)
        
        # Initial Permutation
        block = self._permute(block, self.IP, 8)
        
        # Split into 4-bit Left and Right halves
        L = (block >> 4) & 15
        R = block & 15
        
        # Round 1
        new_R = L ^ self._f_function(R, keys[0])
        new_L = R
        
        # Swap halves for Round 2
        L, R = new_R, new_L
        
        # Round 2
        final_R = L ^ self._f_function(R, keys[1])
        final_L = R
        
        # Combine halves (Note: L and R are not swapped after the final round)
        combined = (final_L << 4) | final_R
        
        # Final Inverse Permutation
        return self._permute(combined, self.IP_INV, 8)

    def encrypt_byte(self, block: int) -> int:
        return self._process_block(block, decrypt=False)

    def decrypt_byte(self, block: int) -> int:
        return self._process_block(block, decrypt=True)

# ==========================================
# Example Usage
# ==========================================
if __name__ == "__main__":
    # 1. Define an 8-bit plaintext block and a 10-bit master key
    # Plaintext: 10101010 (Decimal 170)
    # Key: 1010000010 (Decimal 642)
    plaintext_block = 0b10101010
    master_key = 0b1010000010
    
    print(f"Original Block (Binary): {bin(plaintext_block)[2:].zfill(8)}")
    print(f"Master Key (Binary)    : {bin(master_key)[2:].zfill(10)}\n")
    
    # 2. Initialize S-DES
    sdes = SimplifiedDES(master_key)
    
    # 3. Encrypt the 8-bit block
    encrypted_block = sdes.encrypt_byte(plaintext_block)
    print(f"Encrypted Block        : {bin(encrypted_block)[2:].zfill(8)}")
    
    # 4. Decrypt the block
    decrypted_block = sdes.decrypt_byte(encrypted_block)
    print(f"Decrypted Block        : {bin(decrypted_block)[2:].zfill(8)}")
    
    # Verify the code works correctly
    assert plaintext_block == decrypted_block
