#! /usr/bin/env python
import cv2
import numpy as np
import serial
import matplotlib.pyplot as plt
from sensor_msgs.msg import Image
import time
import rospy
from cv_bridge import CvBridge

class LaneDetection:
    low_yellow = np.array([15, 150, 120])
    high_yellow = np.array([25, 230, 210])
    low_white = np.array([0, 200, 0])
    high_white = np.array([255, 255, 255])
    
    def __init__(self):
        rospy.init_node("ros_cam_receive")
        self.cvbridge = CvBridge()
        self.img_sub1 = rospy.Subscriber("/usb_cam/image_raw",Image,self.convertImg)
        rospy.spin()

    def convertImg(self, img):
        frame = self.cvbridge.imgmsg_to_cv2(img, "bgr8")
        frame = cv2.resize(frame, dsize=(640, 480), interpolation=cv2.INTER_AREA)
        colored_image = self.color_detect(frame)
        bird_eye_image = self.bird_eye(colored_image)
        slidng_list_left = self.sliding_left(bird_eye_image)
        sliding_list_right = self.sliding_right(bird_eye_image)
        frame_steer = self.steering(frame, slidng_list_left, sliding_list_right)

        bird_eye_image = cv2.cvtColor(bird_eye_image, cv2.COLOR_GRAY2BGR)
        for i in slidng_list_left:
            cv2.circle(bird_eye_image, i, 5, (255, 255, 0), -1)
        for i in sliding_list_right:
            cv2.circle(bird_eye_image, i, 5, (255, 255, 0), -1)
        cv2.imshow("bird_eye", bird_eye_image)
        cv2.imshow("frame", frame_steer)
        cv2.waitKey(1)
        

    def steering(self, frame, slidng_list_left, sliding_list_right):
        x_left = []
        x_right = []

        for i in range(0, len(slidng_list_left)): #extract x coordinate from slidng_list_left
            x_left.append(slidng_list_left[i][0])
        left_arr = np.array(x_left)
        left_diff_arr = np.diff(x_left)
        left_diff_sum = np.sum(left_diff_arr)
        left_avg = int(left_diff_sum/5)

        for i in range(0, len(sliding_list_right)): #extract x coordinate from sliding_list_right
            x_right.append(sliding_list_right[i][0])
        right_arr = np.array(x_right)
        right_diff_arr = np.diff(x_right)
        right_diff_sum = np.sum(right_diff_arr)
        right_avg = int(right_diff_sum/5)


        avg_val = int((left_diff_sum + right_diff_sum)/2)
        if np.sum(avg_val) < -7:
            cv2.arrowedLine(frame, (300, 340), (340, 340), (255, 0, 0), 4)
        elif np.sum(avg_val) > 7:
            cv2.arrowedLine(frame, (340, 340), (300, 340), (255, 0, 0), 4)
        else:
            cv2.arrowedLine(frame, (320, 340), (320, 300), (255, 0, 0), 4)

        return frame

    def sliding_left(slef, img):
        left_list = []
        for j in range(259, img.shape[0] - 20, 40): #row: starting at y=259 to y=260, moving distance is 40
            j_list = []
            for i in range(19, int(img.shape[1]/2) - 20, 5): #col: starting at x=19 to y=300, moving distance is 5
                num_sum = np.sum(img[j - 19:j + 21, i - 19:i + 21]) #window size is 20*20
                if num_sum > 100000: #pick i given j where its num_sum is over 100000
                    j_list.append(i)
            try:
                len_list = [] 
                result = np.split(j_list, np.where(np.diff(j_list) > 5)[0] + 1) #cluster if a gap between elements in the list is over 5
                for k in range(0, len(result)):
                    len_list.append(len(result[k])) #append the lengths of each cluster
                largest_integer = max(len_list)
            
                for l in range(0, len(result)):
                    if len(result[l]) == largest_integer: 
                        avg = int(np.sum(result[l]) / len(result[l])) #average
                        left_list.append((avg, j)) #avg points of left side 
            except:
                continue
        return left_list

    def sliding_right(slef, img):
        right_list = []
        for j in range(259, img.shape[0] - 20, 40): #row
            j_list = []
            for i in range(int(img.shape[1]/2), img.shape[1] - 20, 5): #col
                num_sum = np.sum(img[j - 19:j + 21, i - 19:i + 21]) #window size is 20*20
                if num_sum > 100000: #pick i given j where its num_sum is over 100000
                    j_list.append(i)
            try:
                len_list = []
                result = np.split(j_list, np.where(np.diff(j_list) > 5)[0] + 1) #clustering
                for k in range(0, len(result)):
                    len_list.append(len(result[k]))
                largest_integer = max(len_list)
            
                for l in range(0, len(result)):
                    if len(result[l]) == largest_integer: 
                        avg = int(np.sum(result[l]) / len(result[l])) #average
                        right_list.append((avg, j))  
            except:
                continue
        return right_list

    def color_detect(self, img):
        hsl = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)
        mask_white = cv2.inRange(hsl, self.low_white, self.high_white)
        mask_yellow = cv2.inRange(hsl, self.low_yellow, self.high_yellow)
        mask = cv2.bitwise_or(mask_white, mask_yellow)
        return mask

    def bird_eye(self, frame):
        # cv2.circle(frame, (170, 339), 5, (0, 0, 255), -1)
        # cv2.circle(frame, (420, 339), 5, (0, 0, 255), -1)
        # cv2.circle(frame, (90, 419), 5, (0, 0, 255), -1)
        # cv2.circle(frame, (490, 419), 5, (0, 0, 255), -1)
        #cv2.imshow("frame", frame)
        pts1 = np.float32([[180, 339], [410, 339], [90, 419], [490, 419]])
        pts2 = np.float32([[0, 0], [640, 0], [0, 480], [640, 480]])

        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        result = cv2.warpPerspective(frame, matrix, (640, 480))
        return result

if __name__ == '__main__':
    a = LaneDetection()
