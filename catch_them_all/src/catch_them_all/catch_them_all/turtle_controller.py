#! /usr/bin/env python3

import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
import math


class TurtleController(Node):

    def __init__(self):
        super().__init__("turtle_controller")

        self.cmd_vel_pub_ = self.create_publisher(Twist,
                                                  "/turtle1/cmd_vel",
                                                  10)

        self.pose_subscriber_ = self.create_subscription(Pose,
                                                         "/turtle1/pose",
                                                         self.control_loop_,
                                                         10)

        self.target_set_flag = False

        self.get_logger().info("Turtle Controller has been started.")

    def set_target_(self):
        self.target_x = float(input("Target x: "))
        self.target_y = float(input("Target y: "))
        self.target_set_flag = True

    def control_loop_(self, msg: Pose):

        if not self.target_set_flag:
            self.set_target_()

        # vector to target
        dx = self.target_x - msg.x
        dy = self.target_y - msg.y
        distance = math.sqrt(dx**2 + dy**2)

        if (distance > 0.01):

            # desired angle
            desired_angle = math.atan2(dy, dx)  # output in radians

            # angle error
            angle_error = math.atan2(
                math.sin(
                    desired_angle -
                    msg.theta),
                math.cos(
                    desired_angle -
                    msg.theta))

            # compute velocities
            K_ANGLULAR = 2.0
            K_LINEAR = 1.5

            angular_velocity = K_ANGLULAR * angle_error
            linear_velocity = K_LINEAR * distance * math.cos(angle_error)

            # send command to cmd_vel topic
            twist_obj = Twist()
            twist_obj.linear.x = linear_velocity
            twist_obj.angular.z = angular_velocity

            self.cmd_vel_pub_.publish(twist_obj)
        else:
            self.cmd_vel_pub_.publish(Twist())
            self.target_set_flag = False


def main(args=None):

    node = None

    try:
        rclpy.init(args=args)
        node = TurtleController()
        rclpy.spin(node)
    except KeyboardInterrupt:
        print()
    except Exception as e:
        print(f"[-] An error occured: {e}")
    finally:
        if node is not None:
            node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
