import struct

class RC5:
    """
    Implementation of the RC5-32/12/b Block Cipher.
    - Word size (w): 32 bits (Block size is 64 bits)
    - Rounds (r): 12
    - Key size (b): Variable length up to 255 bytes
    """
    def __init__(self, key: bytes):
        self.w = 32
        self.r = 12
        self.b = len(key)
        self.mod = 2 ** self.w
        self.mask = self.mod - 1
        
        # Magic constants for w = 32
        # Derived from odd((e-2)*2^32) and odd((phi-1)*2^32)
        self.P = 0xB7E15163
        self.Q = 0x9E3779B9
        
        self.S = self._key_expansion(key)

    def _left_rotate(self, val: int, shift: int) -> int:
        """Circular left shift (rotation) for a 32-bit word."""
        # Only the lower 5 bits (log2(32)) of the shift amount are used
        shift = shift & (self.w - 1)
        return ((val << shift) & self.mask) | (val >> (self.w - shift))

    def _right_rotate(self, val: int, shift: int) -> int:
        """Circular right shift (rotation) for a 32-bit word."""
        shift = shift & (self.w - 1)
        return (val >> shift) | ((val << (self.w - shift)) & self.mask)

    def _key_expansion(self, key: bytes):
        """Expands the variable-length key into a subkey array S."""
        # 1. Convert the secret key from bytes to an array of 32-bit words (L)
        # Pad with zeros so the byte length is a multiple of 4 (w / 8)
        u = self.w // 8
        b_padded = key + b'\x00' * ((u - len(key) % u) % u)
        
        c = len(b_padded) // u
        if c == 0:
            c = 1
            b_padded = b'\x00' * u
            
        L = [0] * c
        for i in range(len(b_padded)):
            L[i // u] = (L[i // u] + (b_padded[i] << (8 * (i % u)))) & self.mask

        # 2. Initialize the S array with the magic constants
        t = 2 * (self.r + 1)
        S = [0] * t
        S[0] = self.P
        for i in range(1, t):
            S[i] = (S[i-1] + self.Q) & self.mask

        # 3. Mix in the user's secret key (L) to the S array
        i = j = 0
        A = B = 0
        
        # Mix 3 * max(t, c) times
        iterations = 3 * max(t, c)
        for _ in range(iterations):
            A = S[i] = self._left_rotate((S[i] + A + B) & self.mask, 3)
            B = L[j] = self._left_rotate((L[j] + A + B) & self.mask, (A + B))
            i = (i + 1) % t
            j = (j + 1) % c
            
        return S

    def _encrypt_block(self, block: bytes) -> bytes:
        """Encrypts a single 64-bit block."""
        A, B = struct.unpack('<II', block)
        
        A = (A + self.S[0]) & self.mask
        B = (B + self.S[1]) & self.mask
        
        for i in range(1, self.r + 1):
            A = (self._left_rotate((A ^ B), B) + self.S[2 * i]) & self.mask
            B = (self._left_rotate((B ^ A), A) + self.S[2 * i + 1]) & self.mask
            
        return struct.pack('<II', A, B)

    def _decrypt_block(self, block: bytes) -> bytes:
        """Decrypts a single 64-bit block."""
        A, B = struct.unpack('<II', block)
        
        for i in range(self.r, 0, -1):
            B = (self._right_rotate((B - self.S[2 * i + 1]) & self.mask, A)) ^ A
            A = (self._right_rotate((A - self.S[2 * i]) & self.mask, B)) ^ B
            
        A = (A - self.S[0]) & self.mask
        B = (B - self.S[1]) & self.mask
        
        return struct.pack('<II', A, B)

    def crypt(self, data: bytes, mode: str = "encrypt") -> bytes:
        """Encrypts or decrypts arbitrary data in Electronic Codebook (ECB) mode."""
        if isinstance(data, str):
            data = data.encode('utf-8')
            
        encrypt_mode = (mode == "encrypt")
        result = bytearray()
        
        # The block size is 8 bytes (64 bits)
        block_size = 8
        
        # Pad data if encrypting
        if encrypt_mode and len(data) % block_size != 0:
            pad_len = block_size - (len(data) % block_size)
            data += bytes([pad_len] * pad_len)
            
        for i in range(0, len(data), block_size):
            chunk = data[i:i+block_size]
            if encrypt_mode:
                result.extend(self._encrypt_block(chunk))
            else:
                result.extend(self._decrypt_block(chunk))
                
        # Strip padding if decrypting
        if not encrypt_mode:
            pad_len = result[-1]
            if 0 < pad_len <= block_size:
                result = result[:-pad_len]
                
        return bytes(result)

# ==========================================
# Example Usage
# ==========================================
if __name__ == "__main__":
    # 1. Define the secret message and a key (RC5 accepts variable key lengths)
    plaintext = "Data-dependent rotations make RC5 unique!"
    secret_key = b"Rivest1994"
    
    print(f"Original Text: '{plaintext}'")
    print(f"Key          : '{secret_key.decode('utf-8')}'\n")
    
    # 2. Initialize RC5 (Handles key expansion)
    cipher = RC5(secret_key)
    
    # 3. Encrypt the message
    encrypted_bytes = cipher.crypt(plaintext, mode="encrypt")
    print(f"Encrypted (Hex): {encrypted_bytes.hex()}")
    
    # 4. Decrypt the message
    decrypted_bytes = cipher.crypt(encrypted_bytes, mode="decrypt")
    decrypted_text = decrypted_bytes.decode('utf-8')
    
    print(f"Decrypted Text : '{decrypted_text}'")
    
    assert plaintext == decrypted_text
