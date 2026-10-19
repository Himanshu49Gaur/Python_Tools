import random

class RSACrypto:
    """
    An educational implementation of the RSA public-key cryptosystem.
    """
    def __init__(self, key_size_bits=512):
        # A 512-bit prime pair yields a 1024-bit modulus (n)
        self.public_key, self.private_key = self._generate_keypair(key_size_bits)

    # --- Prime Generation & Math ---

    def _is_prime(self, n, k=5):
        """
        Miller-Rabin primality test.
        Returns True if n is likely prime, False if definitely composite.
        """
        if n <= 1: return False
        if n <= 3: return True
        if n % 2 == 0: return False
        
        # Write n-1 as 2^r * d
        r, d = 0, n - 1
        while d % 2 == 0:
            r += 1
            d //= 2
            
        # Witness loop
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
            # Generate a random odd number of 'bits' length
            num = random.getrandbits(bits)
            # Ensure the highest bit is set (to guarantee bit length) and it's odd
            num |= (1 << bits - 1) | 1
            if self._is_prime(num):
                return num

    def _generate_keypair(self, bits):
        """Generates the public and private RSA keys."""
        p = self._generate_prime(bits)
        q = self._generate_prime(bits)
        
        n = p * q
        phi = (p - 1) * (q - 1)
        
        # 65537 is the standard public exponent (2^16 + 1)
        e = 65537
        
        # Calculate the private exponent 'd' using the modular inverse
        # Python 3.8+ natively supports pow(base, -1, mod) for modular inverse
        d = pow(e, -1, phi)
        
        return ((e, n), (d, n))

    # --- Core Cipher ---

    def encrypt(self, plaintext: str, public_key: tuple) -> int:
        """Encrypts a string message using the provided public key."""
        e, n = public_key
        
        # Convert the string to raw bytes, then to a massive integer
        message_bytes = plaintext.encode('utf-8')
        message_int = int.from_bytes(message_bytes, 'big')
        
        if message_int >= n:
            raise ValueError("Message is too long for this RSA key size.")
            
        # Core RSA Encryption: C = M^e mod n
        ciphertext_int = pow(message_int, e, n)
        return ciphertext_int

    def decrypt(self, ciphertext_int: int, private_key: tuple) -> str:
        """Decrypts the ciphertext integer using the provided private key."""
        d, n = private_key
        
        # Core RSA Decryption: M = C^d mod n
        message_int = pow(ciphertext_int, d, n)
        
        # Convert the massive integer back to bytes, then to a string
        # We calculate the required byte length of the integer
        byte_length = (message_int.bit_length() + 7) // 8
        message_bytes = message_int.to_bytes(byte_length, 'big')
        
        return message_bytes.decode('utf-8')


# ==========================================
# Example Usage
# ==========================================
if __name__ == "__main__":
    # 1. Initialize RSA and generate a 1024-bit keypair (2x 512-bit primes)
    print("Generating RSA keypair (this may take a moment)...")
    rsa = RSACrypto(key_size_bits=512)
    
    pub_e, pub_n = rsa.public_key
    priv_d, priv_n = rsa.private_key
    
    # 2. Display the keys
    print("\n--- Public Key (Share freely) ---")
    print(f"Modulus (n) : {hex(pub_n)[:40]}... (truncated)")
    print(f"Exponent (e): {pub_e}")
    
    print("\n--- Private Key (Keep secret) ---")
    print(f"Exponent (d): {hex(priv_d)[:40]}... (truncated)\n")
    
    # 3. Define the secret message
    message = "Asymmetric cryptography allows secure key exchange!"
    print(f"Original Text : '{message}'")
    
    # 4. Encrypt the message using only the Public Key
    ciphertext = rsa.encrypt(message, rsa.public_key)
    print(f"Encrypted Int : {str(ciphertext)[:40]}... (truncated)")
    
    # 5. Decrypt the ciphertext using the Private Key
    decrypted_message = rsa.decrypt(ciphertext, rsa.private_key)
    print(f"Decrypted Text: '{decrypted_message}'")
    
    assert message == decrypted_message
