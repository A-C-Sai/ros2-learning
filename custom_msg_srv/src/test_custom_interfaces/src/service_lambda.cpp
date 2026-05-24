#include "rclcpp/rclcpp.hpp"
#include "custom_msg_srv/srv/add_three_ints.hpp"

#include <memory>

class MinimalService : public rclcpp::Node{
  public:
    MinimalService() : Node("adder"){
      // Create a service (server) obj
      server_ = this->create_service<custom_msg_srv::srv::AddThreeInts>(
        "add_three_ints",
        // Responds with sum of request integers
        [this](
          const custom_msg_srv::srv::AddThreeInts::Request::SharedPtr req,
          const custom_msg_srv::srv::AddThreeInts::Response::SharedPtr res
        ) -> void {
          // log request
          RCLCPP_INFO(this->get_logger(),"Received request: a=%ld, b=%ld, c=%ld", req->a, req->b, req->c);

          // contents of response is automatically sent back to client
          res->sum = req->a + req->b + req->c;

          RCLCPP_INFO(this->get_logger(),"Sending back response: %ld", res->sum);
        }
      );

      RCLCPP_INFO(this->get_logger(),"Ready to add two ints.");
    }

  private:
    rclcpp::Service<custom_msg_srv::srv::AddThreeInts>::SharedPtr server_;
};

int main(int argc, char* argv[]){
  rclcpp::init(argc=argc, argv=argv);
  auto node = std::make_shared<MinimalService>();
  rclcpp::spin(node);
  rclcpp::shutdown();
  return 0;
}