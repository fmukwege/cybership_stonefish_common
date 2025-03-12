cmake_minimum_required(VERSION 3.8)
project(cybership_simulation_common)

find_package(ament_cmake REQUIRED)
find_package(stonefish_ros2 REQUIRED)

install(DIRECTORY
  launch
  scenarios
  data
  metadata
  vessel_models
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
