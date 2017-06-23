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
from PyQt5.QtGui import QCursor, QIcon
from TabPadEvents import *

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
		self.process_counter = 1
		self.dpad_coords = []
		self.quadrant_list = []
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
				else:
					self.createandmove(k, *v)
		self.systraysetup()
		self.setGeometry(overlay_x_position, overlay_y_position, overlay_width, overlay_height)
		self.setWindowTitle('TabPad')
		self.show()
		self.start_process(self.process_counter)
		if start_minimized:
			self.hidepad()
		# self.activateWindow()

	def createandmove(self, label, xper, yper, command, color, btnsize):
		qbtn = QPushButton(label, self)
		stl = self.set_style(button_border_size, button_border_radius, \
			button_border_color, color, button_opacity)
		qbtn.setStyleSheet(stl)
		if label == "Hide" or label == "Close":
			qbtn.clicked.connect(self.keyhandler(label))
		if override_button_size:
			qbtn.resize(*btnsize)
		else:
			qbtn.resize(button_width, button_height)
		xpos, ypos = self.percentconvertor(xper, yper)
		qbtn.move(xpos, ypos)
		qbtn.setFocusPolicy(QtCore.Qt.NoFocus)

	def percentconvertor(self, xpercent, ypercent):
		xpos = int(round((overlay_width * xpercent)/100))
		ypos = int(round((overlay_height * ypercent)/100))
		return xpos, ypos

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
		self.show_action.triggered.connect(self.showpad)
		self.hide_action.triggered.connect(self.hidepad)
		self.quit_action.triggered.connect(self.quithandler)
		self.tray_menu = QMenu()
		self.tray_menu.addAction(self.show_action)
		self.tray_menu.addAction(self.hide_action)
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
		stl = self.set_style(dpad_background_border_size, dpad_background_border_radius, \
			dpad_background_border_color, dpad_background_color, dpad_background_opacity)
		dpad_frame.setStyleSheet(stl)

		if override_button_size:
			dpad_frame.resize(*btnsize)
		else:
			dpad_frame.resize(button_width, button_height)

		xpos, ypos = self.percentconvertor(xper, yper)
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

		stl = self.set_style(dpad_border_size, dpad_border_radius, \
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
		self.eventProcess = newProcess(1, "Event Process " + str(counter), touch_panel, self.screen_width, self.screen_height, self.dpad_coords, self.quadrant_list)
		self.eventProcess.start()

	def set_style(self, border_size, border_radius, border_color, background_color, opacity):
		stl = "background-color:rgba(0, 0, 0, 0%);border-width:" \
		+ str(border_size)  + "px;border-style:solid;border-radius:" \
		+ str(border_radius) + "px;border-color:" + str(border_color) \
		+ ";background-color:rgba(" + str(self.hextorgb(background_color)) + "," \
		+ str(opacity) + '%)' + ";"
		return stl

def main():
	app = QApplication(sys.argv)
	ex = TabPad()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()