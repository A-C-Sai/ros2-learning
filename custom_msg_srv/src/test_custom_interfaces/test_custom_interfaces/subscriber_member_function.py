#! /usr/bin/env python3

import rclpy
from rclpy.node import Node
from custom_msg_srv.msg import Num
from rclpy.executors import ExternalShutdownException


class MinimalSubscriber(Node):
    def __init__(self):
        super().__init__("num_subscriber")

        self._subscription = self.create_subscription(Num,
                                                      "my_num",
                                                      self._listener_callback,
                                                      10
                                                      )

    def _listener_callback(self, msg):
        self.get_logger().info(f'I heard: "{msg.num}"')


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
