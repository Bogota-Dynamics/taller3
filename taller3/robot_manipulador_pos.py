import rclpy
import serial
import serial.tools.list_ports
import numpy as np
from rclpy.node import Node
from math import pi, cos, sin

from geometry_msgs.msg import Twist



class PositionPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(Twist, 'robot_cmPos', 10)
        timer_period = 0.2  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

        self.pos_x = 0
        self.pos_y = 0
        self.angulo1 = 0
        self.angulo2 = 0


        #Conectar arduino automaticamente 
        ports = list(serial.tools.list_ports.comports())
        arduino_port = ports[0].device
        self.arduino = serial.Serial(port=arduino_port, baudrate=250000,timeout=.1)

    def timer_callback(self):      
        if self.arduino.in_waiting>0:
            line = self.arduino.readline().decode('utf-8')
            line = line.split(",")
            self.angulo1 = float(line[0])
            self.angulo2 = float(line[1])
            self.posicionManipulador()

        msg = Twist()
        msg.linear.x = float(self.pos_x)
        msg.linear.y = float(self.pos_y)
        print(msg)
        self.publisher_.publish(msg)
    

    def posicionManipulador(self):
        
        ang1 = self.angulo1*pi/180
        ang2 = (self.angulo2-90)*pi/180


        T1 = [[cos(ang1), -sin(ang1), 0],
              [sin(ang1), cos(ang1), 0],
              [0, 0, 1]]
        
        T2 = [[cos(ang2), -sin(ang2), 12.2],
              [sin(ang2), cos(ang2), 0],
              [0, 0, 1]]
        
        T3 = [[1, 0, 14.9],
              [0, 1, 0],
              [0, 0, 1]]

        resp = np.dot(np.dot(np.dot(T1, T2), T3), [[0],[0],[1]])
        
        self.pos_x = round(resp[0][0], 2)
        self.pos_y = round(resp[1][0], 2)

def main(args=None):
    rclpy.init(args=args)
    minimal_publisher = PositionPublisher()
    rclpy.spin(minimal_publisher)
    minimal_publisher.destroy_node()
    rclpy.shutdown()
    


if __name__ == '__main__':
    main()