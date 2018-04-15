

import numpy as np
import os
import sys
import tensorflow as tf
import cv2
from imutils.video import FPS
import imutils
import time
cap = cv2.VideoCapture('test2.mp4')

fps = FPS().start()
# This is needed since the notebook is stored in the object_detection folder.
sys.path.append("..")
from object_detection.utils import ops as utils_ops

if tf.__version__ < '1.4.0':
  raise ImportError('Please upgrade your tensorflow installation to v1.4.* or later!')



# ## Object detection imports
# Here are the imports from the object detection module.

from utils import label_map_util
from utils import visualization_utils as vis_util


# # Model preparation 

MODEL_NAME = 'frozen_graphs'

# Path to frozen detection graph. This is the actual model that is used for the object detection.
PATH_TO_CKPT = MODEL_NAME + '/frozen_inference_graph_ssd.pb'

# List of the strings that is used to add correct label for each box.
PATH_TO_LABELS = os.path.join('data', 'object_detection.pbtxt')

NUM_CLASSES = 4



# ## Load a (frozen) Tensorflow model into memory.


detection_graph = tf.Graph()
with detection_graph.as_default():
  od_graph_def = tf.GraphDef()
  with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
    serialized_graph = fid.read()
    od_graph_def.ParseFromString(serialized_graph)
    tf.import_graph_def(od_graph_def, name='')


# ## Loading label map

label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)



# # Detection
with detection_graph.as_default():
	with tf.Session(graph=detection_graph) as sess:
		while cap.isOpened():
			ret, image = cap.read()
			ops = tf.get_default_graph().get_operations()
			all_tensor_names = {output.name for op in ops for output in op.outputs}
			tensor_dict = {}
			for key in ['num_detections', 'detection_boxes', 'detection_scores','detection_classes', 'detection_masks']:
				tensor_name = key + ':0'
				if tensor_name in all_tensor_names:
					tensor_dict[key] = tf.get_default_graph().get_tensor_by_name(
						tensor_name)
			if 'detection_masks' in tensor_dict:
			# The following processing is only for single image
				detection_boxes = tf.squeeze(tensor_dict['detection_boxes'], [0])
				detection_masks = tf.squeeze(tensor_dict['detection_masks'], [0])
				# Reframe is required to translate mask from box coordinates to image coordinates and fit the image size.
				real_num_detection = tf.cast(tensor_dict['num_detections'][0], tf.int32)
				detection_boxes = tf.slice(detection_boxes, [0, 0], [real_num_detection, -1])
				detection_masks = tf.slice(detection_masks, [0, 0, 0], [real_num_detection, -1, -1])
				detection_masks_reframed = utils_ops.reframe_box_masks_to_image_masks(
				    detection_masks, detection_boxes, image.shape[0], image.shape[1])
				detection_masks_reframed = tf.cast(
				    tf.greater(detection_masks_reframed, 0.5), tf.uint8)
				# Follow the convention by adding back the batch dimension
				tensor_dict['detection_masks'] = tf.expand_dims(
				    detection_masks_reframed, 0)
			image_tensor = tf.get_default_graph().get_tensor_by_name('image_tensor:0')

			# Run inference
			output_dict = sess.run(tensor_dict,
			                     feed_dict={image_tensor: np.expand_dims(image, 0)})
			start_time = time.time()

			# all outputs are float32 numpy arrays, so convert types as appropriate
			output_dict['num_detections'] = int(output_dict['num_detections'][0])
			output_dict['detection_classes'] = output_dict[
			  'detection_classes'][0].astype(np.uint8)
			output_dict['detection_boxes'] = output_dict['detection_boxes'][0]
			output_dict['detection_scores'] = output_dict['detection_scores'][0]
			if 'detection_masks' in output_dict:
				output_dict['detection_masks'] = output_dict['detection_masks'][0]
			vis_util.visualize_boxes_and_labels_on_image_array(
			image,
			output_dict['detection_boxes'],
			output_dict['detection_classes'],
			output_dict['detection_scores'],
			category_index,
			instance_masks=output_dict.get('detection_masks'),
			use_normalized_coordinates=True,
			line_thickness=8)
			
			fps.stop()
			fps_text = "Frame per second(FPS): {:.2f}".format(fps.fps())+", Elapsed time: {:.2f}".format(time.time()-start_time)+" sec"
			cv2.putText(image, fps_text, (50, 100),
				cv2.FONT_HERSHEY_SIMPLEX, 3.0, (0, 0, 0), 2)

			cv2.imshow('Object detection', cv2.resize(image, (1366,768)))
			fps.update()
			if cv2.waitKey(1000) & 0xFF == ord('q'):
				cv2.destroyAllWindows()
				break




import numpy as np
import os
import sys
import tensorflow as tf
import cv2
from imutils.video import FPS
import imutils
import time
cap = cv2.VideoCapture('test2.mp4')

fps = FPS().start()
# This is needed since the notebook is stored in the object_detection folder.
sys.path.append("..")
from object_detection.utils import ops as utils_ops

if tf.__version__ < '1.4.0':
  raise ImportError('Please upgrade your tensorflow installation to v1.4.* or later!')



# ## Object detection imports
# Here are the imports from the object detection module.

from utils import label_map_util
from utils import visualization_utils as vis_util


# # Model preparation 

MODEL_NAME = 'ssd_mobilenet_drone'

# Path to frozen detection graph. This is the actual model that is used for the object detection.
PATH_TO_CKPT = MODEL_NAME + '/frozen_inference_graph_for_mobilenet.pb'

# List of the strings that is used to add correct label for each box.
PATH_TO_LABELS = os.path.join('training', 'object_detection.pbtxt')

NUM_CLASSES = 4



# ## Load a (frozen) Tensorflow model into memory.


detection_graph = tf.Graph()
with detection_graph.as_default():
  od_graph_def = tf.GraphDef()
  with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
    serialized_graph = fid.read()
    od_graph_def.ParseFromString(serialized_graph)
    tf.import_graph_def(od_graph_def, name='')


# ## Loading label map

label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)



# # Detection
with detection_graph.as_default():
	with tf.Session(graph=detection_graph) as sess:
		while cap.isOpened():
			ret, image = cap.read()
			ops = tf.get_default_graph().get_operations()
			all_tensor_names = {output.name for op in ops for output in op.outputs}
			tensor_dict = {}
			for key in ['num_detections', 'detection_boxes', 'detection_scores','detection_classes', 'detection_masks']:
				tensor_name = key + ':0'
				if tensor_name in all_tensor_names:
					tensor_dict[key] = tf.get_default_graph().get_tensor_by_name(
						tensor_name)
			if 'detection_masks' in tensor_dict:
			# The following processing is only for single image
				detection_boxes = tf.squeeze(tensor_dict['detection_boxes'], [0])
				detection_masks = tf.squeeze(tensor_dict['detection_masks'], [0])
				# Reframe is required to translate mask from box coordinates to image coordinates and fit the image size.
				real_num_detection = tf.cast(tensor_dict['num_detections'][0], tf.int32)
				detection_boxes = tf.slice(detection_boxes, [0, 0], [real_num_detection, -1])
				detection_masks = tf.slice(detection_masks, [0, 0, 0], [real_num_detection, -1, -1])
				detection_masks_reframed = utils_ops.reframe_box_masks_to_image_masks(
				    detection_masks, detection_boxes, image.shape[0], image.shape[1])
				detection_masks_reframed = tf.cast(
				    tf.greater(detection_masks_reframed, 0.5), tf.uint8)
				# Follow the convention by adding back the batch dimension
				tensor_dict['detection_masks'] = tf.expand_dims(
				    detection_masks_reframed, 0)
			image_tensor = tf.get_default_graph().get_tensor_by_name('image_tensor:0')

			# Run inference
			output_dict = sess.run(tensor_dict,
			                     feed_dict={image_tensor: np.expand_dims(image, 0)})
			start_time = time.time()

			# all outputs are float32 numpy arrays, so convert types as appropriate
			output_dict['num_detections'] = int(output_dict['num_detections'][0])
			output_dict['detection_classes'] = output_dict[
			  'detection_classes'][0].astype(np.uint8)
			output_dict['detection_boxes'] = output_dict['detection_boxes'][0]
			output_dict['detection_scores'] = output_dict['detection_scores'][0]
			if 'detection_masks' in output_dict:
				output_dict['detection_masks'] = output_dict['detection_masks'][0]
			vis_util.visualize_boxes_and_labels_on_image_array(
			image,
			output_dict['detection_boxes'],
			output_dict['detection_classes'],
			output_dict['detection_scores'],
			category_index,
			instance_masks=output_dict.get('detection_masks'),
			use_normalized_coordinates=True,
			line_thickness=8)
			
			fps.stop()
			fps_text = "Frame per second(FPS): {:.2f}".format(fps.fps())+", Elapsed time: {:.2f}".format(time.time()-start_time)+" sec"
			cv2.putText(image, fps_text, (50, 100),
				cv2.FONT_HERSHEY_SIMPLEX, 3.0, (0, 0, 0), 2)

			cv2.imshow('Object detection', cv2.resize(image, (1366,768)))
			fps.update()
			if cv2.waitKey(1000) & 0xFF == ord('q'):
				cv2.destroyAllWindows()
				break

