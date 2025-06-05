# Educational CTF Platform

A Python-based Capture The Flag (CTF) platform designed for educational purposes and student practice. This platform provides a user-friendly interface for students to learn and practice various cybersecurity concepts through hands-on challenges.

## Features

- User authentication system
- Challenge categories: Web, Crypto, Reversing, Forensics, and Misc
- Real-time scoring system
- Challenge filtering by category and difficulty
- Modern GUI interface using PyQt5
- Local database for storing user data and challenges

## Requirements

- Python 3.7+
- PyQt5
- bcrypt
- SQLite3
- reportlab
- cryptography

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ctf-platform.git
cd ctf-platform
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Initialize the database and add sample challenges:
```bash
python challenges/sample_challenges.py
```

2. Start the application:
```bash
python main.py
```

3. Create a new account or log in with existing credentials.

4. Browse challenges by category and difficulty.

5. Submit flags to earn points and track your progress.

## Challenge Categories

- **Web**: Web application security challenges
- **Crypto**: Cryptography and encryption challenges
- **Reversing**: Reverse engineering challenges
- **Forensics**: Digital forensics challenges
- **Misc**: Miscellaneous challenges

## Adding New Challenges

To add new challenges, you can either:

1. Use the sample_challenges.py script as a template and add your challenges
2. Create a new Python script that uses the DatabaseManager class to add challenges

Example:
```python
from database.db_manager import DatabaseManager

db = DatabaseManager()
db.add_challenge(
    title="Your Challenge Title",
    category="Category",
    description="Challenge description",
    flag="flag{your_flag}",
    points=100,
    difficulty="Easy"
)
```

## Security Note

This platform is designed for educational purposes only. All challenges are meant to be solved locally and do not involve any real-world exploitation or malicious activities.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 