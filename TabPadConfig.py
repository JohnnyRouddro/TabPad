#!/usr/bin/python3

# Change Settings in this file

# Enter your touch input name below (can be found out by running xinput command)
# Make sure enter this value correctly or the app will fail immediately after launch.
touch_panel = "GDIX1000:00 27C6:1002"

# Enable or disable transparent background.
# It can be useful in precise positioning of buttons.
transparent_background = True

# Position of transparent overlay window in x and y coordinates
overlay_x_position = 0
overlay_y_position = 300

# Width and height of transparent overlay window (DO NOT set these more than your max screen resolution)
overlay_width = 1024
overlay_height = 400

# Global width and height of buttons
button_width = 70
button_height = 70

# Override global button size and use individual button sizes
override_button_size = True

# Change button geometry and color
button_border_size = 1
button_border_radius = 10
button_border_color = "#555555"

# Opacity of buttons in percentage (100 is fully opaque).
button_opacity = 100

# Close button behavior (True minimizes to system tray, False closes the app)
hide_on_close = True

# The dictionary below defines your gamepad layout and properties.
# The first value is identification label for your button (before colon).
# The next two numbers are percentages defining position of a button.
# (Depends on overlay width and height mentioned above.)
# E.g. 6,5 will postion a button horizontally at 6% of total width value.
# And vertically at 5% of total height value.
# The next value in square brackets defines command to be executed on button press.
# Most of the time you will just need to change key combinations (third part in square brackets).
# Xdotool also allows you to map mouse clicks, simulate repeating keys and so on. You can read more about xdotool on Internet.
# The next value defines button color (use only hex color values).
# Last value in brackets define individual button sizes.
# These values will only work if override_button_size is set to True.

# Creating your own buttons is super easy. Just append your own layout entry in dictionary below.
# Make sure you do it in the format shown below to prevent app crashes.
# Don't forget to put a comma after each entry, except for the last one.

# DO NOT change any label ending with underscore, e.g. "Close_"

button_layout = {
	"L1": (6, 5, ["xdotool", "key", "q"], "#ff0000", (70, 40)),
	"L2": (14, 5, ["xdotool", "key", "w"], "#ff0000", (70, 40)),
	"R1": (79, 5, ["xdotool", "key", "o"], "#ff0000", (70, 40)),
	"R2": (87, 5, ["xdotool", "key", "p"], "#ff0000", (70, 40)),
	"U": (12, 52, ["xdotool", "key", "Up"], "#ffffff", (40, 80)),
	"R": (16, 67, ["xdotool", "key", "Right"], "#ffffff", (80, 40)),
	"D": (12, 73, ["xdotool", "key", "Down"], "#ffffff", (40, 80)),
	"L": (4, 67, ["xdotool", "key", "Left"], "#ffffff", (80, 40)),
	"3": (83, 60, ["xdotool", "key", "i"], "#008000", (60, 60)),
	"2": (91, 70, ["xdotool", "key", "l"], "#ffff00", (60, 60)),
	"1": (83, 80, ["xdotool", "key", "k"], "#0000ff", (60, 60)),
	"4": (75, 70, ["xdotool", "key", "j"], "#ffc0cb", (60, 60)),
	"Start": (40, 92, ["xdotool", "key", "v"], "#ffa500", (70, 30)),
	"Select": (50, 92, ["xdotool", "key", "n"], "#800080", (70, 30)),
	"Close_": (45, 5, [], "#808080", (70, 30))
}
