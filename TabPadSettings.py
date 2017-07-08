#!/usr/bin/python3

import os
from PyQt5.QtCore import QSettings

config_folder = os.path.dirname(os.path.realpath(__file__))
full_config_file_path = os.path.join(config_folder, 'settings.conf')
profiles_folder = os.path.join(config_folder, 'profiles')
if not os.path.exists(profiles_folder):
    os.makedirs(profiles_folder)
default_layout_file = os.path.join(profiles_folder, 'DefaultLayout.conf')
profiles_filelist = [x for x in os.listdir(profiles_folder) if x.endswith('.conf')]

def layout_variables():
	button_layout = {}

	button_layout["leftstick"] = [3, 30, 150, 150, "#ffffff", "disabled", '', '']
	button_layout["leftstick_U"] = [-1, -1, -1, -1, "#ffffff", "normal", "key", "Up"]
	button_layout["leftstick_R"] = [-1, -1, -1, -1, "#ffffff", "normal", "key", "Right"]
	button_layout["leftstick_D"] = [-1, -1, -1, -1, "#ffffff", "normal", "key", "Down"]
	button_layout["leftstick_L"] = [-1, -1, -1, -1, "#ffffff", "normal", "key", "Left"]

	button_layout["rightstick"] = [72, 60, 150, 150, "#ffffff", "disabled", '', '']
	button_layout["rightstick_U"] = [-1, -1, -1, -1, "#ffffff", "normal", "key", "Up"]
	button_layout["rightstick_R"] = [-1, -1, -1, -1, "#ffffff", "normal", "key", "Right"]
	button_layout["rightstick_D"] = [-1, -1, -1, -1, "#ffffff", "normal", "key", "Down",]
	button_layout["rightstick_L"] = [-1, -1, -1, -1, "#ffffff", "normal", "key", "Left"]

	button_layout["L1"] = [6, 5, 70, 40, "#ff0000", "normal", "key", "Return"]
	button_layout["L2"] = [14, 5, 70, 40, "#ff0000", "normal", "key", "w"]
	button_layout["R1"] = [79, 5, 70, 40, "#ff0000", "normal", "key", "o"]
	button_layout["R2"] = [87, 5, 70, 40, "#ff0000", "normal", "key", "p"]

	button_layout["dpad"] = [15, 61, 150, 150, "#ffffff", "disabled", '', '']
	button_layout["U"] = [-1, -1, -1, -1, "#ffffff", "normal", "key", "Up"]
	button_layout["R"] = [-1, -1, -1, -1, "#ffffff", "normal", "key", "Right"]
	button_layout["D"] = [-1, -1, -1, -1, "#ffffff", "normal", "key", "Down"]
	button_layout["L"] = [-1, -1, -1, -1, "#ffffff", "normal", "key", "Left"]

	button_layout["3"] = [83, 22, 60, 60, "#008000", "normal", "key", "i"]
	button_layout["2"] = [91, 32, 60, 60, "#ffff00", "normal", "key", "l"]
	button_layout["1"] = [83, 42, 60, 60, "#0000ff", "normal", "key", "k"]
	button_layout["4"] = [75, 32, 60, 60, "#ffc0cb", "normal", "key", "j"]

	button_layout["Start"] = [45, 92, 70, 30, "#ffa500", "normal", "key", "v"]
	button_layout["Select"] = [55, 92, 70, 30, "#800080", "normal", "key", "n"]

	button_layout["Close"] = [35, 92, 70, 30, "#808080", "disabled", '', '']
	button_layout["Stop All Inputs"] = [1, 92, 130, 30, "#808080", "disabled", '', '']
	button_layout["Settings"] = [89, 92, 100, 30, "#808080", "disabled", '', '']

	return button_layout

default_button_layout = layout_variables()

def file_present(filename):
	try:
		if os.stat(filename).st_size > 0:
			file_empty = False
		else:
			file_empty = True
	except OSError:
		pass
	if not os.path.exists(filename) or file_empty == True:
		return False
	return True
	
def create_default_layout():
	settings = QSettings(default_layout_file, QSettings.NativeFormat)
	for k, v in default_button_layout.items():
		settings.beginGroup('Layout')
		settings.setValue(k, v)
		settings.endGroup()
	del settings

def create_new_layout(filename):
	filename = os.path.join(profiles_folder, filename)
	settings = QSettings(filename, QSettings.NativeFormat)
	for k, v in default_button_layout.items():
		settings.beginGroup('Layout')
		settings.setValue(k, v)
		settings.endGroup()
	del settings

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

def read_layout(group, setting='all'):
	filename = read_settings("User_Settings", 'current_layout_file')
	filename = os.path.join(profiles_folder, filename)
	settings = QSettings(filename, QSettings.NativeFormat)
	value = None
	pairs = []
	if setting != 'all':
		settings.beginGroup(group)
		for k, v in default_button_layout.items():
			if k == setting:
				value = settings.value(setting,  v, type=str)
				value[0], value[1], value[2], value[3] = int(value[0]), int(value[1]), int(value[2]), int(value[3])
		if not setting in default_button_layout.keys():
			value = settings.value(setting, type=str)
			value[0], value[1], value[2], value[3] = int(value[0]), int(value[1]), int(value[2]), int(value[3])
		settings.endGroup()
		return value
	if setting == 'all':
		settings.beginGroup(group)
		keys = settings.childKeys()
		for s in keys:
			for k, v in default_button_layout.items():
				if s == k:
					value = settings.value(s,  v, type=str)
					value[0], value[1], value[2], value[3] = int(value[0]), int(value[1]), int(value[2]), int(value[3])
					pairs.append((s, value))
			if not s in default_button_layout.keys():
				value = settings.value(s, type=str)
				value[0], value[1], value[2], value[3] = int(value[0]), int(value[1]), int(value[2]), int(value[3])
				pairs.append((s, value))
		settings.endGroup()
		return pairs

def layout_childkeys_only(group):
	filename = read_settings("User_Settings", 'current_layout_file')
	filename = os.path.join(profiles_folder, filename)
	settings = QSettings(filename, QSettings.NativeFormat)
	settings.beginGroup(group)
	keys = settings.childKeys()
	settings.endGroup()
	return keys	

def delete_layout_key(group, key):
	filename = read_settings("User_Settings", 'current_layout_file')
	filename = os.path.join(profiles_folder, filename)
	settings = QSettings(filename, QSettings.NativeFormat)
	settings.beginGroup(group)
	keys = settings.childKeys()
	if key in keys:
		settings.remove(key)
	settings.endGroup()
	return keys	

def write_layout(group, setting, value):
	filename = read_settings("User_Settings", 'current_layout_file')
	filename = os.path.join(profiles_folder, filename)
	settings = QSettings(filename, QSettings.NativeFormat)
	settings.beginGroup(group)
	settings.setValue(setting, value)
	settings.endGroup()
	del settings

def write_settings(group, setting, value):
	settings = QSettings(full_config_file_path, QSettings.NativeFormat)
	settings.beginGroup(group)
	settings.setValue(setting, value)
	settings.endGroup()
	del settings

def load_layout():
	filename = read_settings("User_Settings", 'current_layout_file')
	filename = os.path.join(profiles_folder, filename)
	settings = QSettings(filename, QSettings.NativeFormat)
	settings.beginGroup("Layout")
	keys = settings.childKeys()
	button_layout = {}
	for ck in keys:
		for k, v in default_button_layout.items():
			if ck == k:
				v[0], v[1], v[2], v[3] = int(v[0]), int(v[1]), int(v[2]), int(v[3])
				value = settings.value(ck,  v, type=str)
				value[0], value[1], value[2], value[3] = int(value[0]), int(value[1]), int(value[2]), int(value[3])
				button_layout[ck] = value
		if not ck in default_button_layout.keys():
			value = settings.value(ck, type=str)
			value[0], value[1], value[2], value[3] = int(value[0]), int(value[1]), int(value[2]), int(value[3])
			button_layout[ck] = value
	globals()['button_layout'] = button_layout
	settings.endGroup()

def load_default_if_custom_layout_file_not_present():
	filename = read_settings("User_Settings", 'current_layout_file')
	profiles_folder = os.path.join(config_folder, 'profiles')
	filename = os.path.join(profiles_folder, filename)

	if filename != default_layout_file and not file_present(filename):
		write_settings('User_Settings', 'current_layout_file', 'DefaultLayout.conf')

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
				'combo_interval', 0.1, float,
				'Time interval between consecutive taps/clicks in seconds when using a combo (e.g. 0.1, 0.5, 1, 2).'
			),

			(
				'current_layout_file', "DefaultLayout.conf", str,
				('Current layout file being used for drawing the gamepad.')
			)
		]

	return v

if not file_present(full_config_file_path):
	try:
		create_settings()
	except KeyboardInterrupt:
		sys.exit(1)
declare_settings()

if not file_present(default_layout_file):
	try:
		create_default_layout()
	except KeyboardInterrupt:
		sys.exit(1)

load_default_if_custom_layout_file_not_present()
load_layout()
# print(button_layout)