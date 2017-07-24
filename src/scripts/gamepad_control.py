from inputs import get_gamepad
import serial
import threading
import time
class ArmControl:
	def __init__(self, port):
		self.port = port
		self.ser = serial.Serial(port=self.port, timeout=1, baudrate=19200)
		serial.Serial()
		serial.Serial()
		print(self.ser.isOpen())

		#              LX RX LY RY
		self.joyPos = [0, 0, 0, 0]
		#              A  B  Y  X
		self.btnPos = [0, 0, 0, 0]
		self.triPos = [0, 0]
		self.update = threading.Condition()
		self.joyNames = ['ABS_Y', 'ABS_X', 'ABS_RY', 'ABS_RX']
		self.btnNames = ['BTN_SOUTH', 'BTN_EAST', 'BTN_WEST', 'BTN_NORTH']
		self.triNames = ['ABS_Z', 'ABS_RZ']
		self.gamepadThread = None
		self.gripperChecked = False
		self.servos = {}
		for i in range(8, 14):
			self.servos[i] = 90
		self.lastServos  = {}
		for i in range(8, 14):
			self.lastServos[i] = 0

	def start(self):
		self.gamepadThread = threading.Thread(target = self.gamepadCapture)
		self.gamepadThread.daemon = True
		self.gamepadThread.start()
		time.sleep(.1)
		try:
			while "READY" not in self.ser.readline():
				print('WAIT')
			print("READY")
			while True:
				changed = self.updateServos()
				for c in changed:
					print('H{} {}T'.format(c, self.servos[c]))
					self.ser.write(' H{} {}T'.format(c, self.servos[c]))
					back = self.ser.readline();
					print(back)
					if "BAD VALUE" in back:
						while "REREADY" not in self.ser.readline():
							print('WAIT')
						print("READY")
					time.sleep(0.01)
		except KeyboardInterrupt:
			print 'Done'
	def gamepadCapture(self):
		while 1:
			events = get_gamepad()
			for e in events:
				if e.ev_type == 'Absolute':
					if e.code in self.joyNames:
						self.joyPos[self.joyNames.index(e.code)] = e.state 
					elif e.code in self.triNames:
						self.triPos[self.triNames.index(e.code)] = e.state
				elif e.ev_type == 'Key':
					if e.code in self.btnNames:
						self.btnPos[self.btnNames.index(e.code)] = e.state
	def updateServos(self):
		for i, j in enumerate(self.joyPos):
			if abs(j) > 8000:
				self.servos[i+10] += int(self.scale(j, 33000.0, -33000.0, 5.0, -5.0))
				self.servos[i+10] = max(0, min(180, self.servos[i+10]))
		if self.triPos[0] > 20:
			self.servos[9] -= int(self.scale(self.triPos[0], 255.0, 0.0, 5.0, 0.0))
			self.servos[9] = max(0, self.servos[9])
		elif self.triPos[1] > 20:
			self.servos[9] += int(self.scale(self.triPos[1], 255.0, 0.0, 5.0, 0.0))
			self.servos[9] = min(180, self.servos[9])
		if self.btnPos[0] == 1 and self.gripperChecked == False:
			self.servos[8] = (not bool(self.servos[8]))*180
			self.gripperChecked = True
		elif self.btnPos[0] == 0 and self.gripperChecked == True:
			self.gripperChecked = False
		ch = [i for i in self.servos if self.servos[i] != self.lastServos[i]]
		self.lastServos = dict(self.servos)
		return ch

	def scale(self, val, inMax, inMin, outMax, outMin):
		return (val-inMin)/(inMax-inMin)*(outMax-outMin) + outMin

if __name__ == '__main__':
	ac = ArmControl('/dev/ttyUSB0')
	ac.start()