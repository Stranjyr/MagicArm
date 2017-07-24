import rospy
from trajectory_msgs import JointTrajectory, JointTrajectoryPoint
class MagicArmRosWrapper:
	def __init__(self, stepperVals, servoVals, servoNames,  servoDefaults = None):
		self.controller = MagicArm(stepperVals, servoVals, servoNames, servoDefaults)
		self.position_sub = rospy.Subscriber("magic_arm_joints", JointTrajectory, self.setJoints)
	def setJoints(self, data):
		self.controller.moveJoints(zip(data.joint_names, data.points.positions))

if __name__ == '__main__':
	ma = MagicArmRosWrapper((5, 6, 23), 
		((8, 198, 185, 553), 
			(9, 198, 185, 553), 
			(10, 198, 185, 553), 
			(11, 198, 185, 553), 
			(12, 198, 209, 578), 
			(13, 198, 209, 578)), 
		('gripper', 'gripper_roll', 'wrist_roll', 'wrist_pitch', 'elbow_roll', 'elbow_pitch'))
	ma.start()
	while not rospy.is_shutdown():
		rospy.sleep(0.01)
	ma.close()

magicword