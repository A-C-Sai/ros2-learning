#include "rclcpp/rclcpp.hpp"
#include "custom_msg_srv/srv/add_three_ints.hpp"
#include <random>
#include <chrono>
#include <memory>

class MinimalClient : public rclcpp::Node{
  public:
    MinimalClient() : Node("minimal_client"){

      // create client obj
      client_ = this->create_client<custom_msg_srv::srv::AddThreeInts>("add_three_ints");

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
          auto req = std::make_shared<custom_msg_srv::srv::AddThreeInts::Request>();
          req->a = std::rand() % 11;
          req->b = std::rand() % 11;
          req->c = std::rand() % 11;

          RCLCPP_INFO(this->get_logger(), "Sending request: a=%ld, b=%ld, c=%ld", req->a, req->b, req->c);

          // send request to server and set callback
          client_->async_send_request(
            req,
            [this](
              const rclcpp::Client<custom_msg_srv::srv::AddThreeInts>::SharedFuture future
            )->void{
              auto res = future.get();
              RCLCPP_INFO(this->get_logger(), "Result: %ld", res->sum);
            }
          );
        }
      );
    }

  private:
    rclcpp::Client<custom_msg_srv::srv::AddThreeInts>::SharedPtr client_;
    rclcpp::TimerBase::SharedPtr timer_;
};

int main(int argc, char* argv[]){
  rclcpp::init(argc, argv);
  auto node = std::make_shared<MinimalClient>();
  rclcpp::spin(node);
  rclcpp::shutdown();
  return 0;
}