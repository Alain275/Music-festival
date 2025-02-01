import bcrypt

def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    salt = bcrypt.gensalt()  # Generate a salt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)  # Hash the password
    return hashed_password.decode('utf-8')  # Return the hashed password as a string

def verify_password(stored_hashed_password: str, provided_password: str) -> bool:
    """Verify if the provided password matches the stored hashed password"""
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_hashed_password.encode('utf-8'))
