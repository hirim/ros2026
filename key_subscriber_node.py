#!/usr/bin/env python3

import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist

# 속도 설정
LINEAR_SPEED = 0.1
ANGULAR_SPEED = 0.5


def callback(msg):

    key = msg.data   # 받은 키

    twist = Twist()

    # 전진
    if key == 'w':
        twist.linear.x = LINEAR_SPEED

    # 후진
    elif key == 'x':
        twist.linear.x = -LINEAR_SPEED

    # 좌회전
    elif key == 'a':
        twist.angular.z = ANGULAR_SPEED

    # 우회전
    elif key == 'd':
        twist.angular.z = -ANGULAR_SPEED

    # 정지
    elif key == 's':
        twist.linear.x = 0
        twist.angular.z = 0

    # 결과 출력 (중요)
    print("--------------------")
    print("입력 키 :", key)
    print("linear.x :", twist.linear.x)
    print("angular.z :", twist.angular.z)

    # /cmd_vel로 전송
    cmd_pub.publish(twist)


def main():

    rospy.init_node('key_subscriber_node')

    # Subscriber
    rospy.Subscriber('/key_input', String, callback)

    rospy.spin()


# Publisher는 전역으로
cmd_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)


if __name__ == '__main__':
    main()
