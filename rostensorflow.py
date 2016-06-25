import rospy
from sensor_msgs.msg import Image
from std_msgs.msg import String
from cv_bridge import CvBridge, CvBridgeError
import cv2
import numpy as np
import tensorflow as tf

import classify_image

class RosTensorFlow():
    def __init__(self):
        classify_image.maybe_download_and_extract()
        self._sub = rospy.Subscriber('image', Image, self.callback, queue_size=1)
        self._pub = rospy.Publisher('result', String, queue_size=1)

    def callback(self, image_msg):
        bridge = CvBridge()
        print 'start'
        cv_image = bridge.imgmsg_to_cv2(image_msg, "bgr8")
        cv2.imwrite('tmp.jpg', cv_image)
        # copy from
        # https://github.com/tensorflow/tensorflow/blob/master/tensorflow/models/image/imagenet/classify_image.py
        image_data = tf.gfile.FastGFile('tmp.jpg', 'rb').read()
        # Creates graph from saved GraphDef.
        classify_image.create_graph()
        with tf.Session() as sess:
            softmax_tensor = sess.graph.get_tensor_by_name('softmax:0')
            predictions = sess.run(softmax_tensor,
                                   {'DecodeJpeg/contents:0': image_data})
            predictions = np.squeeze(predictions)
            # Creates node ID --> English string lookup.
            node_lookup = classify_image.NodeLookup()
            num_top_predictions = 5
            top_k = predictions.argsort()[-num_top_predictions:][::-1]
            for node_id in top_k:
                human_string = node_lookup.id_to_string(node_id)
                score = predictions[node_id]
                print('%s (score = %.5f)' % (human_string, score))
                self._pub.publish(human_string)

    def main(self):
        rospy.spin()

if __name__ == '__main__':
    rospy.init_node('rostensorflow')
    tensor = RosTensorFlow()
    tensor.main()
