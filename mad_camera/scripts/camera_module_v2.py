#! /usr/bin/env python

import rospy

import time, os

import cv2

from std_msgs.msg import String

from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from mad_msgs.srv import CamCmd, CamCmdResponse
from mad_msgs.srv import InitCapture, InitCaptureResponse


camera = None
fb_tp = None
bridge = None
cvimage = None


camm_fb_tp = None
enable = 0
fformat = 'png'
media_root =os.getenv('HOME')+'/Pictures'# None
path ='sitl_drone_tests'# None




def imageCB( img ):
	global cvimage
	cvimage = bridge.imgmsg_to_cv2( img,"rgb8" )

def init_cm_CB(req):
	response = False
	mode_ = req.mode
	mode[mode_](req.file_format, req.media_root)
	response=True	
	return InitCaptureResponse(response)

def initPhoto(ff, mr):
	global enable,fformat,media_root, path
	media_root = mr
	fformat=ff
	path = createPath( media_root )
	#media_root = '../photos{0}'.format( path )
	enable = 2

	
def initVideo(ff,mr):
	global enable, path, fformat, media_root
	media_root = mr
	fformat=ff
	path = createPath( '../videos' )
	#fformat = 'h264'
	#media_root = '../videos{0}'.format( path )
	#path = media_root + '/video_' + time.asctime( time.localtime( time.time() ) ).replace( ' ','_' ) + '.' + fformat
	enable = 1
mode = {'initPhoto': initPhoto, 'initVideo': initVideo}

def createPath( root ):
    try:
        path = time.asctime(time.localtime(time.time())).replace(' ', '_').replace(':', '_')   	  
        os.mkdir(root + '/' + path)
    except OSError:
		rospy.loginfo("Creation of the directory {0} failed. Using local directory.".format(path))
		#return ''
		return os.getcwd()
    else:  
        rospy.loginfo( "Successfully created the directory: {0} ".format( path ) )
        return root+'/{0}'.format(path)
		
def cmdCB(req):
	global path
	response = False	
	#cmds = req.command.data.split(':')
	cmds = req.command.split( ':' )
	if len( cmds ) > 0:
		commands[cmds[0]](cmds[1])
		response=True
		
	return CamCmdResponse(response)

		
def photo(img_seq):
	global cvimage, fformat, path
	img_nm=path+'/'+img_seq+'_'+time.asctime( time.localtime( time.time() ) ).replace( ' ','_' ).replace( ':','_' )
	cv2.imwrite( img_nm+'.'+fformat,cvimage )
	rospy.loginfo( 'saved at {0}'.format( path ) )
	fb_tp.publish( 'ok' )
	
def video( vid_nm ):
	pass
commands = {'photo': photo, 'video': video}
	
def main():
	global fb_tp,bridge
	rospy.init_node( 'camera_module_node',anonymous=False )
	
	cmdcm_tp_nm = rospy.get_param('~cmdcm_tp', 'camm_command')
	init_cm_tp_nm = rospy.get_param( '~init_cm_tp','init_camm' )
	fb_tp_nm = rospy.get_param( '~feedback_tp','feedback' )
	img_tp_nm = rospy.get_param( '~image_tp','/iris/c920/image_raw' )

	rospy.Service(cmdcm_tp_nm, CamCmd, cmdCB)
	rospy.Service(init_cm_tp_nm,InitCapture,init_cm_CB )
	
	rospy.Subscriber( img_tp_nm,Image,imageCB )
	
	fb_tp = rospy.Publisher( fb_tp_nm,String,queue_size=1 )
	
	bridge = CvBridge()

	rospy.spin()
		

if __name__ == '__main__':
	main()
	
