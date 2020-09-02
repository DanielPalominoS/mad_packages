cmake_minimum_required(VERSION 2.8.3)
project( mad_adapters )

SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

## Find catkin macros and libraries
find_package(catkin REQUIRED COMPONENTS
  roscpp
  std_msgs
  mavros_msgs
)

###################################
## catkin specific configuration ##
###################################
## The catkin_package macro generates cmake config files for your package
catkin_package(
  CATKIN_DEPENDS roscpp std_msgs mavros_msgs
)

###########
## Build ##
###########

## Specify additional locations of header files
include_directories( include )
include_directories(
  ${catkin_INCLUDE_DIRS}
)

