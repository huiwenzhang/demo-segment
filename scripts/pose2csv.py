#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
listen the end effecotr transform and recored the pose info ini csv file
"""
"""
BUGS (SOLVED):
1) getch() will wait untill key press happen,
2) keyboard module must be used as root, where ROS env is not accessible 
3) well, callback, rospy.is_shutdown doesn't accept arguments,
"""


import rospy
import tf
import pandas as pd
# import readchar
import sys
pose_data = []  

def saveData():
    my_df = pd.DataFrame(pose_data)
    # file_name = raw_input("Please input the CSV file name:")
    # my_df.to_csv(file_name + '.csv', index=False, header=['t', 'x', 'y', 'z', 'q_x', 'q_y', 'q_z', 'w'])
    my_df.to_csv(file_name + '.csv', index=False, header=False)

rospy.on_shutdown(saveData)

if __name__ == '__main__':
    rospy.init_node('record_ee_pose')
    if len(sys.argv) < 2:
        print "Please specify the name for the save file."
        exit(0)
    file_name = sys.argv[1]
    listener = tf.TransformListener()
    rate = rospy.Rate(10.0)
    time = 0.0
    while not rospy.is_shutdown():
        try:
            # trans is list [x y z], rot is a quat [x y z w]
            print "Look for transform.."
            (trans,rot) = listener.lookupTransform('/base_footprint', '/arm_7_link', rospy.Time(0))
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            continue
        print 'trans', trans
        # print 'rot: ', rot
        tempt = [time] + list(trans) + list(rot)
        pose_data.append(tempt)
        rate.sleep()
        time += 0.1 # update time
   