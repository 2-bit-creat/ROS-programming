#! /usr/bin/env python

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2


class Tutorial:
    def __init__(self):
        self.cvbridge = CvBridge()
        rospy.init_node("tutorial_pub_node")
        self.img_pub = rospy.Publisher(
            "/usb_cam/image_raw",
            Image,
            queue_size=5
        )



if __name__ == "__main__":

    ttt = Tutorial()

    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    while not rospy.is_shutdown():
        #cv2.imshow("test", frame)
        #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.cvtColor(frame,  cv2.COLOR_BGR2GRAY)
        canny = cv2.Canny(gray, 100, 200)
        ttt.img_pub.publish(ttt.cvbridge.cv2_to_imgmsg(canny, "mono8"))
        if cv2.waitKey(1) & 0xff == ord('q'):
             exit(0)
        ret, frame = cap.read()
        