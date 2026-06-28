#! /usr/bin/env python3

"""
Test suite for the ROS 2 minimal publisher node.

This script contains unit tests for verifying the functionality of a minimal ROS 2 publisher.
It tests:
    - node creation
    - message counter increment
    - message content formatting
---------------
Subscribes to:
    None

Publishes to:
    /my_topic (std_msgs/msg/String): Example messages with incrementing counter
"""

import pytest
import rclpy
from std_msgs.msg import String
from unit_tests.publisher_member_function import MinimalPublisher


def test_publisher_creation():
    """
    Test if the publisher node is created correctly.

    This test verifies:
    1. the node name is set correctly
    2. the publisher obj exists
    3. the topic name is correct

    :raises: AssertionError if any of the checks fail
    """

    # initialize ROS 2 communication
    rclpy.init()

    try:
        # create an instance of our publisher node
        node = MinimalPublisher()

        # test 1: verify the node has the expected name
        assert node.get_name() == "minimal_publisher"

        # test 2: verify the publisher exists
        assert hasattr(node, "_publisher")

        # test 3: verify the topic name is correct
        assert node._publisher.topic_name == "/my_topic"
    finally:
        # clean up ROS 2 communication
        rclpy.shutdown()


def test_message_counter():
    """
    Test if the message counter increments correctly.

    This test verifies the the counter (node._counter) increases by 1 after each timer callback execution.

    :raises: AssertionError if the counter doesn't increment properly
    """

    rclpy.init()

    try:
        node = MinimalPublisher()
        initial_count = node._counter

        node._timer_callback()

        assert node._counter == initial_count + 1
    finally:
        rclpy.shutdown()


def test_message_content():
    """
    Test if the message content is formatted correctly.

    This text verifies that the message string is properly formatted using an f-string
    with the current counter value.

    :raises: AssertionError if the message formate doesn't match the expected output
    """

    rclpy.init()

    try:
        node = MinimalPublisher()

        node._counter = 5
        msg = String()

        msg.data = f"{node._counter}: Hello, World!"
        assert msg.data == "5: Hello, World!"
    finally:
        rclpy.shutdown()


if __name__ == "__main__":
    pytest.main(['-v'])
