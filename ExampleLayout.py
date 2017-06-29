#!/usr/bin/python3

# The dictionary below defines your gamepad layout and properties.

# The first value on left is identification label for your button (inside square [] brackets).

# The next two numbers on right are percentages defining position of a button.
# (They depend on overlay width and height mentioned above.)
# E.g. 6, 5 will postion a button horizontally at 6% of total width value.
# And vertically at 5% of total height value.

# The next value in square brackets defines command to be executed on button press.
# Most of the time you will just need to change 'key' or 'click' type (second part in square brackets).
# You can read more about Xdotool and PyUserInput on Internet.
# The last value in square bracket toggles autorepeat on or off.

# The next value defines button color (use only hex color values).

# Last value in brackets define individual button sizes.
# These values will only work if override_button_size is set to True.

# Creating your own buttons is super easy. Just add your own layout entry below.
# Make sure you do it in the format shown below to prevent app crashes.

# *********** DONT'S **********
# DO NOT change any labels of existing button listings.
# DO NOT change first two "None" values in a listing. These buttons are not drawn.
# However, their other properties will still be used.
# DO NOT change empty square [] braces.
# Follow these strictly to prevent app crashes.
# *********** DONT'S **********

button_layout = {} ## DO NOT EDIT THIS

button_layout["leftstick"] = (3, 30, [], "#ffffff", (150, 150))
button_layout["leftstick_U"] = (None, None, ["key", "Up", False], "#ffffff", (40, 80))
button_layout["leftstick_R"] = (None, None, ["key", "Right", False], "#ffffff", (80, 40))
button_layout["leftstick_D"] = (None, None, ["key", "Down", False], "#ffffff", (40, 80))
button_layout["leftstick_L"] = (None, None, ["key", "Left", False], "#ffffff", (80, 40))

button_layout["rightstick"] = (72, 60, [], "#ffffff", (150, 150))
button_layout["rightstick_U"] = (None, None, ["key", "Up", False], "#ffffff", (40, 80))
button_layout["rightstick_R"] = (None, None, ["key", "Right", False], "#ffffff", (80, 40))
button_layout["rightstick_D"] = (None, None, ["key", "Down", False], "#ffffff", (40, 80))
button_layout["rightstick_L"] = (None, None, ["key", "Left", False], "#ffffff", (80, 40))

button_layout["L1"] = (6, 5, ["key", "Return", False], "#ff0000", (70, 40))
button_layout["L2"] = (14, 5, ["key", "w", False], "#ff0000", (70, 40))
button_layout["R1"] = (79, 5, ["key", "o", False], "#ff0000", (70, 40))
button_layout["R2"] = (87, 5, ["key", "p", False], "#ff0000", (70, 40))

button_layout["dpad"] = (15, 61, [], "#ffffff", (150, 150))
button_layout["U"] = (None, None, ["key", "Up", False], "#ffffff", (40, 80))
button_layout["R"] = (None, None, ["key", "Right", False], "#ffffff", (80, 40))
button_layout["D"] = (None, None, ["key", "Down", False], "#ffffff", (40, 80))
button_layout["L"] = (None, None, ["key", "Left", False], "#ffffff", (80, 40))

button_layout["3"] = (83, 22, ["key", "i", False], "#008000", (60, 60))
button_layout["2"] = (91, 32, ["key", "l", False], "#ffff00", (60, 60))
button_layout["1"] = (83, 42, ["key", "k", False], "#0000ff", (60, 60))
button_layout["4"] = (75, 32, ["key", "j", False], "#ffc0cb", (60, 60))

button_layout["Start"] = (45, 92, ["key", "v", False], "#ffa500", (70, 30))
button_layout["Select"] = (55, 92, ["key", "n", False], "#800080", (70, 30))

# button_layout["LMB"] = (3, 26, ["click", "1", False], "#800080", (60, 80))
# button_layout["RMB"] = (90, 26, ["click", "2", False], "#800080", (60, 80))

button_layout["Close"] = (35, 92, [], "#808080", (70, 30))
button_layout["Stop Autorepeat"] = (1, 92, [], "#808080", (130, 30))