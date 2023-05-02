import os
import shutil
import yaml
import sys
import time
import argparse

# Iterate over each file in the Downloads folder
def move_file(filename, mode, retry_time, attempt_limit):
    # Get the file's full path
    filepath = os.path.join(origin_folder, filename)
    if os.path.isfile(filepath):
        # Check if the file's extension matches any group's extension
        for group_name, group_config in extension_groups.items():
            extensions = group_config['extensions']
            if mode == 'default' or override_groups.get(group_name):
                destination = group_config['destination']
            else:
                destination = override_groups[group_name]
                
            if os.path.splitext(filepath)[1].lower() in extensions:
                # Move the file to the group's destination directory
                destination_dir = destination
                if not os.path.exists(destination_dir):
                    os.makedirs(destination_dir)
                # Try to move the file every second until you have permission
                for i in range (attempt_limit):
                    try:
                        shutil.move(filepath, destination_dir)
                        print("Move succesful!")
                        break
                    except PermissionError as e:
                        print(f"Error: {e}. Retrying in {retry_time} second(s)...")
                        time.sleep(retry_time)
                    except Exception as e:
                        print(f"Error: {e}. Exiting...")
                        sys.exit(0)

# Create an ArgumentParser object
parser = argparse.ArgumentParser()

# Add arguments to the parser
parser.add_argument('--filename', type=str, default=None, help='Path to the new file')
parser.add_argument('--mode', type=str, default='default', help='mode to use override paths from')
parser.add_argument('--retry_time', type=float, default=1, help='Retry time in seconds')
parser.add_argument('--attempt_limit', type=int, default=60, help='Maximum number of attempts')

# Parse the command-line arguments
args = parser.parse_args()

# Access the values of the arguments
filename = args.filename
mode = args.mode
retry_time = args.retry_time
attempt_limit = args.attempt_limit

print(args)

# Load the file groups from a YAML file
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)
    origin_folder = config['origin_folder']
    extension_groups = config['extension_groups']
    override_groups = config['modes'][mode].get('override_groups')

# if --filename provided then move file.
if filename:
    move_file(filename, mode, retry_time, attempt_limit)
# else move all files in the directory.
else:
    for filename in os.listdir(origin_folder):
        move_file(filename, mode, 0, 1)