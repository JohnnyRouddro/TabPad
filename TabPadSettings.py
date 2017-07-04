#!/usr/bin/python3

import os
from PyQt5.QtCore import QSettings

config_folder = os.path.dirname(os.path.realpath(__file__))
full_config_file_path = os.path.join(config_folder, 'settings.conf')

def file_present():
	try:
		if os.stat(full_config_file_path).st_size > 0:
			file_empty = False
		else:
			file_empty = True
	except OSError:
		pass
	if not os.path.exists(full_config_file_path) or file_empty == True:
		return False
	return True
	
def create_settings():
	settings = QSettings(full_config_file_path, QSettings.NativeFormat)
	sections = ["Default_Settings", "User_Settings"]
	for s in sections:
		for v in settings_variables():
			settings.beginGroup(s)
			settings.setValue(v[0], v[1])
			settings.endGroup()
	del settings

def declare_settings():
	settings = QSettings(full_config_file_path, QSettings.NativeFormat)
	settings.beginGroup("User_Settings")
	keys = settings.childKeys()
	for s in settings_variables():
		for k in keys:
			if s[0] == k:
				value = settings.value(k,  s[1], type=s[2])
				globals()[k] = value
	settings.endGroup()

def read_settings(group, setting='all'):
	settings = QSettings(full_config_file_path, QSettings.NativeFormat)
	value = None
	pairs = []
	if setting != 'all':
		settings.beginGroup(group)
		for s in settings_variables():
			if s[0] == setting:
				value = settings.value(setting,  s[1], type=s[2])
		settings.endGroup()
		return value

	if setting == 'all':
		settings.beginGroup(group)
		keys = settings.childKeys()
		for s in settings_variables():
			for k in keys:
				if s[0] == k:
					value = settings.value(k,  s[1], type=s[2])
					pairs.append((k, value, s[2]))
		settings.endGroup()
		return pairs

def write_settings(group, setting, value):
	settings = QSettings(full_config_file_path, QSettings.NativeFormat)
	settings.beginGroup(group)
	settings.setValue(setting, value)
	settings.endGroup()
	del settings

def load_layout():
	from importlib import import_module
	file_name = current_layout_file[:-3]
	module = import_module(file_name)
	button_layout = module.button_layout
	globals()['button_layout'] = button_layout

def settings_variables():
	v = [
			(
				"input_method", 'pyuserinput', str, 
				('Available input methods. Choose what works best for you.\n'
				'Possible values are "xdotool" and "pyuserinput" '
				'(pyuserinput has lower latency).')
			),

			(
				'transparent_background', True, bool,
				('Enable or disable transparent background.\n'
				'It can be helpful in precise positioning of buttons.')
			),

			(
				'overlay_x_position', 0, int,
				'Position of gamepad overlay window in terms of percentages of your screen width.'
			),

			(
				'overlay_y_position', 40, int,
				'Position of gamepad overlay window in terms of percentages of your screen height.'
			),
			
			(
				'overlay_width', 100, int,
				'Size of gamepad overlay window in terms of percentages of your screen width.'
			),

			(
				'overlay_height', 50, int,
				'Size of gamepad overlay window in terms of percentages of your screen height.'
			),

			(
				'button_width', 70, int,
				'Global width of buttons (in px).'
			),

			(
				'button_height', 70, int,
				'Global height of buttons (in px).'
			),
			
			(
				'override_button_size', True, bool,
				'Override global button size and use individual button sizes.'
			),

			(
				'dpad_background_border_size', 0, int,
				'Change dpad background frame properties.'

			),

			(
				'dpad_background_border_radius', 10, int,
				'Change dpad background frame properties.'
			),

			(
				'dpad_background_border_color', '#555555', str,
				'Change dpad background frame properties.'
			),

			(
				'dpad_background_opacity', 0, int,
				'Change dpad background frame properties.'
			),

			(
				'dpad_background_color', '#ffffff', str,
				'Change dpad background frame properties.'
			),

			(
				'dpad_border_size', 2, int,
				'Change dpad directional buttons properties.'
			),

			(
				'dpad_border_radius', 8, int,
				'Change dpad directional buttons properties.'
			),

			(
				'dpad_border_color', '#555555', str,
				'Change dpad directional buttons properties.'
			),

			(
				'dpad_color',  '#ffffff', str,
				'Change dpad directional buttons properties.'
			),

			(
				'sticks_border_size', 1, int,
				'Change analog sticks properties.'
			),

			(
				'sticks_border_color', '#555555', str,
				'Change analog sticks properties.'
			),

			(
				'sticks_color', '#ffffff', str,
				'Change analog sticks properties.'
			),

			(
				'sticks_nubs_color', '#ffffff', str,
				'Change analog sticks properties.'
			),

			(
				'deadzone_border_size', 1, int,
				'Change analog sticks deadzone properties.'
			),

			(
				'deadzone_border_color', '#ffffff', str,
				'Change analog sticks deadzone properties.'
			),

			(
				'deadzone_color', '#ffffff', str,
				'Change analog sticks deadzone properties.'
			),

			(
				'button_border_size', 1, int,
				'Change properties of all other buttons.'
			),

			(
				'button_border_radius', 10, int,
				'Change properties of all other buttons.'
			),
			(
				'button_border_color', '#555555', str,
				'Change properties of all other buttons.'
			),

			(
				'button_opacity', 50, int,
				'Change properties of all other buttons.'
			),

			(
				'hide_on_close', True, bool,
				'Minimize to system tray or close the gamepad.'
			),

			(
				'start_minimized', False, bool,
				'Start app minimized to system tray.'
			),

			(
				'deadzone', 10, int,
				'Set analog sticks deadzone in terms of percentages of stick size.'
			),

			(
				'show_deadzone', True, bool,
				'Toggle deadzone visibility.'
			),

			(
				'show_analog_sticks_nub', True, bool,
				'Toggle analog sticks nub visibility.\n' \
				'If you observe lags while using analog sticks, set this to False.'
			),

			(
				'autorepeat_interval', 0.1, float,
				'Autorepeat/Turbo/Rapid-fire interval in seconds (e.g. 0.1, 0.5, 1, 2).'
			),

			(
				'autorepeat_count', 1, int,
				('Number of times you want to repeat keystrokes/clicks between each time interval.\n'
				'DO NOT set it too high (max 5 should be good).\n'
				'Higher values will work but can have all sorts of weird behaviors.\n'
				'Setting it too high can crash your system or your device can go on autoclicking frenzy.\n'
				'If you really want faster autorepeat, try reducing time interval above.\n'
				'Ideally I would always keep it at 1.\n'
				'!!!!! YOU HAVE BEEN WARNED !!!!!')
			),

			(
				'current_layout_file', "DefaultLayout.py", str,
				('Follow the instructions to create new layout profile.\n'
				'Make a copy of "DefaultLayout.py" file.\n'
				'Change the name of new layout file (do not remove .py extension).\n'
				'E.g. "MyLayout.py"\n'
				'Enter the correct name in the box.')
			)
		]

	return v

if not file_present():
	try:
		create_settings()
	except KeyboardInterrupt:
		sys.exit(1)
declare_settings()
load_layout()