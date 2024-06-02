from sensor_msgs.msg import LaserScan
import math
from numpy import *
from trig_table import trig_tab_degrees
import rospy

class ScanFilter:
    def __init__(self):
        self.width = 0.1
        self.height = 0.1
        self.extent_X = self.height
        self.extent_Y = self.width
        self.sub = rospy.Subscriber('/scan', LaserScan, self.callback)
        self.pub = rospy.Publisher('filtered_scan', LaserScan, queue_size=10)
        rospy.loginfo("Publishing the filtered_scan topic. Use RViz to visualize.")

    def callback(self,msg):
        detect_front = None
        detect_back = None
        angles = linspace(msg.angle_min, msg.angle_max, len(msg.ranges))
        points_X = [r * cos(theta) if ((theta >= 0 and theta <= 6.28319)) else inf for r,theta in zip(msg.ranges, angles)]
        points_Y = [r * sin(theta) if ((theta >= 0 and theta <= 6.28319)) else inf for r,theta in zip(msg.ranges, angles)]
        for i,j,theta in zip(points_X, points_Y, angles):
            if((abs(i) < self.extent_X and abs(j) < self.extent_Y) and ((theta >= 0 and theta <= 1.5708) or (theta >= 4.71238 and theta <= 6.28319))):
                 detect_front = True
                 print("Objet détecté devant")
        for i,j,theta in zip(points_X, points_Y, angles):
            if((abs(i) < self.extent_X and abs(j) < self.extent_Y) and (theta >= 1.5708 and theta < 4.71238)):
                 detect_back = True
                 print("Objet détecté derrière")
        new_ranges = [r if(abs(y) < self.extent_Y and abs(x) < self.extent_X) else inf for r,x,y in zip(msg.ranges, points_X, points_Y)]
        msg.ranges = new_ranges
        self.pub.publish(msg)

if __name__ == '__main__':
    rospy.init_node('scan_filter')
    ScanFilter()
    rospy.spin()

