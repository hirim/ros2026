#!/usr/bin/env python3

import rospy
from std_msgs.msg import String

def callback(msg): 
    rospy.loginfo("received data: %s", msg.data) 

def main(): 
    rospy.init_node('Subscriber_Node', anonymous=True)
    rospy.Subscriber('talking_topic', String, callback)
    rospy.spin()

if __name__ == "__main__": 
    try: 
        main()
    except rospy.ROSInterruptException: 
        pass

