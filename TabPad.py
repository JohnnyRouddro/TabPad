#!/usr/bin/python3

# Run command below to install dependencies in Ubuntu.
# sudo apt install python3-pyqt5 xdotool xinput python3-pip
# sudo pip3 install PyUserInput

# Launch TabPad by running command below.
# python3 TabPad.py

from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton
from PyQt5.QtWidgets import QSystemTrayIcon, QStyle, QAction, QMenu
from PyQt5.QtGui import QCursor, QIcon
from TabPadConfig import *
import os, subprocess, sys
from pymouse import PyMouse
from pykeyboard import PyKeyboard

class TabPad(QWidget):
	def __init__(self):
		super(TabPad, self).__init__()
		self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint |
							QtCore.Qt.FramelessWindowHint |
							QtCore.Qt.X11BypassWindowManagerHint |
							QtCore.Qt.WA_ShowWithoutActivating |
							QtCore.Qt.WindowDoesNotAcceptFocus)
		if transparent_background:
			self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
		self.setFocusPolicy(QtCore.Qt.NoFocus)
		self.setAttribute(QtCore.Qt.WA_AcceptTouchEvents)
		QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_SynthesizeTouchForUnhandledMouseEvents)	
		QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_SynthesizeMouseForUnhandledTouchEvents)	
		self.appicon = QIcon.fromTheme("input-gaming")
		# self.appicon = self.style().standardIcon(QStyle.SP_FileDialogListView)
		self.screen_resolution = QApplication.desktop().screenGeometry()
		self.screen_width, self.screen_height = self.screen_resolution.width(), self.screen_resolution.height()
		self.set_overlay(overlay_x_position, overlay_y_position, overlay_width, overlay_height)
		self.dpad_coords = []
		self.quadrant_list = []
		self.leftstick_deadzone_coords = []
		self.rightstick_deadzone_coords = []
		self.keydown_list = []
		self.dpad_keys = [button_layout['U'][2], button_layout['D'][2], button_layout['L'][2], button_layout['R'][2]]
		self.leftstick_keys = [button_layout['leftstick_U'][2], button_layout['leftstick_D'][2], button_layout['leftstick_L'][2], button_layout['leftstick_R'][2]]
		self.rightstick_keys = [button_layout['rightstick_U'][2], button_layout['rightstick_D'][2], button_layout['rightstick_L'][2], button_layout['rightstick_R'][2]]
		self.xdotool = "xdotool"
		self.py_mouse = PyMouse()
		self.py_keyboard = PyKeyboard()
		self.installEventFilter(self)
		self.set_input_type()
		self.initUI()

	def initUI(self):
		if hide_on_close:
			button_layout["Hide"] = button_layout.pop("Close")
		else:
			button_layout["Close"] = button_layout.pop("Close")

		for k, v in button_layout.items():
			if v[0] != None or v[1] != None:
				if k == "dpad":
					self.create_dpad(k, *v)
				elif k == "leftstick":
					self.create_sticks(k, *v)
				elif k == "rightstick":
					self.create_sticks(k, *v)
				else:
					self.createandmove(k, *v)
		self.systraysetup()
		self.setGeometry(self.overlay_x_position, self.overlay_y_position, self.overlay_width, self.overlay_height)
		self.setWindowTitle('TabPad')
		self.show()
		if start_minimized:
			self.hidepad()
		# self.activateWindow()

	def createandmove(self, label, xper, yper, command, color, btnsize):
		qbtn = QPushButton(label, self)
		stl = self.get_style(button_border_size, button_border_radius, \
			button_border_color, color, button_opacity)
		qbtn.setStyleSheet(stl)
		if override_button_size:
			qbtn.resize(*btnsize)
		else:
			qbtn.resize(button_width, button_height)
		xpos = self.percentconvertor(xper, self.overlay_width)
		ypos = self.percentconvertor(yper, self.overlay_height)
		qbtn.move(xpos, ypos)
		qbtn.setFocusPolicy(QtCore.Qt.NoFocus)

	def percentconvertor(self, value, dimension):
		value = self.roundify((value * dimension)/100)
		return value

	def hextorgb(self, hexcolor):
		h = hexcolor.strip('#')
		h = (tuple(int(h[i:i+2], 16) for i in (0, 2 ,4)))
		return (str(h[0]) + "," + str(h[1]) + "," + str(h[2]))

	def systraysetup(self):
		self.tray_icon = QSystemTrayIcon(self)
		self.tray_icon.setIcon(self.appicon)
		self.show_action = QAction("Show", self)
		self.quit_action = QAction("Exit", self)
		self.hide_action = QAction("Hide", self)
		self.settings_action = QAction("Settings", self)
		self.layout_action = QAction("Edit Current Layout", self)
		self.restart_action = QAction("Restart", self)
		self.show_action.triggered.connect(self.showpad)
		self.hide_action.triggered.connect(self.hidepad)
		self.quit_action.triggered.connect(self.quithandler)
		self.settings_action.triggered.connect(lambda: self.open_file("TabPadConfig.py"))
		self.layout_action.triggered.connect(lambda: self.open_file(current_layout_file))
		self.restart_action.triggered.connect(self.restart_program)
		self.tray_menu = QMenu()
		self.tray_menu.addAction(self.show_action)
		self.tray_menu.addAction(self.hide_action)
		self.tray_menu.addAction(self.settings_action)
		self.tray_menu.addAction(self.layout_action)
		self.tray_menu.addAction(self.restart_action)
		self.tray_menu.addAction(self.quit_action)
		self.tray_icon.setContextMenu(self.tray_menu)
		self.tray_icon.show()
		self.tray_icon.activated.connect(self.catchclick)

	def catchclick(self, value):
		if value == self.tray_icon.Trigger: #left click!
			self.tray_menu.exec_(QCursor.pos())

	def quithandler(self):
		QtCore.QCoreApplication.instance().quit()
		sys.exit(1)

	def hidepad(self):
		self.hide()

	def showpad(self):
		self.show()
		# self.activateWindow()

	def create_dpad(self, label, xper, yper, command, color, btnsize):
		dpad_frame = QWidget(self)
		dpad_frame.setObjectName("dpad_frame")
		stl = self.get_style(dpad_background_border_size, dpad_background_border_radius, \
			dpad_background_border_color, dpad_background_color, dpad_background_opacity)
		dpad_frame.setStyleSheet(stl)

		if override_button_size:
			dpad_frame.resize(*btnsize)
		else:
			dpad_frame.resize(button_width, button_height)

		xpos = self.percentconvertor(xper, self.overlay_width)
		ypos = self.percentconvertor(yper, self.overlay_height)
		dpad_frame.move(xpos, ypos)
		dpad_frame.setFocusPolicy(QtCore.Qt.NoFocus)

		upbutton = QPushButton("U", dpad_frame)
		upbutton.resize(self.roundify(btnsize[0]*.25), self.roundify(btnsize[1]*.4))
		upbutton.move(self.roundify(btnsize[0]*.5-btnsize[0]*.125), 0)
		self.dpad_coords.append(self.dpad_geometry(dpad_frame, upbutton))

		downbutton = QPushButton("D", dpad_frame)
		downbutton.resize(self.roundify(btnsize[0]*.25), self.roundify(btnsize[1]*.4))
		downbutton.move(self.roundify(btnsize[0]*.5-btnsize[0]*.125), self.roundify(btnsize[1]*.6))
		self.dpad_coords.append(self.dpad_geometry(dpad_frame, downbutton))

		leftbutton = QPushButton("L", dpad_frame)
		leftbutton.resize(self.roundify(btnsize[0]*.4), self.roundify(btnsize[1]*.25))
		leftbutton.move(0, self.roundify(btnsize[1]*.5-btnsize[1]*.125))
		self.dpad_coords.append(self.dpad_geometry(dpad_frame, leftbutton))
		
		rightbutton = QPushButton("R", dpad_frame)
		rightbutton.resize(self.roundify(btnsize[0]*.4), self.roundify(btnsize[1]*.25))
		rightbutton.move(self.roundify(btnsize[0]*.6), self.roundify(btnsize[1]*.5-btnsize[1]*.125))
		self.dpad_coords.append(self.dpad_geometry(dpad_frame, rightbutton))

		stl = self.get_style(dpad_border_size, dpad_border_radius, \
			dpad_border_color, dpad_color, button_opacity)
		
		upbutton.setStyleSheet(stl)
		downbutton.setStyleSheet(stl)
		leftbutton.setStyleSheet(stl)
		rightbutton.setStyleSheet(stl)
		upbutton.setFocusPolicy(QtCore.Qt.NoFocus)
		downbutton.setFocusPolicy(QtCore.Qt.NoFocus)
		leftbutton.setFocusPolicy(QtCore.Qt.NoFocus)
		rightbutton.setFocusPolicy(QtCore.Qt.NoFocus)

		self.set_dpad_quadrants()

	def roundify(self, value):
		return int(round(value))

	def dpad_geometry(self, frame, btn):
		startx = frame.x() + btn.x()
		endx = startx + btn.width()
		starty = frame.y() + btn.y()
		endy = starty + btn.height()
		return (btn.text(), startx, endx, starty, endy)

	def set_dpad_quadrants(self):
		l = self.dpad_coords
		ur_quadrant = (l[0][0]+l[3][0], l[3][1], l[3][2], l[0][3], l[0][4])
		dr_quadrant = (l[1][0]+l[3][0], l[3][1], l[3][2], l[1][3], l[1][4])
		dl_quadrant = (l[1][0]+l[2][0], l[2][1], l[2][2], l[1][3], l[1][4])
		ul_quadrant = (l[0][0]+l[2][0], l[2][1], l[2][2], l[0][3], l[0][4])
		self.quadrant_list.append(ur_quadrant)
		self.quadrant_list.append(dr_quadrant)
		self.quadrant_list.append(dl_quadrant)
		self.quadrant_list.append(ul_quadrant)

	def get_style(self, border_size, border_radius, border_color, background_color, opacity, extrastyle=None):
		stl = "background-color:rgba(0, 0, 0, 0%);" \
		+ "border-width:" + str(border_size)  + "px;" \
		+ "border-style:solid;" \
		+ "border-radius:" + str(border_radius) + "px;" \
		+ "border-color:" + str(border_color) + ";" \
		+ "background-color:rgba(" + str(self.hextorgb(background_color)) + "," \
		+ str(opacity) + '%)' + ";"
		if extrastyle != None:
			stl += extrastyle
		return stl

	def open_file(self, file):
		directory_path = os.getcwd()
		full_path = os.path.join(directory_path, file)
		subprocess.Popen(["xdg-open", full_path])
		try:
			subprocess.Popen(["xdg-open", full_path])
		except:
			pass

	def set_overlay(self, x, y, w, h):
		self.overlay_x_position = self.percentconvertor(x, self.screen_width)
		self.overlay_y_position = self.percentconvertor(y, self.screen_height)
		self.overlay_width = self.percentconvertor(w, self.screen_width)
		self.overlay_height = self.percentconvertor(h, self.screen_height)

	def create_sticks(self, label, xper, yper, command, color, btnsize):
		stick_widget = QWidget(self)
		nub = QWidget(self)
		dz = QWidget(stick_widget)
		stick_widget.raise_()

		if btnsize[0] != btnsize[1]:
			if btnsize[0] > btnsize[1]:
				btnsize = (btnsize[0], btnsize[0])
			else:
				btnsize = (btnsize[1], btnsize[1])

		if button_width != button_height:
			if button_width > button_height:
				bs = (button_width, button_width)
			elif button_height > button_width:
				bs = (button_height, button_height)
		if button_width == button_height:
			bs = (button_width, button_height)

		if override_button_size:
			stick_widget.resize(*btnsize)
			nub_width, nub_height = btnsize[0]/2, btnsize[1]/2
			nub.resize(nub_width, nub_height)
			dz_size = self.percentconvertor(deadzone, btnsize[0])
			dz.resize(dz_size, dz_size)
			extrastyle = "max-width:" + str(btnsize[0]) + "px;" \
				+ "max-height:" + str(btnsize[0]) + "px;" \
				+ "min-width:" + str(btnsize[0]) + "px;" \
				+ "min-height:" + str(btnsize[0]) + "px;"
			stl = self.get_style(sticks_border_size, btnsize[0]/2, \
				sticks_border_color, sticks_color, button_opacity, extrastyle)
			stick_widget.setStyleSheet(stl)
			extrastyle = "max-width:" + str(nub_width) + "px;" \
				+ "max-height:" + str(nub_width) + "px;" \
				+ "min-width:" + str(nub_width) + "px;" \
				+ "min-height:" + str(nub_width) + "px;"
			stl = self.get_style(sticks_border_size, nub_width/2, \
				sticks_border_color, sticks_nubs_color, button_opacity, extrastyle)
			nub.setStyleSheet(stl)
			extrastyle = "max-width:" + str(dz_size) + "px;" \
				+ "max-height:" + str(dz_size) + "px;" \
				+ "min-width:" + str(dz_size) + "px;" \
				+ "min-height:" + str(dz_size) + "px;"
			stl = self.get_style(deadzone_border_size, dz_size/2, \
				deadzone_border_color, deadzone_color, button_opacity, extrastyle)
			dz.setStyleSheet(stl)
		else:
			stick_widget.resize(*bs)
			nub_width, nub_height = bs[0]/2, bs[1]/2
			nub.resize(nub_width, nub_height)
			dz_size = self.percentconvertor(deadzone, bs[0])
			dz.resize(dz_size, dz_size)
			extrastyle = "max-width:" + str(bs[0]) + "px;" \
				+ "max-height:" + str(bs[0]) + "px;" \
				+ "min-width:" + str(bs[0]) + "px;" \
				+ "min-height:" + str(bs[0]) + "px;"
			stl = self.get_style(sticks_border_size, bs[0]/2, \
				sticks_border_color, sticks_color, button_opacity, extrastyle)
			stick_widget.setStyleSheet(stl)
			extrastyle = "max-width:" + str(nub_width) + "px;" \
				+ "max-height:" + str(nub_width) + "px;" \
				+ "min-width:" + str(nub_width) + "px;" \
				+ "min-height:" + str(nub_width) + "px;"
			stl = self.get_style(sticks_border_size, nub_width/2, \
				sticks_border_color, sticks_nubs_color, button_opacity, extrastyle)
			nub.setStyleSheet(stl)
			extrastyle = "max-width:" + str(dz_size) + "px;" \
				+ "max-height:" + str(dz_size) + "px;" \
				+ "min-width:" + str(dz_size) + "px;" \
				+ "min-height:" + str(dz_size) + "px;"
			stl = self.get_style(deadzone_border_size, dz_size/2, \
				deadzone_border_color, deadzone_color, button_opacity, extrastyle)
			dz.setStyleSheet(stl)
			
		xpos = self.percentconvertor(xper, self.overlay_width)
		ypos = self.percentconvertor(yper, self.overlay_height)
		stick_widget.move(xpos, ypos)
		dzx = self.roundify(stick_widget.width()/2 - dz.width()/2)
		dzy = self.roundify(stick_widget.height()/2 - dz.height()/2)
		dz.move(dzx, dzy)
		nubx = xpos + self.roundify(stick_widget.width()/2 - nub.width()/2)
		nuby = ypos + self.roundify(stick_widget.height()/2 - nub.height()/2)
		nub.move(nubx, nuby)
		if not show_deadzone:
			dz.hide()
		if not show_analog_sticks_nub:
			nub.hide()
		stick_widget.setFocusPolicy(QtCore.Qt.NoFocus)
		dz.setFocusPolicy(QtCore.Qt.NoFocus)
		nub.setFocusPolicy(QtCore.Qt.NoFocus)

		dz_startx = stick_widget.x() + dz.x()
		dz_endx = dz_startx + dz.width()
		dz_starty = stick_widget.y() + dz.y()
		dz_endy = dz_starty + dz.height()
		if label == "leftstick":
			stick_widget.setObjectName('leftstick')
			dz.setObjectName('leftstick_deadzone')
			nub.setObjectName('leftstick_nub')
			self.leftstick_deadzone_coords = [dz_startx, dz_endx, dz_starty, dz_endy]
		if label == "rightstick":
			stick_widget.setObjectName('rightstick')
			dz.setObjectName('rightstick_deadzone')
			nub.setObjectName('rightstick_nub')
			self.rightstick_deadzone_coords = [dz_startx, dz_endx, dz_starty, dz_endy]

	def move_nubs(self, widget, name, event_pos):
		nub = self.findChildren(QWidget, name)
		nub = nub[0]
		widget_startx = widget.x()
		widget_endx = widget_startx + widget.width()
		widget_starty = widget.y()
		widget_endy = widget_starty + widget.height()
		widget_xc = self.roundify((widget_startx + widget_endx)/2)
		widget_yc = self.roundify((widget_starty + widget_endy)/2)
		r = widget.width()/2
		eventx = event_pos.x()
		eventy = event_pos.y()
		if ((eventx - widget_xc)*(eventx - widget_xc) + (eventy - widget_yc)*(eventy - widget_yc)) < r*r:
			x = widget_startx + (event_pos.x() - widget_startx)/2
			y = widget_starty + (event_pos.y() - widget_starty)/2
			nub.move(x,y)
			self.execute_nub_commands(widget, widget_xc, widget_yc, \
				widget_startx, widget_endx, widget_starty, widget_endy, name, eventx, eventy)

	def execute_nub_commands(self, stick, stick_xc, stick_yc, \
		stick_startx, stick_endx, stick_starty, stick_endy, name, x, y):
		if name == "leftstick_nub":
			dz = self.leftstick_deadzone_coords
			u, d, l, r = "leftstick_U", "leftstick_D", "leftstick_L", "leftstick_R"
		if name == "rightstick_nub":
			dz = self.rightstick_deadzone_coords
			u, d, l, r = "rightstick_U", "rightstick_D", "rightstick_L", "rightstick_R"
		if not self.is_point_inside_button(x, y, dz[0], dz[1], dz[2], dz[3]):
			percent = 13
			xc_minus_mod = self.roundify(stick_xc - self.percentconvertor(percent, stick.width()))
			xc_plus_mod = self.roundify(stick_xc + self.percentconvertor(percent, stick.width()))
			yc_minus_mod = self.roundify(stick_yc - self.percentconvertor(percent, stick.height()))
			yc_plus_mod = self.roundify(stick_yc + self.percentconvertor(percent, stick.height()))
			if self.is_point_inside_button(x, y, xc_minus_mod, xc_plus_mod, \
				stick_starty, yc_minus_mod):
				self.keyhandler(u, x, y)
			if self.is_point_inside_button(x, y, xc_minus_mod, xc_plus_mod, \
				yc_plus_mod, stick_endy):
				self.keyhandler(d, x, y)
			if self.is_point_inside_button(x, y, stick_startx, xc_minus_mod, \
				yc_minus_mod, yc_plus_mod):
				self.keyhandler(l, x, y)
			if self.is_point_inside_button(x, y, xc_plus_mod, stick_endx, \
				yc_minus_mod, yc_plus_mod):
				self.keyhandler(r, x, y)
			if self.is_point_inside_button(x, y, stick_startx, xc_minus_mod, \
				stick_starty, yc_minus_mod):
				self.keyhandler("", x, y, [u, l])
			if self.is_point_inside_button(x, y, xc_plus_mod, stick_endx, \
				stick_starty, yc_minus_mod):
				self.keyhandler("", x, y, [u, r])
			if self.is_point_inside_button(x, y, stick_startx, xc_minus_mod, \
				yc_plus_mod, stick_endy):
				self.keyhandler("", x, y, [d, l])
			if self.is_point_inside_button(x, y, xc_plus_mod, stick_endx, \
				yc_plus_mod, stick_endy):
				self.keyhandler("", x, y, [d, r])

	def recenter_nubs(self, widget, nub):
		widget_startx = widget.x()
		widget_endx = widget_startx + widget.width()
		widget_centerx = (widget_startx + widget_endx)/2
		widget_starty = widget.y()
		widget_endy = widget_starty + widget.height()
		widget_centery = (widget_starty + widget_endy)/2
		nub_startx = nub.x()
		nub_endx = nub_startx + nub.width()
		nub_center = (nub_startx + nub_endx)/2
		x = self.roundify(widget_centerx - nub.width()/2)
		y = self.roundify(widget_centery - nub.height()/2)
		if widget_centerx != nub_center or abs(widget_center-nub_center) > 1:
			nub.move(x,y)

	def keyhandler(self, label, x=0, y=0, names=None):
		if names == None:
			cmd = button_layout[label][2]
			if hide_on_close and label == "Hide":
				self.hidepad()
			elif not hide_on_close and label == "Close":
				self.quithandler()
			elif cmd:
				self.diagonal_movement_overlap_fix(label, x, y)
				self.execute_keypress(cmd, 'down', x, y)
				self.keydown_list.append(cmd)
		else:
			if names:
				for n in names:
					cmd = button_layout[n][2]
					self.execute_keypress(cmd, 'down', x, y)
					self.keydown_list.append(cmd)

	def eventFilter(self, source, event):
		if event.type() == QtCore.QEvent.TouchBegin \
			or event.type() == QtCore.QEvent.TouchUpdate:
			tp = event.touchPoints()
			for t in tp:
				event_pos = t.pos().toPoint()
				event_x = event_pos.x()
				event_y = event_pos.y()
				widget = self.childAt(event_pos)
				if widget:
					widget_name = widget.objectName()
					if hasattr(widget, 'text'):
						text = widget.text()
						self.keyhandler(text, event_x, event_y)
					elif widget_name == "leftstick":
						nub_name = 'leftstick_nub'
						self.move_nubs(widget, nub_name, event_pos)
					elif widget_name == "rightstick":
						nub_name = 'rightstick_nub'
						self.move_nubs(widget, nub_name, event_pos)
					else:
						self.check_other_possible_clickables(event_x, event_y)
				else:
					self.trigger_key_up(event_x, event_y)
			return True
		if event.type() == QtCore.QEvent.TouchEnd:
			tp = event.touchPoints()
			for t in tp:
				event_pos = t.pos().toPoint()
				event_x = event_pos.x()
				event_y = event_pos.y()
				self.trigger_key_up(event_x, event_y)
			nub = self.findChildren(QWidget, 'leftstick_nub')
			nub = nub[0]
			widget = self.findChildren(QWidget, 'leftstick')
			widget = widget[0]
			self.recenter_nubs(widget, nub)
			nub = self.findChildren(QWidget, 'rightstick_nub')
			nub = nub[0]
			widget = self.findChildren(QWidget, 'rightstick')
			widget = widget[0]
			self.recenter_nubs(widget, nub)
			return True
		return False

	def check_other_possible_clickables(self, event_x, event_y):
		widget = self.childAt(event_x, event_y)
		if widget:
			name = widget.objectName()
			if name == "dpad_frame":
				for t in self.quadrant_list:
					if self.is_point_inside_button(event_x, event_y, t[1], t[2], t[3], t[4]):
						self.move_diagonally(t[0], event_x, event_y)

	def move_diagonally(self, name, x, y):
		if name == "UR":
			self.keyhandler("", x, y, ["U", "R"])
		if name == "DR":
			self.keyhandler("", x, y, ["D", "R"])
		if name == "DL":
			self.keyhandler("", x, y, ["D", "L"])
		if name == "UL":
			self.keyhandler("", x, y, ["U", "L"])

	def diagonal_movement_overlap_fix(self, name, x, y):
		if name == "U" or name == "D" or name == "L" or name == "R":
			cmd = button_layout[name][2]
			keys = list(self.dpad_keys)
			if cmd in keys:
				keys.remove(cmd)
				self.trigger_key_up(x, y, keys)
		if name == "leftstick_U" or name == "leftstick_D" or name == "leftstick_L" or name == "leftstick_R":
			cmd = button_layout[name][2]
			keys = list(self.leftstick_keys)
			if cmd in keys:
				keys.remove(cmd)
				self.trigger_key_up(x, y, keys)
		if name == "rightstick_U" or name == "rightstick_D" or name == "rightstick_L" or name == "rightstick_R":
			cmd = button_layout[name][2]
			keys = list(self.rightstick_keys)
			if cmd in keys:
				keys.remove(cmd)
				self.trigger_key_up(x, y, keys)

	def is_point_inside_button(self, x, y, startx, endx, starty, endy):
		if x >= startx and x <= endx \
			and y >= starty and y <= endy:
			return True
		return False

	def trigger_key_up(self, x=0, y=0, keys=None):
		if keys != None:
			if keys:
				for k in keys:
					self.execute_keypress(k, 'up', x, y)
					if k in self.keydown_list:
						self.keydown_list.remove(k)
		if keys == None:
			if self.keydown_list:
				for i in self.keydown_list:
					self.execute_keypress(i, 'up', x, y)
				self.keydown_list = []

	def set_input_type(self):
		if input_method == "xdotool":
			self.keydown_string ="keydown"
			self.keyup_string = "keyup"
			self.mousedown_string = "mousedown"
			self.mouseup_string = "mouseup"
		if input_method == "pyuserinput":
			self.keydown_string ="press_key"
			self.keyup_string = "release_key"
			self.mousedown_string = "press"
			self.mouseup_string = "release"

	def modify_keys(self, input_list, input_type):
		if input_list[0] == "key" and input_type == "down":
			input_list[0] = self.keydown_string
		if input_list[0] == "key" and input_type == "up":
			input_list[0] = self.keyup_string
		if input_list[0] == "click" and input_type == "down":
			input_list[0] = self.mousedown_string
		if input_list[0] == "click" and input_type == "up":
			input_list[0] = self.mouseup_string
		return input_list

	def execute_keypress(self, cmnd, keytype, x, y):
		c = list(cmnd)
		if c:
			c = self.modify_keys(c, keytype)
			if input_method == "xdotool":
				c.insert(0, self.xdotool)
				subprocess.Popen(c, stdout=subprocess.PIPE)
			if input_method == "pyuserinput":
				if c[0] == "press_key":
					self.py_keyboard.press_key(c[1])
				if c[0] == "release_key":
					self.py_keyboard.release_key(c[1])
				if c[0] == "press":
					self.py_mouse.press(x, y, int(c[1]))
				if c[0] == "release":
					self.py_mouse.release(x, y, int(c[1]))

	def restart_program(self):
		"""Restarts the current program.
		Note: this function does not return. Any cleanup action (like
		saving data) must be done before calling this function."""
		python = sys.executable
		os.execl(python, python, * sys.argv)
	
def main():
	app = QApplication(sys.argv)
	ex = TabPad()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()