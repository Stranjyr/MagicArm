from inputs import get_gamepad
import threading


class Gamepad_Driver:
	def __init__(self):
		self.states = {['ABS_Y', 0], ['ABS_X', 0], ['ABS_RY', 0], ['ABS_RX', 0],
		['BTN_TR', 0], ['BTN_TL', 0], ['BTN_THUMBR', 0], ['BTN_THUMBL', 0], 
		['BTN_START', 0], ['BTN_SELECT', 0], ['ABS_HAT0X', 0], ['ABS_HAT0Y', 0],
		['BTN_SOUTH', 0], ['BTN_EAST', 0], ['BTN_WEST', 0],  ['BTN_NORTH', 0],
		['ABS_Z',0], ['ABS_RZ', 0]}

		self.update = threading.Condition()
		self.gamepadThread = None

	def start(self):
		self.gamepadThread = threading.Thread(target = self.gamepadCapture)
		self.gamepadThread.daemon = True
		self.gamepadThread.start()
	
	def gamepadCapture(self):
		while 1:
			events = get_gamepad()
			for e in events:
				if e.code in self.states:
					self.states[e.code] = e.state 

'''
Buttons
ev_type = Key
state: 
	press   = 1
	release = 0
code:
	A = BTN_SOUTH
	B = BTN_EAST
	Y = BTN_WEST
	X = BTN_NORTH
	RIGHT BUMPER = BTN_TR
	LEFT BUMPER  = BTN_TL
	RIGHT THUMBPRESS = BTN_THUMBR
	LEFT THUMBPRESS  = BTN_THUMBL
	START =  BTN_START
	SELECT = BTN_SELECT

Thumbsticks
ev_type = Absolute
state:
	LEFT/UP    = -33000
	RIGHT/DOWN = 33000
code:
	LEFT JOYSTICK X = ABS_X
	LEFT JOYSTICK Y = ABS_Y
	RIGHT JOYSTICK X = ABS_RX
	RIGHT JOYSTICK Y = ABS_RY


D PAD
ev_type = Absolute
state:
	Release = 0
	LEFT/UP = -1
	RIGHT/DOWN = 1
code:
	LEFT/RIGHT D PAD = ABS_HAT0X
	UP/DOWN D PAD    = ABS_HAT0Y


Triggers
ev_type = Absolute
state:
	RELEASED = 0
	FULL PRESS = 255
code:
	RIGHT TRIGGER = ABS_RZ
	LEFT TRIGGER  = ABS_Z
'''	