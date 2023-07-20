#!/usr/bin/env python

import rospy
from geometry_msgs.msg import PoseWithCovarianceStamped
from nav_msgs.msg import Odometry
val = 0

# Node initialization
rospy.init_node('init_pose')
pub = rospy.Publisher('/initialpose', PoseWithCovarianceStamped, queue_size = 1)

def extractor(text):
    values = []
    lines = text.strip().split('\n')

    for line in lines:
        if ':' in line:
            key, value = line.split(':')
            key = key.strip()
            value = value.strip()
            if key in ['x', 'y', 'z', 'w']:
                if value:
                    try:
                        value = float(value)
                        values.append(value)
                    except ValueError:
                        pass

    print(values)

def get_odom():
  print("ODOM------------------------------------------------------/")
  # Construct message
  init_msg = PoseWithCovarianceStamped()
  init_msg.header.frame_id = "map"
  # Get initial pose from Gazebo
  odom_msg = rospy.wait_for_message('/odom', Odometry)
  init_msg.pose.pose.position.x = odom_msg.pose.pose.position.x
  init_msg.pose.pose.position.y = odom_msg.pose.pose.position.y
  init_msg.pose.pose.orientation.x = odom_msg.pose.pose.orientation.x
  init_msg.pose.pose.orientation.y = odom_msg.pose.pose.orientation.y
  init_msg.pose.pose.orientation.z = odom_msg.pose.pose.orientation.z
  init_msg.pose.pose.orientation.w = odom_msg.pose.pose.orientation.w

  extractor(str(init_msg))
  return init_msg


def get_amcl():
  amcl_pose_msg = rospy.wait_for_message('/amcl_pose', PoseWithCovarianceStamped)
  
  print("AMCL------------------------------------------------------/")
  # Print the received pose message
  extractor(str(amcl_pose_msg))

  # Return the pose message
  return amcl_pose_msg    
  

while True:
  val = input("enter 2 for /odom and 3 for /amcl_pose for coords: ")
  if val == 2:
    get_odom()
  if val == 3:
    get_amcl()
