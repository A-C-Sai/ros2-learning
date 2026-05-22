#include <functional>
#include <memory>
#include <chrono>
#include <string>
#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

using namespace std::chrono_literals;

/**
 * @brief Publisher that periodically sends out a "Hello, World!" message
 *
*/

class MinimalPublisher : public rclcpp::Node
{
  public:
    /**
     * @brief Constructor (call Node class constructor with node name)
     *
     */
    MinimalPublisher() : Node("minimal_publisher"){
      // Counter for messages sent
      count_ = 0;
      // Create publisher obj
      publisher_ = this->create_publisher<std_msgs::msg::String>("my_topic",10);
      // Periodically call method
      timer_ = this->create_wall_timer(1s, std::bind(&MinimalPublisher::timer_callback, this));
      RCLCPP_INFO(this->get_logger(), "Publishing at 1Hz");
    }

  private:
    // Declare member variables
    size_t count_; // Keep track of the number of messages published
    rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_; // The publisher obj
    rclcpp::TimerBase::SharedPtr timer_;

    /**
     * @brief Publish simple message to topic
     *
     */
    void timer_callback(){
      // Fill out String message
      auto message = std_msgs::msg::String();
      message.data = std::to_string(count_) + ": Hello, World!";
      // Publish message to topic
      RCLCPP_INFO(this->get_logger(), "Publishing: %s", message.data.c_str());
      this->publisher_->publish(message);
      // Increment counter
      count_++;
    }
};

/**
 * @brief Main entrypoint
 *
 * @param argc
 * @param argv
 * @return int
 */
int main(int argc, char* argv[]){
  // Initialize ROS 2
  rclcpp::init(argc, argv);

  // Initialize and run node
  auto node = std::make_shared<MinimalPublisher>();
  rclcpp::spin(node);

  // Cleanup
  rclcpp::shutdown();

  return 0;
}