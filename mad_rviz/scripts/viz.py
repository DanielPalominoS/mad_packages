#! /usr/bin/env python

import rospy

from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Odometry

hedge_viz_tp = None
ekf_viz_tp = None

def hedgeCB( msg ):
	od = Odometry()
	od.header = msg.header
	od.header.frame_id = "map"
	od.child_frame_id = "base_link"
	od.pose.pose = msg.pose
	hedge_viz_tp.publish( od )
	

def ekfCB( msg ):
	od = Odometry()
	od.header = msg.header
	od.header.frame_id = "map"
	od.child_frame_id = "base_link"
	od.pose.pose = msg.pose
	ekf_viz_tp.publish( od )
	

def init():
	global hedge_viz_tp,ekf_viz_tp
	h_tp_nm = rospy.get_param( '~hedge_tp','/mavros/vision_pose/pose' )
	ekf_tp_nm = rospy.get_param( '~ekf_tp','/mavros/local_position/pose' )
	h_od_tp_nm = rospy.get_param( '~hedeg_odom_tp','/hedge_odom' )
	ekf_od_tp_nm = rospy.get_param( '~ekf_odom_tp','/ekf_odom' )

	rospy.init_node( 'drone_viz_node',anonymous=False )


	rospy.Subscriber( h_tp_nm,PoseStamped,hedgeCB )
	rospy.Subscriber( ekf_tp_nm,PoseStamped,ekfCB )
	
	hedge_viz_tp = rospy.Publisher( h_od_tp_nm,Odometry,queue_size=1 )
	ekf_viz_tp = rospy.Publisher( ekf_od_tp_nm,Odometry,queue_size=1 )


if __name__ == '__main__':
	init()
	rospy.spin()
	
