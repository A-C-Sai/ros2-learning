#! /usr/bin/env python3

import rclpy
from rclpy.node import Node
import random
import math
from turtlesim.srv import Spawn


class TurtleSpawner(Node):

    def __init__(self):

        super().__init__("turtle_spawner")

        self.lower_boundary_ = 0.0
        self.upper_boundary_ = 11.0
        self.period_ = 1.0

        self.spawn_client_ = self.create_client(Spawn, "spawn")
        self.service_check_timer_ = self.create_timer(self.period_, self.check_service_)

        self.get_logger().info("Turtle Spawner has been started.")

    def check_service_(self):
        if self.spawn_client_.service_is_ready():
            self.get_logger().info("Spawn service available!")
            self.spawn_turtle_()
        else:
            self.get_logger().warn("Waiting for Service")

    def spawn_turtle_(self):
        pos_x, pos_y = (random.uniform(self.lower_boundary_, self.upper_boundary_),
                        random.uniform(self.lower_boundary_, self.upper_boundary_))
        theta = random.uniform(0.0, 2 * math.pi)

        req = Spawn.Request()
        req.x = pos_x
        req.y = pos_y
        req.theta = theta

        future = self.spawn_client_.call_async(req)
        future.add_done_callback(lambda future: self.response_callback_(future, request=req))

    def response_callback_(self, future, request):
        res = future.result()
        self.get_logger().info(f'''New turtle spawned!
                             Name: {res.name}
                             (x,y): ({request.x},{request.y})
                             facing: {round(request.theta * (180 / math.pi), 1)}°''')


def main(args=None):

    node = None

    try:
        rclpy.init(args=args)
        node = TurtleSpawner()
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
