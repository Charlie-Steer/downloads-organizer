import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
import os
import yaml

file_organizer = 'file_organizer.py'

class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        print('file modified')
        if event.is_directory:
            return
        else:
            filename = os.path.basename(event.src_path)
            subprocess.call(['python', file_organizer, '--filename', filename], universal_newlines=True)
            print('subprocess called')
    def on_modified(self, event):
        print('file modified')
        if event.is_directory:
            return
        else:
            filename = os.path.basename(event.src_path)
            subprocess.call(['python', file_organizer, '--filename', filename], universal_newlines=True)
            print('subprocess called')


# Load the config from the YAML file
with open('config.yaml', 'r') as file:
    origin_folder = yaml.safe_load(file)['origin_folder']
    
# Listen for new files in the origin_folder
event_handler = MyHandler()
observer = Observer()
observer.schedule(event_handler, origin_folder, recursive=False)
observer.start()
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()
