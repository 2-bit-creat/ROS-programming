#! /usr/bin/env python
import cv2
import numpy as np
import serial
import matplotlib.pyplot as plt
from sensor_msgs.msg import Image
from std_msgs.msg import Int32
import time
import rospy
from cv_bridge import CvBridge

class visualization:
    def __init__(self):
        rospy.init_node("viz_node")
        self.cvbridge = CvBridge()
        self.frame_sub = rospy.Subscriber("/frame",Image,self.convertIng)   
        rospy.spin()

    def convertIng(self, img):
        frame = self.cvbridge.imgmsg_to_cv2(img, "bgr8")
        cv2.imshow("frame", frame)
        cv2.waitKey(1)

if __name__ == '__main__':
    a = visualization()