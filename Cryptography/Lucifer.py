class LuciferConceptCipher:
    """
    A structural implementation of the Lucifer block cipher architecture.
    Demonstrates a 128-bit block Feistel network, 4-bit S-Box substitutions,
    and a key schedule generating subkeys.
    """
    # A standard 4-bit to 4-bit Substitution Box (S-Box)
    # Maps an input nibble (0-15) to a non-linear output nibble.
    S_BOX = [12, 5, 6, 11, 9, 0, 10, 13, 3, 14, 15, 8, 4, 7, 1, 2]

    def __init__(self, key: bytes):
        if len(key) != 16:
            raise ValueError("This Lucifer variant requires exactly a 128-bit (16-byte) key.")
        self.key = int.from_bytes(key, 'big')
        self.num_rounds = 16
        self.subkeys = self._generate_key_schedule()

    def _generate_key_schedule(self):
        """
        Generates 16 unique 64-bit subkeys from the 128-bit master key.
        Uses a simple shift-and-extract method to simulate Lucifer's key schedule.
        """
        subkeys = []
        current_key = self.key
        
        for _ in range(self.num_rounds):
            # Extract the upper 64 bits to use as the round subkey
            subkeys.append(current_key >> 64)
            
            # Rotate the 128-bit master key left by 7 bits to prep for the next round
            # (Shift left, then wrap the overflow bits back to the right)
            overflow = current_key >> (128 - 7)
            current_key = ((current_key << 7) & ((1 << 128) - 1)) | overflow
            
        return subkeys

    def _f_function(self, right_half: int, subkey: int) -> int:
        """
        The core Feistel Round Function (Substitution-Permutation Network).
        Operates on 64-bit halves.
        """
        # 1. Key Mixing
        mixed = right_half ^ subkey
        
        # 2. Substitution (S-boxes)
        # Process the 64-bit integer as sixteen 4-bit nibbles
        substituted = 0
        for i in range(16):
            # Extract the 4-bit nibble
            nibble = (mixed >> (i * 4)) & 0xF
            # Run through the S-Box
            sub_nibble = self.S_BOX[nibble]
            # Place the new nibble back into the integer
            substituted |= (sub_nibble << (i * 4))
            
        # 3. Permutation (P-boxes)
        # Simulated here with a 13-bit circular left shift across the 64-bit block
        # to provide diffusion for the next round.
        overflow = substituted >> (64 - 13)
        permuted = ((substituted << 13) & ((1 << 64) - 1)) | overflow
        
        return permuted

    def _process_block(self, block_bytes: bytes, encrypt: bool) -> bytes:
        """
        Processes a single 128-bit (16-byte) block through the Feistel network.
        """
        if len(block_bytes) != 16:
            # Pad the block if it's smaller than 16 bytes (PKCS#7 style padding logic could apply here)
            block_bytes = block_bytes.ljust(16, b'\x00')
            
        block_int = int.from_bytes(block_bytes, 'big')
        
        # Split the 128-bit block into Left (64-bit) and Right (64-bit) halves
        L = block_int >> 64
        R = block_int & ((1 << 64) - 1)
        
        # Determine the order of the subkeys
        keys = self.subkeys if encrypt else reversed(self.subkeys)
        
        # The 16-round Feistel Loop
        for round_key in keys:
            # R becomes the new L.
            # L is XORed with the output of the F-function to become the new R.
            next_L = R
            next_R = L ^ self._f_function(R, round_key)
            
            L = next_L
            R = next_R
            
        # After the final round, the halves are NOT swapped (standard Feistel design).
        # We re-combine R (upper) and L (lower) to form the final 128-bit ciphertext block.
        final_block = (R << 64) | L
        return final_block.to_bytes(16, 'big')

    def crypt(self, data: bytes, mode: str = "encrypt") -> bytes:
        """
        Encrypts or decrypts arbitrary-length data in Electronic Codebook (ECB) mode.
        Note: ECB mode is insecure for real-world use because identical plaintext 
        blocks produce identical ciphertext blocks, but it serves to demonstrate the cipher.
        """
        if isinstance(data, str):
            data = data.encode('utf-8')
            
        encrypt_mode = (mode == "encrypt")
        result = bytearray()
        
        # Process the data in 16-byte (128-bit) chunks
        for i in range(0, len(data), 16):
            chunk = data[i:i+16]
            processed_chunk = self._process_block(chunk, encrypt_mode)
            result.extend(processed_chunk)
            
        return bytes(result)

# ==========================================
# Example Usage
# ==========================================
if __name__ == "__main__":
    # 1. Define the secret message and a 128-bit (16-byte) key
    plaintext = "IBM Lucifer 1971" # Exactly 16 bytes
    secret_key = b"A16ByteSecretKey"
    
    print(f"Original Text: '{plaintext}'")
    print(f"Key          : '{secret_key.decode('utf-8')}'\n")
    
    # 2. Initialize the Lucifer cipher
    cipher = LuciferConceptCipher(secret_key)
    
    # 3. Encrypt the message
    encrypted_bytes = cipher.crypt(plaintext, mode="encrypt")
    print(f"Encrypted (Hex): {encrypted_bytes.hex()}")
    
    # 4. Decrypt the message
    decrypted_bytes = cipher.crypt(encrypted_bytes, mode="decrypt")
    decrypted_text = decrypted_bytes.decode('utf-8').rstrip('\x00') # Strip padding if any
    
    print(f"Decrypted Text : '{decrypted_text}'")
    
    # Verify the code works correctly
    assert plaintext == decrypted_text
