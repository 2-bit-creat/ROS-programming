#! /usr/bin/env python
import rospy
from geometry_msgs.msg import Twist #Twist is class


rospy.init_node('topic_publisher')
speed = rospy.get_param('~turtle_speed_x', 0.0) #private
angular_speed = rospy.get_param('~turtle_ang_vel', 0.0) #private
#angular_speed1 = rospy.get_param('/turtle_ang_vel1', 0.0) #global

pub = rospy.Publisher('cmd_vel', Twist, queue_size = 5)

msg = Twist()
msg.linear.x = speed
msg.linear.y = 0.0
msg.linear.z = 0.0
msg.angular.x = 0.0
msg.angular.y = 0.0
msg.angular.z = angular_speed
rate = rospy.Rate(2)

while not rospy.is_shutdown():
	pub.publish(msg)
	rate.sleep()
