import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
import os
import sys

file_organizer = 'file_organizer.py'

class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        if len(sys.argv) >= 3:
            filename = os.path.basename(event.src_path)
            print(f"New file created: {filename}")
            retry_time = sys.argv[1]
            attempt_limit = sys.argv[2]
            subprocess.call(['python', file_organizer, filename, retry_time, attempt_limit])
        else:
            print("Arguments missing.")


if __name__ == "__main__":
    path = "D:/TEST/downloads"
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
