#! /usr/bin/env python3

"""
Description:
This ROS2 node periodically publishes user specified message (defaults to "Hello, World!")
to a topic at a sepecified rate (defaults to 1.0Hz).
---
Publishes to: /my_topic (std_msgs/msg/String)
---
Subscribes to: None
---
Usage Example:
-> ros2 run params pub_with_params.py --ros-args -p message:="I'm BATMAN" -p timer_period:=0.5
---
Author: Sai C Akella
Date: 28/05/2026
"""

import rclpy
from rclpy.node import Node
from rclpy.executors import ExternalShutdownException
from std_msgs.msg import String
from rcl_interfaces.msg import ParameterDescriptor


class PublisherWithParams(Node):

    def __init__(self):

        # call the node class constructor with the node name
        super().__init__("pub_with_params")

        # declare params
        self.declare_parameter('message', 'Hello, World!',
                               ParameterDescriptor(description="Message that will be published."))
        self.declare_parameter('timer_period', 1.0,  # data type matters 1 != 1.0
                               ParameterDescriptor(description="Rate at which messages are published."))

        # set parameters
        self._message = self.get_parameter('message').value
        self._timer_period = self.get_parameter('timer_period').value

        # configure callback for runtime parameter update
        self.add_post_set_parameters_callback(self._post_set_paramater_callback)

        # create a publisher obj
        self._publisher = self.create_publisher(String, "my_topic", 10)
        # periodically call method
        self._timer = self.create_timer(self._timer_period, self._timer_callback)

    def _timer_callback(self):

        msg = String()
        msg.data = self._message

        self._publisher.publish(msg)

        self.get_logger().info(f'Publishing: "{msg}"')

    def _post_set_paramater_callback(self, parameter_list):
        for param in parameter_list:
            if param.name == "message":
                self.get_logger().info(f"Updated {param.name} to {param.value}")
                self._message = param.value  # updating member variable
            elif param.name == "timer_period":
                self.get_logger().info(f"Updated {param.name} to {param.value}")
                self._timer_period = param.value
                # reset timer
                self._timer.cancel()
                self._timer = self.create_timer(self._timer_period, self._timer_callback)
            else:
                self.get_logger().warn(f"Unknown paramater: {param.name}")


def main(args=None):

    node = None  # guarantees finally can always safely reference it

    try:
        rclpy.init(args=args)
        node = PublisherWithParams()
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        print()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if node is not None:
            node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
