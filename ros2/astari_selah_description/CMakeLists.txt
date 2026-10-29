cmake_minimum_required(VERSION 3.8)
project(astari_selah_description)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)

# Install assets, models, launches, and configurations to share directory
install(
  DIRECTORY
    urdf
    launch
    rviz
    meshes
    config
  DESTINATION share/${PROJECT_NAME}
)

# Install python executable nodes
install(
  PROGRAMS
    scripts/esp32_bridge.py
    scripts/test_arm_control_execution.py
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
