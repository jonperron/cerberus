# cerberus
Open-source CCTV solution with real time recognition

# Requires
* [Tensorflow](https://www.tensorflow.org/)
* [Tensorflow object detection API](https://github.com/tensorflow/models/tree/master/research/object_detection)
* [OpenCV](https://opencv.org/)
* [Falcon](https://falconframework.org/)
* [Redis](https://redis.io) installed on the host system

# How to use it ?
It's written to run on a Raspberry Pi 3 at least, using an external USB Webcam. Follow [to install OpenCV on raspbian](www.pyimagesearch.com/2016/04/18/install-guide-raspberry-pi-3-raspbian-jessie-opencv-3/). 
[Tensorflow object detection] needs to be cloned in the `Tensorflow` folder as it is. Then call `Cerberus().guard()` and it should work, as it works on my own system.
