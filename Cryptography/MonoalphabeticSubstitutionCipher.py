import string
import random

def generate_substitution_key():
    """
    Generates a random 26-letter key consisting of shuffled lowercase letters.
    """
    alphabet = list(string.ascii_lowercase)
    random.shuffle(alphabet)
    return ''.join(alphabet)

def encrypt_monoalphabetic(plaintext, key):
    """
    Encrypts a message using a monoalphabetic substitution cipher.
    """
    standard_alphabet = string.ascii_lowercase
    
    # Create a mapping for both lowercase and uppercase letters
    # Example: 'a' -> key[0], 'b' -> key[1], 'A' -> key[0].upper(), etc.
    cipher_map = str.maketrans(
        standard_alphabet + standard_alphabet.upper(),
        key + key.upper()
    )
    
    # Translate the characters; non-alphabetical characters remain unchanged
    return plaintext.translate(cipher_map)

def decrypt_monoalphabetic(ciphertext, key):
    """
    Decrypts a message that was encrypted with a monoalphabetic substitution cipher.
    """
    standard_alphabet = string.ascii_lowercase
    
    # Create the reverse mapping from the key back to the standard alphabet
    reverse_map = str.maketrans(
        key + key.upper(),
        standard_alphabet + standard_alphabet.upper()
    )
    
    return ciphertext.translate(reverse_map)

# ==========================================
# Example Usage
# ==========================================
if __name__ == "__main__":
    # 1. Define the secret message
    original_message = "Security Assessment: Vulnerability found in the mainframe!"
    print(f"Original Text: {original_message}\n")

    # 2. Generate a random key (or you could provide a static 26-character string)
    # Example static key: "qwertyuiopasdfghjklzxcvbnm"
    secret_key = generate_substitution_key()
    print(f"Standard Alphabet: {string.ascii_lowercase}")
    print(f"Substitution Key : {secret_key}\n")

    # 3. Encrypt the message
    encrypted_message = encrypt_monoalphabetic(original_message, secret_key)
    print(f"Encrypted Text: {encrypted_message}")

    # 4. Decrypt the message back to its original state
    decrypted_message = decrypt_monoalphabetic(encrypted_message, secret_key)
    print(f"Decrypted Text: {decrypted_message}")
    
    # Verify the logic holds true
    assert original_message == decrypted_message
