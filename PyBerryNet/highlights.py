"""
Ref: https://github.com/DT42/BerryNet/blob/master/inference/detection_server.py
"""
import cv2
import numpy as np


def draw_bounding(raw_image, output_path, results, color_map):
    """Draw bounding boxes on an image.
    :param 
    image: image path
    output_path: output image file path
    results: Darkflow inference results
    color_map: Bounding box color candidates, list of RGB tuples.
    
    :return
    A saved picture with drawing boards on the recognized items.
    """
    for res in results:
        # read in image as a numpy array.
        image = cv2.imread(raw_image)

        left = res['topleft']['x']
        top = res['topleft']['y']
        right = res['bottomright']['x']
        bottom = res['bottomright']['y']
        color_index = res['coloridx']
        color = color_map[color_index]
        label = res['label']
        confidence = res['confidence']
        img_height, img_width, _ = image.shape
        thick = int((img_height + img_width) // 300)

        cv2.rectangle(image,(left, top), (right, bottom), color, thick)
        cv2.putText(image, label, (left, top - 12), 0, 1e-3 * img_height, color, thick//3)

    cv2.imwrite(output_path, image)