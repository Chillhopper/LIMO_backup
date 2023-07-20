#!/usr/bin/env python

import rospy
from geometry_msgs.msg import PoseWithCovarianceStamped
import threading
import roslib
import sys, select, termios, tty

rospy.init_node('pose_publisher')
pub = rospy.Publisher('/initialpose', PoseWithCovarianceStamped, queue_size=10)
curr_pose = None

def pose_callback(pose_msg):
	global curr_pose
	curr_pose = pose_msg
	
def getKey(key_timeout):
    settings = termios.tcgetattr(sys.stdin)
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], key_timeout)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

def subscriber():
	rospy.Subscriber('/amcl_pose', PoseWithCovarianceStamped, pose_callback)	


print("wasd, 'p' to exit")
while True:
	subscriber() #updates current position
	if curr_pose is not None:
		pose_msg = curr_pose
		key_timeout = rospy.get_param("~key_timeout", 0.0)
		val = getKey(key_timeout)
		if val == 'w':
			print('w\n')
			print(pose_msg)
			pose_msg.pose.pose.position.x+=0.1
		elif val == 'a':
			print('a\n')
			pose_msg.pose.pose.position.y+=0.1
		elif val == 's':
			print('s\n')
			pose_msg.pose.pose.position.x-=0.1
		elif val == 'd':
			print('d\n')
			pose_msg.pose.pose.position.y-=0.1
		elif val == 'p':
		     print("exiting...")
		     break
		
		pub.publish(pose_msg)	

