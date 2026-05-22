#! /usr/bin/env python3

"""
Description:
This ROS2 nose subscribes to "Hello, World!" messages.
---
Publishes to: None
---
Subscribes to:
The channel containing the "Hello, World!" messages
/my_topic (std_msgs/msg/String)
---
Author: Sai C Akella
Date: 18/05/2026
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from rclpy.executors import ExternalShutdownException


class MinimalSubscriber(Node):
    def __init__(self):
        super().__init__("minimal_subscriber")

        self._subscription = self.create_subscription(String,
                                                      "my_topic",
                                                      # callback gets called as soon as it receives
                                                      # a message.
                                                      self._listener_callback,
                                                      10
                                                      )

    def _listener_callback(self, msg):
        # simply prints an info message to the console, along with the data it received
        self.get_logger().info(f'I heard: "{msg.data}"')


def main(args=None):
    try:
        rclpy.init(args=args)
        node = MinimalSubscriber()
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
