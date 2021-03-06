#!/usr/bin/env python
import roslib
roslib.load_manifest('finger_counter')
import rospy
import cv2
import numpy as np
import processing as process

from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

class image_feature:

    def __init__(self):
        '''Initialize ros subscriber'''
				
				#init bridge 
				self.bridge = CvBridge()
        # subscribed Topic
        self.subscriber = rospy.Subscriber("/camera/image_raw",
            image, self.callback,  queue_size = 1)
				#init background image
				input_folder = "images_main/"
				self.bckground_image = cv2.imread(input_folder+"ueye_background.png")

    def callback(self, ros_data):
        '''Callback function of subscribed topic. 
        Here images get converted and features detected'''
        #### direct conversion to CV2 ####
				cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        
				hand_image = process.remove_background(test_image, bckground_image)
				skel_image = process.skeletonize(hand_image)

				hand_image_contours = hand_image.copy()
				contour_selected = process.get_largest_contour(hand_image_contours)

				hull = cv2.convexHull(contour_selected)
				cv2.drawContours(hand_image, contour_selected, 0, (128,128,128), 3)
				cv2.drawContours(hand_image, [hull], 0, (75,75,75), 5)

				hull = cv2.convexHull(contour_selected, returnPoints = False)
				defects = cv2.convexityDefects(contour_selected, hull) 

				fingers_detected = process.detect_fingers(defects)

				#display result on image
				cv2.putText(hand_image,"Fingers detected: " + str(fingers_detected), (100, 100), cv2.FONT_HERSHEY_PLAIN, 2, 255)
   
				cv2.imshow('test_image', test_image)
				cv2.imshow('hand_image', hand_image)
				#cv2.imshow('skel image', skel_image)
				cv2.waitKey(5) 

def main(args):
    '''Initializes and cleanup ros node'''
    fd = finger_counter()
    rospy.init_node('finger_counter', anonymous=True)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print "Shutting down ROS Image feature detector module"
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
