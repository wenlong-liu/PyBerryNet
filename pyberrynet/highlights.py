"""
Ref: https://github.com/DT42/BerryNet/blob/master/inference/detection_server.py
"""
import cv2
import matplotlib.pyplot as plt


def draw_bounding(image, results, color_map):
    """Draw bounding boxes on an image.
    :param image: numpy array of image.
    :param results: Darkflow inference results
    :param color_map: Bounding box color candidates, list of RGB tuples. Imported from matplotlib.
    
    :return A picture with drawing boards on the recognized items.
    """
    for res in results:
        # read in image as a numpy array.
        left = res['topleft']['x']
        top = res['topleft']['y']
        right = res['bottomright']['x']
        bottom = res['bottomright']['y']
        color_index = res['coloridx']
        cmap = plt.get_cmap(color_map)
        color = cmap(color_index)
        label = res['label']
        confidence = res['confidence']
        img_height, img_width, _ = image.shape
        thick = int((img_height + img_width) // 300)

        cv2.rectangle(image,(left, top), (right, bottom), color, thick)
        cv2.putText(image, label, (left, top - 12), 0, 1e-3 * img_height, color, thick//3)

        return image
