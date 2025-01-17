import subprocess, sys, os

script_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the script
logs_dir = os.path.join(script_dir, "logs")

# Ensure the logs directory exists
#os.makedirs(logs_dir, exist_ok=True)
location_path = os.path.join(logs_dir, "location.txt")
log_path = os.path.join(logs_dir, "log.txt")
print(f"Current directory: {script_dir}")
print(f"Logs directory: {logs_dir}")
print(f"Location file: {location_path}")
print(f"Log file: {log_path}")