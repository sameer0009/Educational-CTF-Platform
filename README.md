# Educational CTF Platform

This project is an educational Capture The Flag (CTF) platform built using PyQt5 and SQLite. It provides a graphical user interface for users to solve various cybersecurity challenges across different categories and track their progress on a leaderboard.

## Features

*   User authentication (Login/Logout - _Note: User registration might need implementation or a separate initial setup_).
*   Categorized challenges (Web, Crypto, Reversing, Forensics, Misc).
*   Challenge descriptions, points, and difficulty levels.
*   Flag submission and verification.
*   Score tracking for users.
*   Leaderboard display.
*   Basic dark and light theme support.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

You need to have Python installed on your system. The project also uses PyQt5 and other libraries listed in `gui/requirements.txt`.

You can install the required Python packages using pip:

```bash
pip install -r gui/requirements.txt
```

### Installation

1.  Clone the repository:
    ```bash
git clone https://github.com/sameer0009/Educational-CTF-Platform.git
    ```
2.  Navigate into the project directory:
    ```bash
cd Educational-CTF-Platform
    ```

### Running the Application

From the root directory of the project (`KALI TOOLS`), run the main Python script:

```bash
python main.py
```

The application window should open, starting with the login screen.

## Project Structure

*   `main.py`: The main entry point of the application, handles window switching and database initialization.
*   `gui/`: Contains the PyQt5 GUI files (`login.py`, `dashboard.py`, `leaderboard.py`).
*   `database/`: Contains the database management logic (`db_manager.py`).
*   `challenges/`: (Currently contains sample challenges data in `main.py`, could be expanded for loading/managing challenges).

## Known Issues

*   **Challenge cards are not displaying correctly in the scrollable area on the dashboard.** Currently, only the first challenge card is visible in each category tab. This is a known issue that needs to be resolved to make the platform fully functional. We are actively working on diagnosing and fixing this layout problem.

## Contributing

We welcome contributions to improve this educational CTF platform! If you'd like to contribute, please follow these steps:

1.  Fork the repository.
2.  Create a new branch for your feature or bugfix.
3.  Make your changes and test them thoroughly.
4.  Commit your changes with clear and concise messages.
5.  Push your branch to your fork.
6.  Create a pull request to the main repository, describing your changes.

Please feel free to open issues to report bugs or suggest new features.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

*   Mention any libraries, tools, or resources that were helpful. 