import face_recognition as fr
from typing import Callable, List, TypeVar, Dict, Union
import base64
from io import BytesIO
from PIL import Image
import numpy as np
import pickle
from fastapi import HTTPException, status, Response
import time
from pathlib import Path

FACE_PATH = Path("security/Encodings.pkl")

def face_op() -> Dict:
    faces = pickle.load(open(FACE_PATH, "rb"))
    return faces

def face_dp(faces: Dict) -> None:
    pickle.dump(faces, open(FACE_PATH, "wb"))

def recogize(encoding1: TypeVar('numpy.ndarray'), encoding2: TypeVar('numpy.ndarray'), tolerance = 0.5) -> bool:
    ''' return True if the two images are same else False'''
    result = fr.compare_faces([encoding1], encoding2, tolerance=tolerance)
    return result[0]

def recogize_user(data):
    encoding = get_encoding(decoded_image(data.password))
    known_encodings = get_faces(data.username)
    print(f"Recognizing {data.username} at: {time.strftime('%H:%M:%S', time.localtime())}")
    result1 = recogize(known_encodings[0][0], encoding[0])
    result2 = recogize(known_encodings[1][0], encoding[0])
    result3 = recogize(known_encodings[2][0], encoding[0])
    final_result = (result1 or result2 or result3)
    print("Finished at:", time.strftime("%H:%M:%S", time.localtime()))
    return final_result

def read_images(image1, image2, image3):
    image1 = np.array(Image.open(BytesIO(image1)))
    image2 = np.array(Image.open(BytesIO(image2)))
    image3 = np.array(Image.open(BytesIO(image3)))
    encodings = [get_encoding(image1, 1), get_encoding(image2, 2),
                    get_encoding(image3, 3)]
    return encodings

def get_encoding(image: TypeVar('numpy.ndarray'), image_name = None) -> TypeVar('numpy.ndarray'):
    '''return len of 128 encoded vector'''
    try:
        encodings = fr.face_encodings(image)
    except Exception as e:
        # print()
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail=str(e))

    if not (len(encodings) == 1 and len(encodings[0]) == 128):
        if image_name:
            detail = f"Please Retake Verification Image {image_name}"
        else:
            detail = "Please Retake Verification Image"
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail=detail)
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

def get_all_encodings():
    return face_op()

def remove_encoding(username: str):
    encodings = get_all_encodings()
    try:
        del encodings[username]
        face_dp(encodings)
        return True
    except Exception as e:
        print("="*20)
        print(f"Failed to remove encodings for the user: {username}")
        print("="*20)
        return False
    


def put_faces(name: str, encoded_faces: List) -> None:
    faces = get_faces()
    faces[name] = encoded_faces
    face_dp(faces)

def update_username(old_username: str, new_username: str) -> None:
    faces = get_faces()
    user_face = faces[old_username]
    faces.pop(old_username)
    faces[new_username] = user_face
    face_dp(faces)


def verification_image(username, image1, image2, image3):
    print("Getting encodings for images at", time.strftime("%H:%M:%S", time.localtime()))
    encodings = read_images(image1, image2, image3)
    print("Saving encoded vectors at", time.strftime("%H:%M:%S", time.localtime()))
    put_faces(username, encodings)
    print("Saved encoded vectors at", time.strftime("%H:%M:%S", time.localtime()))
    return Response(status_code=204)