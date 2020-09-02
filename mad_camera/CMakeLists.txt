cmake_minimum_required(VERSION 2.8.3)
project( mad_camera )

SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

## Find catkin macros and libraries
find_package(catkin REQUIRED COMPONENTS
  roscpp
  std_msgs
  mavros_msgs
  mad_msgs
)

#find_package( -larducam_mipicamera )
find_package(OpenCV)

###################################
## catkin specific configuration ##
###################################
## The catkin_package macro generates cmake config files for your package
catkin_package(
  CATKIN_DEPENDS roscpp std_msgs mavros_msgs mad_msgs
)
catkin_install_python(PROGRAMS scripts/camera_module_v2.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
###########
## Build ##
###########

## Specify additional locations of header files
include_directories( include )
include_directories(
  ${catkin_INCLUDE_DIRS}
)

