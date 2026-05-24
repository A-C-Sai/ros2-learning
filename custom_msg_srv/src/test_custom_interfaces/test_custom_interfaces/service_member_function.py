#! /usr/bin/env python3

import rclpy
from rclpy.node import Node
from custom_msg_srv.srv import AddThreeInts
from rclpy.executors import ExternalShutdownException


class MinimalService(Node):

    def __init__(self):

        super().__init__("adder")

        self._srv = self.create_service(
            AddThreeInts,
            "add_three_ints",
            self._sum_callback
        )

    def _sum_callback(self, req, res):
        res.sum = req.a + req.b + req.c
        self.get_logger().info(f"Received request a={req.a}, b={req.b}, c={req.c}")

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
