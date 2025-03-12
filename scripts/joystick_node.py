import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray
from sensor_msgs.msg import Joy, JointState
import numpy as np

class JoystickNode(Node):
    def __init__(self):
        super().__init__('joystick_node')
        self.joy_sub = self.create_subscription(Joy, 'joy', self.joy_callback, 1)
        self.joint_state_pub = self.create_publisher(JointState, '/voyager/servos', 1)
        self.thrust_pub = self.create_publisher(Float64MultiArray, '/voyager/thrusters', 1)
        self.servo_sub = self.create_subscription(JointState, '/voyager/servo_state', self.servo_callback, 1)

        self.angles = [0, 0] # port, starboard
        self.velocities = [0, 0] # port, starboard

        self.get_logger().info('Joystick node started')

    def servo_callback(self, msg: JointState):
        self.angles = msg.position
        self.velocities = msg.velocity

    def joy_callback(self, msg: Joy):
        gain = 2
        joint_state_msg = JointState()
        names = ['Voyager/azimuth_port_joint', 'Voyager/azimuth_starboard_joint']
        joint_state_msg.name = names
        port_x = msg.axes[1]
        port_y = -msg.axes[0]
        star_x = msg.axes[4]
        star_y = -msg.axes[3]

        tunnel = (msg.axes[2] - msg.axes[5]) / 2 * gain
        star_force = np.hypot(star_x, star_y) * gain
        port_force = np.hypot(port_x, port_y) * gain
        
        star_angle = np.arctan2(star_y, star_x)
        port_angle = np.arctan2(port_y, port_x)
        vel_port, vel_star = self.calculate_azimuth_velocity(port_angle, star_angle)
        joint_state_msg.velocity = [vel_port, vel_star]

        force_msg = Float64MultiArray()
        force_msg.data = [port_force, star_force, tunnel]
        self.joint_state_pub.publish(joint_state_msg)
        self.thrust_pub.publish(force_msg)

    def calculate_azimuth_velocity(self, ref_port, ref_star):
        kp = 2
        kd = 0.2
        e_star = self.ssa(ref_star - self.angles[1])
        e_port = self.ssa(ref_port - self.angles[0])
        vel_port = kp * e_port + kd * self.velocities[0]
        vel_star = kp * e_star + kd * self.velocities[1]
        return vel_port, vel_star

    @staticmethod
    def ssa(angle):
        return (angle + np.pi) % (2 * np.pi) - np.pi
    

def main(args=None):
    rclpy.init(args=args)
    node = JoystickNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()