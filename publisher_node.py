#!/usr/bin/env python3
import rospy
from std_msgs.msg import String
def talker():
    # 1. 노드 초기화
    rospy.init_node('publisher_node')
    rospy.loginfo('publisher node started. now publish message')

    # 2. 퍼블리셔 생성
    pub = rospy.Publisher('talking_topic', String, queue_size=10)

    # 3. 주기 설정 (2Hz)
    rate = rospy.Rate(2)

    # 4. 반복 발행
    while not rospy.is_shutdown():
        msg = "call me please"
        rospy.loginfo(msg)
        pub.publish(msg)
        rate.sleep()

# 5. 메인 실행 구조
if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
