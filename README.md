# downloads-organizer

Windows System Tray utility that automatically moves files from a directory (e.g. Downloads) according to customizable file extension groups created in a the configuration YAML file.
You can also create modes that will override the destination directory of whichever groups you want to other directory, for use in particular situations (e.g. for use while video editing or any other task where you would like files to be routed elsewhere).
You can assign keyboard shortcuts to switch between modes (or just right click on the system tray icon). Also change mode icons to your liking.

To start the application open 'download_organizer_tray.pyw' with Python (preferably with 'pythonw.exe' instead of 'python.exe' so no consoles open). An icon should appear on the system tray.
But first you should configure your 'origin_folder', 'extension_groups' and if you want to 'modes' (you can delete any other than 'default'). There are also a few other settings you can change. Close the application and open it again to ensure changes work correctly.

There is a also a setting to automatically convert WEBP files to PNG. It is turned off by default. Implemented for its ubiquity on the internet, but lack of compatibility with some software.
Also, the file 'file_organizer.pyw', can be run by itself and it will try to move all the files that match your extension groups settings, as if they were just written to the folder; in case files have accumulated in your origin folder.

Further instructions in the 'config.yaml' comments.
