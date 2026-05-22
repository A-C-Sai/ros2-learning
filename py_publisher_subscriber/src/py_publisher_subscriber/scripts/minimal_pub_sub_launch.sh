#! /usr/bin/env bash

# Launch publisher and subscriber nodes with cleanup handling

cleanup(){
  echo "Restarting ROS 2 daemon to cleanup before shutting down all processes..."
  ros2 daemon stop
  sleep 1
  ros2 daemon start
  echo "Terminating all ROS 2-related processes..."
  kill 0
  exit
}

trap cleanup SIGINT

ros2 run py_publisher_subscriber publisher_member_function &
ros2 run py_publisher_subscriber subscriber_member_function