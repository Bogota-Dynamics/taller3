import rclpy
import serial
import serial.tools.list_ports
import math
from rclpy.node import Node
from geometry_msgs.msg import Vector3

class RobotManipulatorPlanner(Node):
    def __init__(self):
        super().__init__('robot_manipulator_planner')
        self.subscription = self.create_subscription(
            Vector3,
            '/robot_manipulator_goal',
            self.goal_callback,
            10
        )
        #Encontrar puerto Automaticamente
        ports = list(serial.tools.list_ports.comports())
        arduino_port = ports[0].device

        self.arduino = serial.Serial(port=arduino_port, baudrate=250000,timeout=.1)
    
    def goal_callback(self, msg):
        
        x = msg.x
        y = msg.y
        z = msg.z

        a1 = 0.122  
        a2 = 0.149 


        costheta2 = (1/(2*a1*a2))*(((x**2)*(y**2))-((a1**2)+a2**2))
        sentheta2 = math.sqrt(1-(costheta2**2))

        costheta1 = (1/((x**2)+(y**2)))*(x*(a1+a2*costheta2)+y*a2*math.sqrt(1-(costheta2**2)))
        sentheta1 = (1/((x**2)+(y**2)))*(y*(a1+a2*costheta2)+x*a2*math.sqrt(1-(costheta2**2)))


        r = math.sqrt(x**2 + y**2)

        cos_theta2 = (r**2 - a1**2 - a2**2) / (2 * a1 * a2)
        sin_theta2 = math.sqrt(1 - cos_theta2**2)

        theta2 = math.atan2(sin_theta2, cos_theta2)*(180/math.pi)
        theta1 = (math.atan2(y, x) - math.atan2(a2 * sin_theta2, a1 + a2 * cos_theta2))*(180/math.pi)






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
