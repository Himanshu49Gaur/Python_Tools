import math

def encrypt_transposition(plaintext, keyword):
    """
    Encrypts a message using a Columnar Transposition Cipher.
    """
    # Create a list of strings, one for each column
    columns = [""] * len(keyword)
    
    # Fill the grid row by row
    for col in range(len(keyword)):
        pointer = col
        while pointer < len(plaintext):
            columns[col] += plaintext[pointer]
            pointer += len(keyword)
            
    # Determine the alphabetical order of the keyword
    # Example: keyword "HACK" -> [(H, 0), (A, 1), (C, 2), (K, 3)]
    # Sorted -> [(A, 1), (C, 2), (H, 0), (K, 3)]
    key_order = sorted([(char, i) for i, char in enumerate(keyword)])
    
    encrypted_text = ""
    # Read the columns in the alphabetical order of the keyword
    for char, original_index in key_order:
        encrypted_text += columns[original_index]
        
    return encrypted_text


def decrypt_transposition(ciphertext, keyword):
    """
    Decrypts a message that was encrypted with a Columnar Transposition Cipher.
    """
    cols = len(keyword)
    rows = math.ceil(len(ciphertext) / cols)
    
    # Calculate how many "empty" cells exist in the last row of the grid
    num_empty_cells = (cols * rows) - len(ciphertext)
    
    # Determine the length of each column in the original grid
    # Columns at the end of the grid (index >= cols - num_empty_cells) are 1 character shorter
    col_lengths = [rows] * cols
    for i in range(cols - num_empty_cells, cols):
        col_lengths[i] = rows - 1
        
    key_order = sorted([(char, i) for i, char in enumerate(keyword)])
    
    # Reconstruct the columns based on their lengths and the keyword order
    grid_columns = [""] * cols
    ciphertext_ptr = 0
    
    for char, original_index in key_order:
        length = col_lengths[original_index]
        grid_columns[original_index] = ciphertext[ciphertext_ptr : ciphertext_ptr + length]
        ciphertext_ptr += length
        
    # Read the reconstructed grid row by row to get the plaintext
    decrypted_text = ""
    for r in range(rows):
        for c in range(cols):
            # Ensure we don't try to read an empty cell in the shorter columns
            if r < len(grid_columns[c]):
                decrypted_text += grid_columns[c][r]
                
    return decrypted_text

# ==========================================
# Example Usage
# ==========================================
if __name__ == "__main__":
    # 1. Define the secret message and keyword
    # Note: Spaces and punctuation are treated as regular characters and are transposed too.
    original_message = "DEFEND THE EAST WALL OF THE CASTLE!"
    keyword = "ZEBRA"
    
    print(f"Original Text : '{original_message}'")
    print(f"Keyword       : '{keyword}'\n")
    
    # 2. Encrypt the message
    encrypted_message = encrypt_transposition(original_message, keyword)
    print(f"Encrypted Text: '{encrypted_message}'")
    
    # 3. Decrypt the message
    decrypted_message = decrypt_transposition(encrypted_message, keyword)
    print(f"Decrypted Text: '{decrypted_message}'")
    
    # Verify the code works correctly
    assert original_message == decrypted_message
