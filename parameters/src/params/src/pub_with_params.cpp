#include <functional>
#include <memory>
#include <chrono>
#include <string>
#include <vector>
#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"
#include "rcl_interfaces/msg/parameter_descriptor.hpp"

using namespace std::chrono_literals;

/**
 * @brief Publisher that periodically sends out a "Hello, World!" message
 *
*/

class PublisherWithParams : public rclcpp::Node
{
  public:
    /**
     * @brief Constructor (call Node class constructor with node name)
     *
     */
    PublisherWithParams() : Node("pub_with_params"){
      // Declare parameters
      auto message_desc = rcl_interfaces::msg::ParameterDescriptor();
      message_desc.description = "Message the will be published.";
      this->declare_parameter("message", "Hello, World!", message_desc);
      auto timer_period_desc = rcl_interfaces::msg::ParameterDescriptor();
      timer_period_desc.description = "Rate at which messages are published.";
      this->declare_parameter("timer_period", 1.0, timer_period_desc);

      // Get parameters and set to member varibales
      message_ = this->get_parameter("message").as_string();
      timer_period_ = this->get_parameter("timer_period").as_double();

      // Configure callback for runtime parameter update
      param_cb_handle = this->add_post_set_parameters_callback(
        [this](const std::vector<rclcpp::Parameter> &parameters){
          for(const auto &param : parameters){
            if(param.get_name() == "message"){
              this->message_ = param.get_value<std::string>(); // param.as_string()
              RCLCPP_INFO(this->get_logger(),
              "Updated %s to %s", param.get_name().c_str(), this->message_.c_str());
            }
            else if(param.get_name() == "timer_period"){
              this->timer_period_ = param.get_value<double>();
              RCLCPP_INFO(this->get_logger(),
              "Updated %s to %f", param.get_name().c_str(), this->timer_period_);

              // Reset timer
              this->timer_->cancel();
              this->timer_ = this->create_wall_timer(
                std::chrono::duration<double>(timer_period_),
                std::bind(&PublisherWithParams::timer_callback, this));
            }
            else {
              RCLCPP_WARN(this->get_logger(), "Unknown parameter: %s", param.get_name().c_str());
            }
          }
        }
      );

      // Create publisher obj
      publisher_ = this->create_publisher<std_msgs::msg::String>("my_topic",10);
      // Periodically call method
      timer_ = this->create_wall_timer(1s, std::bind(&PublisherWithParams::timer_callback, this));
      // RCLCPP_INFO(this->get_logger(), "Publishing at 1Hz");
    }

  private:
    // Declare member variables
    rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_; // The publisher obj
    rclcpp::TimerBase::SharedPtr timer_;
    std::string message_;
    double timer_period_;
    rclcpp::node_interfaces::PostSetParametersCallbackHandle::SharedPtr param_cb_handle;

    /**
     * @brief Publish simple message to topic
     *
     */
    void timer_callback(){
      // Fill out String message
      auto message = std_msgs::msg::String();
      message.data = this->message_;
      // Publish message to topic
      RCLCPP_INFO(this->get_logger(), "Publishing: %s", message.data.c_str());
      this->publisher_->publish(message);
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
  auto node = std::make_shared<PublisherWithParams>();
  rclcpp::spin(node);

  // Cleanup
  rclcpp::shutdown();

  return 0;
}