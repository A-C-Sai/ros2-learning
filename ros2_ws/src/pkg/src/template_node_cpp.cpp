#include "rclcpp/rclcpp.hpp"
#include "example_interfaces/msg/string.hpp"
#include "example_interfaces/srv/add_two_ints.hpp"

class SuperNode : public rclcpp::Node {
  private:
    // Minimal Node
    // rclcpp::TimerBase::SharedPtr timer_;
    // int counter_;

    // Minimal Node
    // void minimalCallback(){
    //   RCLCPP_INFO(this->get_logger(), "%d: Hello from callback", this->counter_);
    //   this->counter_++;
    // }

    // Publisher
    // rclcpp::Publisher<example_interfaces::msg::String>::SharedPtr publisher_;
    // rclcpp::TimerBase::SharedPtr timer_;

    // void publish_(){
    //   auto msg = example_interfaces::msg::String();
    //   msg.data = std::string("Hello from Super. Over.");
    //   this->publisher_->publish(msg);
    // }

    // Subscriber
    // rclcpp::Subscription<example_interfaces::msg::String>::SharedPtr subscriber_;

    // void subscriberCallback_(const example_interfaces::msg::String::SharedPtr & msg){
    //   RCLCPP_INFO(this->get_logger(), "%s",msg->data.c_str());
    // }

    // Server
    // rclcpp::Service<example_interfaces::srv::AddTwoInts>::SharedPtr server_;

    // Client
    // rclcpp::Client<example_interfaces::srv::AddTwoInts>::SharedPtr client_;
    // rclcpp::TimerBase::SharedPtr check_service_timer_;

    // void check_service_(){
    //   if(this->client_->service_is_ready()){
    //     RCLCPP_INFO(this->get_logger(), "Service ready! Sending request...");
    //     this->check_service_timer_->cancel();
    //     this->send_request_();
    //   }else{
    //     RCLCPP_WARN(this->get_logger(), "Waiting for service....");
    //   }
    // }

    // void send_request_(){
    //   auto req = std::make_shared<example_interfaces::srv::AddTwoInts::Request>();
    //   req->a = 2; req->b = 3;
    //   this->client_->async_send_request(req, std::bind(&SuperNode::responseCallback_, this, std::placeholders::_1));
    // }

    // void responseCallback_(const rclcpp::Client<example_interfaces::srv::AddTwoInts>::SharedFuture future){
    //   auto res = future.get();
    //   RCLCPP_INFO(this->get_logger(),"Result: %d", (int)res->sum);
    // }

  public:
    SuperNode() : Node("super"){

      // Minimal Node
      // this->counter_ = 0;
      // this->timer_ = this->create_wall_timer(std::chrono::seconds(1),
      //                                  std::bind(&CustomNode::minimalCallback, this));

      // Publisher
      // publisher_ = this->create_publisher<example_interfaces::msg::String>("topic", 10);
      // timer_ = this->create_wall_timer(std::chrono::seconds(1),
      //                                  std::bind(&SuperNode::publish_, this));

      // Subscriber
      // subscriber_ = this->create_subscription<example_interfaces::msg::String>("topic", 10,
      //                                                                          std::bind(&SuperNode::subscriberCallback, this, std::placeholders::_1),
      //                                                                      );

      // Server
      // server_ = this->create_service<example_interfaces::srv::AddTwoInts>("service",
      // [this](
      //   const example_interfaces::srv::AddTwoInts::Request::SharedPtr req,
      //   const example_interfaces::srv::AddTwoInts::Response::SharedPtr res
      // )->void{
      //   res->sum = req->a + req->b;
      // });

      // Client
      // client_ = this->create_client<example_interfaces::srv::AddTwoInts>("service");
      // check_service_timer_ = this->create_wall_timer(
      //   std::chrono::seconds(2),
      //   std::bind(&SuperNode::check_service_, this)
      // );

      RCLCPP_INFO(this->get_logger(), "Super Node has been started.");
    }
};

int main(int argc, char* argv[]){
  rclcpp::init(argc, argv);
  // auto node = std::make_shared<rclcpp::Node>();
  // RCLCPP_INFO(node->get_logger(), "Hello");
  auto node = std::make_shared<SuperNode>();
  rclcpp::spin(node);
  rclcpp::shutdown();
  return 0;
}