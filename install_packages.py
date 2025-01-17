import subprocess, sys, os

def install_requirements():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "./reqs/requirements.txt"])
        print("All required packages installed successfully.")
    except subprocess.CalledProcessError as e:
        print("An error occurred while installing packages:", e)

def write_location():
    print("\nWriting log file.")
    with open("./logs/log.txt", "w") as file:
        file.write("")

if __name__ == "__main__":
    install_requirements()
    write_location()
