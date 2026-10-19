import struct

class IDEA:
    """
    Implementation of the International Data Encryption Algorithm (IDEA).
    Operates on 64-bit blocks using a 128-bit key.
    """
    def __init__(self, key: bytes):
        if len(key) != 16:
            raise ValueError("IDEA requires exactly a 128-bit (16-byte) key.")
            
        self.encrypt_subkeys = self._generate_subkeys(key)
        self.decrypt_subkeys = self._invert_subkeys(self.encrypt_subkeys)

    # --- Core Mathematical Operations (16-bit) ---

    @staticmethod
    def _add(a: int, b: int) -> int:
        """Addition modulo 2^16."""
        return (a + b) & 0xFFFF

    @staticmethod
    def _mul(a: int, b: int) -> int:
        """
        Multiplication modulo (2^16 + 1).
        In IDEA, 0 is treated as 2^16.
        """
        if a == 0:
            a = 0x10000
        if b == 0:
            b = 0x10000
            
        result = (a * b) % 0x10001
        
        # If the result is 2^16, map it back to 0 for a 16-bit word
        if result == 0x10000:
            return 0
        return result

    @staticmethod
    def _mul_inv(a: int) -> int:
        """
        Calculates the multiplicative inverse modulo (2^16 + 1)
        using the Extended Euclidean Algorithm.
        """
        if a == 0:
            return 0
            
        m0 = 0x10001
        y = 0
        x = 1
        
        while a > 1:
            q = a // m0
            t = m0
            
            m0 = a % m0
            a = t
            t = y
            
            y = x - q * y
            x = t
            
        if x < 0:
            x += 0x10001
            
        return x

    @staticmethod
    def _add_inv(a: int) -> int:
        """Calculates the additive inverse modulo 2^16."""
        return (0x10000 - a) & 0xFFFF

    # --- Key Scheduling ---

    def _generate_subkeys(self, key: bytes):
        """Generates 52 16-bit subkeys for encryption."""
        # Start with the 128-bit key as an integer
        key_int = int.from_bytes(key, 'big')
        subkeys = []
        
        # IDEA requires 52 subkeys (8 rounds * 6 keys + 4 keys for the half round)
        while len(subkeys) < 52:
            # Extract eight 16-bit words from the current 128-bit key
            for i in range(7, -1, -1):
                subkeys.append((key_int >> (i * 16)) & 0xFFFF)
                
            # Shift the 128-bit key left by 25 bits (circular shift)
            key_int = ((key_int << 25) | (key_int >> (128 - 25))) & ((1 << 128) - 1)
            
        return subkeys[:52]

    def _invert_subkeys(self, keys: list):
        """
        Generates 52 decryption subkeys by calculating mathematical inverses
        and reversing the order.
        """
        dec_keys = [0] * 52
        
        # The half-round (Round 9) keys become the first decryption keys
        dec_keys[0] = self._mul_inv(keys[48])
        dec_keys[1] = self._add_inv(keys[49])
        dec_keys[2] = self._add_inv(keys[50])
        dec_keys[3] = self._mul_inv(keys[51])
        
        # The 8 full rounds in reverse
        for i in range(1, 9):
            idx1 = i * 6
            idx2 = 54 - idx1
            
            # The XOR keys for the inner structure remain identical
            dec_keys[idx1 - 2] = keys[idx2 - 4]
            dec_keys[idx1 - 1] = keys[idx2 - 3]
            
            dec_keys[idx1] = self._mul_inv(keys[idx2 - 6])
            
            # Note: The inner addition keys (2 and 3) swap places for rounds 1-7
            if i < 8:
                dec_keys[idx1 + 1] = self._add_inv(keys[idx2 - 4])
                dec_keys[idx1 + 2] = self._add_inv(keys[idx2 - 5])
            else:
                dec_keys[idx1 + 1] = self._add_inv(keys[idx2 - 5])
                dec_keys[idx1 + 2] = self._add_inv(keys[idx2 - 4])
                
            dec_keys[idx1 + 3] = self._mul_inv(keys[idx2 - 3])
            
        return dec_keys

    # --- Core Cipher ---

    def _process_block(self, block: bytes, subkeys: list) -> bytes:
        """Processes a 64-bit block through the 8.5 rounds of IDEA."""
        # Unpack 64-bit block into four 16-bit quarters (X1, X2, X3, X4)
        X1, X2, X3, X4 = struct.unpack('>HHHH', block)
        
        k_idx = 0
        
        # 8 Full Rounds
        for _ in range(8):
            # Step 1: Multiply X1 and K1
            step1 = self._mul(X1, subkeys[k_idx]); k_idx += 1
            # Step 2: Add X2 and K2
            step2 = self._add(X2, subkeys[k_idx]); k_idx += 1
            # Step 3: Add X3 and K3
            step3 = self._add(X3, subkeys[k_idx]); k_idx += 1
            # Step 4: Multiply X4 and K4
            step4 = self._mul(X4, subkeys[k_idx]); k_idx += 1
            
            # Step 5: XOR Step 1 and Step 3
            step5 = step1 ^ step3
            # Step 6: XOR Step 2 and Step 4
            step6 = step2 ^ step4
            
            # Step 7: Multiply Step 5 by K5
            step7 = self._mul(step5, subkeys[k_idx]); k_idx += 1
            # Step 8: Add Step 6 and Step 7
            step8 = self._add(step6, step7)
            # Step 9: Multiply Step 8 by K6
            step9 = self._mul(step8, subkeys[k_idx]); k_idx += 1
            # Step 10: Add Step 7 and Step 9
            step10 = self._add(step7, step9)
            
            # Step 11-14: Update quarters for the next round (with swap of middle two)
            X1 = step1 ^ step9
            X2 = step3 ^ step9
            X3 = step2 ^ step10
            X4 = step4 ^ step10
            
        # Half Round (Final Transformation)
        out1 = self._mul(X1, subkeys[k_idx]); k_idx += 1
        out2 = self._add(X3, subkeys[k_idx]); k_idx += 1 # Note: X2 and X3 are swapped back
        out3 = self._add(X2, subkeys[k_idx]); k_idx += 1
        out4 = self._mul(X4, subkeys[k_idx])
        
        # Pack the 16-bit quarters back into a 64-bit byte string
        return struct.pack('>HHHH', out1, out2, out3, out4)

    def crypt(self, data: bytes, mode: str = "encrypt") -> bytes:
        """Encrypts or decrypts data using Electronic Codebook (ECB) mode."""
        if isinstance(data, str):
            data = data.encode('utf-8')
            
        encrypt_mode = (mode == "encrypt")
        keys = self.encrypt_subkeys if encrypt_mode else self.decrypt_subkeys
        
        result = bytearray()
        
        # Pad data to 8 bytes (64 bits)
        if encrypt_mode and len(data) % 8 != 0:
            pad_len = 8 - (len(data) % 8)
            data += bytes([pad_len] * pad_len)
            
        for i in range(0, len(data), 8):
            chunk = data[i:i+8]
            processed_chunk = self._process_block(chunk, keys)
            result.extend(processed_chunk)
            
        if not encrypt_mode:
            pad_len = result[-1]
            if 0 < pad_len <= 8:
                result = result[:-pad_len]
                
        return bytes(result)

# ==========================================
# Example Usage
# ==========================================
if __name__ == "__main__":
    # 1. Define the secret message and a 128-bit (16-byte) key
    plaintext = "Secure email via PGP and IDEA!"
    secret_key = b"A16ByteSecretKey"
    
    print(f"Original Text: '{plaintext}'")
    print(f"Key          : '{secret_key.decode('utf-8')}'\n")
    
    # 2. Initialize IDEA
    cipher = IDEA(secret_key)
    
    # 3. Encrypt the message
    encrypted_bytes = cipher.crypt(plaintext, mode="encrypt")
    print(f"Encrypted (Hex): {encrypted_bytes.hex()}")
    
    # 4. Decrypt the message
    decrypted_bytes = cipher.crypt(encrypted_bytes, mode="decrypt")
    decrypted_text = decrypted_bytes.decode('utf-8')
    
    print(f"Decrypted Text : '{decrypted_text}'")
    
    assert plaintext == decrypted_text
