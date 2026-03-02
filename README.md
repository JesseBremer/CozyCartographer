Setup Instructions
This project uses a Python Virtual Environment (venv) to manage dependencies safely without affecting your system Python installation.

1. Create the Environment
If you haven't already, create the virtual environment folder:

Bash
python3 -m venv cozycart
2. Activate the Environment
You must run this command every time you open a new terminal to work on the project:

Bash
source cozycart/bin/activate
Note: Your terminal prompt should now be prefixed with (cozycart).

3. Install Dependencies
Once the environment is active, install the required libraries:

Bash
pip install pygame-ce
Running the Project
To start the application, ensure your environment is active and run:

Bash
python main.py
WSL Troubleshooting
If you are running this via WSL2 on Windows:

Ensure you have a Wayland/X11 server (standard on Windows 11 WSLg).

If you see "No available video device," try updating your WSL kernel: wsl --update in PowerShell.

Project Structure
cozycart/ - Virtual environment files (keep out of version control!)
assets/ - Images, fonts, and sounds.
main.py - The entry point for the application.

Pro-Tip: The .gitignore
Since you created your environment inside your project folder (/CozyCartographer/cozycart), you should create a file named .gitignore and add the following line so you don't accidentally upload thousands of library files to GitHub:

Plaintext
cozycart/
__pycache__/
*.pyc