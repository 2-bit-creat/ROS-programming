#! /usr/bin/env python
import cv2
import serial
import time
import numpy as np
import ctypes
import rospy
from std_msgs.msg import Int32

class serial_com:
    def __init__(self):
        rospy.init_node("main_node")
        self.flag_sub = rospy.Subscriber(
            "/flag",
            Int32,
            self.ch_flag
        )
        self.flag = 0

    def ch_flag(self, _data):
        self.flag = _data.data

    def writeBuffer(self, data, speed, _steer):
        direction = 0

        speed = np.uint16(speed)
        _steer = np.uint16(_steer)
        speed_Lo = speed & 0xFF
        speed_Hi = speed >> 8
        steer_Lo = _steer & 0xFF
        steer_Hi = _steer >> 8

        sum = direction + speed_Lo + speed_Hi + steer_Lo + steer_Hi + 220 + 5 + 10 + 13
        clc = np.uint8(~sum)

        data.append(0x53)
        data.append(0x54)
        data.append(0x58)
        data.append(direction)
        data.append(speed_Lo)
        data.append(speed_Hi)
        data.append(steer_Lo)
        data.append(steer_Hi)
        data.append(0xDC)
        data.append(0x05)
        data.append(0x00)
        data.append(0x0D)
        data.append(0x0A)
        data.append(clc)


    def serWrite(self, ser, _speed, _steer):
        data = []
        self.writeBuffer(data, _speed, _steer)

        for i in range(0, len(data), 1):
            data[i] = np.uint8(data[i])
        #print(data)
        ser.write(data)
        
    def run(self): #the while loop here can replace rospy.spin
        rate = rospy.Rate(40)
        seri = serial.Serial('/dev/ttyUSB1', 115200)
        while True:
            if self.flag == 0:
                self.serWrite(seri, 150, 1550)
            elif self.flag == 1:
                self.serWrite(seri, 0, 1550)
                time.sleep(2)
            rate.sleep()

if __name__ == "__main__":
    a = serial_com()
    a.run()