cmake_minimum_required(VERSION 2.8.3)
project(mad_utilities)


find_package(catkin REQUIRED COMPONENTS
  roscpp
  std_msgs
  tf
  sensor_msgs
)

catkin_package(
CATKIN_DEPENDS roscpp std_msgs sensor_msgs
)

include_directories( ${catkin_INCLUDE_DIRS} )

add_executable(imu_to_tf src/mbpo_attitude_to_tf_node.cpp )
target_link_libraries(imu_to_tf ${catkin_LIBRARIES})
