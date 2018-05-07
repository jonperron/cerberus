#! /usr/bin/python3

import cv2
import multiprocessing
import tensorflow as tf

from multiprocessing import Queue, Pool
from cerberus.firsthead import FirstHead
from cerberus.secondhead import SecondHead

class Cerberus:
    """
    Main class, guarding.
    """
    def __init__(self, *args, **kwargs):
        self.firsthead = FirstHead()
        self.secondhead = SecondHead()
		
    def worker(self, input_q):
        # Load a (frozen) Tensorflow model into memory.
        detection_graph = tf.Graph()
        with detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(self.secondhead.model_file, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')

            sess = tf.Session(graph=detection_graph)

        while True:
            frame = input_q.get()
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            objects = self.secondhead.detect_objects(frame_rgb, sess, detection_graph)
            print(objects)

        sess.close()

    def guard(self, *args, **kwargs):
        input_q = Queue(maxsize=1)
        pool = Pool(2, self.worker, (input_q,))

        video_capture = self.firsthead.start()
        
        while True:
            ret, frame = video_capture.read()
            input_q.put(frame)
        
            if cv2.waitKey(5000) & 0xFF == ord("q"):
                self.firsthead.stop()
                break
