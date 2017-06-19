#!/usr/bin/python3

# Run command below to install dependencies in Ubuntu.
# sudo apt install python3-pyqt5 xdotool python3-evdev xinput

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
		self.eventProcess = newProcess(1, "Event Process 1", touch_panel, self.screen_width, self.screen_height)
		self.eventProcess.start()
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
		if label == "Hide" or label == "Close":
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
		self.eventProcess = newProcess(1, "Event Process 1", touch_panel, self.screen_width, self.screen_height)
		self.eventProcess.start()
		# self.activateWindow()

def main():
	app = QApplication(sys.argv)
	ex = TabPad()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()