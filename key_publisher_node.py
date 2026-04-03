#!/usr/bin/env python3

import rospy
from std_msgs.msg import String

def main():
    rospy.init_node('key_publisher_node')
    pub = rospy.Publisher('/key_input', String, queue_size=10)

    print("""
         w
    a    s    d
         x
    s : stop   q : quit
    """)

    while not rospy.is_shutdown():
        key = input("키 입력 : ")

        if key == 'q':
            print("프로그램 종료")
            break

        elif key in ['w', 'a', 's', 'd', 'x']:
            msg = String()
            msg.data = key
            pub.publish(msg)

            print(f"전송 : {key}")

        else:
            print("잘못된 입력 → 프로그램 종료")
            break


if __name__ == '__main__':
    main()
