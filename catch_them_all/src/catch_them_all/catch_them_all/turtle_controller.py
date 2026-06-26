#! /usr/bin/env python3

import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
import math
from interfaces.msg import TurtleArray, Turtle
from interfaces.srv import CatchTurtle


class TurtleController(Node):

    def __init__(self):

        super().__init__("turtle_controller")
        self.declare_parameter("catch_closest_turtle", True)
        self.declare_parameter("K_ANGULAR_BASE", 1.0)
        self.declare_parameter("K_LINEAR_BASE", 1.0)
        self.declare_parameter("GROWTH_RATE", 0.05)  # 5% increase per catch
        self.declare_parameter("MAX_MULTIPLIER", 5.0)  # cap so it doesn't get absurd

        self.pose_: Pose = None
        self.target_turtle_: Turtle = None
        self.catch_closest_turtle_ = self.get_parameter("catch_closest_turtle").value
        self.caught_turtles_ = []
        self.number_turtles_caught_ = 0

        self.cmd_vel_pub_ = self.create_publisher(Twist,
                                                  "/turtle1/cmd_vel",
                                                  10)

        self.pose_sub_ = self.create_subscription(Pose,
                                                  "/turtle1/pose",
                                                  self.callback_pose_,
                                                  10)

        self.alive_turtles_sub_ = self.create_subscription(
            TurtleArray, "alive_turtles", self.callback_alive_turtles_, 10)

        self.catch_turtle_client_ = self.create_client(CatchTurtle, "catch_turtle")

        self.control_loop_timer_ = self.create_timer(0.01, self.control_loop_)

        self.get_logger().info("Turtle Controller has been started.")

    def callback_pose_(self, pose: Pose):
        self.pose_ = pose

    def callback_alive_turtles_(self, alive_turtles: TurtleArray):
        if len(alive_turtles.turtles) > 0:
            if self.catch_closest_turtle_:
                closest_turtle = None
                closest_turtle_distance = None

                for turtle in alive_turtles.turtles:
                    dx = turtle.x - self.pose_.x
                    dy = turtle.y - self.pose_.y
                    distance = math.sqrt(dx**2 + dy**2)

                    if closest_turtle is None or distance < closest_turtle_distance:
                        closest_turtle = turtle
                        closest_turtle_distance = distance
                else:
                    if closest_turtle.name not in self.caught_turtles_:  # ignoring duplicate targets due to race conditions
                        self.target_turtle_ = closest_turtle
            else:
                self.target_turtle_ = alive_turtles.turtles[0]

    def send_catch_turtle_request_(self, name):
        req = CatchTurtle.Request()
        req.turtle_name = name
        future = self.catch_turtle_client_.call_async(req)
        future.add_done_callback(
            lambda future: self.callback_catch_turtle_response_(
                future, request=req))

    def callback_catch_turtle_response_(self, future, request):
        res = future.result()

        if res.success:
            self.get_logger().info(
                f"{request.turtle_name} successfully elimated and cleared from sim!")
        else:
            self.get_logger().error(f"Unsuccessful in eliminating {request.turtle_name}!")

    def get_scaled_constants(self):
        GROWTH_RATE = self.get_parameter("GROWTH_RATE").value
        MAX_MULTIPLIER = self.get_parameter("MAX_MULTIPLIER").value
        K_ANGULAR_BASE = self.get_parameter("K_ANGULAR_BASE").value
        K_LINERA_BASE = self.get_parameter("K_LINEAR_BASE").value
        multiplier = min(1 + GROWTH_RATE * self.number_turtles_caught_, MAX_MULTIPLIER)
        k_angular = K_ANGULAR_BASE * multiplier
        k_linear = K_LINERA_BASE * multiplier
        return k_angular, k_linear

    def control_loop_(self):

        if self.target_turtle_ and self.pose_:

            # vector to target
            dx = self.target_turtle_.x - self.pose_.x
            dy = self.target_turtle_.y - self.pose_.y
            distance = math.sqrt(dx**2 + dy**2)

            if (distance > 0.5):

                # desired angle
                desired_angle = math.atan2(dy, dx)  # output in radians

                # angle error
                angle_error = math.atan2(
                    math.sin(
                        desired_angle -
                        self.pose_.theta),
                    math.cos(
                        desired_angle -
                        self.pose_.theta))

                # compute velocities
                K_ANGLULAR, K_LINEAR = self.get_scaled_constants()

                angular_velocity = K_ANGLULAR * angle_error
                linear_velocity = K_LINEAR * distance * math.cos(angle_error)

                # send command to cmd_vel topic
                twist_obj = Twist()
                twist_obj.linear.x = linear_velocity
                twist_obj.angular.z = angular_velocity

                self.cmd_vel_pub_.publish(twist_obj)
            else:
                self.cmd_vel_pub_.publish(Twist())
                self.caught_turtles_.append(self.target_turtle_.name)
                self.number_turtles_caught_ += 1
                while not self.catch_turtle_client_.service_is_ready():
                    self.get_logger().warn("waiting for catch turtle service!")
                else:
                    self.send_catch_turtle_request_(self.target_turtle_.name)
                    self.target_turtle_ = None


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
