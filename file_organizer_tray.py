from infi.systray import SysTrayIcon
import yaml
import subprocess
import sys
import csv

def setActiveMode(systray, mode):
    with open('active_mode.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([mode])
    print(mode)
    systray.update(icon=config['modes'][mode]['icon'])

# Open program in 'default' mode
with open('active_mode.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['default'])

# Load the modes from a YAML file
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)
    modes = config['modes']

# Open the script that watches for new file additions in the origin folder
process = subprocess.Popen(['python', 'watch_directory.py'], universal_newlines=True)

print("The script continues")

# Get a list of correctly formated menu entries (must convert to tuple to pass to menu options)
modes_keys = list(modes.keys())
menu_entries = []
for key in modes_keys:
    print("key: " + key)
    menu_entries.append((modes[key]['display_name'], None, lambda x, y=key: setActiveMode(systray, y)))

menu_options = (tuple(menu_entries))

systray = SysTrayIcon(modes['default']['icon'], "Example tray icon", menu_options)
systray.start()

# This is the only way I managed for the watch_directory.py subprocess to print to the console.
# But if you leave it uncommented it will get stuck in this loop.
# For testing purposes only!
# while True:
#     output, error = process.communicate()
#     if output:
#         print(output.decode('utf-8'))
#     if error:
#         print(error.decode('utf-8'), file=sys.stderr)
