from infi.systray import SysTrayIcon
import yaml


# Load the modes from a YAML file
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)
    modes = config['modes']

def testf(systray):
    print("hello")

# Get a list of correctly formated menu entries (must convert to tuple to pass to menu options)
modes_keys = list(modes.keys())
menu_entries = []
for key in modes_keys:
    menu_entries.append((modes[key]['display_name'], None, testf))

menu_options = (tuple(menu_entries))

systray = SysTrayIcon(modes['default']['icon'], "Example tray icon", menu_options)
systray.start()

# print(modes[default][icon])