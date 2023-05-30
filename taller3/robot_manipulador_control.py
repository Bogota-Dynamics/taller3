import rclpy
import serial
import serial.tools.list_ports
from rclpy.node import Node
from my_msgs.msg import Manipulator

class robot_manipulador_control(Node):

    def __init__(self):
        super().__init__('robot_manipulador_control')
        self.subscription = self.create_subscription(
            Manipulator,
            'robot_manipulator_angles',
            self.listener_callback,
            10)
    

        #Encontrar puerto Automaticamente
        ports = list(serial.tools.list_ports.comports())
        arduino_port = ports[0].device

        self.arduino = serial.Serial(port=arduino_port, baudrate=250000,timeout=.1)
    

    def listener_callback(self, msg):

        servo1 = msg.angle1
        servo2 = msg.angle2
        servo3 = msg.angle3

        mensaje = f'{servo1},{servo2},{servo3}'

        self.write(mensaje)

        
    def write(self, x):
        self.arduino.write(bytes(x, 'utf-8'))  
        print("Done")


def main(args=None):
    rclpy.init(args=args)
    interface = robot_manipulador_control()
    rclpy.spin(interface)
    interface.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()