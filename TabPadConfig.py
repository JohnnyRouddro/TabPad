#!/usr/bin/python3

# Change Settings in this file

# Available input methods. Choose that works best for you.
# Possible values are "xdotool" and "pyuserinput".
# (pyuserinput has lower latency)
input_method = "pyuserinput"

# Enable or disable transparent background.
# It can be helpful in precise positioning of buttons.
transparent_background = True

# Position of gamepad overlay window in terms of percentages of your screen width and height.
overlay_x_position = 0
overlay_y_position = 40

# Size of gamepad overlay window in terms of percentages of your screen width and height.
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

# Change analog sticks properties
sticks_border_size = 1
sticks_border_color = "#555555"
sticks_color = "#ffffff"
sticks_nubs_color = "#ffffff"

# Change deadzone properties
deadzone_border_size = 1
deadzone_border_color = "#ffffff"
deadzone_color = "#ffffff"

# Change properties of all other buttons
button_border_size = 1
button_border_radius = 10
button_border_color = "#555555"
button_opacity = 50 # 100 is fully opaque

# Close button behavior (True minimizes to system tray, False closes the app)
hide_on_close = True

# Start app minimized to system tray
start_minimized = False

# Set analog sticks deadzone in terms of percentages of stick size.
deadzone = 10

# Toggle deadzone visibility.
show_deadzone = True

# Toggle analog sticks nub visibility. If you observe lags while using analog sticks, set this to False.
show_analog_sticks_nub = True

# Follow the instructions below to create new layout profile.
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