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

# Position of overlay window in x and y coordinates
overlay_x_position = 0
overlay_y_position = 300

# Width and height of overlay window (DO NOT set these more than your max screen resolution)
overlay_width = 1024
overlay_height = 400

# Global width and height of buttons
button_width = 70
button_height = 70

# Override global button size and use individual button sizes
override_button_size = True

# Change dpad background frame properties
dpad_background_border_size = 1
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

# The dictionary below defines your gamepad layout and properties.
# The first value on left is identification label for your button (inside square [] brackets).
# The next two numbers on right are percentages defining position of a button.
# (Depends on overlay width and height mentioned above.)
# E.g. 6,5 will postion a button horizontally at 6% of total width value.
# And vertically at 5% of total height value.
# The next value in square brackets defines command to be executed on button press.
# Most of the time you will just need to change 'key' or 'click' type (second part in square brackets).
# You can read more about Xdotool and PyUserInput on Internet.
# The next value defines button color (use only hex color values).
# Last value in brackets define individual button sizes.
# These values will only work if override_button_size is set to True.

# Creating your own buttons is super easy. Just add your own layout entry below.
# Make sure you do it in the format shown below to prevent app crashes.

# *********** DONT'S **********
# DO NOT change any labels of existing button listings.
# DO NOT change first two "None" values in a listing. These buttons are not drawn.
# However, their other properties may still be used.
# Follow these strictly to prevent app crashes.
# *********** DONT'S **********

button_layout = {}

button_layout["dpad"] = (3, 35, [], "#ffffff", (250, 250))
button_layout["L1"] = (6, 5, ["key", "q"], "#ff0000", (70, 40))
button_layout["L2"] = (14, 5, ["key", "w"], "#ff0000", (70, 40))
button_layout["R1"] = (79, 5, ["key", "o"], "#ff0000", (70, 40))
button_layout["R2"] = (87, 5, ["key", "p"], "#ff0000", (70, 40))
button_layout["U"] = (None, None, ["key", "Up"], "#ffffff", (40, 80))
button_layout["R"] = (None, None, ["key", "Right"], "#ffffff", (80, 40))
button_layout["D"] = (None, None, ["key", "Down"], "#ffffff", (40, 80))
button_layout["L"] = (None, None, ["key", "Left"], "#ffffff", (80, 40))
button_layout["3"] = (83, 60, ["key", "i"], "#008000", (60, 60))
button_layout["2"] = (91, 70, ["key", "l"], "#ffff00", (60, 60))
button_layout["1"] = (83, 80, ["key", "k"], "#0000ff", (60, 60))
button_layout["4"] = (75, 70, ["key", "j"], "#ffc0cb", (60, 60))
button_layout["Start"] = (45, 92, ["key", "v"], "#ffa500", (70, 30))
button_layout["Select"] = (55, 92, ["key", "n"], "#800080", (70, 30))
# button_layout["LMB"] = (3, 26, ["key", "F1"], "#800080", (60, 80))
# button_layout["RMB"] = (90, 26, ["key", "F3"], "#800080", (60, 80))
button_layout["Close"] = (35, 92, [], "#808080", (70, 30))

# ADVANCED OPTIONS
# DO NOT change them unless you know what you are doing.

coord_adjustment_factor = 2