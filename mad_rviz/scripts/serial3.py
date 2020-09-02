#! /usr/bin/env python

import rospy
import serial
import io
import sys
from std_msgs.msg import Int16MultiArray
from std_msgs.msg import String

serial_port = None
serial_port_io = None
output = None
base_cmd = '!G'

def sendCmd( data ):
	cmd = 'hello =)'
	serial_port.write( cmd )
	rospy.loginfo( 'sent:%s' % cmd )

def init():
	global serial_port,output,serial_port_io
	
	rospy.init_node( 'serial_port_node',anonymous=True )
	
	serial_port_name = rospy.get_param( 'mbpo_port','/dev/tty1' )
	serial_port_baud = rospy.get_param( 'mbpo_baud',115200 )
	rospy.Subscriber( 'control_cmd',Int16MultiArray,sendCmd )
	output = rospy.Publisher( 'roboteq_output',String,queue_size=2 )
	try:
		rospy.loginfo( 'Openning roboteq serial port... port: %s' % serial_port_name )
		serial_port = serial.Serial(
			port = serial_port_name,
			baudrate = serial_port_baud,
			parity = serial.PARITY_NONE,
			stopbits = serial.STOPBITS_ONE,
			bytesize = serial.EIGHTBITS,
			xonxoff=False,
			rtscts=False,
			dsrdtr=False,
			timeout=1
		)
	except Exception:
		rospy.logerr( 'Serial port: port not available' )
		sys.exit() 
	rospy.loginfo( 'Roboteq serial port: %s.' % 'Ok!' if serial_port.isOpen() else 'Error!' )
	#rospy.spin()

def readline():
	global serial_port
	eol = b'\r'
	leneol = len(eol)
	line = bytearray()
	while True:
		c = serial_port.read( 1 )
		if c:
			line += c
			if line[-leneol:] == eol:
				break
		else:
			break
	return bytes( line )

if __name__ == '__main__':
	init()
	rate = rospy.Rate( 50 ) # 10hz
	while not rospy.is_shutdown():
		line = serial_port_io.readline( )
		#line = readline( )
		#serial_port.flush()
		output.publish( line )
		#rospy.loginfo( line )
		rate.sleep()
