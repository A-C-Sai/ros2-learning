#include "rclcpp/rclcpp.hpp"
#include "example_interfaces/srv/add_two_ints.hpp"
#include <chrono>
#include <memory>
#include <string>

class MinimalClient : public rclcpp::Node{
  public:
    MinimalClient() : Node("minimal_client"){

      // create client obj
      client_ = this->create_client<example_interfaces::srv::AddTwoInts>("add_two_ints");

      // wait for service
      while (!client_->wait_for_service(std::chrono::seconds(2))){
        RCLCPP_INFO(this->get_logger(), "waiting for service...");
      }
    }

    rclcpp::Client<example_interfaces::srv::AddTwoInts>::SharedFuture send_request(int64_t a, int64_t b){
      auto req = std::make_shared<example_interfaces::srv::AddTwoInts::Request>();
      req->a = a;
      req->b = b;
      RCLCPP_INFO(this->get_logger(), "Sending request: a=%ld, b=%ld", req->a, req->b);
      return client_->async_send_request(req).future.share();
    }

  private:
    rclcpp::Client<example_interfaces::srv::AddTwoInts>::SharedPtr client_;
};

int main(int argc, char* argv[]){
  rclcpp::init(argc, argv);

  if(argc != 3){
    RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "usage: ros2 run srv_cli cpp_client_lambda_2 4 5");
    return 1;
  }

  auto node = std::make_shared<MinimalClient>();
  auto future = node->send_request(std::stoll(argv[1]), std::stoll(argv[2]));
  if(rclcpp::spin_until_future_complete(node, future) == rclcpp::FutureReturnCode::SUCCESS){
    auto res = future.get();
    RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "Result: %ld", res->sum);
  }else {
    RCLCPP_ERROR(rclcpp::get_logger("rclcpp"), "Failed to call service add_two_ints");
  }

  rclcpp::shutdown();
  return 0;

}