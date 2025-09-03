# Python Cyber Tools

Welcome to Python Cyber Tools! This repository is a curated collection of practical, standalone Python scripts designed for common cybersecurity and utility tasks. Each script serves as a clear, functional example for both educational purposes and real-world use.

---

## Scripts Included

### 1. Password Strength Checker (`password_strength_checker.py`)

A robust, command-line tool to check if a password meets common security criteria. It provides immediate, specific feedback to help users create stronger passwords.

#### Description

This script evaluates a password against a set of rules essential for basic security hygiene. The goal is to encourage the creation of passwords that are more resistant to brute-force and dictionary attacks by enforcing complexity. It checks criteria sequentially and reports the very first rule that is violated.

#### How It Works

The script operates on a simple set of boolean checks:

1.  **Minimum Length**: It first verifies if the password is at least **8 characters** long.
2.  **Uppercase Letter**: It checks for the presence of at least one uppercase letter (`A-Z`).
3.  **Lowercase Letter**: It checks for the presence of at least one lowercase letter (`a-z`).
4.  **Digit**: It ensures there is at least one numerical digit (`0-9`).
5.  **Special Character**: It confirms that the password contains at least one special character from the set `!@#$%^&*()-_=+[]{};:'",.<>?/\|~`.

If all checks pass, the script declares the password as "strong."

#### How to Run

This script has **no external dependencies** and can be run directly with Python.

1.  Navigate to the repository folder in your terminal.
2.  Run the script:
    ```
    python password_strength_checker.py
    ```
3.  Enter a password when prompted and press Enter.

#### Example Usage

```
$ python password_strength_checker.py
Enter a password to check: mypassword123
Password must contain at least one uppercase letter.

$ python password_strength_checker.py
Enter a password to check: MyPassword123
Password must contain at least one special character.

$ python password_strength_checker.py
Enter a password to check: My$tr0ngP@ssw0rd!
Password is strong!
```

---

### 2. Image Encryption Tool (`image_encryptor_tool.py`)

A simple and secure graphical user interface (GUI) application built with Streamlit to encrypt image files using symmetric encryption.

#### Description

This tool provides an easy-to-use web interface for encrypting images. It uses the **Fernet** implementation from the `cryptography` library, which guarantees that an encrypted message cannot be manipulated or read without the key. It is designed for local use to secure sensitive image files.

#### Technology Stack

* **Streamlit**: A fast and easy way to build beautiful data apps and GUIs in Python.
* **Cryptography (Fernet)**: A library providing high-level recipes for secure symmetric encryption. Fernet uses AES-128 in CBC mode for encryption and HMAC with SHA256 for authentication, ensuring both confidentiality and integrity.

#### How It Works

1.  **Key Management**: When the application starts, it looks for a file named `Secret.key` in the same directory.
    * If the key file is **found**, it's loaded and used for encryption.
    * If the key file is **not found**, a new, cryptographically secure key is generated and saved as `Secret.key`.

2.  **Encryption Process**:
    * The user uploads an image file (`.jpg`, `.png`, etc.) via the web interface.
    * The application reads the image's raw binary data.
    * This data is then encrypted using the loaded or newly generated Fernet key.
    * The resulting encrypted data is saved as `encrypted_image.enc`, and a download link is provided.

#### Important Security Notice

The `Secret.key` file is **absolutely essential**.

* **Do Not Lose It**: If you lose this key, your encrypted images **cannot be recovered**. Back it up in a secure location, like a password manager or an encrypted drive.
* **Do Not Share It**: Anyone with this key can decrypt your files.
* **Do Not Commit It**: **Never** commit the `Secret.key` file to a public GitHub repository. Add `Secret.key` to your `.gitignore` file to prevent this.

#### How to Run

1.  **Set Up a Virtual Environment (Recommended)**:
    ```
    # Create a virtual environment
    python -m venv venv

    # Activate it
    # On macOS/Linux:
    source venv/bin/activate
    # On Windows:
    .\venv\Scripts\activate
    ```

2.  **Install Dependencies**:
    ```
    pip install -r requirements.txt
    ```

3.  **Run the Streamlit App**:
    ```
    streamlit run image_encryptor_tool.py
    ```

4.  **Use the Tool**: Open the local URL provided by Streamlit (usually `http://localhost:8501`) in your web browser. Upload your image and click "Encrypt Image".
