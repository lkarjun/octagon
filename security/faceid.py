import face_recognition as fr
from typing import TypeVar, Dict
import base64
from io import BytesIO
from PIL import Image
import numpy as np


def recogize(encoding1: TypeVar('numpy.ndarray'), encoding2: TypeVar('numpy.ndarray'), tolerance = 0.5) -> bool:
    ''' return True if the two images are same else False'''
    result = fr.compare_faces([encoding1], encoding2, tolerance=tolerance)
    return result

def get_encoding(image: TypeVar('numpy.ndarray')) -> TypeVar('numpy.ndarray'):
    '''return len of 128 encoded vector'''
    encodings = fr.face_encodings(image)
    return encodings

def decoded_image(base64_image: str) -> None:
    img = base64.b64decode(base64_image)
    img = Image.open(BytesIO(img))
    img = np.asarray(img)
    assert img.shape == (1000, 1000, 3), 'Error image shape should be (1000, 1000, 3) an rgb image'