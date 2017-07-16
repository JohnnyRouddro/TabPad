#!/usr/bin/python3

from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QHBoxLayout, \
QVBoxLayout, QScrollArea, QLabel, QComboBox, QCheckBox, QColorDialog, \
QLineEdit, QSpinBox, QDoubleSpinBox, QDialog, QDialogButtonBox, QStyleFactory, \
QScroller, QScrollerProperties, QGridLayout, QListWidget, QStackedWidget, QSizePolicy
from TabPadSettings import *
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore
from functools import partial

class MainSettings(QDialog):
	def __init__(self, parent):
		super(MainSettings, self).__init__()
		self.setWindowFlags(QtCore.Qt.Window)
		self.setModal(True)
		self.screen_resolution = QApplication.desktop().screenGeometry()
		self.screen_width, self.screen_height = self.screen_resolution.width(), self.screen_resolution.height()
		self.parent = parent
		self.setStyleSheet('font-size:20px')
		self.changed_values = []
		self.initUI()
		
	def initUI(self):      
		applyButton = QPushButton(" Apply ")
		quitButton = QPushButton(" Quit ")
		cancelButton = QPushButton(" Cancel ")
		defaultsButton = QPushButton(" Restore Defaults ")
		layoutButton = QPushButton(" Change Gamepad Layout ")

		cancelButton.clicked.connect(self.cancel_settings)
		applyButton.clicked.connect(self.on_apply_clicked)
		defaultsButton.clicked.connect(self.restore_defaults)
		quitButton.clicked.connect(self.parent.quithandler)
		layoutButton.clicked.connect(self.parent.show_layout_window)

		cancelButton.setIcon(QIcon.fromTheme("window-close"))
		defaultsButton.setIcon(QIcon.fromTheme("view-refresh"))
		quitButton.setIcon(QIcon.fromTheme("application-exit"))
		applyButton.setIcon(QIcon.fromTheme("document-save"))
		layoutButton.setIcon(QIcon.fromTheme("input-gaming"))

		cancelButton.setMinimumHeight(50)
		applyButton.setMinimumHeight(50)
		defaultsButton.setMinimumHeight(50)
		quitButton.setMinimumHeight(50)
		layoutButton.setMinimumHeight(50)

		scroll = QScrollArea()
		scroll.setWidgetResizable(True)
		widget = QWidget()
		vlayout = QVBoxLayout()

		hbox = QHBoxLayout()
		hbox.addWidget(quitButton)
		hbox.addWidget(defaultsButton)
		hbox.addWidget(layoutButton)
		hbox.addStretch(1)
		hbox.addWidget(cancelButton)
		hbox.addWidget(applyButton)
		
		vbox = QVBoxLayout()
		for i in read_settings('User_Settings'):
			for j in settings_variables():
				if i[0] == j[0]:
					self.createandmove(i[0], i[1], j[-1], i[-1], vlayout)

		self.createandmove(
			'New Layout File', 
			' Click to Create New Layout File ',
			'A new layout file will be created based on default layout (the app will restart after creating the file.)',
			str, vlayout
			)

		widget.setLayout(vlayout)
		scroll.setWidget(widget)

		qs = QScroller.scroller(scroll.viewport())
		props = qs.scrollerProperties()
		# props.setScrollMetric(QScrollerProperties.VerticalOvershootPolicy, QScrollerProperties.OvershootAlwaysOff)
		props.setScrollMetric(QScrollerProperties.DecelerationFactor, 0.35)
		props.setScrollMetric(QScrollerProperties.DragStartDistance, .001)
		qs.setScrollerProperties(props)
		qs.grabGesture(scroll.viewport(), QScroller.TouchGesture)
		# print(qs.scrollerProperties().scrollMetric(QScrollerProperties.DecelerationFactor))
		# print(qs.scrollerProperties().scrollMetric(QScrollerProperties.DragStartDistance))
		
		vbox.addWidget(scroll)
		vbox.addLayout(hbox)
		self.setLayout(vbox)
	
		w, h = self.screen_width*.9, self.screen_height*.8
		self.setGeometry((self.screen_width-w)/2, (self.screen_height-h)/2, w, h)
		self.setWindowTitle('Settings')
		# self.show()

	def restore_defaults(self):
		text = ("Do you want to restore all settings to default values?\n"
				"This step cannot be undone. Do you want to proceed?")
		result = self.show_dialog(text, 'Reset All Settings?')
		if result == 1:
			try:
				create_settings()
			except KeyboardInterrupt:
				sys.exit(1)
			self.parent.restart_program()

	def createandmove(self, label, value, text, value_type, box):
		lbl = label.replace('_', ' ')
		lbl = lbl.title()
		w = QWidget(self)
		h = QHBoxLayout()
		vbtn = None
		qbtn = QLabel(lbl, self)

		if value_type == int:
			if label == 'button_border_radius' or label == 'button_border_size' \
				or label == 'deadzone_border_size' or label == 'sticks_border_size' \
				or label == 'dpad_border_radius' or label == 'dpad_border_size' \
				or label == 'dpad_background_border_radius' or label == 'dpad_background_border_size':
				vbtn = QSpinBox()
				vbtn.setMinimum(0)
				vbtn.setMaximum(1000)
				vbtn.setSingleStep(1)
				vbtn.setValue(value)
				vbtn.valueChanged.connect(lambda: self.write_widget_value(label, vbtn.value()))
			if label == 'autorepeat_count':
				vbtn = QSpinBox()
				vbtn.setMinimum(1)
				vbtn.setMaximum(10)
				vbtn.setSingleStep(1)
				vbtn.setValue(value)
				vbtn.valueChanged.connect(lambda: self.write_widget_value(label, vbtn.value()))
			if label == 'button_width' or label == 'button_height':
				vbtn = QSpinBox()
				vbtn.setMinimum(1)
				vbtn.setMaximum(1000)
				vbtn.setSingleStep(10)
				vbtn.setValue(value)
				vbtn.valueChanged.connect(lambda: self.write_widget_value(label, vbtn.value()))
			if label == 'overlay_x_position' or label == 'overlay_y_position' \
				or label == 'overlay_width' or label == 'overlay_height' \
				or label == 'dpad_background_opacity' or label == 'deadzone' \
				or label == 'button_opacity':
				vbtn = QSpinBox()
				vbtn.setMinimum(0)
				vbtn.setMaximum(100)
				vbtn.setSingleStep(1)
				vbtn.setValue(value)
				vbtn.valueChanged.connect(lambda: self.write_widget_value(label, vbtn.value()))
		
		if value_type == float:
			if label == 'autorepeat_interval' or label == 'combo_interval':
				vbtn = QDoubleSpinBox()
				vbtn.setDecimals(3)
				vbtn.setMinimum(0.001)
				vbtn.setMaximum(10.0)
				vbtn.setSingleStep(0.01)
				vbtn.setValue(value)
				vbtn.valueChanged.connect(lambda: self.write_widget_value(label, vbtn.value()))
		
		if label == 'current_layout_file':
			vbtn = QComboBox()
			items = list(profiles_filelist)
			item1 = read_settings('User_Settings', 'current_layout_file')
			if items:
				if item1 in items:
					vbtn.addItem(item1)
					items.remove(item1)
			for p in items:
				vbtn.addItem(p)
			vbtn.currentIndexChanged.connect(lambda: self.write_widget_value(label, vbtn.currentText()))
		
		if value_type == str and value.startswith('#'):
			if len(value) == 7:
				vbtn = QPushButton()
				color_name = read_settings('User_Settings', label)
				stl = "background-color:%s;" % color_name
				vbtn.setStyleSheet(stl)
				vbtn.clicked.connect(lambda: self.get_color(label, vbtn))
		
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
		
		if label == 'New Layout File':
			vbtn = QPushButton()
			vbtn.setText(value)
			vbtn.clicked.connect(self.create_new_layout_file)

		ibtn = QPushButton()
		ibtn.setIcon(QIcon.fromTheme("dialog-information"))
		ibtn.setMinimumSize(QtCore.QSize(50, 50))
		ibtn.clicked.connect(lambda: self.show_dialog(text))
		h.addWidget(qbtn)

		if vbtn != None:
			vbtn.setMinimumSize(QtCore.QSize(200, 50))
			if value_type == bool:
				vbtn.setMinimumSize(QtCore.QSize(125, 50))
				vbtn.setStyleSheet(
					'QCheckBox::indicator {min-width:50;min-height:50;border-radius:25px;border:4px solid #555555;}'
					'QCheckBox::indicator:checked {background-color:green;}'
					'QCheckBox::indicator:unchecked {background-color:grey;}'
				)
			h.addStretch(1)
			h.addWidget(vbtn)
	
		h.addWidget(ibtn)
		w.setLayout(h)
		w.setMinimumHeight(70)
		w.setObjectName('SettingsRow')
		w.setStyleSheet('#SettingsRow { \
			background-color:#eeeeee;border: 1px solid #bbbbbb; \
			border-radius:5px; \
		}')
		box.addWidget(w)

	def on_apply_clicked(self):
		if self.changed_values:
			for v in self.changed_values:
				write_settings(*v)
			self.parent.restart_program()

	def write_widget_value(self, label, val):
		self.changed_values.append(('User_Settings', label, val))

	def get_color(self, label, btn):
		color = QColorDialog.getColor()
		if color.isValid():
			color = color.name()
			stl = "background-color:%s;" % color
			btn.setStyleSheet(stl)
			self.changed_values.append(('User_Settings', label, color))

	def show_dialog(self, text, title='Information'):
		d = Dialog(self, text, title)
		result = d.exec_()
		return result
		
	def closeEvent(self, event):
		event.accept()
		# self.parent.showpad()

	def cancel_settings(self):
		self.close()
		# self.parent.showpad()

	def  create_new_layout_file(self):
		text = ("Enter the name of new layout file below.\n"
				"E.g. MyLayout\n"
				"The app will restart after creating new file."
				)
		d = NewFileDialog(self, text)
		result = d.exec_()
		if result == 1:
			f = d.filename()
			if f != '':
				if len(f) < 5:
					f = f + '.conf'
				else:
					if f[-5] != '.conf':
						f = f + '.conf'
				create_new_layout(f)
				self.parent.restart_program()

class NewFileDialog(QDialog):
	def __init__(self, parent, text):
		super(NewFileDialog, self).__init__(parent)
		self.setModal(True)
		self.screen_resolution = QApplication.desktop().screenGeometry()
		self.screen_width, self.screen_height = self.screen_resolution.width(), self.screen_resolution.height()
		self.parent = parent
		self.text = text
		self.setStyleSheet('font-size:20px')
		self.initUI()
		
	def initUI(self):
		w = QLabel()
		w.setText(self.text)
		self.le = QLineEdit()

		hbox = QHBoxLayout()
		hbox.addStretch(1)

		self.buttons = QDialogButtonBox(
		   QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
		   QtCore.Qt.Horizontal, self)

		self.buttons.accepted.connect(self.accept)
		self.buttons.rejected.connect(self.reject)

		for b in self.buttons.buttons():
			b.setMinimumHeight(50)

		hbox.addWidget(self.buttons)
		vbox = QVBoxLayout()
		vbox.addWidget(w)
		vbox.addWidget(self.le)
		vbox.addSpacing(20)
		vbox.addLayout(hbox)
		self.setLayout(vbox)

		width, height = self.sizeHint().width(), self.sizeHint().height()
		pwidth = self.parent.parent.frameGeometry().width()
		pheight = self.parent.frameGeometry().height()
		self.setGeometry((pwidth-width)/2, (pheight-height)/2, width, height)
		self.setWindowTitle('Create New Layout File')

	def close_settings(self):
		self.close()

	def filename(self):
		return self.le.text()
		

class Dialog(QDialog):
	def __init__(self, parent, text, window_title='Information'):
		super(Dialog, self).__init__(parent)
		self.setModal(True)
		self.screen_resolution = QApplication.desktop().screenGeometry()
		self.screen_width, self.screen_height = self.screen_resolution.width(), self.screen_resolution.height()
		self.parent = parent
		self.text = text
		self.window_title = window_title
		self.setStyleSheet('font-size:20px')
		self.initUI()
		
	def initUI(self):
		w = QLabel()
		w.setOpenExternalLinks(True)
		w.setText(self.text)
		hbox = QHBoxLayout()
		hbox.addStretch(1)

		self.buttons = QDialogButtonBox(
		   QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
		   QtCore.Qt.Horizontal, self)

		self.buttons.accepted.connect(self.accept)
		self.buttons.rejected.connect(self.reject)

		for b in self.buttons.buttons():
			b.setMinimumHeight(50)

		hbox.addWidget(self.buttons)
		vbox = QVBoxLayout()
		vbox.addWidget(w)
		vbox.addSpacing(20)
		vbox.addLayout(hbox)
		self.setLayout(vbox)

		width, height = self.sizeHint().width(), self.sizeHint().height()
		if type(self.parent.parent).__name__ != 'TabPad':
			pwidth = self.screen_width
			pheight = self.screen_height
		else:
			pwidth = self.parent.parent.frameGeometry().width()
			pheight = self.parent.frameGeometry().height()
		self.setGeometry((pwidth-width)/2, (pheight-height)/2, width, height)
		self.setWindowTitle(self.window_title)

	def close_settings(self):
		self.close()

class InputDialog(QDialog):
	def __init__(self, parent):
		super(InputDialog, self).__init__(parent)
		self.setWindowFlags(QtCore.Qt.Window)
		self.setModal(True)
		self.screen_resolution = QApplication.desktop().screenGeometry()
		self.screen_width, self.screen_height = self.screen_resolution.width(), self.screen_resolution.height()
		self.parent = parent
		self.key_list = []
		self.click_list = []
		self.current_selection = []
		self.setStyleSheet('font-size:20px')
		self.initUI()
		
	def initUI(self):
		widget = QWidget()
		vbox = QVBoxLayout()
		leftlist = QListWidget()
		leftlist.setMaximumWidth(100)
		leftlist.insertItem (0, 'key' )
		leftlist.insertItem (1, 'click' )

		keystack = QWidget()
		clickstack = QWidget()

		syms = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b',
		'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 
		'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 
		'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 
		'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'Up', 'Down', 'Left', 
		'Right', 'Alt_L', 'Alt_R', 'BackSpace', 'Cancel', 'Caps_Lock', 'Control_L', 
		'Control_R', 'Shift_L', 'Shift_R', 'Tab', 'space', 'Delete', 'End', 
		'Super_L', 'Suprer_R', 'Return', 
		'Escape', 'Execute', 'F1', 'F2', 'F3', 'F4', 
		'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12', 'Fi',
		'KP_0', 'KP_1', 'KP_2', 'KP_3', 'KP_4', 'KP_5', 
		'KP_6', 'KP_7', 'KP_8', 'KP_9', 'KP_Add', 'KP_Begin', 'KP_Decimal', 
		'KP_Delete', 'KP_Divide', 'KP_Down', 'KP_End', 'KP_Enter', 'KP_Home', 
		'KP_Insert', 'KP_Left', 'KP_Multiply', 'KP_Next', 'KP_Prior', 'KP_Right', 
		'KP_Subtract', 'KP_Up', 
		'Home', 'Insert', 'Linefeed', 
		'Next', 'Num_Lock', 'Pause', 'Print', 'Prior', 
		'Scroll_Lock', 'exclam', 
		'quotedbl', 'numbersign', 'dollar', 'percent', 'ampersand', 'quoteright', 
		'parenleft', 'parenright', 'asterisk', 'plus', 'comma', 'minus', 'period', 
		'slash', 'colon', 'semicolon', 'less', 'equal', 'greater', 'question', 'at', 
		'grave', 'bracketleft', 'bracketright', 'backslash', 
		'apostrophe']

		click_types = ['1', '2', '3']

		self.btnstyle = 'background-color:#dddddd;font-size:24px;'

		self.keyUI(syms, keystack)
		self.clickUI(click_types, clickstack)

		self.Stack = QStackedWidget()
		self.Stack.addWidget(keystack)
		self.Stack.addWidget(clickstack)

		hbox = QHBoxLayout(self)
		hbox.addWidget(leftlist)
		hbox.addWidget(self.Stack)
		h = QHBoxLayout()

		deleteButton = QPushButton(" Delete Last Input")
		clearButton = QPushButton(" Clear All ")
		deleteButton.setMinimumHeight(50)
		clearButton.setMinimumHeight(50)

		deleteButton.clicked.connect(self.delete_last)
		clearButton.clicked.connect(self.clear_all)

		self.buttons = QDialogButtonBox(
		   QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
		   QtCore.Qt.Horizontal, self)

		self.buttons.accepted.connect(self.accept)
		self.buttons.rejected.connect(self.reject)

		self.buttons.setMinimumSize(QtCore.QSize(50, 50))
		for b in self.buttons.buttons():
			b.setMinimumSize(QtCore.QSize(50, 50))

		h.addWidget(clearButton)
		h.addWidget(deleteButton)
		h.addStretch(1)
		h.addWidget(self.buttons)
		widget.setLayout(hbox)

		selection_box = QHBoxLayout()
		self.selection_widget = QLabel(self.input_display_text())
		self.selection_widget.setMinimumHeight(50)
		self.selection_widget.setObjectName('SelectionWidget')
		self.selection_widget.setStyleSheet('#SelectionWidget { \
			background-color:#cccccc;border: 1px solid #aaaaaa; \
			border-radius:5px;color:blue; \
		}')

		selection_box.addStretch(1)
		selection_box.addWidget(self.selection_widget)
		selection_box.addStretch(1)
		vbox.addLayout(selection_box)
		vbox.addWidget(widget)
		vbox.addLayout(h)
		self.setLayout(vbox)
		leftlist.currentRowChanged.connect(self.display)

		w, h = self.screen_width*.9, self.screen_height*.8
		self.setGeometry((self.screen_width-w)/2, (self.screen_height-h)/2, w, h)
		self.setWindowTitle('Select Input(s). You can choose multiple keys/clicks.')

	def close_settings(self):
		self.close()

	def keyUI(self, syms, keystack):
		layout = QGridLayout()
		scroll = QScrollArea()
		scroll.setWidgetResizable(True)
		widget = QWidget()
		vbox = QVBoxLayout()
		widget.setLayout(layout)
		btn_list = []
		positions = [(i,j) for i in range(int(len(syms)/4)+1) for j in range(4)]
		for position, name in zip(positions, syms):
			kbtn = QPushButton(name)
			kbtn.setMinimumSize(QtCore.QSize(50, 50))
			kbtn.setStyleSheet(self.btnstyle)
			layout.addWidget(kbtn, *position)
			kbtn.clicked.connect(partial(self.all_keys_list, name, kbtn, 'key'))
		scroll.setWidget(widget)

		qs = QScroller.scroller(scroll.viewport())
		props = qs.scrollerProperties()
		props.setScrollMetric(QScrollerProperties.DecelerationFactor, 0.35)
		props.setScrollMetric(QScrollerProperties.DragStartDistance, .001)
		qs.setScrollerProperties(props)
		qs.grabGesture(scroll.viewport(), QScroller.TouchGesture)
		
		vbox.addWidget(scroll)
		keystack.setLayout(vbox)
			
	def clickUI(self, click_types, clickstack):
		layout = QVBoxLayout()
		widget = QWidget()
		hbox = QHBoxLayout()

		for name in click_types:
			cbtn = QPushButton(name)
			cbtn.setMinimumSize(QtCore.QSize(100, 50))
			cbtn.setStyleSheet(self.btnstyle)
			cbtn.clicked.connect(partial(self.all_keys_list, name, cbtn, 'click'))
			layout.addWidget(cbtn)
		
		widget.setLayout(layout)
		hbox.addStretch(1)
		hbox.addWidget(widget)
		hbox.addStretch(1)
		clickstack.setLayout(hbox)

	def display(self, i):
		self.Stack.setCurrentIndex(i)

	def all_keys_list(self, name, btn, input_type):
		label = btn.text()
		if label:
			self.key_list.append(input_type)
			self.key_list.append(label)
			self.selection_widget.setText(self.input_display_text())

	def input_display_text(self):
		if self.key_list:
			t = ' '.join(self.key_list)
		else:
			t = 'Nothing Selected'
		return t

	def delete_last(self):
		if self.key_list:
			del self.key_list[-2:]
			self.selection_widget.setText(self.input_display_text())

	def clear_all(self):
		if self.key_list:
			self.key_list = []
			self.selection_widget.setText(self.input_display_text())

	def all_input_values(self):
		return self.key_list

class LayoutSettings(QDialog):
	def __init__(self, parent):
		super(LayoutSettings, self).__init__()
		self.setWindowFlags(QtCore.Qt.Window)
		self.setModal(True)
		self.screen_resolution = QApplication.desktop().screenGeometry()
		self.screen_width, self.screen_height = self.screen_resolution.width(), self.screen_resolution.height()
		self.parent = parent
		self.setStyleSheet('font-size:20px')
		self.changed_values = []
		self.initUI()
		
	def initUI(self):      
		applyButton = QPushButton(" Apply ")
		quitButton = QPushButton(" Quit ")
		cancelButton = QPushButton(" Cancel ")
		defaultsButton = QPushButton(" Restore Defaults ")
		settingsButton = QPushButton(" Settings ")
		newButton = QPushButton(" NewButton ")
		helpButton = QPushButton(" Help ")

		cancelButton.clicked.connect(self.cancel_layout)
		applyButton.clicked.connect(self.on_apply_clicked)
		defaultsButton.clicked.connect(self.restore_defaults)
		quitButton.clicked.connect(self.parent.quithandler)
		settingsButton.clicked.connect(self.parent.show_settings_window)
		newButton.clicked.connect(self.show_new_button_dialog)
		helpButton.clicked.connect(self.show_help_button_dialog)

		cancelButton.setIcon(QIcon.fromTheme("window-close"))
		defaultsButton.setIcon(QIcon.fromTheme("view-refresh"))
		quitButton.setIcon(QIcon.fromTheme("application-exit"))
		applyButton.setIcon(QIcon.fromTheme("document-save"))
		settingsButton.setIcon(QIcon.fromTheme("preferences-other"))
		helpButton.setIcon(QIcon.fromTheme("help-contents"))
		newButton.setIcon(QIcon.fromTheme("list-add"))

		cancelButton.setMinimumHeight(50)
		applyButton.setMinimumHeight(50)
		defaultsButton.setMinimumHeight(50)
		quitButton.setMinimumHeight(50)
		settingsButton.setMinimumHeight(50)
		newButton.setMinimumHeight(50)
		helpButton.setMinimumHeight(50)

		scroll = QScrollArea()
		scroll.setWidgetResizable(True)
		widget = QWidget()
		vlayout = QVBoxLayout()

		hbox = QHBoxLayout()
		hbox.addWidget(quitButton)
		hbox.addWidget(helpButton)
		hbox.addWidget(defaultsButton)
		hbox.addWidget(settingsButton)
		hbox.addWidget(newButton)
		hbox.addStretch(1)
		hbox.addWidget(cancelButton)
		hbox.addWidget(applyButton)

		titlebox = QHBoxLayout()
		titlewidget = QWidget()
		titlewidget.setObjectName('TitleRow')
		titlewidget.setStyleSheet('#TitleRow { \
			background-color:#cccccc;border: 1px solid #aaaaaa; \
			border-radius:5px; \
		}')
		titlewidget.setMinimumSize(QtCore.QSize(50, 50))
		titletext = read_settings('User_Settings', 'current_layout_file')
		titletext = "Now editing  <font color='blue'>" + '<b>' + titletext + '</b>' + '</font> Profile'
		titlelabel = QLabel(titletext)
		titlebox.addStretch(1)
		titlebox.addWidget(titlelabel)
		titlebox.addStretch(1)
		titlewidget.setLayout(titlebox)
		vlayout.addWidget(titlewidget)

		all_layout_lists = read_layout('Layout')
		for i in all_layout_lists:
			self.createandmove(i[0], i[1], vlayout)
		
		widget.setLayout(vlayout)
		scroll.setWidget(widget)

		qs = QScroller.scroller(scroll.viewport())
		props = qs.scrollerProperties()
		props.setScrollMetric(QScrollerProperties.DecelerationFactor, 0.35)
		props.setScrollMetric(QScrollerProperties.DragStartDistance, .001)
		qs.setScrollerProperties(props)
		qs.grabGesture(scroll.viewport(), QScroller.TouchGesture)
		
		vbox = QVBoxLayout()
		vbox.addWidget(scroll)
		vbox.addLayout(hbox)
		self.setLayout(vbox)
		
		w, h = self.screen_width*.9, self.screen_height*.8
		self.setGeometry((self.screen_width-w)/2, (self.screen_height-h)/2, w, h)
		self.setWindowTitle('Change Gamepad Layout')
		# self.show()

	def createandmove(self, label, value, box):
		lbl = label.replace('_', ' ')
		lbl = lbl.title()
		w = QWidget(self)
		h = QHBoxLayout()

		behavior_list = ['normal', 'sticky', 'autorepeat', 'combo']
		keytype_list = ['key', 'click', '']
		click_types = ['1', '2', '3']
		cmd_list = []
		vbtn = None

		qbtn = QLabel(lbl, self)
		qbtn.setMinimumHeight(50)
		h.addWidget(qbtn)

		xbtn = QSpinBox()
		xbtn.setMinimumHeight(50)
		xbtn.setMinimum(-1)
		xbtn.setMaximum(100)
		xbtn.setSingleStep(1)
		xbtn.setValue(value[0])
		if value[0] < 0:
			xbtn.setEnabled(False)
			xbtn.setStyleSheet('background-color:#cccccc')
		h.addWidget(xbtn)
		xbtn.valueChanged.connect(lambda: self.write_widget_value(label, value, 0, xbtn.value()))

		ybtn = QSpinBox()
		ybtn.setMinimumHeight(50)
		ybtn.setMinimum(-1)
		ybtn.setMaximum(100)
		ybtn.setSingleStep(1)
		ybtn.setValue(value[1])
		if value[0] < 0:
			ybtn.setEnabled(False)
			ybtn.setStyleSheet('background-color:#cccccc')
		h.addWidget(ybtn)
		ybtn.valueChanged.connect(lambda: self.write_widget_value(label, value, 1, ybtn.value()))

		wbtn = QSpinBox()
		wbtn.setMinimumHeight(50)
		wbtn.setMinimum(0)
		wbtn.setMaximum(1000)
		wbtn.setSingleStep(1)
		wbtn.setValue(value[2])
		if value[0] < 0:
			wbtn.setEnabled(False)
			wbtn.setStyleSheet('background-color:#cccccc')
		h.addWidget(wbtn)
		wbtn.valueChanged.connect(lambda: self.write_widget_value(label, value, 2, wbtn.value()))
			
		hbtn = QSpinBox()
		hbtn.setMinimumHeight(50)
		hbtn.setMinimum(0)
		hbtn.setMaximum(1000)
		hbtn.setSingleStep(1)
		hbtn.setValue(value[3])
		if value[0] < 0:
			hbtn.setEnabled(False)
			hbtn.setStyleSheet('background-color:#cccccc')
		h.addWidget(hbtn)
		hbtn.valueChanged.connect(lambda: self.write_widget_value(label, value, 3, hbtn.value()))

		cbtn = QPushButton()
		cbtn.setMinimumHeight(50)
		stl = "background-color:%s;" % value[4]
		cbtn.setStyleSheet(stl)
		h.addWidget(cbtn)
		cbtn.clicked.connect(lambda: self.get_color(label, value, 4, cbtn))

		bbtn = QComboBox()
		bbtn.setMinimumHeight(50)
		items = list(behavior_list)
		item1 = value[5]
		if item1 == 'disabled':
			bbtn.setEnabled(False)
			bbtn.setStyleSheet('background-color:#cccccc')
		else:
			if items:
				if item1 in items:
					bbtn.addItem(item1)
					items.remove(item1)
			for p in items:
				bbtn.addItem(p)
		h.addWidget(bbtn)
		bbtn.currentIndexChanged.connect(lambda: self.write_widget_value(label, value, 5, bbtn.currentText()))

		l = []
		for v in range(6, len(value)):
			item = value[v]
			l.append(item)
			cmd_list = [label, value, v, l]
		if cmd_list:
			t = ' '.join(cmd_list[3])
			kbtn = QPushButton(t)
			kbtn.setMinimumHeight(50)
			if '' in cmd_list[3]:
				kbtn.setEnabled(False)
				kbtn.setText('Disabled')
				kbtn.setStyleSheet('background-color:#cccccc')
			h.addWidget(kbtn)
			kbtn.clicked.connect(lambda: self.keypicker(label, value, kbtn))

		rbtn = QPushButton("Remove")
		rbtn.setMinimumHeight(50)
		if label in default_button_layout.keys():
			rbtn.setEnabled(False)
			rbtn.setStyleSheet('background-color:#cccccc')
		rbtn.clicked.connect(lambda: self.delete_button_entry(label))
		h.addWidget(rbtn)
		
		w.setLayout(h)
		w.setObjectName('SettingsRow')
		w.setStyleSheet('#SettingsRow { \
			background-color:#eeeeee;border: 1px solid #bbbbbb; \
			border-radius:5px; \
		}')
		box.addWidget(w)

	def delete_button_entry(self, key):
		t = ("Are you sure you want to remove this custom button?\n"
			"This step cannot be undone. Proceed?"
			)
		d = Dialog(self, t, 'Remove Button?')
		r = d.exec_()
		if r == 1:
			delete_layout_key('Layout', key)
			self.parent.restart_program()

	def keypicker(self, label, value, btn):
		picker = InputDialog(self)
		result = picker.exec_()
		if result == 1:
			keys = picker.all_input_values()
		else:
			keys = None
		if keys:
			value[6:] = keys
			btn.setText(' '.join(keys))
			self.changed_values.append(('Layout', label, value))

	def on_apply_clicked(self):
		if self.changed_values:
			for v in self.changed_values:
				write_layout(*v)
			self.parent.restart_program()

	def write_widget_value(self, label, value_list, index, value):
		value_list[index] = value
		self.changed_values.append(('Layout', label, value_list))

	def get_color(self, label, value_list, index, btn):
		color = QColorDialog.getColor()
		if color.isValid():
			color = color.name()
			stl = "background-color:%s;" % color
			btn.setStyleSheet(stl)
			value_list[index] = color
			self.changed_values.append(('Layout', label, value_list))

	def restore_defaults(self):
		text = ("Do you want to restore all layout settings to default values?\n"
				'A fresh new "DefaultLayout.conf" file will be created and old one will be removed.\n' 
				"Your custom layout files won't be touched.\n"
				"This step cannot be undone. Do you want to proceed?")
		result = self.show_dialog(text, 'Reset All Buttons to Default Layout?')
		if result == 1:
			if os.path.isfile(default_layout_file):
				os.remove(default_layout_file)
			try:
				create_default_layout()
			except KeyboardInterrupt:
				sys.exit(1)

			write_settings('User_Settings', 'current_layout_file', 'DefaultLayout.conf')
			self.parent.restart_program()

	def show_dialog(self, text, title='Information'):
		d = Dialog(self, text, title)
		result = d.exec_()
		return result

	def show_new_button_dialog(self):
		d = NewButtonDialog(self)
		result = d.exec_()
		if result == 1:
			l = d.final_list()
			if l and l[0] not in layout_childkeys_only('Layout'):
				write_layout('Layout', l[0], l[1:])
				self.parent.restart_program()
			else:
				text = ("Error: Failed to create new button.\n\n"
					"It seems you havn't defined all the eight fields properly.\n"
					"Or you have entered a name same as an existing button.\n"
					"Please try again and make sure that all fields have values and the name is unused.")
				d = Dialog(self, text, 'Error: Cannot Create New Button.')
				result = d.exec_()

	def show_help_button_dialog(self):
		d = HelpButtonDialog(self)
		result = d.exec_()

	def closeEvent(self, event):
		event.accept()
		# self.parent.showpad()

	def cancel_layout(self):
		self.close()
		# self.parent.showpad()

class NewButtonDialog(QDialog):
	def __init__(self, parent):
		super(NewButtonDialog, self).__init__(parent)
		# self.setWindowFlags(QtCore.Qt.Window)
		self.setModal(True)
		self.screen_resolution = QApplication.desktop().screenGeometry()
		self.screen_width, self.screen_height = self.screen_resolution.width(), self.screen_resolution.height()
		self.parent = parent
		self.values = [None, 50, 50, 50, 50, None, 'normal', None]
		self.setStyleSheet('font-size:20px')
		self.initUI()
		
	def initUI(self):
		w = QLabel()
		text = 'Define properties of your new button below.'
		w.setText(text)
		hbox = QHBoxLayout()
		hbox.addStretch(1)

		self.buttons = QDialogButtonBox(
		   QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
		   QtCore.Qt.Horizontal, self)

		self.buttons.accepted.connect(self.accept)
		self.buttons.rejected.connect(self.reject)

		self.buttons.setMinimumSize(QtCore.QSize(50, 50))
		for b in self.buttons.buttons():
			b.setMinimumHeight(50)

		hbox.addWidget(self.buttons)
		vbox = QVBoxLayout()
		h = QHBoxLayout()
		vbox.addWidget(w)

		l = ['Name', 'X Positon', 'Y Position', 'Width', 'Height',
			'Color', 'Behavior', 'Input']
		behavior_list = ['normal', 'sticky', 'autorepeat', 'combo']

		for i in range(8):
			if i == 0:
				new_vbox = QVBoxLayout()
				new_widget = QWidget()
				lbl = QLabel(l[i])
				b = QLineEdit()
				b.setMinimumHeight(50)
				new_vbox.addWidget(lbl)
				new_vbox.addWidget(b)
				new_widget.setLayout(new_vbox)
				h.addWidget(new_widget)
				b.textChanged.connect(partial(self.write_widget_value, i, b.text))
			if i > 0 and i <= 4:
				new_vbox = QVBoxLayout()
				new_widget = QWidget()
				lbl = QLabel(l[i])
				b = QSpinBox()
				b.setMinimum(0)
				b.setMaximum(100)
				b.setSingleStep(1)
				b.setValue(50)
				b.setMinimumHeight(50)
				new_vbox.addWidget(lbl)
				new_vbox.addWidget(b)
				new_widget.setLayout(new_vbox)
				h.addWidget(new_widget)
				b.valueChanged.connect(partial(self.write_widget_value, i, b.value))
			if i == 5:
				new_vbox = QVBoxLayout()
				new_widget = QWidget()
				lbl = QLabel(l[i])
				b = QPushButton()
				b.setMinimumHeight(50)
				new_vbox.addWidget(lbl)
				new_vbox.addWidget(b)
				new_widget.setLayout(new_vbox)
				h.addWidget(new_widget)
				b.clicked.connect(partial(self.get_color, i, b))
			if i == 6:
				new_vbox = QVBoxLayout()
				new_widget = QWidget()
				lbl = QLabel(l[i])
				b = QComboBox()
				b.setMinimumHeight(50)
				b.addItem(behavior_list[0])
				b.addItem(behavior_list[1])
				b.addItem(behavior_list[2])
				new_vbox.addWidget(lbl)
				new_vbox.addWidget(b)
				new_widget.setLayout(new_vbox)
				h.addWidget(new_widget)
				b.currentIndexChanged.connect(partial(self.write_widget_value, i, b.currentText))
			if i == 7:
				new_vbox = QVBoxLayout()
				new_widget = QWidget()
				lbl = QLabel(l[i])
				b = QPushButton()
				b.setMinimumHeight(50)
				new_vbox.addWidget(lbl)
				new_vbox.addWidget(b)
				new_widget.setLayout(new_vbox)
				h.addWidget(new_widget)
				b.clicked.connect(partial(self.keypicker, i, b))

		vbox.addSpacing(10)
		vbox.addLayout(h)
		vbox.addSpacing(20)
		vbox.addLayout(hbox)
		self.setLayout(vbox)

		w, h = self.screen_width*.9, self.sizeHint().height()
		self.setGeometry((self.screen_width-w)/2, (self.screen_height-h)/2, w, h)
		self.setWindowTitle('Create a New Button')

	def close_settings(self):
		self.close()

	def write_widget_value(self, index, value):
		value = value()
		self.values[index] = value

	def get_color(self, index, btn):
		color = QColorDialog.getColor()
		if color.isValid():
			color = color.name()
			stl = "background-color:%s;" % color
			btn.setStyleSheet(stl)
			self.values[index] = color
	
	def keypicker(self, index, btn):
		picker = InputDialog(self)
		result = picker.exec_()
		if result == 1:
			keys = picker.all_input_values()
		else:
			keys = None
		if keys:
			self.values = self.values[:7]
			self.values = self.values + keys
			btn.setText(' '.join(keys))

	def final_list(self):
		for i in self.values:
			if i == None:
				self.values = []
				break
		return self.values

class HelpButtonDialog(QDialog):
	def __init__(self, parent):
		super(HelpButtonDialog, self).__init__(parent)
		self.setWindowFlags(QtCore.Qt.Window)
		self.setModal(True)
		self.screen_resolution = QApplication.desktop().screenGeometry()
		self.screen_width, self.screen_height = self.screen_resolution.width(), self.screen_resolution.height()
		self.parent = parent
		self.setStyleSheet('font-size:20px')
		self.initUI()
		
	def initUI(self):
		w = QLabel()
		text = 'Big wall of text below.'
		w.setText(text)
		hbox = QHBoxLayout()
		hbox.addStretch(1)

		self.buttons = QDialogButtonBox(
		   QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
		   QtCore.Qt.Horizontal, self)

		self.buttons.accepted.connect(self.accept)
		self.buttons.rejected.connect(self.reject)

		self.buttons.setMinimumSize(QtCore.QSize(50, 50))
		for b in self.buttons.buttons():
			b.setMinimumHeight(50)

		hbox.addWidget(self.buttons)
		vbox = QVBoxLayout()
		h = QHBoxLayout()
		vbox.addWidget(w)

		l = ['Name', 'X Positon', 'Y Position', 'Width', 'Height',
			'Color', 'Behavior', 'Input']
		behavior_list = ['normal', 'sticky', 'autorepeat', 'combo']

		for i in range(8):
			if i == 0:
				new_vbox = QVBoxLayout()
				new_widget = QWidget()
				lbl = QLabel(l[i])
				b = QLineEdit()
				b.setText('Z1')
				b.setMinimumHeight(50)
				new_vbox.addWidget(lbl)
				new_vbox.addWidget(b)
				new_widget.setLayout(new_vbox)
				h.addWidget(new_widget)
			if i > 0 and i <= 4:
				new_vbox = QVBoxLayout()
				new_widget = QWidget()
				lbl = QLabel(l[i])
				b = QSpinBox()
				b.setMinimum(0)
				b.setMaximum(100)
				b.setSingleStep(1)
				b.setValue(50)
				b.setMinimumHeight(50)
				new_vbox.addWidget(lbl)
				new_vbox.addWidget(b)
				new_widget.setLayout(new_vbox)
				h.addWidget(new_widget)
			if i == 5:
				new_vbox = QVBoxLayout()
				new_widget = QWidget()
				lbl = QLabel(l[i])
				b = QPushButton()
				b.setStyleSheet('background-color:green')
				b.setMinimumHeight(50)
				new_vbox.addWidget(lbl)
				new_vbox.addWidget(b)
				new_widget.setLayout(new_vbox)
				h.addWidget(new_widget)
			if i == 6:
				new_vbox = QVBoxLayout()
				new_widget = QWidget()
				lbl = QLabel(l[i])
				b = QComboBox()
				b.setMinimumHeight(50)
				b.addItem(behavior_list[0])
				b.addItem(behavior_list[1])
				b.addItem(behavior_list[2])
				new_vbox.addWidget(lbl)
				new_vbox.addWidget(b)
				new_widget.setLayout(new_vbox)
				h.addWidget(new_widget)
			if i == 7:
				new_vbox = QVBoxLayout()
				new_widget = QWidget()
				lbl = QLabel(l[i])
				b = QPushButton()
				b.setText('key D click 2')
				b.setMinimumHeight(50)
				new_vbox.addWidget(lbl)
				new_vbox.addWidget(b)
				new_widget.setLayout(new_vbox)
				h.addWidget(new_widget)

		scroll = QScrollArea()
		scroll.setWidgetResizable(True)
		widget = QLabel()
		widget.setWordWrap(True)
		
		t = ("<font color='blue'>Some fields in default buttons are disabled. "
			"This has been done on purpose to define a standard set of buttons. "
			"However, there are no such restrictions on creating a new button. "
			"If you want to hide an existing button, set its width and height to zero.</font><br><br>"

			"<b>Name:</b> Identification label for your button. "
			"You cannot change names of existing buttons. "
			"However you can always create a new button with any name.<br><br>"

			"<b>X Position:</b> Defines horizontal position of a button in terms of percentages of 'Overlay Width'. "
			"E.g., a value of 6 will postion a button horizontally at 6% of total overlay width value. "
			"Please note that overlay width may not be your screen width. " 
			"You can change overlay width in settings.<br><br>"

			"<b>Y Position:</b> Defines vertical position of a button in terms of percentages of 'Overlay Height'. "
			"E.g., a value of 30 will postion a button vertically at 30% of total overlay height value. "
			"Please note that overlay height may not be your screen height. " 
			"You can change overlay height in settings.<br><br>"

			"<b>Width:</b> Defines width of the button. "
			"If 'Override Button Size' is enabled in settings, this value will have no effect on button.<br><br>"

			"<b>Height:</b> Defines height of the button. "
			"If 'Override Button Size' is enabled in settings, this value will have no effect on button.<br><br>"

			"<font color='blue'><u>Tip:</u> To hide a button, set its width and height to zero.</font><br><br>"

			"<b>Color:</b> Sets the color of the button.<br><br>"

			"<b>Behavior:</b> Defines behavior of the button.<br>"
			"<font color='blue'>Some of the options below will only work if your game/emulator supports it.</font><br>"
			"<u>Normal:</u> Standard tap or long press on a button. "
			"Duplicate keys like 'Up, Up, Down, Down' will not work in this mode.<br>"
			"<u>Sticky:</u> Simulates press and hold behavior on a single press (continues unless stopped). "
			"Duplicate keys like 'Up, Up, Down, Down' will not work in this mode.<br>"
			"<u>Autorepeat:</u> Also known as rapid-fire/turbo. After touching once, it goes on and on, unless stopped. "
			"Duplicate keys like 'Up, Up, Down, Down' will not work in this mode.<br>"
			"<u>Combo:</u> Auto-executes keys one by one in a time interval defined in the settings. "
			"Once a combo starts, it cannot be interrupted until its done. "
			"Duplicate keys like 'Up, Up, Down, Down' will work in this mode if the game/emulator supports it.<br><br>"

			"<font color='blue'><u>Tip:</u> Tap on 'Stop All Inputs' to halt all sticky and autorepeating keys/clicks.</font><br><br>"			

			"<b>Input:</b> Choose one or multiple keys/clicks to be executed on a button press. "
			"You can even combine keys and clicks together. "
			"There are more than 150 options, so you can now execute all those 'Soul Calibur' combos in one hit.<br><br>"

			"<font color='blue'><u>Tip:</u> If you find that the app is crashing at startup,"
			" delete 'settings.conf' file in main app folder and 'DefaultLayout.conf'"
			" file in profiles folder and then relaunch the app.</font><br><br>"
			)
		widget.setText(t)
		widget.setContentsMargins(10,10,10,10)
		widget.setAlignment(QtCore.Qt.AlignJustify)
		widget.setStyleSheet('background-color:white;')

		scroll.setWidget(widget)
		scroll.setObjectName('scroll1')
		scroll.setStyleSheet('#scroll1 {background-color:white;}')

		qs = QScroller.scroller(scroll.viewport())
		props = qs.scrollerProperties()
		props.setScrollMetric(QScrollerProperties.DecelerationFactor, 0.35)
		props.setScrollMetric(QScrollerProperties.DragStartDistance, .001)
		qs.setScrollerProperties(props)
		qs.grabGesture(scroll.viewport(), QScroller.TouchGesture)

		vbox.addSpacing(10)
		vbox.addLayout(h)
		vbox.addSpacing(20)
		vbox.addWidget(scroll)
		vbox.addLayout(hbox)
		self.setLayout(vbox)

		w, h = self.screen_width*.9, self.sizeHint().height()
		self.setGeometry((self.screen_width-w)/2, (self.screen_height-h)/2, w, h)
		self.setWindowTitle('Help')

	def close_settings(self):
		self.close()