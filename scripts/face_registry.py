import numpy
import face_recognition

known_face_encodings = []
known_face_names = []


def register(image: numpy.ndarray, name: str):
    face_encodings = face_recognition.face_encodings(image)
    if len(face_encodings) > 0:
        face_encoding = face_encodings[0]
        return {"encoding": face_encoding, "name": name}
    raise Exception("No face detected!")

def clear_registry():
    known_face_encodings.clear()
    known_face_names.clear()


def load(face_encoding: numpy.ndarray, name: str):
    known_face_encodings.append(face_encoding)
    known_face_names.append(name)