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

        theta1 =1
        theta2 = 0
        theta3 =0


        
        mensaje = f'{theta1},{theta2},{theta3}'

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
