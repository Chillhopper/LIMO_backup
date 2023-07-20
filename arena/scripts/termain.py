#!/usr/bin/env python

import rospy
import actionlib
from geometry_msgs.msg import Twist
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import threading
import sys
import select
import termios
import tty

# Node Initialisation
rospy.init_node('goal_pose')


# Callbacks definition
def active_cb(extra = 0):
    rospy.loginfo("Goal pose being processed")


def stop():
    navclient = actionlib.SimpleActionClient('move_base',MoveBaseAction)
    print("Stop goal sent")
    navclient.cancel_all_goals()
    

def feedback_cb(feedback):
    print("press s to stop")
    myval = getKey(rospy.get_param("~key_timeout", 0.1))
    #print("my val is: " + myval)
    if myval == 's':
        print("i am feedback")
	stop()
    #rospy.loginfo("Current location: "+str(feedback))

def done_cb(status, result):
    if status == 3:
        rospy.loginfo("Goal reached")
    if status == 2 or status == 8:
        rospy.loginfo("Goal cancelled")
    if status == 4:
        rospy.loginfo("Goal aborted")
    
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

# Coord Base
#x,y,z(coords) xyzw(pos) 
coords = [[-0.386695382833, 0.0424879298046, 0.0, 0.0, 0.0, -0.00250490153905, 0.999996862729], #index 0 ORGIN 
          [-1.69126015951, -0.0463478109254, 0.0, 0.0, 0.0, -0.997993223511, 0.0633208166852], #index 1 SENTOSA
          [-1.62103342139, -1.397156136, 0.0, 0.0, 0.0, 0.964335910138, 0.264681416837], #index 2 WOT
          [-0.583018437589, -1.43758706949, 0.0, 0.0, 0.0, 0.0277631894284, 0.999614528362], #Index 3 USS
          [-1.98383854798, 1.55219513185, 0.0, 0.0, 0.0, -0.957368842284, 0.288868308792],  #Index 4 SEAAQ
          [0.892950614959, -1.42552667051, 0.0, 0.0, 0.0, -0.994537768641, 0.104377328704],  #Index 5 Fort Siloso
          [0.897141718353, -0.31868321714, 0.0, 0.0, 0.0, -0.246880601993, 0.969045906219],  #Index 6 Merlion
          [-0.186661168817, 1.53146227893, 0.0, 0.0, 0.0, -0.998496600755, 0.0548136687429],  #Index 7 Rainbow Road
          [0.425864884563, 1.56001601173, 0.0, 0.0, 0.0, 0.95305514272, 0.302796788186]] #Index 8 iFly/Luge


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
    sui(coords[val])
