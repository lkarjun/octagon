import face_recognition as fr
from typing import Callable, List, TypeVar, Dict, Union
import base64
from io import BytesIO
from PIL import Image
import numpy as np
import pickle
from fastapi import HTTPException, status

face_op = lambda: pickle.load(open('security/faces.pkl', 'rb'))
face_dp = lambda faces: pickle.dump(faces, open('security/faces.pkl', 'wb'))

def recogize(encoding1: TypeVar('numpy.ndarray'), encoding2: TypeVar('numpy.ndarray'), tolerance = 0.5) -> bool:
    ''' return True if the two images are same else False'''
    result = fr.compare_faces([encoding1], encoding2, tolerance=tolerance)
    return result

def read_images(image1, image2, image3):
    image1 = np.array(Image.open(BytesIO(image1)))
    image2 = np.array(Image.open(BytesIO(image2)))
    image3 = np.array(Image.open(BytesIO(image3)))
    encodings = [get_encoding(image1), get_encoding(image2),
                    get_encoding(image3)]
    return encodings

def get_encoding(image: TypeVar('numpy.ndarray')) -> TypeVar('numpy.ndarray'):
    '''return len of 128 encoded vector'''
    encodings = fr.face_encodings(image)
    if not len(encodings) == 128:
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail="Please Retake image")
    return encodings

def decoded_image(base64_image: str) -> None:
    img = base64.b64decode(base64_image)
    img = Image.open(BytesIO(img))
    img = np.asarray(img)
    assert img.shape == (1000, 1000, 3), 'Error image shape should be (1000, 1000, 3) an rgb image'
    return img

def get_faces(name: Union[str, bool] = False, delete: bool = False) -> Union[Dict, List, str]:
    '''opens pickle'''
    faces = face_op()
    if name:
        if not delete: return faces[name]
        del faces[name]
        face_dp(faces)
        return 'removed'

    return faces

def put_faces(name: str, encoded_faces: List) -> None:
    faces = get_faces()
    faces[name] = encoded_faces
    face_dp(faces)


if __name__ == '__main__':
    print(get_faces())
    put_faces('lalkrishna', [[2,3,], [12121]])
    print();print(get_faces())