#include "rclcpp/rclcpp.hpp"
#include "example_interfaces/srv/add_two_ints.hpp"

#include <memory>

class MinimalService : public rclcpp::Node{
  public:
    MinimalService() : Node("minimal_service"){
      // Create a service (server) obj
      server_ = this->create_service<example_interfaces::srv::AddTwoInts>(
        "add_two_ints",
        // Responds with sum of request integers
        [this](
          const example_interfaces::srv::AddTwoInts::Request::SharedPtr req,
          const example_interfaces::srv::AddTwoInts::Response::SharedPtr res
        ) -> void {
          // log request
          RCLCPP_INFO(this->get_logger(),"Received request: a=%ld, b=%ld", req->a, req->b);

          // contents of response is automatically sent back to client
          res->sum = req->a + req->b;

          RCLCPP_INFO(this->get_logger(),"Sending back response: %ld", res->sum);
        }
      );

      RCLCPP_INFO(this->get_logger(),"Ready to add two ints.");
    }

  private:
    rclcpp::Service<example_interfaces::srv::AddTwoInts>::SharedPtr server_;
};

int main(int argc, char* argv[]){
  rclcpp::init(argc=argc, argv=argv);
  auto node = std::make_shared<MinimalService>();
  rclcpp::spin(node);
  rclcpp::shutdown();
  return 0;
}