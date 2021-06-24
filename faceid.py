import face_recognition as fr
from typing import TypeVar

def recogize(encoding1: TypeVar('numpy.ndarray'), encoding2: TypeVar('numpy.ndarray'), tolerance = 0.5) -> bool:
    ''' return True if the two images are same else False'''
    result = fr.compare_faces([encoding1], encoding2, tolerance=tolerance)
    return result

def get_encoding(image: TypeVar('numpy.ndarray')) -> TypeVar('numpy.ndarray'):
    '''return len of 128 encoded vector'''
    encodings = fr.face_encodings(image)
    return encodings
