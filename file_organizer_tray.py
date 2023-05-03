from infi.systray import SysTrayIcon
import yaml
import subprocess
import csv
import keyboard

# Change mode
def setActiveMode(systray, mode):
    # Rewrite active_mode.csv to pass to the file_organizer.py script
    with open('active_mode.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([mode])
    print(mode)
    icon = config['modes'][mode].get('icon', None)
    if icon:
        systray.update(icon=icon)
    else:
        systray.update(icon=defaultIcon)

# Start on 'default' mode
with open('active_mode.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['default'])

# Load the config from the YAML file
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)
    modes = config['modes']
defaultIcon = modes['default']['icon']

# Open the script that listens for new files in the origin folder
process = subprocess.Popen(['python', 'watch_directory.py'], universal_newlines=True)

# Get a list of correctly formated menu entries (must convert to tuple to pass to menu options)
modes_keys = list(modes.keys())
menu_entries = []

# Adds menu entries for the 'modes' to the system tray icon and assigns them a shortcut
for key in modes_keys:
    mode = modes[key]
    print("key: " + key)
    print('mode: ')
    print(mode)
    display_name = mode.get('display_name', key)
    print("display_name: " + display_name)
    menu_entries.append((display_name, None, lambda x, y=key: setActiveMode(systray, y)))
    shortcut = mode.get('shortcut', None)
    if shortcut:
        keyboard.add_hotkey(shortcut, lambda x=key: setActiveMode(systray, x))

#
menu_options = (tuple(menu_entries))
systray = SysTrayIcon(defaultIcon, "Example tray icon", menu_options)
systray.start()

print(__name__ + " successfully executed")
# This is the only way I managed for the watch_directory.py subprocess to print to the console.
# But if you leave it uncommented it will get stuck in this loop.
# For testing purposes only!
# while True:
#     output, error = process.communicate()
#     if output:
#         print(output.decode('utf-8'))
#     if error:
#         print(error.decode('utf-8'), file=sys.stderr)
