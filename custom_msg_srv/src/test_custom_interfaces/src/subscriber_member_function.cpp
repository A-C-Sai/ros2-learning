#include <functional>
#include <memory>
#include "rclcpp/rclcpp.hpp" // ROS 2 C++ Client Lib
#include "custom_msg_srv/msg/num.hpp" // Handling String messages

using std::placeholders::_1; //Placeholder for callback function

class MinimalSubscriber : public rclcpp::Node {
  public:
    MinimalSubscriber() : Node("num_subscriber"){
      subscription_ = this->create_subscription<custom_msg_srv::msg::Num>(
        "my_num", 10, std::bind(&MinimalSubscriber::topic_callback, this, _1));
    }

  private:
    void topic_callback(const custom_msg_srv::msg::Num & msg) const {
      RCLCPP_INFO(this->get_logger(), "I heard: %ld", msg.num);
    }
    rclcpp::Subscription<custom_msg_srv::msg::Num>::SharedPtr subscription_;
};

int main(int argc, char* argv[]){
  rclcpp::init(argc, argv);
  auto node = std::make_shared<MinimalSubscriber>();
  rclcpp::spin(node);
  rclcpp::shutdown();
  return 0;
}
