import rclpy
import serial
import serial.tools.list_ports
import math
from rclpy.node import Node
from geometry_msgs.msg import Vector3
from scipy.optimize import fsolve


class RobotManipulatorLego(Node):
    def __init__(self):
        super().__init__('robot_manipulator_lego')
        self.subscription = self.create_subscription(
            Vector3,
            '/robot_manipulator_zone',
            self.goal_callback,
            10
        )
        # Encontrar puerto automáticamente
        ports = list(serial.tools.list_ports.comports())
        arduino_port = ports[0].device

        self.arduino = serial.Serial(port=arduino_port, baudrate=250000, timeout=.1)
    
    def lego(self):

        L1 = 12.2
        L2 = 15

        
        theta1 = 90 
        theta2 = 180
        theta3= 170

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
    robot_manipulator_lego = RobotManipulatorLego()
    rclpy.spin(robot_manipulator_lego)
    robot_manipulator_lego.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
