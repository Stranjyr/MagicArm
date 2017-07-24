import math

class MagicArm:
	def __init__(self, stepperVals, servoVals, servoNames, servoDefaults = None):
		self.stepper = StepperDriver(*stepperVals)
		self.servos = {}
		for i, s in enumerate(servoVals):
			self.servos[servoNames[i]] = ServoDriver(*servoVals[i])
		self.defaults = []
		if defaults == None:
			for i in range(len(self.servos)):
				self.defaults.append(self.servos[i].max_angle/2)

	def start(self):
		for i, s in enumerate(self.servos):
			s.set_angle(math.degrees(self.defaults[i]))
		self.stepper.zero()

	def close(self):
		self.stepper.close()

	#Pass a list of tuples in the form:
	#	(Joint_Name, AngleToReach)
	#
	#Where the names are defined in the constructor, 
	#	save for the stepper which is designated 'shoulder'
	#
	#And the angles are in radians
	def moveJoints(self, movements):
		for i in movements:
			if i[0] in self.servos:
				self.servos[i[0]].set_angle(math.degrees(i[1]))
			elif i[0] == 'shoulder':
				self.stepper.turnTo(i[1])