#!/usr/bin/python3

import subprocess
import time
import evdev
import threading
from evdev import ecodes
from decimal import Decimal
from TabPadConfig import *

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

			if ev.code == 53:
				if ev.value > 0:
					x_abs_val = ev.value
			if ev.code == 54:
				if ev.value > 0:
					y_abs_val = ev.value

			if lift_time != None and x_abs_val != None and y_abs_val != None:
				self.compare_coords(self.xdotool_coords()[0], self.xdotool_coords()[1])

	def percentconvertor(self, val, dimension):
		val = int(round((dimension * val)/100))
		return val

	def compare_coords(self, actual_x, actual_y):
		l = []
		button_area = self.circle_points(actual_x, actual_y, 10)
		for k, v in button_layout.items():
			self.x_start_pos = self.percentconvertor(v[0], overlay_width)
			self.x_end_pos = self.x_start_pos + v[4][0]
			self.y_start_pos = self.percentconvertor(v[1], overlay_height)
			self.y_end_pos = self.y_start_pos + v[4][1] 
			for c in button_area:
				if c[0] >= self.x_start_pos and c[0] <= self.x_end_pos:
					if c[1] >= self.y_start_pos and c[1] <= self.y_end_pos:
						l.append(v[2])
		l = self.remove_duplicates_in_array(l)
		self.command_executor(l)

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
			for c in command_array:
				if c:
					subprocess.Popen(c, stdout=subprocess.PIPE)

	def circle_points(self, xcenter, ycenter, radius):
		r = radius
		xc = xcenter
		yc = ycenter
		points_array = []
		for x in range(xc-r, xc+1):
			for y in range(yc-r, yc+1):
				if ((x - xc)*(x - xc) + (y - yc)*(y - yc)) <= r*r:
					xcord = xc - (x - xc)
					ycord = yc - (y - yc)
					points_array.append((xcord, ycord))
		return points_array

	def remove_duplicates_in_array(self, array):
		array = sorted(array)
		a = [array[i] for i in range(len(array)) if i == 0 or array[i] != array[i-1]]
		return a