#! /usr/bin/env python

import rospy

import cv2

from std_msgs.msg import String

from sensor_msgs.msg import Image
from cv_bridge import CvBridge

camera = None
fb_tp = None
bridge = None
cvimage = None


def cmdCB( cmd ):
	cmds = cmd.data.split( ':' )
	if len( cmds ) > 0:
		commands[cmds[0]]( cmds[1] )
		
		
def imageCB( img ):
	global cvimage
	cvimage = bridge.imgmsg_to_cv2( img,"rgb8" )
		
def photo( path ):
		cv2.imwrite( "/home/ubuntu/photos/"+path+".png",cvimage )
		rospy.loginfo( 'saved at {0}'.format( path ) )
		fb_tp.publish( 'ok' )
	
def video( path ):
	pass

commands = {'photo':photo,'video':video}

def initCamera( mode ):
	global camera
	if mode == 'photo':
		camera = picamera.PiCamera( resolution=(3280,2464) )
	else:
		camera = picamera.PiCamera()
		camera.resolution = '1080p'
		camera.framerate = 24
	
	
def main():
	global fb_tp,bridge
	rospy.init_node( 'camera_module_node',anonymous=False )
	
	cmdcm_tp_nm = rospy.get_param( '~cmdcm_tp','camm_command' )
	fb_tp_nm = rospy.get_param( '~feedback_tp','feedback' )
	img_tp_nm = rospy.get_param( '~image_tp','/usb_cam/image_raw' )

	rospy.Subscriber( cmdcm_tp_nm,String,cmdCB )
	
	rospy.Subscriber( img_tp_nm,Image,imageCB )
	
	fb_tp = rospy.Publisher( fb_tp_nm,String,queue_size=1 )
	
	bridge = CvBridge()

	rospy.spin()
		

if __name__ == '__main__':
	main()
	
