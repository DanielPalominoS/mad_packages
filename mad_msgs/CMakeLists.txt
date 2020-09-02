cmake_minimum_required( VERSION 2.8.3 )
project( mad_msgs )

SET( CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11" )

## Find catkin macros and libraries
find_package(catkin REQUIRED COMPONENTS
  roscpp
  std_msgs
  message_generation
)

add_message_files(
  FILES
  ModuleError.msg
)

add_service_files(
  FILES
  CamCmd.srv
  InitCapture.srv
)

generate_messages(
  DEPENDENCIES
  std_msgs
)

###################################
## catkin specific configuration ##
###################################
## The catkin_package macro generates cmake config files for your package
catkin_package(
  CATKIN_DEPENDS roscpp std_msgs message_runtime
)

include_directories(
# include
  ${catkin_INCLUDE_DIRS}
)
