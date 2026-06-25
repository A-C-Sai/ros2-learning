#! /usr/bin/env python3

import rclpy
from rclpy.node import Node
from example_interfaces.msg import String
from example_interfaces.srv import AddTwoInts
from rclpy.parameter import Parameter


class SuperNode(Node):

    def __init__(self):
        super().__init__("super")

        # Minimal Node
        '''
        self.counter_ = 0
        self.get_logger().info("Hello")
        self.create_timer(1.0, self.minimal_callback)
        '''

        # Parameters
        '''
        self.declare_parameter("<param_name>",<default_value>) # default value can be overridden at runtime
        self.<var>_ = self.get_parameter("<param_name>").value # we can validate params also instead of blindly assigning them to variables
        '''

        # Parameter Callback
        '''
        self.add_post_set_parameters_callback(self._post_set_parameter_callback)
        '''

        # Publisher
        '''
        self.publisher_ = self.create_publisher(String, "topic", 10) # adding a leading / to topic will not change even if add a namespace. This goes for node, service, topic etc.. names
        self.timer_ = self.create_timer(1.0, self.publish_)
        '''

        # Subscriber
        '''
        self.subscriber_ = self.create_subscription(String,
                                                    "topic",
                                                    self.subscriber_callback_,
                                                    10)
        '''

        # Server
        '''
        self.server_ = self.create_service(AddTwoInts, 'service', self.service_callback_)
        '''

        # Client
        '''
        self.client_ = self.create_client(AddTwoInts, "service")
        self.service_check_timer_ = self.create_timer(2.0, self.check_service_)
        '''

        self.get_logger().info("Super Node has been started.")

    # Minimal Node
    '''
    def minimal_callback(self):
        self.get_logger().info(f"{self.counter_}: Hello from callback")
        self.counter_ += 1
    '''

    # Parameter Callback
    '''
    def _post_set_parameter_callback(self, parameter_list: list[Parameter]):
        for param in parameter_list:
            if param.name == "<name>":
                self.<var>_ = param.value
    # NOTE: If changing timer period, we need to also use cancel() method on the existing timer and create a new timer.
    '''

    # Publisher
    '''
    def publish_(self):
        msg = String()
        msg.data = "Hello from Super. Over."
        self.publisher_.publish(msg)
    '''

    # Subscriber
    '''
    def subscriber_callback_(self, msg: String):
        self.get_logger().info(msg.data)
    '''

    # Service
    '''
    def service_callback_(self, req: AddTwoInts.Request, res: AddTwoInts.Response):
        # validation logic (optional)
        res.sum = req.a + req.b
        return res
    '''

    # Client
    '''
    def check_service_(self):
        if self.client_.service_is_ready():
            self.get_logger().info("Service available! Sending request...")
            self.service_check_timer_.cancel()
            self.send_request_()
        else:
            self.get_logger().warn("Waiting for Service...")

    def send_request_(self):
        req = AddTwoInts.Request()
        req.a = 2
        req.b = 3
        future = self.client_.call_async(req)
        # from functools import partial
        # future.add_conde_callback(partial(self.response_callback_, request=req))
        future.add_done_callback(lambda future: self.response_callback_(future, request=req))

    def response_callback_(self, future, request):
        self.get_logger().info("Recieved response!")
        res = future.result()
        self.get_logger().info(f"Result: {request.a} + {request.b} = {res.sum}")
    '''

    # Current Time
    '''
    def get_current_time_seconds(self):
        seconds, nanoseconds = self.get_clock().now().seconds_nanoseconds()
        return seconds + (nanoseconds / 1e9)
    '''


def main(args=None):

    node = None

    try:
        rclpy.init(args=args)
        # node = Node("my_node")
        # node.get_logger().info("Hello World")
        node = SuperNode()
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
