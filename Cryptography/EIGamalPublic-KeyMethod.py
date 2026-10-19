import random
import secrets

class ElGamalCrypto:
    """
    An educational implementation of the ElGamal public-key cryptosystem.
    """
    def __init__(self, key_size_bits=512):
        self.public_key, self.private_key = self._generate_keypair(key_size_bits)

    # --- Prime Generation ---

    def _is_prime(self, n, k=5):
        """Miller-Rabin primality test."""
        if n <= 1: return False
        if n <= 3: return True
        if n % 2 == 0: return False
        
        r, d = 0, n - 1
        while d % 2 == 0:
            r += 1
            d //= 2
            
        for _ in range(k):
            a = random.randint(2, n - 2)
            x = pow(a, d, n)
            if x == 1 or x == n - 1:
                continue
            for _ in range(r - 1):
                x = pow(x, 2, n)
                if x == n - 1:
                    break
            else:
                return False
        return True

    def _generate_prime(self, bits):
        """Generates a random prime number of the specified bit length."""
        while True:
            num = random.getrandbits(bits)
            num |= (1 << bits - 1) | 1
            if self._is_prime(num):
                return num

    # --- Key Management ---

    def _generate_keypair(self, bits):
        """Generates the ElGamal public and private keys."""
        # 1. Generate a large prime p
        p = self._generate_prime(bits)
        
        # 2. Choose a generator g (using 2 is common for educational simplicity)
        g = 2 
        
        # 3. Choose a random private key x
        x = secrets.randbelow(p - 3) + 2
        
        # 4. Compute y = g^x mod p
        y = pow(g, x, p)
        
        return ((p, g, y), x)

    # --- Core Cipher ---

    def encrypt(self, plaintext: str, public_key: tuple) -> tuple:
        """
        Encrypts a string message using the provided public key.
        Returns a ciphertext pair (C1, C2).
        """
        p, g, y = public_key
        
        # Convert the string to raw bytes, then to a massive integer
        message_bytes = plaintext.encode('utf-8')
        message_int = int.from_bytes(message_bytes, 'big')
        
        if message_int >= p:
            raise ValueError("Message is too long for this key size. 'p' must be larger than 'M'.")
            
        # 1. Choose a random ephemeral key 'k'
        k = secrets.randbelow(p - 3) + 2
        
        # 2. Compute C1 = g^k mod p
        c1 = pow(g, k, p)
        
        # 3. Compute shared secret S = y^k mod p
        s = pow(y, k, p)
        
        # 4. Compute C2 = (M * S) mod p
        c2 = (message_int * s) % p
        
        return (c1, c2)

    def decrypt(self, ciphertext: tuple, private_key: int, public_key: tuple) -> str:
        """
        Decrypts the ciphertext pair (C1, C2) using the private key.
        """
        c1, c2 = ciphertext
        p, g, y = public_key
        x = private_key
        
        # 1. Recreate the shared secret S = C1^x mod p
        s = pow(c1, x, p)
        
        # 2. Find the modular multiplicative inverse of S
        # Python 3.8+ supports pow(base, -1, mod) for modular inverse
        s_inv = pow(s, -1, p)
        
        # 3. Recover the original message M = (C2 * s_inv) mod p
        message_int = (c2 * s_inv) % p
        
        # Convert the massive integer back to bytes, then to a string
        byte_length = (message_int.bit_length() + 7) // 8
        message_bytes = message_int.to_bytes(byte_length, 'big')
        
        return message_bytes.decode('utf-8')


# ==========================================
# Example Usage
# ==========================================
if __name__ == "__main__":
    print("Generating ElGamal keypair (this may take a moment)...")
    # Initialize ElGamal with a 512-bit prime
    elgamal = ElGamalCrypto(key_size_bits=512)
    
    pub_p, pub_g, pub_y = elgamal.public_key
    priv_x = elgamal.private_key
    
    print("\n--- Public Key (Share freely) ---")
    print(f"Prime (p)    : {hex(pub_p)[:40]}... (truncated)")
    print(f"Generator (g): {pub_g}")
    print(f"Value (y)    : {hex(pub_y)[:40]}... (truncated)")
    
    print("\n--- Private Key (Keep secret) ---")
    print(f"Value (x)    : {hex(priv_x)[:40]}... (truncated)\n")
    
    # Define the secret message
    message = "ElGamal relies on the Discrete Logarithm Problem!"
    print(f"Original Text: '{message}'\n")
    
    # Encrypt the message twice to demonstrate probabilistic encryption
    ciphertext_A = elgamal.encrypt(message, elgamal.public_key)
    ciphertext_B = elgamal.encrypt(message, elgamal.public_key)
    
    print("--- Encryption A ---")
    print(f"C1: {str(ciphertext_A[0])[:30]}...")
    print(f"C2: {str(ciphertext_A[1])[:30]}...\n")
    
    print("--- Encryption B (Same message, different ephemeral key) ---")
    print(f"C1: {str(ciphertext_B[0])[:30]}...")
    print(f"C2: {str(ciphertext_B[1])[:30]}...\n")
    
    # Decrypt the first ciphertext
    decrypted_message = elgamal.decrypt(ciphertext_A, elgamal.private_key, elgamal.public_key)
    print(f"Decrypted Text: '{decrypted_message}'")
    
    assert message == decrypted_message
