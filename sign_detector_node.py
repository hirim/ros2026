#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import Image
from std_msgs.msg import String
from cv_bridge import CvBridge
import cv2
import numpy as np
import tflite_runtime.interpreter as tflite
import os

# 경로 자동 설정 (중요 ⭐)
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_PATH, "model", "model.tflite")
LABEL_PATH = os.path.join(BASE_PATH, "model", "labels.txt")

bridge = CvBridge()

# 모델 로드
interpreter = tflite.Interpreter(model_path=MODEL_PATH)
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# 라벨 로드
with open(LABEL_PATH, "r") as f:
    class_names = f.read().splitlines()

pub = None

def callback(msg):
    global pub

    # 이미지 변환
    frame = bridge.imgmsg_to_cv2(msg, "bgr8")

    # 전처리
    img = cv2.resize(frame, (224, 224))
    img = np.asarray(img, dtype=np.float32)
    img = (img / 127.5) - 1
    img = np.expand_dims(img, axis=0)

    # 추론
    interpreter.set_tensor(input_details[0]['index'], img)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])

    index = np.argmax(output_data)
    label = class_names[index]

    # 디버그 출력
    rospy.loginfo(f"Detected: {label}")

    # 퍼블리시 (요청하신 토픽)
    pub.publish(label)


def main():
    global pub

    rospy.init_node('sign_detector_node')

    pub = rospy.Publisher('/key_input', String, queue_size=10)

    rospy.Subscriber('/camera/image', Image, callback)

    rospy.loginfo("Sign detector node started")

    rospy.spin()


if __name__ == '__main__':
    main()