/**
 * @file test_publisher.cpp
 * @brief Unit tests for the ROS 2 minimal publisher node
 *
 * This file contains test cases to verify the functionality of our minimal publisher.
 * The following things are tested:
 * 1. That the node is created correctly with the right name and topic
 * 2. That it published the expected "Hello World!" message
 *
 * Testing Framework:
 *  Google Test (gtest) for C++ unit testing
 *
 * Tests:
 *  TestNodeCreation: Verifies node name and publisher setup
 *  TestMessageContent: Verifies published message format
 */

#include <gtest/gtest.h>
#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

class MinimalPublisher;

#define TESTING_EXCLUDE_MAIN
#include "../../src/publisher_member_function.cpp"

class TestMinimalPublisher : public ::testing::Test
{
  protected:
    void SetUp() override
    {
      rclcpp::init(0, nullptr);
      node = std::make_shared<MinimalPublisher>();
    }
    void TearDown() override
    {
      node.reset();
      rclcpp::shutdown();
    }
    std::shared_ptr<MinimalPublisher> node;
};

TEST_F(TestMinimalPublisher, TestNodeCreation)
{
  EXPECT_EQ(std::string(node->get_name()), std::string("minimal_publisher"));

  auto pub_endpoints = node->get_publishers_info_by_topic("/my_topic");
  EXPECT_EQ(pub_endpoints.size(), 1u);

}

TEST_F(TestMinimalPublisher, TestssageCountent)
{
  std::shared_ptr<std_msgs::msg::String> received_msg;

  auto subscription = node->create_subscription<std_msgs::msg::String>(
    "/my_topic", 10,
  [&received_msg](const std_msgs::msg::String::SharedPtr msg){
    received_msg = std::make_shared<std_msgs::msg::String>(*msg);
  });

  node->timer_callback();

  rclcpp::spin_some(node);

  EXPECT_EQ(received_msg->data.substr(0, 13), "Hello, World!");
}

int main(int argc, char** argv)
{
  testing::InitGoogleTest(&argc, argv);
  return RUN_ALL_TESTS();
}