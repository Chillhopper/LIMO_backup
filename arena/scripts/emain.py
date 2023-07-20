#!/usr/bin/env python

import rospy
import actionlib
from geometry_msgs.msg import Twist
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from std_msgs.msg import Int8
import threading
import sys
import select
import termios
import tty


# Node Initialisation
rospy.init_node('goal_pose')

# Global variables
g_num = None

# Callbacks definition
def active_cb(extra = 0):
    rospy.loginfo("Goal pose being processed")

# def gui_callback(num):
#    global g_num
#    g_num = num.data
#    rospy.loginfo("Received message: %s", num.data)

def gui_listener():
    #global g_num
    #rospy.Subscriber('/button', Int8, gui_callback)
    message = rospy.wait_for_message('/button', Int8)
    return_val = message.data
    #g_num = None
    return return_val
    

def stop():
    navclient = actionlib.SimpleActionClient('move_base',MoveBaseAction)
    print("Stop goal sent")
    navclient.cancel_all_goals()
    

def feedback_cb(feedback):
    rospy.loginfo("press s to stop")
    myval = rospy.wait_for_message('/stopButton', Int8)
    rospy.loginfo(myval)
    #myval = getKey(rospy.get_param("~key_timeout", 0.05))
    #print("my val is: " + myval)
    if myval.data == 10:
        #print(myval)
        stop()
    #rospy.loginfo("Current location: "+str(feedback))

def done_cb(status, result):
    if status == 3:
        rospy.loginfo("Goal reached")
    if status == 2 or status == 8:
        rospy.loginfo("Goal cancelled")
    if status == 4:
        rospy.loginfo("Goal aborted")
    
# def getKey(key_timeout):
#     settings = termios.tcgetattr(sys.stdin)
#     tty.setraw(sys.stdin.fileno())
#     rlist, _, _ = select.select([sys.stdin], [], [], key_timeout)
#     if rlist:
#         key = sys.stdin.read(1)
#     else:
#         key = ''
#     termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
#     return key

# Coord Base
#x,y,z(coords) xyzw(pos) 
coords = [[0.186934063707, 0.000327325188509, 0.0, 0.0, 0.0, -0.1485751123, 0.988901125495], #index 0 ORGIN 
          [-0.111057405966, -1.27893318731, 0.0, 0.0, 0.0, -0.704684159816, 0.709521130696], #index 1 SENTOSA
          [1.22589575051, -1.3442649677, 0.0, 0.0, 0.0, 0.500792662841, 0.865567275747], #index 2 WOT
          [1.29840717381, -0.145297664525, 0.0, 0.0, 0.0, -0.158803895941, 0.987310145108], #Index 3 USS
          [-1.56816469511, -1.13540218329, 0.0, 0.0, 0.0, -0.836970448576, 0.547248086529],  #Index 4 SEAAQ
          [1.6965823744, 1.16698949311, 0.0, 0.0, 0.0, -0.909185233366, 0.41639189645],  #Index 5 Fort Siloso
          [-0.0729955176653, 1.51557513167, 0.0, 0.0, 0.0, 0.999985740603, 0.0053402800872],  #Index 6 Merlion
          [-1.39797990522, 0.25858949477, 0.0, 0.0, 0.0, -0.997053055782, 0.0767150829744],  #Index 7 Rainbow Road
          [-1.11706536093, 1.23499048882, 0.0, 0.0, 0.0, -0.540018814683, 0.841652944977]] #Index 8 iFly/Luge


def navclient_thread(navclient, goal):
   navclient.send_goal(goal, done_cb, active_cb, feedback_cb)


def result_thread(navclient):
    finished = navclient.wait_for_result()
    if not finished:
        rospy.logerr("Action server not available!")
    else:
        rospy.loginfo ( navclient.get_result())

def sui(coordList):
    navclient = actionlib.SimpleActionClient('move_base',MoveBaseAction)
    rospy.loginfo("waiting for server")
    navclient.wait_for_server()
    rospy.loginfo("server found")
    # Example of navigation goal
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()

    goal.target_pose.pose.position.x = coordList[0]
    goal.target_pose.pose.position.y = coordList[1]
    goal.target_pose.pose.position.z = coordList[2]
    goal.target_pose.pose.orientation.x = coordList[3]
    goal.target_pose.pose.orientation.y = coordList[4]
    goal.target_pose.pose.orientation.z = coordList[5]
    goal.target_pose.pose.orientation.w = coordList[6]

    navclient_thread(navclient, goal)
    result_thread(navclient)

#----------------------------------------------------------------------
while True:
    """
    val = input(
  "[0] Origin\n"
  "[1] Sentosa\n"
  "[2] Wings of Time\n"
  "[3] Universal Studios\n"
  "[4] SEA Aquarium\n"
  "[5] Fort Siloso\n"
  "[6] Merlion\n"
  "[7] Rainbow Reef\n"
  "[8] iFly/Luge\n"
  "\n"
  "enter index of area: ")
    """
    command = gui_listener()

    if command != None:
        sui(coords[command])
