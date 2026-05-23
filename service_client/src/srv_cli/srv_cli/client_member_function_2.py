#! /usr/bin/env python3

import rclpy
from rclpy.node import Node
from rclpy.executors import ExternalShutdownException
from example_interfaces.srv import AddTwoInts
import sys


class MinimalClient(Node):

    def __init__(self):

        super().__init__("minimal_client")

        # create a client obj
        self._client = self.create_client(
            AddTwoInts,
            "add_two_ints"
        )

        # wait for service
        while not self._client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("waiting for service...")

        # request object
        self._req = AddTwoInts.Request()

    def send_request(self, a, b):
        """Send request to server asking it to add two integers
        """

        # fill out request obj
        self._req.a = a
        self._req.b = b

        return self._client.call_async(self._req)


def main(args=None):

    if len(sys.argv) != 3:
        print(f"(+) Usage: ros2 run srv_cli client_member_function_2.py <a_int> <b_int>")
        print(f"(+) Example: ros2 run srv_cli client_member_function_2.py 2 3")
        sys.exit(-1)

    try:
        rclpy.init(args=args)
        node = MinimalClient()
        future = node.send_request(int(sys.argv[1]), int(sys.argv[2]))
        rclpy.spin_until_future_complete(node, future)
        res = future.result()
        node.get_logger().info(f"Result: {sys.argv[1]} + {sys.argv[2]} = {res.sum}")
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
