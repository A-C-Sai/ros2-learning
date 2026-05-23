#! /usr/bin/env python3

import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts
from rclpy.executors import ExternalShutdownException


class MinimalService(Node):
    """
    Server that adds two integers and responds with result
    """

    def __init__(self):

        super().__init__("minimal_service")

        # Create a service obj
        self._srv = self.create_service(
            AddTwoInts,
            "add_two_ints",
            self._sum_callback  # method that is called when client sends a request
        )

    def _sum_callback(self, req, res):
        res.sum = req.a + req.b
        self.get_logger().info(f"Received request a={req.a}, b={req.b}")

        return res


def main(args=None):
    try:
        rclpy.init(args=args)
        node = MinimalService()
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        print()
    except Exception as e:
        print(f"An error occured: {e}")
    finally:
        if node is not None:
            node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
