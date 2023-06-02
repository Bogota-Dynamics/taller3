import rclpy
import serial
import serial.tools.list_ports
import math
from rclpy.node import Node
from geometry_msgs.msg import Vector3
from scipy.optimize import fsolve


class RobotManipulatorPlanner(Node):
    def __init__(self):
        super().__init__('robot_manipulator_planner')
        self.subscription = self.create_subscription(
            Vector3,
            '/robot_manipulator_goal',
            self.goal_callback,
            10
        )
        # Encontrar puerto automáticamente
        ports = list(serial.tools.list_ports.comports())
        arduino_port = ports[0].device

        self.arduino = serial.Serial(port=arduino_port, baudrate=250000, timeout=.1)
    
    def goal_callback(self, msg):
        target_x = msg.x 
        target_y = msg.y 
        z = msg.z

        L1 = 12.2
        L2 = 15

        # Calculate the distance from the origin to the target point
        distance = math.sqrt(target_x**2 + target_y**2)

        # Check if the target point is reachable
        if distance > L1 + L2:
            print("Target point is out of reach")
            return None

        # Calculate the angle between the line connecting the origin and the target point
        # and the line connecting the origin and the intersection point of the two links
        alpha = math.acos((L1**2 + distance**2 - L2**2) / (2 * L1 * distance))

        # Calculate the angle between the line connecting the target point and the intersection point
        # and the line connecting the target point and the x-axis
        beta = math.atan2(target_y, target_x)

        # Calculate the joint angles
        theta1 = math.fabs(alpha-beta)
        theta2 = math.pi - math.acos((L1**2 + L2**2 - distance**2) / (2 * L1 * L2))

        # Convert the angles to degrees
        theta1 = math.degrees(theta1)
        theta2 = math.degrees(theta2) + 90


        theta3=0

        x1 = L1 * math.cos(math.radians(theta1)) + L2 * math.cos(math.radians(theta1 + theta2))
        y1 = L1 * math.sin(math.radians(theta1)) + L2 * math.sin(math.radians(theta1 + theta2))
        print(x1,y1)

        mensaje = f'{theta1},{theta2},{theta3}'
        print(mensaje)

        self.write(mensaje)

    def write(self, x):
        self.arduino.write(bytes(x, 'utf-8'))
        print(self.arduino.readline().decode('utf-8'))  
        print("Done")


def main(args=None):
    rclpy.init(args=args)
    robot_manipulator_planner = RobotManipulatorPlanner()
    rclpy.spin(robot_manipulator_planner)
    robot_manipulator_planner.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
