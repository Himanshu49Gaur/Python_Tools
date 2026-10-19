import hashlib
import struct

class SEALCipher:
    """
    A structural implementation of the SEAL stream cipher concept.
    Demonstrates the heavy key-setup (using SHA-1) and the fast, 
    32-bit word, position-dependent keystream generation.
    """
    def __init__(self, key: bytes):
        if len(key) != 20:
            raise ValueError("SEAL requires exactly a 160-bit (20-byte) key.")
        
        self.key = key
        # Precomputed tables (using 32-bit integers)
        self.T = [] # 512 words
        self.S = [] # 256 words
        self.R = [] # 16 words
        
        self._key_setup()

    def _hash_to_word(self, index: int, table_id: str) -> int:
        """Helper to generate deterministic pseudo-random 32-bit words using SHA-1."""
        hasher = hashlib.sha1()
        hasher.update(self.key)
        hasher.update(table_id.encode('utf-8'))
        hasher.update(index.to_bytes(4, 'big'))
        # Take the first 4 bytes of the hash and convert to a 32-bit integer
        return struct.unpack('>I', hasher.digest()[:4])[0]

    def _key_setup(self):
        """
        Phase 1: Heavy Key Setup.
        Expands the 160-bit key into massive internal tables.
        """
        # Generate T table (512 words)
        for i in range(512):
            self.T.append(self._hash_to_word(i, "T_TABLE"))
            
        # Generate S table (256 words)
        for i in range(256):
            self.S.append(self._hash_to_word(i, "S_TABLE"))
            
        # Generate R table (16 words)
        for i in range(16):
            self.R.append(self._hash_to_word(i, "R_TABLE"))

    def _generate_block(self, position: int) -> bytes:
        """
        Phase 2: Keystream Generation.
        Generates a block of keystream for a specific position index.
        """
        # Initialize the 4 internal 32-bit registers based on the position
        # In actual SEAL, this involves specific XORs with the R table
        A = position ^ self.R[0]
        B = (position >> 8) ^ self.R[1]
        C = (position >> 16) ^ self.R[2]
        D = (position >> 24) ^ self.R[3]
        
        keystream_words = []
        
        # Core SEAL mixing loop (simplified representation of the 32-bit operations)
        for _ in range(4): 
            # Mix A, B, C, D using addition (mod 2^32), XOR, and table lookups
            P = A & 0x7FC # 9-bit mask for T table (which has 512 entries)
            B = (B + self.T[P >> 2]) & 0xFFFFFFFF
            A = (A >> 9) | ((A << 23) & 0xFFFFFFFF) # Right rotation
            
            P = B & 0x3FC # 8-bit mask for S table (which has 256 entries)
            C = (C ^ self.S[P >> 2]) & 0xFFFFFFFF
            B = (B >> 9) | ((B << 23) & 0xFFFFFFFF)
            
            P = C & 0x7FC
            D = (D + self.T[P >> 2]) & 0xFFFFFFFF
            C = (C >> 9) | ((C << 23) & 0xFFFFFFFF)
            
            P = D & 0x3FC
            A = (A ^ self.S[P >> 2]) & 0xFFFFFFFF
            D = (D >> 9) | ((D << 23) & 0xFFFFFFFF)
            
            # Append mixed registers to the keystream
            keystream_words.extend([A, B, C, D])
            
        # Convert the generated 32-bit words into raw bytes
        block_bytes = bytearray()
        for word in keystream_words:
            block_bytes.extend(struct.pack('>I', word))
            
        return bytes(block_bytes)

    def crypt(self, data: bytes) -> bytes:
        """
        Encrypts or decrypts data using the SEAL stream cipher.
        Because it is position-dependent, we generate keystream blocks 
        based on the chunk index and XOR them.
        """
        if isinstance(data, str):
            data = data.encode('utf-8')
            
        result = bytearray()
        block_size = 64 # Our simplified loop generates 16 words (64 bytes) per position
        
        for i in range(0, len(data), block_size):
            # Calculate which block position we are currently in
            position_index = i // block_size
            
            # Generate the specific keystream block for this position
            keystream_block = self._generate_block(position_index)
            
            # Extract the chunk of data to XOR
            data_chunk = data[i : i + block_size]
            
            # XOR the data chunk with the keystream block
            for b1, b2 in zip(data_chunk, keystream_block):
                result.append(b1 ^ b2)
                
        return bytes(result)

# ==========================================
# Example Usage
# ==========================================
if __name__ == "__main__":
    # 1. Define the secret message and a 160-bit (20-byte) key
    plaintext = "SEAL is extremely fast on 32-bit software architectures!"
    # Using SHA-1 to easily generate a valid 20-byte key from a passphrase
    secret_key = hashlib.sha1(b"MySecurePassphrase").digest()
    
    print(f"Original Text: {plaintext}")
    print(f"Key (Hex)    : {secret_key.hex()}\n")
    
    # 2. Initialize the SEAL cipher (Performs heavy table generation)
    cipher = SEALCipher(secret_key)
    
    # 3. Encrypt the message
    encrypted_bytes = cipher.crypt(plaintext)
    print(f"Encrypted (Hex): {encrypted_bytes.hex()}")
    
    # 4. Decrypt the message
    # Stream ciphers using XOR are symmetric; calling crypt() again decrypts it
    decrypted_bytes = cipher.crypt(encrypted_bytes)
    decrypted_text = decrypted_bytes.decode('utf-8')
    
    print(f"Decrypted Text : {decrypted_text}")
    
    # Verify the code works correctly
    assert plaintext == decrypted_text
