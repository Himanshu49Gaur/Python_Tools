def encrypt_vigenere(plaintext, keyword):
    """
    Encrypts a message using the Vigenère polyalphabetic substitution cipher.
    """
    encrypted_text = []
    keyword = keyword.upper()
    key_length = len(keyword)
    key_index = 0
    
    for char in plaintext:
        if char.isalpha():
            # Calculate the shift based on the current keyword letter (A=0, B=1, ..., Z=25)
            shift = ord(keyword[key_index]) - ord('A')
            
            if char.isupper():
                # Shift uppercase letters
                new_char = chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
                encrypted_text.append(new_char)
            else:
                # Shift lowercase letters
                new_char = chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
                encrypted_text.append(new_char)
                
            # Move to the next letter in the keyword, wrapping around if necessary
            key_index = (key_index + 1) % key_length
        else:
            # Leave spaces and punctuation unchanged
            encrypted_text.append(char)
            
    return ''.join(encrypted_text)


def decrypt_vigenere(ciphertext, keyword):
    """
    Decrypts a message that was encrypted with the Vigenère cipher.
    """
    decrypted_text = []
    keyword = keyword.upper()
    key_length = len(keyword)
    key_index = 0
    
    for char in ciphertext:
        if char.isalpha():
            # Calculate the reverse shift
            shift = ord(keyword[key_index]) - ord('A')
            
            if char.isupper():
                # Reverse shift uppercase letters
                new_char = chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
                decrypted_text.append(new_char)
            else:
                # Reverse shift lowercase letters
                new_char = chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
                decrypted_text.append(new_char)
                
            key_index = (key_index + 1) % key_length
        else:
            decrypted_text.append(char)
            
    return ''.join(decrypted_text)

# ==========================================
# Example Usage
# ==========================================
if __name__ == "__main__":
    # 1. Define the secret message and the repeating keyword
    original_message = "The eagle flies at midnight!"
    secret_keyword = "LEMON"
    
    print(f"Original Text : {original_message}")
    print(f"Keyword       : {secret_keyword}\n")
    
    # 2. Encrypt the message
    # 'T' shifted by 'L' (11), 'h' shifted by 'E' (4), 'e' shifted by 'M' (12), etc.
    encrypted_message = encrypt_vigenere(original_message, secret_keyword)
    print(f"Encrypted Text: {encrypted_message}")
    
    # 3. Decrypt the message
    decrypted_message = decrypt_vigenere(encrypted_message, secret_keyword)
    print(f"Decrypted Text: {decrypted_message}")
    
    # Verify the code works correctly
    assert original_message == decrypted_message
