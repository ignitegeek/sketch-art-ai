import cv2
import os

def convert_to_sketch(image_path, result_folder):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    inverted = 255 - gray
    blurred = cv2.GaussianBlur(inverted, (21, 21), 0)
    sketch = cv2.divide(gray, 255 - blurred, scale=256)
    result_filename = os.path.basename(image_path).replace('img_', 'sketch_')
    result_path = os.path.join(result_folder, result_filename)
    cv2.imwrite(result_path, sketch)
    return result_path
