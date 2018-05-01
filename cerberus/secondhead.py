#! /usr/bin/python3,

import os
import numpy as np
import tensorflow as tf

from tensorflow.models.research.object_detection.utils import label_map_util
from tensorflow.models.research.object_detection.utils import visualization_utils as vis_util

class SecondHead:
	"""
	Second Head : Thinking.
	
	Uses Tensorflow to find intruders.
	"""
	# Load model from tf_models folder
	CURRENT_DIR = os.path.dirname(os.getcwd())
	
	# List of the strings used to add correct label for each box
	LABELS_FILE = os.path.join(CURRENT_DIR, 'lib/python3.5/site-packages/tensorflow/models/research/object_detection/data', 'mscoco_label_map.pbtxt')

	def __init__(
		self,
		model_name='ssd_mobilenet_v1_coco_2017_11_17',
		num_classes=90,
		*args,
		**kwargs
	):
		self.model_file = os.path.join(self.CURRENT_DIR, 'tf_models', model_name, 'frozen_inference_graph.pb')
		self.category_index = self.get_category_index(self.LABELS_FILE, num_classes)
		
	def get_category_index(self, labels_file, num_classes):
		"""
		Create category index.
		
		Adapted from TF object recognition tutorial.
		"""
		label_map = label_map_util.load_labelmap(labels_file)
		categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=num_classes, use_display_name=True)
		category_index = label_map_util.create_category_index(categories)
		return category_index

	def detect_objects(self, image_np, sess, detection_graph):
		"""
		Detect objects using tensorflow session.
		
		Adapted from TF object recognition tutorial.
		"""
		# Expand dimensions since the model expects images to have shape: [1, None, None, 3]
		image_np_expanded = np.expand_dims(image_np, axis=0)
		image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

		# Each box represents a part of the image where a particular object was detected.
		boxes = detection_graph.get_tensor_by_name('detection_boxes:0')

		# Each score represent how level of confidence for each of the objects.
		# Score is shown on the result image, together with the class label.
		scores = detection_graph.get_tensor_by_name('detection_scores:0')
		classes = detection_graph.get_tensor_by_name('detection_classes:0')
		num_detections = detection_graph.get_tensor_by_name('num_detections:0')

		# Actual detection.
		(boxes, scores, classes, num_detections) = sess.run(
			[boxes, scores, classes, num_detections],
			feed_dict={image_tensor: image_np_expanded})

		classes = list(classes[0])
		objects_set = set(classes)

		# Key = objects' labels; value : counts.
		
		objects_found = {
			self.category_index[value]['name']: classes.count(value) for value in set(classes)
		}
		return objects_found
