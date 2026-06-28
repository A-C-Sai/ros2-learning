/**
 * @file subscriber_member_function.cpp
 * @author Sai C Akella
 * @brief This ROS2 node subscribes to "Hello, World!" messages
 * @version 0.1
 * @date 2026-05-22
 *
 * ----------
 * Subscribes to:
 * /my_topic - std_msgs/msg/String
 *
 * Publishes to:
 * None
 */

#include <functional>
#include <memory>
#include "rclcpp/rclcpp.hpp" // ROS 2 C++ Client Lib
#include "std_msgs/msg/string.hpp" // Handling String messages

using std::placeholders::_1; //Placeholder for callback function

class MinimalSubscriber : public rclcpp::Node {
  public:
    MinimalSubscriber() : Node("minimal_subscriber"){
      subscription_ = this->create_subscription<std_msgs::msg::String>(
        "my_topic", 10, std::bind(&MinimalSubscriber::topic_callback, this, _1));
    }

  private:
    void topic_callback(const std_msgs::msg::String & msg) const {
      RCLCPP_INFO(this->get_logger(), "I heard: %s", msg.data.c_str());
    }
    rclcpp::Subscription<std_msgs::msg::String>::SharedPtr subscription_;
};

int main(int argc, char* argv[]){
  rclcpp::init(argc, argv);
  auto node = std::make_shared<MinimalSubscriber>();
  rclcpp::spin(node);
  rclcpp::shutdown();
  return 0;
}
