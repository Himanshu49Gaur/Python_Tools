import secrets

class Secp256k1Curve:
    """
    An educational implementation of Elliptic Curve cryptography math.
    Uses the exact parameters of the secp256k1 curve (Bitcoin's curve).
    y^2 = x^3 + 7 (mod p)
    """
    # 1. Curve Parameters
    P = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F # Prime field
    A = 0
    B = 7
    
    # 2. Base Point (Generator G)
    G_X = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
    G_Y = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
    G = (G_X, G_Y)
    
    # 3. Order of the curve (Maximum number of points)
    N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

    def point_addition(self, P1, P2):
        """
        Adds two points on the elliptic curve.
        """
        # If either point is at infinity (None), return the other
        if P1 is None: return P2
        if P2 is None: return P1

        x1, y1 = P1
        x2, y2 = P2

        # If points are vertically aligned, they cancel out to infinity
        if x1 == x2 and y1 != y2:
            return None

        # Calculate the slope (m) of the line intersecting the points
        if x1 == x2:
            # Point doubling (tangent line)
            # m = (3x^2 + a) / (2y) mod p
            numerator = (3 * x1 * x1 + self.A) % self.P
            denominator = (2 * y1) % self.P
        else:
            # Standard addition (secant line)
            # m = (y2 - y1) / (x2 - x1) mod p
            numerator = (y2 - y1) % self.P
            denominator = (x2 - x1) % self.P

        # Modular inverse of the denominator (requires Python 3.8+)
        inv_denominator = pow(denominator, -1, self.P)
        m = (numerator * inv_denominator) % self.P

        # Calculate the new point
        x3 = (m * m - x1 - x2) % self.P
        y3 = (m * (x1 - x3) - y1) % self.P

        return (x3, y3)

    def scalar_multiplication(self, k, point):
        """
        Multiplies a point by an integer k using the "Double-and-Add" algorithm.
        This is the core of ECC, allowing O(log k) computation time.
        """
        result = None # Point at infinity
        addend = point

        while k > 0:
            if k & 1: # If the current lowest bit is 1
                result = self.point_addition(result, addend)
            addend = self.point_addition(addend, addend) # Double the point
            k >>= 1 # Shift right to process the next bit

        return result


class ECDHParticipant:
    """
    Represents a user engaging in Elliptic Curve Diffie-Hellman Key Exchange.
    """
    def __init__(self):
        self.curve = Secp256k1Curve()
        # Private key is a random integer between 1 and the curve's order (N)
        self.__private_key = secrets.randbelow(self.curve.N - 1) + 1
        
        # Public key is Private Key * Generator Point
        self.public_key = self.curve.scalar_multiplication(self.__private_key, self.curve.G)

    def compute_shared_secret(self, received_public_key):
        """
        Computes the shared secret by multiplying the received public key
        by this participant's private key.
        """
        # Shared Secret = Private Key * Other's Public Point
        shared_point = self.curve.scalar_multiplication(self.__private_key, received_public_key)
        
        # In ECDH, the X-coordinate of the resulting point is used as the shared secret
        return shared_point[0]


# ==========================================
# Example Usage
# ==========================================
if __name__ == "__main__":
    print("Initializing ECDH over secp256k1...\n")
    
    # 1. Alice and Bob generate their private and public keys
    alice = ECDHParticipant()
    bob = ECDHParticipant()
    
    # 2. The public keys are exchanged over the open internet. 
    # They are represented as (X, Y) coordinates on the curve.
    print("--- Public Key Exchange ---")
    print(f"Alice's Public Key (X): {hex(alice.public_key[0])[:30]}...")
    print(f"Bob's Public Key (X)  : {hex(bob.public_key[0])[:30]}...\n")
    
    # 3. Both parties independently compute the shared secret
    # Alice multiplies Bob's public point by her private key
    alice_shared_secret = alice.compute_shared_secret(bob.public_key)
    
    # Bob multiplies Alice's public point by his private key
    bob_shared_secret = bob.compute_shared_secret(alice.public_key)
    
    print("--- Shared Secret Calculation ---")
    print(f"Alice derives secret: {hex(alice_shared_secret)}")
    print(f"Bob derives secret  : {hex(bob_shared_secret)}\n")
    
    # 4. Verification
    if alice_shared_secret == bob_shared_secret:
        print("Success! Both parties derived the exact same shared secret.")
        print("This 256-bit integer can now be hashed and used as an AES key.")
    else:
        print("Error: Shared secrets do not match.")
