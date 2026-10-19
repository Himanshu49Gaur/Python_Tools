import struct
import hashlib

class EducationalBlowfish:
    """
    A structural implementation of the Blowfish block cipher.
    Note: To avoid 400+ lines of Pi constants, the initial state is generated
    deterministically using a hash function. The key setup and Feistel loops 
    are mathematically authentic to Schneier's algorithm.
    """
    def __init__(self, key: bytes):
        if not (4 <= len(key) <= 56):
            raise ValueError("Blowfish key must be between 4 and 56 bytes (32 to 448 bits).")
            
        # 1. Initialize P-array (18 words) and S-boxes (4 x 256 words)
        # In real Blowfish, these are the fractional digits of Pi.
        self.P = []
        self.S = [[0] * 256 for _ in range(4)]
        self._initialize_state_without_pi()
        
        # 2. Key Expansion (The core of Blowfish's strength)
        self._expand_key(key)

    def _initialize_state_without_pi(self):
        """Generates pseudo-random 32-bit integers to simulate Pi initialization."""
        counter = 0
        def get_next_word():
            nonlocal counter
            h = hashlib.sha256(counter.to_bytes(4, 'big')).digest()
            counter += 1
            return struct.unpack('>I', h[:4])[0]
            
        self.P = [get_next_word() for _ in range(18)]
        for i in range(4):
            for j in range(256):
                self.S[i][j] = get_next_word()

    def _expand_key(self, key: bytes):
        """
        The Blowfish Key Schedule.
        Mutates the P-array and S-boxes using the secret key.
        """
        key_len = len(key)
        
        # Step 1: XOR P-array with the key (cycling through the key if necessary)
        for i in range(18):
            # Extract 4 bytes from the key, wrapping around
            k_word = 0
            for j in range(4):
                k_word = (k_word << 8) | key[(i * 4 + j) % key_len]
            self.P[i] ^= k_word

        # Step 2: Encrypt the all-zero block 521 times to replace all P and S arrays
        L, R = 0, 0
        
        # Replace P-array
        for i in range(0, 18, 2):
            L, R = self._encrypt_block(L, R)
            self.P[i] = L
            self.P[i+1] = R
            
        # Replace S-boxes
        for i in range(4):
            for j in range(0, 256, 2):
                L, R = self._encrypt_block(L, R)
                self.S[i][j] = L
                self.S[i][j+1] = R

    def _f_function(self, x: int) -> int:
        """
        The Blowfish F-Function.
        Splits the 32-bit input into four 8-bit quarters and passes them through the S-boxes.
        """
        # Extract 8-bit chunks
        a = (x >> 24) & 0xFF
        b = (x >> 16) & 0xFF
        c = (x >> 8) & 0xFF
        d = x & 0xFF
        
        # Calculate: F(x) = (((S1[a] + S2[b]) ^ S3[c]) + S4[d]) mod 2^32
        res = (self.S[0][a] + self.S[1][b]) % (2**32)
        res ^= self.S[2][c]
        res = (res + self.S[3][d]) % (2**32)
        
        return res

    def _encrypt_block(self, L: int, R: int):
        """Encrypts a 64-bit block (provided as two 32-bit halves)."""
        for i in range(16):
            L ^= self.P[i]
            R ^= self._f_function(L)
            # Swap L and R
            L, R = R, L
            
        # Undo the last swap
        L, R = R, L
        
        # Final XOR with the last two P-array entries
        R ^= self.P[16]
        L ^= self.P[17]
        
        return L, R

    def _decrypt_block(self, L: int, R: int):
        """Decrypts a 64-bit block (provided as two 32-bit halves)."""
        for i in range(17, 1, -1):
            L ^= self.P[i]
            R ^= self._f_function(L)
            L, R = R, L
            
        L, R = R, L
        
        R ^= self.P[1]
        L ^= self.P[0]
        
        return L, R

    def crypt(self, data: bytes, mode: str = "encrypt") -> bytes:
        """Encrypts or decrypts arbitrary data in Electronic Codebook (ECB) mode."""
        if isinstance(data, str):
            data = data.encode('utf-8')
            
        encrypt_mode = (mode == "encrypt")
        result = bytearray()
        
        # Pad data to a multiple of 8 bytes (64 bits)
        if encrypt_mode and len(data) % 8 != 0:
            padding_len = 8 - (len(data) % 8)
            data += bytes([padding_len] * padding_len)
            
        for i in range(0, len(data), 8):
            chunk = data[i:i+8]
            L, R = struct.unpack('>II', chunk)
            
            if encrypt_mode:
                out_L, out_R = self._encrypt_block(L, R)
            else:
                out_L, out_R = self._decrypt_block(L, R)
                
            result.extend(struct.pack('>II', out_L, out_R))
            
        # If decrypting, strip padding
        if not encrypt_mode:
            pad_len = result[-1]
            if 0 < pad_len <= 8:
                result = result[:-pad_len]
                
        return bytes(result)

# ==========================================
# Example Usage
# ==========================================
if __name__ == "__main__":
    # 1. Define the secret message and a key (up to 56 bytes)
    plaintext = "Blowfish is highly resistant to brute force!"
    secret_key = b"Schneier1993"
    
    print(f"Original Text: '{plaintext}'")
    print(f"Key          : '{secret_key.decode('utf-8')}'\n")
    
    # 2. Initialize Blowfish (This runs the heavy key expansion)
    print("Initializing key-dependent S-boxes...")
    cipher = EducationalBlowfish(secret_key)
    
    # 3. Encrypt the message
    encrypted_bytes = cipher.crypt(plaintext, mode="encrypt")
    print(f"Encrypted (Hex): {encrypted_bytes.hex()}")
    
    # 4. Decrypt the message
    decrypted_bytes = cipher.crypt(encrypted_bytes, mode="decrypt")
    decrypted_text = decrypted_bytes.decode('utf-8')
    
    print(f"Decrypted Text : '{decrypted_text}'")
    
    assert plaintext == decrypted_text
