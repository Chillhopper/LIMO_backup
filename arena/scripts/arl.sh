#!/bin/bash

# Open Terminal 1 and run roscore
gnome-terminal --tab -- bash -c "roslaunch limo_bringup limo_start.launch pub_odom_tf:=false"

# Wait for a few seconds to allow roscore to initialize
sleep 5

# Open Terminal 1 and run roscore
gnome-terminal --tab -- bash -c "roslaunch limo_bringup limo_navigation_diff.launch"

# Wait for a few seconds to allow roscore to initialize
sleep 5

# Open Terminal 2 and run emain.py
gnome-terminal --tab -- bash -c "rosrun arena emain.py"

# Wait for a few seconds to allow emain.py to initialize
sleep 5

# Open Terminal 3 and run egui.py and poseHub.py
gnome-terminal --tab -- bash -c "rosrun arena egui.py"


exit 0

