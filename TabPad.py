#!/usr/bin/python3

# Run command below to install dependencies in Ubuntu.
# sudo apt install python3-pyqt5 xdotool

# Launch TabPad by running command below.
# python3 TabPad.py

import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton
from PyQt5.QtWidgets import QSystemTrayIcon, QStyle, QAction, QMenu
import subprocess
from TabPadConfig import *
from PyQt5.QtGui import QCursor, QIcon, QKeyEvent
import time
import evdev
import threading
from evdev import ecodes
from decimal import Decimal

class TabPad(QWidget):
	def __init__(self):
		super(TabPad, self).__init__()
		self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint |
							QtCore.Qt.FramelessWindowHint |
							QtCore.Qt.X11BypassWindowManagerHint |
							QtCore.Qt.WA_ShowWithoutActivating |
							QtCore.Qt.WindowDoesNotAcceptFocus
							)
		if transparent_background:
			self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
		self.setFocusPolicy(QtCore.Qt.NoFocus)	
		self.appicon = QIcon.fromTheme("input-gaming")
		self.screen_resolution = QApplication.desktop().screenGeometry()
		self.screen_width, self.screen_height = self.screen_resolution.width(), self.screen_resolution.height()
		self.eventThread = newThread(1, "Event Thread 1", touch_panel, self.screen_width, self.screen_height)
		self.eventThread.start()
		self.initUI()

	def initUI(self):
		if hide_on_close:
			button_layout["Hide"] = button_layout.pop("Close_")
		else:
			button_layout["Close"] = button_layout.pop("Close_")

		for k, v in button_layout.items():
			self.createandmove(k, *v)
		self.systraysetup()
		self.setGeometry(overlay_x_position, overlay_y_position, overlay_width, overlay_height)
		self.setWindowTitle('TabPad')
		self.show()
		# self.activateWindow()

	def createandmove(self, label, xper, yper, command, color, btnsize):
		self.qbtn = QPushButton(label, self)
		self.clr = "background-color:rgba(0, 0, 0, 0%);border-width:" \
		+ str(button_border_size)  + "px;border-style:solid;border-radius:" \
		+ str(button_border_radius) + "px;border-color:" + str(button_border_color) \
		+ ";background-color:rgba(" + str(self.hextorgb(color)) + "," \
		+ str(button_opacity) + '%)' + ";"
		self.qbtn.setStyleSheet(self.clr)
		self.qbtn.clicked.connect(self.keyhandler(label))
		if override_button_size:
			self.qbtn.resize(*btnsize)
		else:
			self.qbtn.resize(button_width, button_height)
		xpos, ypos = self.percentconvertor(xper, yper)
		self.qbtn.move(xpos, ypos)
		self.qbtn.setFocusPolicy(QtCore.Qt.NoFocus)

	def percentconvertor(self, xpercent, ypercent):
		xpos = int(round((overlay_width * xpercent)/100))
		ypos = int(round((overlay_height * ypercent)/100))
		return xpos, ypos

	def keyhandler(self, lbl):
		# print (lbl)
		def processinput():
			if hide_on_close and lbl == "Hide":
				self.hide()
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
		self.hide_action.triggered.connect(self.hide)
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

	def showpad(self):
		self.show()
		# self.activateWindow()

class newThread (threading.Thread):
	def __init__(self, threadID, name, touch_panel, screen_width, screen_height):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.daemon = True
		self.touch_panel = touch_panel
		self.no_device_found = True
		self.screen_width = screen_width
		self.screen_height= screen_height
		self.devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
		# print (self.devices)
		self.inputsetup()

	def run(self):
		print ("Starting " + self.name)
		self.eventloop()

	def inputsetup(self):
		for d in self.devices:
			# print(d.fn, d.name, device.phys)
			# print (d.name)
			if (d.name == self.touch_panel):
				input_node = d.fn
				self.no_device_found = False

		if self.no_device_found == True:
			print ("No touch input detected.")
			print ("Please make sure you have entered correct touch panel name in user settings.")
			print ("And that you are running the app with root access.")
			print ("Quitting in 10 seconds.")
			time.sleep(10)
			quit()
			sys.exit(1)

		self.device = evdev.InputDevice(input_node)

	def eventloop(self):
		touch_time = None
		lift_time = None
		x_abs_val = None
		y_abs_val = None
		for ev in self.device.read_loop():
			# print (evdev.util.categorize(ev))
			if ev.code == 330 and ev.value == 1:
				touch_time = Decimal(str(ev.sec) + "." + str(ev.usec))
				# print touch_time

			if ev.code == 330 and ev.value == 0:
				lift_time = Decimal(str(ev.sec) + "." + str(ev.usec))
				# print lift_time
			else:
				lift_time = None

			if ev.code == 0:
				if ev.value > 0:
					x_abs_val = ev.value
			if ev.code == 1:
				if ev.value > 0:
					y_abs_val = ev.value

			if lift_time != None and x_abs_val != None and y_abs_val != None:
				self.compare_coords(self.xdotool_coords()[0], self.xdotool_coords()[1])

	def percentconvertor(self, val, dimension):
		val = int(round((dimension * val)/100))
		return val

	def compare_coords(self, actual_x, actual_y):
		for k, v in button_layout.items():
			self.x_start_pos = self.percentconvertor(v[0], overlay_width)
			self.x_end_pos = self.x_start_pos + v[4][0]
			self.y_start_pos = self.percentconvertor(v[1], overlay_height)
			self.y_end_pos = self.y_start_pos + v[4][1]
			if actual_x >= self.x_start_pos and actual_x <= self.x_end_pos:
				if actual_y >= self.y_start_pos and actual_y <= self.y_end_pos:
					# print (v[2])
					self.command_executor(v[2])

	def xdotool_coords(self):
		proc = subprocess.Popen("eval $(xdotool getmouselocation --shell) && echo $X $Y", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell = True ).communicate()
		p = str(proc[0]).strip("\\n'")
		p = p.strip("b'") 
		xc = int(p.partition(' ')[0])
		yc = int(p.partition(' ')[2])
		# print (xc, yc)
		if overlay_width < self.screen_width:
			xc = xc - overlay_x_position
			if xc < 0:
				xc = 0
		if overlay_height < self.screen_height:
			yc = yc - overlay_y_position
			if yc < 0:
				yc = 0
			return (xc, yc)

	def command_executor(self, command_array):
		if command_array:
			subprocess.Popen(command_array, stdout=subprocess.PIPE)


def main():
	app = QApplication(sys.argv)
	ex = TabPad()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()