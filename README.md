rostensorflow
=====================

- Install tensorflow (see https://www.tensorflow.org/versions/r0.9/get_started/os_setup.html)
- Install ROS (see http://wiki.ros.org)

$ sudo apt-get install ros-indigo-cv-bridge ros-indigo-cv-camera

$ roscore
$ rosrun cv_camera cv_camera_node # you can use your favorite camera driver!
$ python rostensorflow.py image:=/cv_camera/image_raw
$ rostopic echo /result

rostensorflow.py
---------------------------

* publish: /result (std_msgs/String)
* subscribe: /image (sensor_msgs/Image)
