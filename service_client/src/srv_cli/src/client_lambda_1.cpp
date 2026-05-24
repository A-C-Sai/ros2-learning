#include "rclcpp/rclcpp.hpp"
#include "example_interfaces/srv/add_two_ints.hpp"
#include <random>
#include <chrono>
#include <memory>

class MinimalClient : public rclcpp::Node{
  public:
    MinimalClient() : Node("minimal_client"){

      // create client obj
      client_ = this->create_client<example_interfaces::srv::AddTwoInts>("add_two_ints");

      // wait for service
      while (!client_->wait_for_service(std::chrono::seconds(2))){
        RCLCPP_INFO(this->get_logger(), "waiting for service...");
      }

      // seed random number generator with current time
      std::srand(std::time(nullptr));

      // periodically call function
      timer_ = this->create_wall_timer(
        std::chrono::milliseconds(2000),
        [this]()->void{
          // fill out request message
          auto req = std::make_shared<example_interfaces::srv::AddTwoInts::Request>();
          req->a = std::rand() % 11;
          req->b = std::rand() % 11;

          RCLCPP_INFO(this->get_logger(), "Sending request: a=%ld, b=%ld", req->a, req->b);

          // send request to server and set callback
          client_->async_send_request(
            req,
            [this](
              const rclcpp::Client<example_interfaces::srv::AddTwoInts>::SharedFuture future
            )->void{
              auto res = future.get();
              RCLCPP_INFO(this->get_logger(), "Result: %ld", res->sum);
            }
          );
        }
      );
    }

  private:
    rclcpp::Client<example_interfaces::srv::AddTwoInts>::SharedPtr client_;
    rclcpp::TimerBase::SharedPtr timer_;
};

int main(int argc, char* argv[]){
  rclcpp::init(argc, argv);
  auto node = std::make_shared<MinimalClient>();
  rclcpp::spin(node);
  rclcpp::shutdown();
  return 0;
}