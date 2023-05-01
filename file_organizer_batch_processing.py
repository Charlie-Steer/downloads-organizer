import os
import shutil
import yaml

# Load the file groups from a YAML file
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)
    origin_folder = config['origin_folder']
    extension_groups = config['extension_groups']

# Iterate over each file in the Downloads folder
for filename in os.listdir(origin_folder):
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
                shutil.move(filepath, destination_dir)