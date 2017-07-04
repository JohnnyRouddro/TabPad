#!/usr/bin/python3

from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QHBoxLayout, \
QVBoxLayout, QScrollArea, QLabel, QComboBox, QCheckBox, QColorDialog, \
QLineEdit, QSpinBox, QDoubleSpinBox, QDialog, QDialogButtonBox
from TabPadSettings import *
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore

class MainSettings(QWidget):
	def __init__(self, parent):
		super(MainSettings, self).__init__()
		self.screen_resolution = QApplication.desktop().screenGeometry()
		self.screen_width, self.screen_height = self.screen_resolution.width(), self.screen_resolution.height()
		self.parent = parent
		self.setStyleSheet('font-size:20px')
		self.changed_values = []
		self.current_values = []
		self.initUI()

		
	def initUI(self):      
		applyButton = QPushButton("Apply")
		quitButton = QPushButton("Quit")
		cancelButton = QPushButton("Cancel")
		defaultsButton = QPushButton("Restore Defaults")
		cancelButton.clicked.connect(self.cancel_settings)
		applyButton.clicked.connect(self.on_apply_clicked)
		defaultsButton.clicked.connect(self.restore_defaults)
		quitButton.clicked.connect(self.parent.quithandler)
		cancelButton.setMinimumSize(QtCore.QSize(50, 50))
		applyButton.setMinimumSize(QtCore.QSize(50, 50))
		defaultsButton.setMinimumSize(QtCore.QSize(50, 50))
		quitButton.setMinimumSize(QtCore.QSize(50, 50))

		scroll = QScrollArea()
		scroll.setWidgetResizable(True)
		widget = QWidget()
		vlayout = QVBoxLayout()

		hbox = QHBoxLayout()
		hbox.addWidget(quitButton)
		hbox.addWidget(defaultsButton)
		hbox.addStretch(1)
		hbox.addWidget(cancelButton)
		hbox.addWidget(applyButton)
		
		vbox = QVBoxLayout()
		for i in read_settings('User_Settings'):
			for j in settings_variables():
				if i[0] == j[0]:
					self.createandmove(i[0], i[1], j[-1], i[-1], vlayout)
		widget.setLayout(vlayout)
		scroll.setWidget(widget)
		vbox.addWidget(scroll)
		vbox.addLayout(hbox)
		self.setLayout(vbox)
	
		w, h = self.screen_width*.9, self.screen_height*.8
		self.setGeometry((self.screen_width-w)/2, (self.screen_height-h)/2, w, h)
		self.setWindowTitle('Settings')
		self.show()

	def restore_defaults(self):
		text = ("Do you want to restore all settings to default values?\n"
				"This step cannot be undone. Do you want to proceed?")
		result = self.show_dialog(text)
		if result == 1:
			try:
				create_settings()
			except KeyboardInterrupt:
				sys.exit(1)
			self.parent.restart_program()

	def createandmove(self, label, value, text, value_type, box):
		l = label.replace('_', ' ')
		l = l.title()
		w = QWidget(self)
		h = QHBoxLayout()
		vbtn = None
		qbtn = QLabel(l, self)

		if value_type == int:
			if label == 'button_border_radius' or label == 'button_border_size' \
				or label == 'deadzone_border_size' or label == 'sticks_border_size' \
				or label == 'dpad_border_radius' or label == 'dpad_border_size' \
				or label == 'dpad_background_border_radius' or label == 'dpad_background_border_size':
				vbtn = QSpinBox()
				vbtn.setMinimum(0)
				vbtn.setMaximum(1000)
				vbtn.setSingleStep(1)
				val = read_settings('User_Settings', label)
				vbtn.setValue(val)
				vbtn.valueChanged.connect(lambda: self.write_widget_value(label, vbtn.value()))
			if label == 'autorepeat_count':
				vbtn = QSpinBox()
				vbtn.setMinimum(1)
				vbtn.setMaximum(10)
				vbtn.setSingleStep(1)
				val = read_settings('User_Settings', label)
				vbtn.setValue(val)
				vbtn.valueChanged.connect(lambda: self.write_widget_value(label, vbtn.value()))
			if label == 'button_width' or label == 'button_height':
				vbtn = QSpinBox()
				vbtn.setMinimum(1)
				vbtn.setMaximum(1000)
				vbtn.setSingleStep(10)
				val = read_settings('User_Settings', label)
				vbtn.setValue(val)
				vbtn.valueChanged.connect(lambda: self.write_widget_value(label, vbtn.value()))
			if label == 'overlay_x_position' or label == 'overlay_y_position' \
				or label == 'overlay_width' or label == 'overlay_height' \
				or label == 'dpad_background_opacity' or label == 'deadzone' \
				or label == 'button_opacity':
				vbtn = QSpinBox()
				vbtn.setMinimum(0)
				vbtn.setMaximum(100)
				vbtn.setSingleStep(1)
				val = read_settings('User_Settings', label)
				vbtn.setValue(val)
				vbtn.valueChanged.connect(lambda: self.write_widget_value(label, vbtn.value()))
		
		if value_type == float:
			if label == 'autorepeat_interval':
				vbtn = QDoubleSpinBox()
				vbtn.setDecimals(3)
				vbtn.setMinimum(0.001)
				vbtn.setMaximum(10.0)
				vbtn.setSingleStep(0.01)
				val = read_settings('User_Settings', label)
				vbtn.setValue(val)
				vbtn.valueChanged.connect(lambda: self.write_widget_value(label, vbtn.value()))
		
		if label == 'current_layout_file':
			vbtn = QLineEdit()
			name = read_settings('User_Settings', label)
			vbtn.setText(name)
			vbtn.textChanged.connect(lambda: self.write_widget_value(label, vbtn.text()))
		
		if value_type == str and value.startswith('#'):
			if len(value) == 7:
				vbtn = QPushButton()
				color_name = read_settings('User_Settings', label)
				stl = "background-color:%s;" % color_name
				vbtn.setStyleSheet(stl)
				vbtn.clicked.connect(lambda: self.get_color(label, vbtn, color_name))
		
		if value_type == bool:
			vbtn = QCheckBox()
			status = read_settings('User_Settings', label)
			vbtn.setChecked(status)
			vbtn.minimumSizeHint()
			vbtn.stateChanged.connect(lambda: self.write_widget_value(label, vbtn.isChecked()))
		
		if label == 'input_method':
			vbtn = QComboBox()
			item1 = read_settings('User_Settings', 'input_method')
			vbtn.addItem(item1)
			if item1 == 'xdotool':
				item2 = 'pyuserinput'
			else:
				item2 = 'xdotool'
			vbtn.addItem(item2)
			vbtn.currentIndexChanged.connect(lambda: self.write_widget_value(label, vbtn.currentText()))
		
		ibtn = QPushButton(self)
		ibtn.setIcon(QIcon.fromTheme("help-faq"))
		ibtn.setMinimumSize(QtCore.QSize(50, 50))
		ibtn.clicked.connect(lambda: self.show_dialog(text))
		h.addWidget(qbtn)

		if vbtn != None:
			self.current_values.append(('User_Settings', label, vbtn, value, value_type))
			vbtn.setMinimumSize(QtCore.QSize(200, 50))
			if value_type == bool:
				vbtn.setStyleSheet(
					'QCheckBox::indicator {min-width:50;min-height:50;}'
					'QCheckBox::indicator:checked {background-color:limegreen;border:5px solid #555555;}'
					'QCheckBox::indicator:unchecked {background-color:grey;border:5px solid #555555;}'
					)
			h.addStretch(1)
			h.addWidget(vbtn)
	
		h.addWidget(ibtn)
		w.setLayout(h)
		w.setMinimumSize(QtCore.QSize(50, 60))
		box.addWidget(w)

	def on_apply_clicked(self):
		if self.changed_values:
			for v in self.changed_values:
				write_settings(*v)
			self.parent.restart_program()

	def write_widget_value(self, label, val):
		self.changed_values.append(('User_Settings', label, val))

	def get_color(self, label, btn, initial):
		color = QColorDialog.getColor()
		if color.isValid():
			color = color.name()
			stl = "background-color:%s;" % color
			btn.setStyleSheet(stl)
			self.changed_values.append(('User_Settings', label, color))

	def show_dialog(self, text, dialog_type='normal'):
		d = Dialog(self, text, dialog_type)
		result = d.exec_()
		return result
		
	def closeEvent(self, event):
		self.restore_widget_state()
		event.accept()
		self.parent.showpad()

	def restore_widget_state(self):
		if self.current_values:
			for i in self.current_values:
				val = read_settings(i[0], i[1])
				if i[1] == 'current_layout_file':
					i[-3].setText(val)
				elif i[-1] == bool:
					i[-3].setChecked(val)
				elif i[-1] == str and i[-2].startswith('#'):
					if len(i[-2]) == 7:
						stl = "background-color:%s;" % val
						i[-3].setStyleSheet(stl)
				elif i[1] == 'input_method':
					index = i[-3].findText(val)
					if index >= 0:
						i[-3].setCurrentIndex(index)
				else:
					i[-3].setValue(val)

	def cancel_settings(self):
		self.restore_widget_state()
		self.close()
		self.parent.showpad()

class Dialog(QDialog):
	def __init__(self, parent, text, dialog_type="normal"):
		super(Dialog, self).__init__(parent)
		self.screen_resolution = QApplication.desktop().screenGeometry()
		self.screen_width, self.screen_height = self.screen_resolution.width(), self.screen_resolution.height()
		self.parent = parent
		self.text = text
		self.dialog_type = dialog_type
		self.setStyleSheet('font-size:20px')
		self.initUI()
		
	def initUI(self):
		w = QLabel()
		w.setText(str(self.text))
		hbox = QHBoxLayout()
		hbox.addStretch(1)

		self.buttons = QDialogButtonBox(
		   QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
		   QtCore.Qt.Horizontal, self)

		self.buttons.accepted.connect(self.accept)
		self.buttons.rejected.connect(self.reject)
		self.buttons.setMinimumSize(QtCore.QSize(50, 50))
		for b in self.buttons.buttons():
			b.setMinimumSize(QtCore.QSize(50, 50))

		hbox.addWidget(self.buttons)
		vbox = QVBoxLayout()
		vbox.addWidget(w)
		vbox.addSpacing(20)
		vbox.addLayout(hbox)
		self.setLayout(vbox)

		width, height = self.sizeHint().width(), self.sizeHint().height()
		pwidth = self.parent.parent.frameGeometry().width()
		pheight = self.parent.frameGeometry().height()
		self.setGeometry((pwidth-width)/2, (pheight-height)/2, width, height)
		self.setWindowTitle('Information')

	def close_settings(self):
		self.close()