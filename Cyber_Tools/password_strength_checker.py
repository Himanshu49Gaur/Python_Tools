def password_checker(password):
    
    min_length = 8
    has_upper = any(char.isupper() for char in password)
    has_lower = any(char.islower() for char in password)
    has_digit = any(char.isdigit() for char in password)
    has_special = any(char in "!@#$%^&*()-_=+[]{};:'\",.<>?/\\|`~" for char in password)

    
    if len(password) < min_length:
        return "Password is too short. It must be at least 8 characters long."
    if not has_upper:
        return "Password must contain at least one uppercase letter."
    if not has_lower:
        return "Password must contain at least one lowercase letter."
    if not has_digit:
        return "Password must contain at least one digit."
    if not has_special:
        return "Password must contain at least one special character."

    return "Password is strong!"

password = input("Enter a password to check: ")
print(password_checker(password))

    
    