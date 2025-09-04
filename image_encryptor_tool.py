import streamlit as st
from cryptography.fernet import Fernet
import os


# Function to generate and save encryption key
def generate_key():
    key = Fernet.generate_key()
    with open("Secret.key", "wb") as key_file:
        key_file.write(key)
    return key


# Function to load the encryption key
def load_key():
    with open("Secret.key", "rb") as key_file:
        return key_file.read()


# Function to encrypt an image
def encrypt_image(image_data):
    # Generate or load the encryption key
    try:
        key = load_key()
    except FileNotFoundError:
        key = generate_key()
    fernet = Fernet(key)

    # Encrypt the image data
    encrypted_data = fernet.encrypt(image_data)
    return encrypted_data


# Streamlit GUI
def main():
    st.title("Image Encryption Tool")
    st.write("Upload an image to encrypt it securely.")

    # Upload an image file
    uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png", "bmp"])

    if uploaded_file:
        # Display uploaded image
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

        # Encrypt image
        if st.button("Encrypt Image"):
            # Read the file bytes
            image_data = uploaded_file.read()
            encrypted_data = encrypt_image(image_data)

            # Save the encrypted file
            encrypted_file_path = "encrypted_image.enc"
            with open(encrypted_file_path, "wb") as file:
                file.write(encrypted_data)

            st.success("Image encrypted successfully!")
            st.write(f"Encrypted file saved as '{encrypted_file_path}'.")

            # Provide download link
            st.download_button(
                label="Download Encrypted File",
                data=encrypted_data,
                file_name="encrypted_image.enc",
                mime="application/octet-stream",
            )


if __name__ == "__main__":
    main()
