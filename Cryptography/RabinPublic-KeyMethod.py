import random

class RabinCrypto:
    """
    An educational implementation of the Rabin public-key cryptosystem.
    Includes a padding scheme to resolve the 4-root decryption ambiguity.
    """
    # A magic 4-byte suffix used to identify the correct plaintext root
    PADDING_SUFFIX = b'\xAB\xCD\xEF\x99'

    def __init__(self, key_size_bits=512):
        self.public_key, self.private_key = self._generate_keypair(key_size_bits)

    # --- Prime Generation & Math ---

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

    def _generate_blum_prime(self, bits):
        """
        Generates a prime number p such that p ≡ 3 (mod 4).
        This specific property makes calculating modular square roots much faster.
        """
        while True:
            num = random.getrandbits(bits)
            num |= (1 << bits - 1) | 1
            # Check the modulo condition before running the expensive primality test
            if num % 4 == 3 and self._is_prime(num):
                return num

    def _extended_gcd(self, a, b):
        """
        Extended Euclidean Algorithm.
        Returns (gcd, x, y) such that a*x + b*y = gcd.
        """
        if a == 0:
            return (b, 0, 1)
        else:
            gcd, x, y = self._extended_gcd(b % a, a)
            return (gcd, y - (b // a) * x, x)

    # --- Key Management ---

    def _generate_keypair(self, bits):
        """Generates the Rabin public and private keys."""
        p = self._generate_blum_prime(bits)
        q = self._generate_blum_prime(bits)
        
        n = p * q
        
        # Public Key: n
        # Private Key: (p, q)
        return (n, (p, q))

    # --- Core Cipher ---

    def encrypt(self, plaintext: str, public_key: int) -> int:
        """
        Encrypts a string message using the Rabin cryptosystem.
        C = M^2 mod n
        """
        n = public_key
        
        # Convert string to bytes, then append our verification padding
        message_bytes = plaintext.encode('utf-8') + self.PADDING_SUFFIX
        message_int = int.from_bytes(message_bytes, 'big')
        
        if message_int >= n:
            raise ValueError("Message is too long for this Rabin key size.")
            
        # Encryption is simply squaring the message modulo n
        ciphertext_int = pow(message_int, 2, n)
        return ciphertext_int

    def decrypt(self, ciphertext: int, private_key: tuple) -> str:
        """
        Decrypts the ciphertext using the private key.
        Yields 4 roots, filters them using the padding, and returns the original string.
        """
        p, q = private_key
        n = p * q
        
        # 1. Calculate the square roots modulo p and q
        # Because p, q ≡ 3 (mod 4), the formula is C^((p+1)/4) mod p
        mp = pow(ciphertext, (p + 1) // 4, p)
        mq = pow(ciphertext, (q + 1) // 4, q)
        
        # 2. Use Extended Euclidean Algorithm to find yp, yq where yp*p + yq*q = 1
        _, yp, yq = self._extended_gcd(p, q)
        
        # 3. Use the Chinese Remainder Theorem to find the 4 possible roots
        r1 = (yp * p * mq + yq * q * mp) % n
        r2 = n - r1
        r3 = (yp * p * mq - yq * q * mp) % n
        r4 = n - r3
        
        possible_roots = [r1, r2, r3, r4]
        
        # 4. Find the root that contains our padding suffix
        for root in possible_roots:
            try:
                # Convert the massive integer back to bytes
                byte_length = (root.bit_length() + 7) // 8
                root_bytes = root.to_bytes(byte_length, 'big')
                
                # Check if it ends with our magic padding
                if root_bytes.endswith(self.PADDING_SUFFIX):
                    # Strip the padding and decode
                    original_bytes = root_bytes[:-len(self.PADDING_SUFFIX)]
                    return original_bytes.decode('utf-8')
            except UnicodeDecodeError:
                continue
                
        raise ValueError("Decryption failed: None of the 4 roots contained valid padding.")


# ==========================================
# Example Usage
# ==========================================
if __name__ == "__main__":
    print("Generating Rabin keypair (this may take a moment)...")
    # Initialize Rabin with a 1024-bit modulus (2x 512-bit primes)
    rabin = RabinCrypto(key_size_bits=512)
    
    pub_n = rabin.public_key
    priv_p, priv_q = rabin.private_key
    
    print("\n--- Public Key (Share freely) ---")
    print(f"Modulus (n): {hex(pub_n)[:40]}... (truncated)")
    
    print("\n--- Private Key (Keep secret) ---")
    print(f"Prime (p)  : {hex(priv_p)[:40]}... (truncated)")
    print(f"Prime (q)  : {hex(priv_q)[:40]}... (truncated)\n")
    
    # Define the secret message
    message = "Rabin encryption squares the padded message modulo n!"
    print(f"Original Text : '{message}'")
    
    # Encrypt the message
    ciphertext = rabin.encrypt(message, rabin.public_key)
    print(f"Encrypted Int : {str(ciphertext)[:40]}... (truncated)")
    
    # Decrypt the ciphertext
    decrypted_message = rabin.decrypt(ciphertext, rabin.private_key)
    print(f"Decrypted Text: '{decrypted_message}'")
    
    assert message == decrypted_message
