import secrets
import string

class LinearCongruentialGenerator:
    """
    A basic Pseudo-Random Number Generator (PRNG) using the LCG algorithm.
    WARNING: This is strictly for educational purposes and is NOT cryptographically secure.
    """
    def __init__(self, seed, a=1664525, c=1013904223, m=2**32):
        # The constants default to the values used in Numerical Recipes.
        self.state = seed
        self.a = a
        self.c = c
        self.m = m

    def next_integer(self):
        """Generates the next random integer in the sequence."""
        self.state = (self.a * self.state + self.c) % self.m
        return self.state

    def next_float(self):
        """Generates a random float between 0.0 and 1.0."""
        return self.next_integer() / self.m

    def choice(self, sequence):
        """Picks a random element from a sequence."""
        if not sequence:
            raise IndexError("Cannot choose from an empty sequence")
        index = self.next_integer() % len(sequence)
        return sequence[index]

# ==========================================
# Example Usage
# ==========================================
if __name__ == "__main__":
    print("--- 1. Insecure PRNG (Linear Congruential Generator) ---")
    # Initialize the generator with a seed value (e.g., 42)
    # If you use the same seed, you will get the exact same sequence of numbers.
    lcg = LinearCongruentialGenerator(seed=42)
    
    print(f"Random Int 1: {lcg.next_integer()}")
    print(f"Random Int 2: {lcg.next_integer()}")
    print(f"Random Float: {lcg.next_float():.6f}")
    
    items = ["Apple", "Banana", "Cherry", "Date"]
    print(f"Random Choice: {lcg.choice(items)}\n")

    print("--- 2. Cryptographically Secure PRNG (Python 'secrets') ---")
    # For cybersecurity applications, ALWAYS use the 'secrets' module or 'os.urandom'.
    # It draws entropy from the operating system (e.g., /dev/urandom on Linux).
    
    # Generate a secure 32-byte hexadecimal token (useful for API keys, session IDs)
    secure_token = secrets.token_hex(32)
    print(f"Secure Token: {secure_token}")
    
    # Generate a secure random password
    alphabet = string.ascii_letters + string.digits + string.punctuation
    secure_password = ''.join(secrets.choice(alphabet) for _ in range(16))
    print(f"Secure Password: {secure_password}")
