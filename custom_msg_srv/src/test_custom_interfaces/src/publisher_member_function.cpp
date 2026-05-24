#include <functional>
#include <memory>
#include <chrono>
#include "rclcpp/rclcpp.hpp"
#include "custom_msg_srv/msg/num.hpp"

using namespace std::chrono_literals;

class MinimalPublisher : public rclcpp::Node
{
  public:

    MinimalPublisher() : Node("num_publisher"){

      count_ = 0;

      publisher_ = this->create_publisher<custom_msg_srv::msg::Num>("my_num",10);

      timer_ = this->create_wall_timer(1s, std::bind(&MinimalPublisher::timer_callback, this));
      RCLCPP_INFO(this->get_logger(), "Publishing at 1Hz");
    }

  private:

    size_t count_;
    rclcpp::Publisher<custom_msg_srv::msg::Num>::SharedPtr publisher_;
    rclcpp::TimerBase::SharedPtr timer_;


    void timer_callback(){

      auto message = custom_msg_srv::msg::Num();
      message.num = count_;

      RCLCPP_INFO(this->get_logger(), "Publishing: %ld", message.num);
      this->publisher_->publish(message);

      count_++;
    }
};


int main(int argc, char* argv[]){

  rclcpp::init(argc, argv);


  auto node = std::make_shared<MinimalPublisher>();
  rclcpp::spin(node);

  rclcpp::shutdown();

  return 0;
}