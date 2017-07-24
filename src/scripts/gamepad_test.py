from inputs import get_gamepad

def joystickTest():
	x1, x2, y1, y2 = 0, 0, 0, 0
	while 1:
		events = get_gamepad()
		for e in events:
			print (e.ev_type, e.code, e.state)

if __name__ == '__main__':
	try:
		joystickTest()
	except KeyboardInterrupt:
		print("done")

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