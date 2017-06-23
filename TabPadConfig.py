#!/usr/bin/python3

# Change Settings in this file

# Delete what you see in quotes and enter your own touch panel name below.
# It can be found out by running xinput command.
# Make sure that you enter this value correctly or the app will fail immediately after launch.
touch_panel = "GDIX1000:00 27C6:1002"

# Available input methods. Choose that works best for you.
# Possible values are "xdotool" and "pyuserinput"
input_method = "pyuserinput"

# Toggle this if you see weird, displaced or ghost touches.
coord_hack = True

# Enable or disable transparent background.
# It can be helpful in precise positioning of buttons.
transparent_background = True

# Position of overlay window in terms of percentages of your screen width and height.
overlay_x_position = 0
overlay_y_position = 40

# Size of overlay window in terms of percentages of your screen width and height.
overlay_width = 100
overlay_height = 50

# Global width and height of buttons (in px)
button_width = 70
button_height = 70

# Override global button size and use individual button sizes
override_button_size = True

# Change dpad background frame properties
dpad_background_border_size = 0
dpad_background_border_radius = 10
dpad_background_border_color = "#555555"
dpad_background_opacity = 0
dpad_background_color = "#ffffff"

# Change dpad properties
dpad_border_size = 2
dpad_border_radius = 8
dpad_border_color = "#555555"
dpad_color = "#ffffff"

# Change properties of all other buttons
button_border_size = 1
button_border_radius = 10
button_border_color = "#555555"

# Opacity of buttons in percentage (100 is fully opaque).
button_opacity = 50

# Close button behavior (True minimizes to system tray, False closes the app)
hide_on_close = True

# Start app minimized to system tray
start_minimized = False

# Make a copy of "DefaultLayout.py" file.
# Change the name of new layout file (do not remove .py extension).
# E.g. "MyLayout.py"
# Enter new profile name as shown below.
current_layout_file = "DefaultLayout.py"

# *********** ADVANCED OPTIONS ***********
# DO NOT change them unless you know what you are doing.
# *********** ADVANCED OPTIONS ***********

from importlib import import_module
file_name = current_layout_file[:-3]
module = import_module(file_name)
button_layout = module.button_layout

coord_adjustment_factor = 2