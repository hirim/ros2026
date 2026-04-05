#!/usr/bin/env python3

import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import numpy as np

bridge = CvBridge()

def callback(msg):
    global pub

    # ROS → OpenCV
    frame = bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

    # HSV 변환
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 🔴 빨강
    lower_red1 = np.array([0, 100, 100])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([160, 100, 100])
    upper_red2 = np.array([179, 255, 255])

    red_mask = cv2.inRange(hsv, lower_red1, upper_red1) + \
               cv2.inRange(hsv, lower_red2, upper_red2)

    # 🟢 초록
    lower_green = np.array([40, 100, 100])
    upper_green = np.array([80, 255, 255])
    green_mask = cv2.inRange(hsv, lower_green, upper_green)

    # 픽셀 수
    red_count = cv2.countNonZero(red_mask)
    green_count = cv2.countNonZero(green_mask)

    out_msg = String()

    # 판단 ⭐
    if red_count > 5000:
        out_msg.data = 's'
    elif green_count > 5000:
        out_msg.data = 'w'
    else:
        pass 

    pub.publish(out_msg)

    # 디버깅
    cv2.imshow("frame", frame)
    cv2.imshow("red", red_mask)
    cv2.imshow("green", green_mask)
    cv2.waitKey(1)


rospy.init_node('color_publisher')

# 출력 토픽 변경 ⭐
pub = rospy.Publisher('/key_input', String, queue_size=10)

# 입력 토픽 변경 ⭐
rospy.Subscriber('/camera/image', Image, callback)

rospy.spin()