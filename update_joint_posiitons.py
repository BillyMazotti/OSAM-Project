#!/usr/bin/env python3

import rospy
from std_msgs.msg import String
from sensor_msgs.msg import JointState
from write_json import write_to_json
import time
import numpy as np
import h5py

json_path_on_hose = "/run/user/1000/gvfs/sftp:host=billys-macbook-pro-5.local/Users/billymazotti/Documents/UofM/StirlingGroup/OSAM_HRI/OSAM-Project/test_connection.json"
joint_positions = {
    "timestamp": 0.0,
	"joint_1" : 0.0, 
	"joint_2" : 0.0, 
	"joint_3" : 0.0, 
	"joint_4" : 0.0, 
	"joint_5" : 0.0, 
	"joint_6" : 0.0, 
	"joint_7" : 0.0, 
	"joint_8" : 0.0, 
	"joint_9" : 0.0, 
}

hd5f_path_on_host = '/run/user/1000/gvfs/sftp:host=billys-macbook-pro-5.local/Users/billymazotti/Documents/UofM/StirlingGroup/OSAM_HRI/OSAM-Project/test_connection.h5'




def callback(data):
    rospy.loginfo("receiving data...")
    t0 = time.time()

    # send
    #  to JSON
    # joint_positions["timestamp"] = data.header.stamp.secs + 1e-9*data.header.stamp.nsecs
    # joint_positions["joint_1"] = data.position[0]
    # joint_positions["joint_2"] = data.position[1]
    # joint_positions["joint_3"] = data.position[2]
    # joint_positions["joint_4"] = data.position[3]
    # joint_positions["joint_5"] = data.position[4]
    # joint_positions["joint_6"] = data.position[5]
    # joint_positions["joint_7"] = data.position[6]
    # joint_positions["joint_8"] = data.position[7]
    # joint_positions["joint_9"] = data.position[8]
    # write_to_json(json_path_on_hose,joint_positions)

    # send ot HD5F
    joints_array = np.array([data.header.stamp.secs + 1e-9*data.header.stamp.nsecs,
                             data.position[0],
                             data.position[1],
                             data.position[2],
                             data.position[3],
                             data.position[4],
                             data.position[5],
                             data.position[6],
                             data.position[7],
                             data.position[8]]).astype(float)
    h5f = h5py.File(hd5f_path_on_host,'w')
    h5f.create_dataset('joints_dataset',data=joints_array)
    print(f"Update Frequency {int(1/(time.time()-t0))} hz")
    
def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber("/joint_states", JointState, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()