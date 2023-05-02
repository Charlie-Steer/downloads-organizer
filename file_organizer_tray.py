from infi.systray import SysTrayIcon
import yaml
import subprocess
import sys

def testf(systray):
    print("hello")

# Load the modes from a YAML file
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)
    modes = config['modes']

# Open the script that watches for new file additions in the origin folder
parameters = config['parameters']
process = subprocess.Popen(['python', 'watch_directory.py', '--attempt_limit', '420'], universal_newlines=True)

print("The script continues")


# Get a list of correctly formated menu entries (must convert to tuple to pass to menu options)
modes_keys = list(modes.keys())
menu_entries = []
for key in modes_keys:
    menu_entries.append((modes[key]['display_name'], None, testf))

menu_options = (tuple(menu_entries))

systray = SysTrayIcon(modes['default']['icon'], "Example tray icon", menu_options)
systray.start()

# This is the only way I managed for the watch_directory.py subprocess to print to the console.
# But if you leave it uncommented it will get stuck in this loop.
# For testing purposes only!
while True:
    output, error = process.communicate()
    if output:
        print(output.decode('utf-8'))
    if error:
        print(error.decode('utf-8'), file=sys.stderr)
