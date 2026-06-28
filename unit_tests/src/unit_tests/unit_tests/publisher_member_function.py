#! /usr/bin/env python3

"""
Description:
This ROS2 node periodically publishes "Hello, World!" messages to a topic.
---
Publishes to: /my_topic (std_msgs/msg/String)
---
Subscribes to: None
---
Author: Sai C Akella
Date: 13/05/2026
"""


import rclpy  # import the ROS2 client lib for pyhton
from rclpy.node import Node  # import the Node class, used for creating nodes
from rclpy.executors import ExternalShutdownException
from std_msgs.msg import String  # Import String message type for ROS2
# from example_interfaces.msg import String


class MinimalPublisher(Node):
    """
    Create a minimal publisher node
    """

    def __init__(self):
        """
        Create a custom node class for publishing messages
        """
        # initialize the node with a name i.e. call the Node class constructor
        # passing in the node name as argument
        super().__init__("minimal_publisher")

        # create a publisher obj
        # create_publisher declares that the node publishes messages
        # of type std_msgs/msg/String, over a topic named topic,
        # and that the “queue size” is 10.
        # Queue size is a required Quality of Service (QoS)
        # setting that limits the amount of queued messages
        # if a subscriber is not receiving them fast enough.
        self._publisher = self.create_publisher(String, "my_topic", 10)

        # create a timer with a period of 1 sec to trigger publishing of message
        self._timer_period = 1
        self._timer = self.create_timer(self._timer_period, self._timer_callback)

        # initialize counter variable for message count
        self._counter = 0

    def _timer_callback(self):
        """
        Callback function executed periodically by the timer
        """
        # create a new String msg object
        msg = String()

        # set message data with a counter
        msg.data = f"{self._counter}: Hello, World!"

        # publish message created above to the respective topic
        self._publisher.publish(msg)

        # Log a message indicating the message has been published (prints it to the console)
        self.get_logger().info(f'Publishing: "{msg}"')

        # increment counter
        self._counter += 1


def main(args=None):
    """
    Main function to start the ROS 2 Node

    Args:
        args (List, optional): Command-line arguments. Defaults to None.
    """

    try:
        # Initialize
        rclpy.init(args=args)
        # Create an instance of the minimal Publisher Node
        node = MinimalPublisher()
        # Run node
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
