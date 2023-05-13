import os
import shutil
import yaml
import sys
import time
import argparse
import file_converter
from pathlib import Path

print('CAN PRINT')

# Iterate over each file in the Downloads folder
def moveFile(filename, mode, retry_time=1.0, attempt_limit=60):
    # Get the file's full path
    filepath = os.path.join(origin_folder, filename)
    if os.path.isfile(filepath):
        for group_name, group_config in extension_groups.items():
            extensions = group_config['extensions']
            # If the extension is in a group => move file
            if os.path.splitext(filepath)[1].lower() in extensions:
                # Assess destination
                if mode == 'default' or not override_groups or not override_groups.get(group_name):
                    destination = group_config['destination']
                else:
                    destination = override_groups[group_name]
                # If destination directory doesn't exist => create it
                if not os.path.exists(destination):
                    os.makedirs(destination)
                # Move file if it doesn't already exist
                fileAlreadyExists = Path(destination + '/' + os.path.basename(filepath)).exists()
                if (not fileAlreadyExists):
                    # Move the file to the group's destination directory
                    # Try to move the file every second until you have permission
                    for i in range (attempt_limit):
                        try:
                            new_path = shutil.move(filepath, destination)
                            convertWebpToPng(new_path)
                        except PermissionError as e:
                            print(f"Error: {e}. Retrying in {retry_time} second(s)...")
                            time.sleep(retry_time)
                        except Exception as e:
                            print(f"Error: {e}. Exiting...")
                            sys.exit(0)

def convertWebpToPng(image_path=None):
    if convert_webp_to_png and os.path.splitext(image_path)[1].lower() == '.webp' and image_path:
        image, save_path = file_converter.convert_to_png(image_path)
        file_converter.save_image(image, save_path, image_path, True)


# Create an ArgumentParser object
parser = argparse.ArgumentParser()
# Add arguments to the parser
parser.add_argument('--filename', type=str, default=None, help='Path to the new file')
parser.add_argument('--mode', type=str, default='default', help='Mode to use for override paths')
# Parse the command-line arguments
args = parser.parse_args()
# Access the values of the arguments
filename = args.filename
mode = args.mode

# Read current 'mode'
if filename:
    with open('active_mode.csv', 'r') as file:
        mode = file.read().strip()

# Load the file groups from a YAML file
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)
    origin_folder = config['origin_folder']

    parameters = config['parameters']
    retry_time = parameters['retry_time']
    attempt_limit = parameters['attempt_limit']
    convert_webp_to_png = parameters['convert_webp_to_png']

    extension_groups = config['extension_groups']

    modes = config['modes']
    override_groups = modes[mode].get('override_groups')

# if --filename provided then move file.
if filename:
    moveFile(filename, mode, retry_time, attempt_limit)
# else move all files in the directory.
else:
    for filename in os.listdir(origin_folder):
        moveFile(filename, mode, 0, 1)