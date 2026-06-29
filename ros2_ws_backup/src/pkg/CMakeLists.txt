cmake_minimum_required(VERSION 3.8)
project(pkg)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Locate and configure packages required by the project.
find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclpy REQUIRED)
find_package(example_interfaces REQUIRED)
# find_package(interfaces REQUIRED)

# Define a CMake variable named dependencies that lists all
# ROS 2 packages and other dependencies the project requires.
set(dependencies
  rclcpp
  # std_msgs
  example_interfaces
  # interfaces
)

# Add the specified directories to the list of paths that the compiler
# uses to search for header files. This is important for C++
# projects where you have custom header files that are not located
# in the standard system include paths.
include_directories(
  include
)

# Uncomment Section for C++ projects
# Tells CMake to create an executable target from the source file
# Also make sure CMake knows about the program's dependencies.
# add_executable(<executable_name> src/<filename>.cpp)
# ament_target_dependencies(<executable_name> ${dependencies})


# Copy necessary files to designated locations in the project
install(
  DIRECTORY pkg scripts
  DESTINATION share/${PROJECT_NAME}
)

install(
  DIRECTORY include/
  DESTINATION include
)

# Uncomment Section for C++ projects
# Install cpp executables
# install(
#   TARGETS
#   <executable_name>
#   DESTINATION lib/${PROJECT_NAME}
# )

# Uncomment Section for Python projects
# Install Python modules for import
#ament_python_install_package(${PROJECT_NAME})

# Uncomment Section for Python projects
# Install python scripts
# install(
#   PROGRAMS
#   pkg/<filename>.py
#   DESTINATION lib/${PROJECT_NAME}
# )

# Uncomment Section if any scripts are present
# Make sure your script actually has the executable bit set
# Install python scripts
# install(
#   PROGRAMS
#   scripts/<filename>.sh
#   DESTINATION lib/${PROJECT_NAME}
# )

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)

  find_package(ament_cmake_pytest REQUIRED)
  find_package(ament_cmake_gtest REQUIRED)

  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()

  # Python tests
  # ament_add_pytest_test(<executable> test/pytest/<filename>.py
  #   TIMEOUT 60
  # )

  # C++ tests
  # ament_add_gtest(
  #   <executable> test/gtest/<filename>.cpp
  # )

  # Add dependencies for the C++ test executable
  # ament_target_dependencies(<executable>
  #   ${dependencies}
  # )

endif()

# Used to export include directories of a package so that they can be easily
# included by other packages that depend on this package.
ament_export_include_directories(include)

ament_package()
