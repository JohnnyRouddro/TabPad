#!/usr/bin/python3

# Run command below to install dependencies in Ubuntu.
# sudo apt install python3-pyqt5 xdotool python3-evdev xinput python3-pip
# sudo pip3 install PyUserInput

# Launch TabPad by running command below.
# sudo python3 TabPad.py

import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton
from PyQt5.QtWidgets import QSystemTrayIcon, QStyle, QAction, QMenu
from PyQt5.QtGui import QCursor, QIcon, QRegion
from TabPadEvents import *
import os

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
		# self.appicon = QIcon.fromTheme("input-gaming")
		self.appicon = self.style().standardIcon(QStyle.SP_FileDialogListView)
		self.screen_resolution = QApplication.desktop().screenGeometry()
		self.screen_width, self.screen_height = self.screen_resolution.width(), self.screen_resolution.height()
		self.set_overlay(overlay_x_position, overlay_y_position, overlay_width, overlay_height)
		self.process_counter = 1
		self.dpad_coords = []
		self.quadrant_list = []
		self.leftstick_deadzone_coords = []
		self.rightstick_deadzone_coords = []
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
		self.start_process(self.process_counter)
		if start_minimized:
			self.hidepad()
		# self.activateWindow()

	def createandmove(self, label, xper, yper, command, color, btnsize):
		qbtn = QPushButton(label, self)
		stl = self.get_style(button_border_size, button_border_radius, \
			button_border_color, color, button_opacity)
		qbtn.setStyleSheet(stl)
		if label == "Hide" or label == "Close":
			qbtn.clicked.connect(self.keyhandler(label))
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

	def keyhandler(self, lbl):
		# print (lbl)
		def processinput():
			if hide_on_close and lbl == "Hide":
				self.hidepad()
			elif not hide_on_close and lbl == "Close":
				self.quithandler()
		return processinput

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
		self.show_action.triggered.connect(self.showpad)
		self.hide_action.triggered.connect(self.hidepad)
		self.quit_action.triggered.connect(self.quithandler)
		self.settings_action.triggered.connect(lambda: self.open_file("TabPadConfig.py"))
		self.layout_action.triggered.connect(lambda: self.open_file(current_layout_file))
		self.tray_menu = QMenu()
		self.tray_menu.addAction(self.show_action)
		self.tray_menu.addAction(self.hide_action)
		self.tray_menu.addAction(self.settings_action)
		self.tray_menu.addAction(self.layout_action)
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
		# os.kill(self.eventProcess.pid, signal.SIGSTOP)
		self.eventProcess.kill_process()
		self.hide()

	def showpad(self):
		# os.kill(self.eventProcess.pid, signal.SIGCONT)
		self.show()
		if self.eventProcess.is_alive():
			self.eventProcess.kill_process()
		self.process_counter += 1
		self.start_process(self.process_counter)
		# self.activateWindow()

	def create_dpad(self, label, xper, yper, command, color, btnsize):
		dpad_frame = QWidget(self)
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

	def start_process(self, counter):
		self.eventProcess = newProcess(1, "Event Process " + str(counter), touch_panel, self.screen_width, \
			self.screen_height, self.dpad_coords, self.quadrant_list, self.leftstick_deadzone_coords, \
			self.rightstick_deadzone_coords)
		self.eventProcess.start()

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
		dz = QWidget(stick_widget)

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
			dz_size = self.percentconvertor(deadzone, btnsize[0])
			dz.resize(dz_size, dz_size)
			extrastyle = "max-width:" + str(btnsize[0]) + "px;" \
				+ "max-height:" + str(btnsize[0]) + "px;" \
				+ "min-width:" + str(btnsize[0]) + "px;" \
				+ "min-height:" + str(btnsize[0]) + "px;"
			stl = self.get_style(sticks_border_size, btnsize[0]/2, \
				sticks_border_color, sticks_color, button_opacity, extrastyle)
			stick_widget.setStyleSheet(stl)
			extrastyle = "max-width:" + str(dz_size) + "px;" \
				+ "max-height:" + str(dz_size) + "px;" \
				+ "min-width:" + str(dz_size) + "px;" \
				+ "min-height:" + str(dz_size) + "px;"
			stl = self.get_style(0, dz_size/2, \
				sticks_border_color, sticks_color, button_opacity, extrastyle)
			dz.setStyleSheet(stl)
		else:
			stick_widget.resize(*bs)
			dz_size = self.percentconvertor(deadzone, bs[0])
			dz.resize(dz_size, dz_size)
			extrastyle = "max-width:" + str(bs[0]) + "px;" \
				+ "max-height:" + str(bs[0]) + "px;" \
				+ "min-width:" + str(bs[0]) + "px;" \
				+ "min-height:" + str(bs[0]) + "px;"
			stl = self.get_style(sticks_border_size, bs[0]/2, \
				sticks_border_color, sticks_color, button_opacity, extrastyle)
			stick_widget.setStyleSheet(stl)
			extrastyle = "max-width:" + str(dz_size) + "px;" \
				+ "max-height:" + str(dz_size) + "px;" \
				+ "min-width:" + str(dz_size) + "px;" \
				+ "min-height:" + str(dz_size) + "px;"
			stl = self.get_style(0, dz_size/2, \
				sticks_border_color, sticks_color, button_opacity, extrastyle)
			dz.setStyleSheet(stl)
			
		xpos = self.percentconvertor(xper, self.overlay_width)
		ypos = self.percentconvertor(yper, self.overlay_height)
		stick_widget.move(xpos, ypos)
		dzx = self.roundify(stick_widget.width()/2 - dz.width()/2)
		dzy = self.roundify(stick_widget.height()/2 - dz.height()/2)
		dz.move(dzx, dzy)
		if not show_deadzone:
			dz.hide()
		stick_widget.setFocusPolicy(QtCore.Qt.NoFocus)
		dz.setFocusPolicy(QtCore.Qt.NoFocus)

		dz_startx = stick_widget.x() + dz.x()
		dz_endx = dz_startx + dz.width()
		dz_starty = stick_widget.y() + dz.y()
		dz_endy = dz_starty + dz.height()
		if label == "leftstick":
			self.leftstick_deadzone_coords = [dz_startx, dz_endx, dz_starty, dz_endy]
		if label == "rightstick":
			self.rightstick_deadzone_coords = [dz_startx, dz_endx, dz_starty, dz_endy]

def main():
	app = QApplication(sys.argv)
	ex = TabPad()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()