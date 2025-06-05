from database.db_manager import DatabaseManager

def add_sample_challenges():
    db = DatabaseManager()
    
    # Web Challenge
    db.add_challenge(
        title="SQL Injection Basics",
        category="Web",
        description="""Learn about SQL injection by finding the admin password.
        The website is vulnerable to SQL injection in the login form.
        Hint: Try using ' OR '1'='1 in the username field.""",
        flag="flag{sql_injection_master}",
        points=100,
        difficulty="Easy"
    )
    
    # Crypto Challenge
    db.add_challenge(
        title="Caesar Cipher",
        category="Crypto",
        description="""Decrypt this message that was encrypted using a Caesar cipher:
        'KHOOR ZRUOG'
        Hint: The shift is 3.""",
        flag="flag{hello_world}",
        points=50,
        difficulty="Easy"
    )
    
    # Reversing Challenge
    db.add_challenge(
        title="Simple Password Check",
        category="Reversing",
        description="""Analyze this Python script and find the correct password:
        ```python
        def check_password(password):
            if len(password) != 8:
                return False
            if password[0] != 'p':
                return False
            if password[7] != 'd':
                return False
            return True
        ```
        What password will make this function return True?""",
        flag="flag{password}",
        points=150,
        difficulty="Medium"
    )
    
    # Forensics Challenge
    db.add_challenge(
        title="Hidden in Plain Sight",
        category="Forensics",
        description="""A secret message was hidden in this image using steganography.
        Download the image and use a tool like steghide to extract the hidden data.
        Hint: The password is 'secret'.""",
        flag="flag{steganography_is_fun}",
        points=200,
        difficulty="Medium"
    )
    
    # Misc Challenge
    db.add_challenge(
        title="Binary to Text",
        category="Misc",
        description="""Convert this binary string to text:
        01000110 01001100 01000001 01000111
        Hint: Each group of 8 bits represents one ASCII character.""",
        flag="flag{FLAG}",
        points=75,
        difficulty="Easy"
    )

if __name__ == "__main__":
    add_sample_challenges() 