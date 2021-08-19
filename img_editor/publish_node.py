#! /usr/bin/env python

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import numpy as np

class img_editor:
    def __init__(self, name):
        self.cvbridge = CvBridge()
        self.img_pub = rospy.Publisher(
            name,
            Image,
            queue_size=5
        )    

    def Canny(self, img):
        edges = cv2.Canny(img, 100, 200)
        return edges

    def Thresh(self, img):
        ret, thr = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
        return thr

    def Blur(self, img):
        blur = cv2.GaussianBlur(img, (0, 0), 5)
        return blur

    def Color(self, img):
        low_white = np.array([0, 0, 0])
        high_white = np.array([100, 255, 255])
        mask = cv2.inRange(img, low_white, high_white)
        output = cv2.bitwise_and(img, img, mask=mask)
        return output

    def Combine(self, img1, img2, img3, img4):
        row = img1.shape[0]
        col = img1.shape[1]
        img1 = np.dstack([img1]*3)
        addv1 = np.vstack((img1, img3))
        addv2 = np.vstack((img2, img4))
        addh = np.hstack((addv1, addv2))
        addh = cv2.resize(addh, dsize=(640, 480), interpolation=cv2.INTER_AREA)
        return addh
    
class ros_cam_receive(img_editor):
    def __init__(self):
        rospy.init_node("ros_cam_receive")
        self.cvbridge = CvBridge()
        self.img_sub1 = rospy.Subscriber("/usb_cam/image_raw",Image,self.convertImg)
        rospy.spin()

    def convertImg(self, img):
        img = self.cvbridge.imgmsg_to_cv2(img, "bgr8")
        self.pub("image_data2").publish(self.cvbridge.cv2_to_imgmsg(self.Color(img)))

    def pub(self):
        self.cvbridge = CvBridge()
        self.img_pub = rospy.Publisher(
            "image_data2",
            Image,
            queue_size=5
        )   
        return self.img_pub


if __name__ == "__main__":
    rospy.init_node("asd")
    a = img_editor("image_data1")
    b = img_editor("image_data2")
    c = img_editor("image_data3")
    d = img_editor("image_data4")
    e = img_editor("image_data5")
    #f = ros_cam_receive()


    cap = cv2.VideoCapture(0)
    
    ret, frame = cap.read()
    while not rospy.is_shutdown():
        cv2.imshow("frame",frame)
        a.img_pub.publish(a.cvbridge.cv2_to_imgmsg(a.Combine(a.Canny(frame), a.Color(frame), a.Thresh(frame), a.Blur(frame)), "rgb8"))
        b.img_pub.publish(b.cvbridge.cv2_to_imgmsg(a.Blur(frame),"rgb8"))
        c.img_pub.publish(c.cvbridge.cv2_to_imgmsg(a.Color(frame),"rgb8"))
        d.img_pub.publish(d.cvbridge.cv2_to_imgmsg(a.Thresh(frame),"rgb8"))
        e.img_pub.publish(e.cvbridge.cv2_to_imgmsg(a.Canny(frame),"mono8"))
        if cv2.waitKey(1) & 0xff == ord('q'):
             exit(0)
        ret, frame = cap.read()
        