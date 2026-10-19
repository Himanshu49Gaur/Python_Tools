def rc4_ksa(key):
    """
    Key-Scheduling Algorithm (KSA)
    Initializes the permutation array S based on the provided key.
    """
    key_length = len(key)
    # Initialize the array with identity permutation
    S = list(range(256))
    
    j = 0
    for i in range(256):
        # Scramble the array using the key
        j = (j + S[i] + key[i % key_length]) % 256
        S[i], S[j] = S[j], S[i]  # Swap values
        
    return S


def rc4_prga(S, data_length):
    """
    Pseudo-Random Generation Algorithm (PRGA)
    Generates a keystream of the specified length.
    """
    i = 0
    j = 0
    keystream = []
    
    for _ in range(data_length):
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]  # Swap values
        
        # Output byte
        K = S[(S[i] + S[j]) % 256]
        keystream.append(K)
        
    return keystream


def rc4_crypt(data, key):
    """
    Encrypts or decrypts data using the RC4 stream cipher.
    RC4 is symmetric; applying the same function twice yields the original data.
    """
    # Ensure inputs are byte arrays
    if isinstance(data, str):
        data = data.encode('utf-8')
    if isinstance(key, str):
        key = key.encode('utf-8')
        
    # Phase 1: Initialize the state vector
    S = rc4_ksa(key)
    
    # Phase 2: Generate the keystream
    keystream = rc4_prga(S, len(data))
    
    # Phase 3: XOR the data with the keystream
    result = bytearray()
    for data_byte, key_byte in zip(data, keystream):
        result.append(data_byte ^ key_byte)
        
    return bytes(result)

# ==========================================
# Example Usage
# ==========================================
if __name__ == "__main__":
    # 1. Define the secret message and key
    plaintext = "Secure communication via RC4 stream cipher!"
    secret_key = "SecretKey123"
    
    print(f"Original Text: {plaintext}")
    print(f"Secret Key   : {secret_key}\n")
    
    # 2. Encrypt the message
    encrypted_bytes = rc4_crypt(plaintext, secret_key)
    # Convert raw bytes to hex for safe display
    print(f"Encrypted (Hex): {encrypted_bytes.hex()}")
    
    # 3. Decrypt the message
    # Because it is a stream cipher using XOR, we just pass the ciphertext 
    # back through the exact same crypt function with the same key.
    decrypted_bytes = rc4_crypt(encrypted_bytes, secret_key)
    decrypted_text = decrypted_bytes.decode('utf-8')
    
    print(f"Decrypted Text : {decrypted_text}")
    
    # Verify the code works correctly
    assert plaintext == decrypted_text
