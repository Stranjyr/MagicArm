import rospy
from trajectory_msgs import JointTrajectory, JointTrajectoryPoint
import gampad_driver
import math

btnChecked = False
gripperOpen = False
pos = [0, 0, 0, 0, 0, 0, 0]
def scale(val, inMin, inMax, outMin, outMax):
		return (val-inMin)/(inMax-inMin)*(outMax-outMin) + outMin

def posFromGamepad(pad):
	if pad.states['BTN_SOUTH'] == 1 and btnChecked == False:
		pos[0] = (not gripperOpen)*math.pi
		gripperOpen = not gripperOpen
		btnChecked = False
	elif pad.states['BTN_SOUTH'] == 0 and btnChecked == True:
		btnChecked = False


	if pad.states['ABS_TL'] >  25:
		pos[1] -= scale(pad.states['ABS_TL'], 25.0, 255.0, 0.0, .1)
	elif pad.states['ABS_TR'] > 25:
		pos[1] += scale(pad.states['ABS_TL'], 25.0, 255.0, 0.0, .1)

	if abs(pad.states['ABS_X'] > 8000:
		pos[2] += scale(pad.states['ABS_X'], -33000.0, 33000.0, -.2, .2)
	if abs(pad.states['ABS_y'] > 8000:
		pos[3] += scale(pad.states['ABS_y'], -33000.0, 33000.0, -.2, .2)
	if abs(pad.states['ABS_RX'] > 8000:
		pos[4] += scale(pad.states['ABS_RX'], -33000.0, 33000.0, -.2, .2)
	if abs(pad.states['ABS_RY'] > 8000:
		pos[5] += scale(pad.states['ABS_RY'], -33000.0, 33000.0, -.2, .2)
	
	if pad.states['BTN_TL'] == 1:
		pos[6] -= 0.1
	if pad.states['BTN_TR'] == 1:
		pos[6] += 0.1

	for i in range(1, 7):
		pos[i] = max[0, min(math.pi, pos[i])]

def rosLoop():
	rospy.init_node("gamepad")
	jointPub = rospy.Publisher("magic_arm_joints", JointTrajectory, queue_size=10)
	pad = gampad_driver.Gamepad_Driver()
	joints = ('gripper', 'gripper_roll', 'wrist_roll', 'wrist_pitch', 'elbow_roll', 'elbow_pitch')
    r = rospy.Rate(.5)
    while not rospy.is_shutdown():
        msg = JointTrajectory()
        msg.header.stamp = rospy.Time.now()
        msg.header.frame_id = "magic_arm_joints"
        msg.joint_names = joints
        posFromGamepad()
        msg.points.positions = pos
        jointPub.publish(msg)
        r.sleep()

if __name__ == '__main__':
	rosLoop()