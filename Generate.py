import subprocess
import sys
import os
import platform

def clear_screen():
    """Clear the terminal screen based on the operating system."""
    if os.name == 'nt':  # For Windows
        os.system('cls')
    else:  # For macOS and Linux
        os.system('clear')

def install_packages(requirements_file):
    """Install packages listed in the requirements file."""
    if not os.path.isfile(requirements_file):
        print(f"Error: {requirements_file} not found.")
        sys.exit(1)
    
    with open(requirements_file, 'r') as file:
        packages = file.readlines()
    
    for package in packages:
        package = package.strip()
        if package:
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            except subprocess.CalledProcessError as e:
                print(f"Error installing package '{package}': {e}")
                sys.exit(1)

def run_main_script(main_script):
    """Run the main script."""
    if not os.path.isfile(main_script):
        print(f"Error: {main_script} not found.")
        sys.exit(1)
    
    try:
        clear_screen()  # Clear the screen before running the main script
        subprocess.check_call([sys.executable, main_script])
    except subprocess.CalledProcessError as e:
        print(f"Error running main script '{main_script}': {e}")
        sys.exit(1)

if __name__ == "__main__":
    requirements_file = os.path.join('bin', 'requirements.txt')

    # Detect the OS and select the main script accordingly
    if platform.system() == 'Linux':
        main_script = os.path.join('bin', 'CLI_linux.py')  # Main script for Linux
    else:
        main_script = os.path.join('bin', 'cli.py.py')  # Main script for Windows or others

    install_packages(requirements_file)
    run_main_script(main_script)
