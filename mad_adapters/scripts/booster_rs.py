#! /usr/bin/env python

import rospy
import tf
from sensor_msgs.msg import LaserScan
from mad_msgs.msg import ModuleError


last_time = None
error_pub = None

source_tp_name = None
module_name = None

scale_factor = 1.0

delta_time = 0.1


def monitorCB( msg ):
	global last_time
	last_time = rospy.Time.now()

def cmdCB( msg ):
	pass

def timerEvent( event ):
	dt = (rospy.Time.now() - last_time).secs
	if dt > delta_time:
		err = ModuleError()
		err.stamp = rospy.Time.now()
		err.module = module_name
		err.error = 403
		err.description = "Data link lost! Topic not available"
		tpls = rospy.get_published_topics( "/" )
		for ls in tpls:
			if source_tp_name == ls[0]:
				err.error = 404
				err.description = "Data link lost! Logical or physical link lost"
		error_pub.publish( err )
		rospy.loginfo( "{0}, {1}, {2}".format( err.module,err.error,err.description ) )

def init():
	global error_pub,last_time,delta_time,source_tp_name,module_name,scale_factor

	rospy.init_node( 'topic_monitor_node',anonymous=False )

	source_tp_name = rospy.get_param( '~source_tp','/roombot/scan' )
	module_name = rospy.get_param( '~module_name','RPLidar Sensor' )
	delta_time = rospy.get_param( '~wd_freq_tp',0.1 )
	errors_tp_name = rospy.get_param( '~stderr_tp','stderr' )
	scale_factor = rospy.get_param( '~scale_factor',1.0 )

	rospy.Subscriber( source_tp_name,rospy.AnyMsg,monitorCB )
	error_pub = rospy.Publisher( errors_tp_name,ModuleError,queue_size=1 )

	last_time = rospy.Time.now()

	timer = rospy.Timer( rospy.Duration( 0.5 ),timerEvent )


if __name__ == '__main__':
	init()
	rospy.spin()