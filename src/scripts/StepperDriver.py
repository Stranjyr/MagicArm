import RPi.GPIO as gpio
import time
import math
import numpy as np
class StepperDriver:
	def __init__(self, dirPin, stepPin, zeroPin, stepsToRot=1024):
		self.dirPin = dirPin
		self.stepPin = stepPin
		self.zeroPin = zeroPin

		self.steps = 0
		self.stepsToRot=stepsToRot
		#
		gpio.setwarnings(False)
		gpio.setmode (gpio.BCM)
		#outputs
		gpio.setup(self.dirPin, gpio.OUT)
		gpio.setup(self.stepPin, gpio.OUT)
		gpio.setup(self.zeroPin, gpio.IN)

	def step(self, dir):
		if dir == 1:
			gpio.output(self.dirPin, True)
		elif dir == -1:
			gpio.output(self.dirPin, False)
		else:
			return
		gpio.output(self.stepPin, True)
		time.sleep(0.0001)
		gpio.output(self.stepPin, False)
		self.steps+=dir

	def zero(self):
		return
		while gpio.input(self.zeroPin) == True:
			self.step(-1)
		self.steps = 0

	def currRads(self):
		return steps/self.stepsToRot*2*math.pi

	def turnRadians(self, rads):
		d = np.sign(rads)
		steps = abs(rads)*stepsToRot/(2*math.pi)
		for i in range(0, math.round(steps)):
			self.step(d)

	def turnTo(self, rads):
		if(rads < 0):
			rads = 0
		elif rads > 180:
			rads = 180
		delta = rads-self.currRads()
		self.turnRadians(delta)

	def close(self):
		gpio.cleanup()

if __name__ == '__main__':
	s = StepperDriver(6, 5, 23)
	try:
		while True:
			for i in range(0, 10000):
				s.step(1)
			for i in range(0, 1000):
				s.step(-1)
	except KeyboardInterrupt:
		print "DONE"
		s.close()