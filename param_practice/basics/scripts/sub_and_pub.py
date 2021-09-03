#! /usr/bin/env python
import rospy
from geometry_msgs.msg import Twist

rospy.init_node('topic_subscriber')
pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size = 5)
def cb(data):
    pub.publish(data)
sub = rospy.Subscriber('cmd_vel', Twist, cb)

rospy.spin()