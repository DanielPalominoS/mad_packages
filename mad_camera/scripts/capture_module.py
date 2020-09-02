#! /usr/bin/env python

import rospy

import time,os

from std_msgs.msg import String
from mavros_msgs.msg import WaypointReached


camm_fb_tp = None

enable = 0
fformat = None
media_root = None
path = None



def takePhoto( index ):
	#path = media_root + '/photo_' + time.asctime( time.localtime( time.time() ) ).replace( ' ','_' ) + '-' + str( index ) + '.' + fformat
	#path = 'photo_' + time.asctime( time.localtime( time.time() ) ).replace( ' ','_' ) + '-' + str( index ) + '.' + fformat
	path = '' + time.asctime( time.localtime( time.time() ) ).replace( ' ','_' ).replace( ':','_' )
	camm_fb_tp.publish( 'photo:'+path )

def takeVideo():
	pass
		
def initPhoto():
	global enable,fformat,media_root
	path = createPath( '../photos' )
	fformat = 'png'
	media_root = '../photos{0}'.format( path )
	enable = 2
	takePhoto( 0 )
	
def initVideo():
	global enable,path,fformat,media_root
	path = createPath( '../videos' )
	fformat = 'h264'
	media_root = '../videos{0}'.format( path )
	path = media_root + '/video_' + time.asctime( time.localtime( time.time() ) ).replace( ' ','_' ) + '.' + fformat
	enable = 1

commands = {'photo':initPhoto,'video':initVideo}

def cmdCB( cmd ):
	cmds = 'photo'#cmd.data.split( ':' )
	if len( cmds ) > 0:
		commands[cmds[0]](  )

def feedbackCamModuleCB( msg ):
	if enable == 1: # video
		pass
	elif enable == 2: # photo
		pass #motm_fb_tp.publish( None )

def feedbackMotionModuleCB( msg ):
	takePhoto( msg.wp_seq )

def createPath( root ):
    try:
        path = time.asctime( time.localtime( time.time() ) ).replace( ' ','_' ).replace( ':','_' )        	  
        #os.mkdir( root+'/'+path )
    except OSError:  
        rospy.loginfo( "Creation of the directory {0} failed. Using default directory.".format( path ) )
        return ''
    else:  
        rospy.loginfo( "Successfully created the directory: {0} ".format( path ) )
        return '/{0}'.format( path )
	
	
def main():
	global camm_fb_tp,motm_fb_tp
	rospy.init_node( 'capture_module_node',anonymous=False )
	
	cmd_tp_nm = rospy.get_param( '~cmd_tp','/mavros/mission/reached' )

	camm_tp_nm = rospy.get_param( '~cmdcm_tp','camm_command' )
	camm_fb_tp_nm = rospy.get_param( '~camm_feedback_tp','camm_feedback' )

	motm_tp_nm = rospy.get_param( '~motcm_tp','motm_command' )
	motm_fb_tp_nm = rospy.get_param( '~motm_feedback_tp','mavros/mission/reached' )

	rospy.Subscriber( cmd_tp_nm,WaypointReached,cmdCB )
	rospy.Subscriber( camm_fb_tp_nm,String,feedbackCamModuleCB )
	rospy.Subscriber( motm_fb_tp_nm,WaypointReached,feedbackMotionModuleCB )

	camm_fb_tp = rospy.Publisher( camm_tp_nm,String,queue_size=1 )
	motm_fb_tp = rospy.Publisher( motm_tp_nm,String,queue_size=1 )

	rospy.spin()
		

if __name__ == '__main__':
	main()
	
