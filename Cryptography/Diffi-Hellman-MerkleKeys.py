import secrets

class DiffieHellmanEntity:
    """
    Represents a participant in a Diffie-Hellman Key Exchange.
    """
    def __init__(self, p: int, g: int):
        self.p = p
        self.g = g
        # Generate a private key: a random integer between 2 and p-2
        # Using the secrets module for cryptographic randomness
        self.__private_key = secrets.randbelow(p - 3) + 2
        
    def generate_public_key(self) -> int:
        """
        Calculates A = g^a mod p (or B = g^b mod p)
        """
        return pow(self.g, self.__private_key, self.p)
        
    def compute_shared_secret(self, received_public_key: int) -> int:
        """
        Calculates S = B^a mod p (or A^b mod p)
        """
        return pow(received_public_key, self.__private_key, self.p)

# ==========================================
# Example Usage
# ==========================================
if __name__ == "__main__":
    # 1. Public Parameters (Usually standardized, e.g., RFC 3526)
    # For this example, we use a small prime so the output is readable.
    # In reality, 'p' would be 2048 or 4096 bits long.
    prime_p = 0xFFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD1
    generator_g = 2
    
    print(f"Public Prime (p): {hex(prime_p)}")
    print(f"Generator (g)   : {generator_g}\n")
    
    # 2. Initialization
    alice = DiffieHellmanEntity(prime_p, generator_g)
    bob = DiffieHellmanEntity(prime_p, generator_g)
    
    # 3. Public Key Exchange (This happens over the public internet)
    alice_public = alice.generate_public_key()
    bob_public = bob.generate_public_key()
    
    print("--- Intercepted over public channel ---")
    print(f"Alice's Public Key: {hex(alice_public)}")
    print(f"Bob's Public Key  : {hex(bob_public)}")
    print("---------------------------------------\n")
    
    # 4. Shared Secret Computation (Done offline locally by each party)
    alice_shared_secret = alice.compute_shared_secret(bob_public)
    bob_shared_secret = bob.compute_shared_secret(alice_public)
    
    print(f"Alice's Computed Secret: {hex(alice_shared_secret)}")
    print(f"Bob's Computed Secret  : {hex(bob_shared_secret)}\n")
    
    # 5. Verification
    if alice_shared_secret == bob_shared_secret:
        print("Success! Both parties derived the exact same shared secret.")
        # In a real application, you would pass this secret through a Key Derivation 
        # Function (like HKDF) to generate a clean AES key.
    else:
        print("Error: Shared secrets do not match.")
