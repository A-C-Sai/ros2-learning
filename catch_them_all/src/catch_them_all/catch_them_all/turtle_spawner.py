#! /usr/bin/env python3

import rclpy
from rclpy.node import Node
import random
import math
from turtlesim.srv import Spawn, Kill
from interfaces.msg import Turtle, TurtleArray
from interfaces.srv import CatchTurtle


class TurtleSpawner(Node):

    def __init__(self):

        super().__init__("turtle_spawner")
        self.declare_parameter("spawn_frequency", 1.0)

        self.alive_turtles_ = TurtleArray()
        self.publisher_ = self.create_publisher(TurtleArray, "alive_turtles", 10)

        self.spawn_client_ = self.create_client(Spawn, "spawn")
        self.spawn_turtle_timer = self.create_timer(
            1.0 / self.get_parameter("spawn_frequency").value, self.spawn_turtle_)

        self.catch_turtle_service_ = self.create_service(
            CatchTurtle, "catch_turtle", self.callback_catch_turtle_)
        self.kill_client_ = self.create_client(Kill, "kill")

        self.get_logger().info("Turtle Spawner has been started.")

    def spawn_turtle_(self):
        while not self.spawn_client_.service_is_ready():
            self.get_logger().warn("waiting for spawn service....")
        else:
            self.get_logger().info("spawn service available!")

        pos_x, pos_y = (random.uniform(0.0, 11.0),
                        random.uniform(0.0, 11.0))
        theta = random.uniform(0.0, 2 * math.pi)

        req = Spawn.Request()
        req.x = pos_x
        req.y = pos_y
        req.theta = theta

        future = self.spawn_client_.call_async(req)
        future.add_done_callback(lambda future: self.callback_spawn_turtle_(future, request=req))

    def callback_spawn_turtle_(self, future, request):
        res: Spawn.Response = future.result()

        if res.name:
            self.get_logger().info(f'''New turtle spawned!
                                Name: {res.name}
                                (x,y): ({request.x},{request.y})
                                facing: {round(request.theta * (180 / math.pi), 1)}°''')

        new_turtle = Turtle()
        new_turtle.name = res.name
        new_turtle.x = request.x
        new_turtle.y = request.y

        self.alive_turtles_.turtles.append(new_turtle)

        self.publisher_.publish(self.alive_turtles_)

    def callback_catch_turtle_(self, req: CatchTurtle.Request, res: CatchTurtle.Response):

        self.call_kill_service_(req.turtle_name)

        res.success = True
        return res

    def call_kill_service_(self, turtle_name):
        while not self.kill_client_.wait_for_service(1.0):
            self.get_logger().warn("waiting for kill service!")

        request = Kill.Request()
        request.name = turtle_name
        future = self.kill_client_.call_async(request)
        future.add_done_callback(
            lambda future: self.callback_call_kill_service_(
                future, name=turtle_name))

    def callback_call_kill_service_(self, future, name):

        names = [turtle.name for turtle in self.alive_turtles_.turtles]
        idx = names.index(name)
        self.alive_turtles_.turtles.pop(idx)
        self.publisher_.publish(self.alive_turtles_)


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
