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

def get_user_selection():
    """Prompt user for selection between default prescription and NIT template."""
    print("Select the template:")
    print("1. Default Medicine Prescription")
    print("2. NIT Template")
    selection = input("Enter your choice (1 or 2): ")
    if selection not in ['1', '2']:
        print("Invalid selection. Please enter 1 or 2.")
        sys.exit(1)
    return selection

if __name__ == "__main__":
    requirements_file = os.path.join('bin', 'requirements.txt')
    
    # Install the required packages
    install_packages(requirements_file)

    # Get user selection (Default or NIT Template)
    selection = get_user_selection()

    # Detect the OS and select the main script accordingly
    if platform.system() == 'Linux':
        if selection == '1':  # Default medicine prescription
            main_script = os.path.join('bin', 'default_linux.py')
        else:  # NIT Template
            main_script = os.path.join('bin', 'nit_linux.py')
    
    elif platform.system() == 'Darwin':  # macOS
        if selection == '1':  # Default medicine prescription
            main_script = os.path.join('bin', 'default_mac.py')
        else:  # NIT Template
            main_script = os.path.join('bin', 'nit_mac.py')
    
    elif platform.system() == 'Windows':
        if selection == '1':  # Default medicine prescription
            main_script = os.path.join('bin', 'default_windows.py')
        else:  # NIT Template
            main_script = os.path.join('bin', 'nit_windows.py')
    
    else:
        print(f"Unsupported OS: {platform.system()}")
        sys.exit(1)

    # Run the selected main script
    run_main_script(main_script)
