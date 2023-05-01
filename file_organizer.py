import os
import shutil
import yaml
import sys
import time

# Iterate over each file in the Downloads folder
def move_file(filename, retry_time = 1, attempt_limit = 60):
    # Get the file's full path
    filepath = os.path.join(origin_folder, filename)
    if os.path.isfile(filepath):
        # Check if the file's extension matches any group's extension
        for group_name, group_config in extension_groups.items():
            if os.path.splitext(filepath)[1].lower() in group_config['extensions']:
                # Move the file to the group's destination directory
                destination_dir = group_config['destination']
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

# Load the file groups from a YAML file
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)
    origin_folder = config['origin_folder']
    extension_groups = config['extension_groups']

if len(sys.argv) >= 4:
    filename = sys.argv[1]
    retry_time = float(sys.argv[2])
    attempt_limit = int(sys.argv[3])
    move_file(filename, retry_time, attempt_limit)
else:
    for filename in os.listdir(origin_folder):
        move_file(filename)