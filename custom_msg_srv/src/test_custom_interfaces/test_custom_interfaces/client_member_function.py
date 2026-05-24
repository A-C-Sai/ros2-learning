#! /usr/bin/env python3

import rclpy
from rclpy.node import Node
from rclpy.executors import ExternalShutdownException
from custom_msg_srv.srv import AddThreeInts
import random


class MinimalClient(Node):

    def __init__(self):

        super().__init__("minimal_client")

        # create a client obj
        self._client = self.create_client(
            AddThreeInts,
            "add_three_ints"
        )

        # wait for service
        while not self._client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("waiting for service...")

        # Periodically call method
        self._timer = self.create_timer(1.0, self._timer_callback)

        # request object
        self._req = AddThreeInts.Request()

    def _timer_callback(self):
        """Send request to server asking it to add three integers
        """

        # fill out request obj
        self._req.a = random.randint(0, 10)
        self._req.b = random.randint(0, 10)
        self._req.c = random.randint(0, 10)

        # send request to server and set callback
        self._future = self._client.call_async(self._req)
        self._future.add_done_callback(self._response_callback)

    def _response_callback(self, future):
        """Log result when received from server
        """
        try:
            res = self._future.result()
            self.get_logger().info(
                f"Result: {self._req.a} + {self._req.b} + {self._req.c} = {res.sum}")
        except Exception as e:
            self.get_logger().error(f"An error occured: {str(e)}")


def main(args=None):

    try:
        rclpy.init(args=args)
        node = MinimalClient()
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
