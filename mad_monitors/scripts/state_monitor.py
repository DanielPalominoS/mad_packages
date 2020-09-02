#! /usr/bin/env python

import rospy
from mad_msgs.msg import ModuleError
from std_msgs.msg import Empty
from mavros_msgs.srv import *


mav_tp = None
mavros_srv_name = ''

	
def errorCB( msg ):
	mavrosSRV()

def mavrosSRV():
	rospy.wait_for_service( mavros_srv_name )
	try:
		mavCMD = rospy.ServiceProxy( mavros_srv_name,CommandTOL )
		resp = mavCMD( CommandTOLRequest() )
		rospy.loginfo( 'Mavros command sent {0}'.format( resp ) )
	except:
		rospy.loginfo( 'Mavros service error' )
	
	
def main():
	global mav_tp,mavros_srv_name
	
	rospy.init_node( 'state_monitor_node',anonymous=False )
	
	error_tp_nm = rospy.get_param( '~error_tp','stderr' )
	cmd_tp_nm = rospy.get_param( '~cmd_tp','mavros' )
	mavros_srv_name = rospy.get_param( '~mavros_srv_name','mavros/cmd/land' )

	rospy.Subscriber( error_tp_nm,ModuleError,errorCB )
	
	mav_tp = rospy.Publisher( cmd_tp_nm,Empty,queue_size=1 )

	rospy.spin()
		


if __name__ == '__main__':
	main()

	