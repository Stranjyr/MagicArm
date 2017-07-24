import Adafruit_PCA9685
class ServoDriver:
    def __init__(self, channel, max_angle = 120, servo_min = 150, servo_max = 600):
        self.servo = Adafruit_PCA9685.PCA9685()
        self.channel = channel
        self.max_angle = max_angle
        # Configure min and max servo pulse lengths
        self.servo_min = servo_min  # Min pulse length out of 4096
        self.servo_max = servo_max  # Max pulse length out of 4096
        self.servo.set_pwm_freq(60)

        
    #Set the servo position by providing an angle
    def set_angle(self, deg):
        pulseEnd = int((deg/self.max_angle)*(self.servo_max - self.servo_min)+self.servo_min)
        self.servo.set_pwm(self.channel, 0, pulse)

if __name__ == '__main__':
    channel = int(raw_input("Enter Servo Channel::  "))
    maxAng = int(raw_input("Enter the maximum angle::  "))
    s = ServoDriver.ServoDriver(channel, maxAng)
    try:
        while True:
            s.set_servo_angle(0)
            time.sleep(1)
            s.set_servo_angle(maxAng)
            time.sleep(1)
    except KeyboardInterrupt:
        print("Done")