#! /usr/bin/env python

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

class Tutorial:
    def __init__(self):
        rospy.init_node("tutorial_node")
        self.cvbridge = CvBridge()
        self.imgSubFromUsbCamPackage = rospy.Subscriber(
            "/usb_cam/image_raw",
            Image,
            self.convertImg
        )

        # self.img_pub = rospy.Publisher(
        #     "/test_img",
        #     Image,
        #     queue_size=5
        # )
        
        rospy.spin() #it starts when typing

    def convertImg(self, _img):
        #print("receivce")
        _img = self.cvbridge.imgmsg_to_cv2(_img, "bgr8")
        cv2.imshow("usb_cam_img", _img)
        if cv2.waitKey(1) & 0xff == ord('q'):
            exit(0)
        # gray Image "bgr8" -> "mono8"

    # def run(self):
    #     cap = cv2.VideoCapture(0)
    #     ret, frame = cap.read()
    #     while ret:
    #         cv2.imshow("test", frame)
    #         if cv2.waitKey(1) & 0xff == ord('q'):
    #             exit(0)
    #         ret, frame = cap.read()
    #         self.img_pub.publish(self.cvbridge.cv2_to_imgmsg(frame, "bgr8"))



if __name__ == "__main__":
    ttt = Tutorial()
    #ttt.run()