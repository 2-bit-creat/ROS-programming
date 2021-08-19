#! /usr/bin/env python

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import numpy as np

class img_editor:

    def __init__(self, node_name, topic_name):
        rospy.init_node(node_name)
        self.cvbridge = CvBridge()
        self.img_sub1 = rospy.Subscriber(topic_name,Image,self.convertImg)
        rospy.spin()

    
    def convertImg(self, img):
        img = self.cvbridge.imgmsg_to_cv2(img, "bgr8")
        cv2.imshow("image", img)
        if cv2.waitKey(1) & 0xff == ord('q'):
            exit(0)

if __name__ == "__main__":
    a = img_editor("sub_node1", "image_data1")