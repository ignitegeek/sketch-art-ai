import cv2
import numpy as np
import tempfile

def convert_to_sketch(uploaded_image):
    image_stream = uploaded_image.stream
    file_bytes = np.asarray(bytearray(image_stream.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    inv_gray = 255 - gray
    blur = cv2.GaussianBlur(inv_gray, (21, 21), 0)
    sketch = cv2.divide(gray, 255 - blur, scale=256)
    _, buffer = cv2.imencode('.png', sketch)
    temp = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
    temp.write(buffer.tobytes())
    temp.close()
    return temp.name
