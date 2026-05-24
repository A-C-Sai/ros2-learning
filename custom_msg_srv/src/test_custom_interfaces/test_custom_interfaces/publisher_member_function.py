#! /usr/bin/env python3

import rclpy  # import the ROS2 client lib for pyhton
from rclpy.node import Node  # import the Node class, used for creating nodes
from rclpy.executors import ExternalShutdownException
from custom_msg_srv.msg import Num


class MinimalPublisher(Node):

    def __init__(self):

        super().__init__("num_publisher")

        self._publisher = self.create_publisher(Num, "my_num", 10)

        self._timer_period = 1
        self._timer = self.create_timer(self._timer_period, self._timer_callback)

        self._counter = 0

    def _timer_callback(self):

        msg = Num()

        msg.num = self._counter

        self._publisher.publish(msg)

        self.get_logger().info(f'Publishing: "{msg}"')

        self._counter += 1


def main(args=None):

    try:

        rclpy.init(args=args)

        node = MinimalPublisher()

        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        print()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if node is not None:
            # Destroy the node explicitly
            node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()  # Shutdown ROS 2 communication


if __name__ == "__main__":
    main()  # execute the main function if the script is run directly
