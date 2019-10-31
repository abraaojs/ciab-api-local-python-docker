import face_recognition
from exceptions.userException import UserException
import numpy as np

class FaceRecognition():

    def imageEncoding(file):
        image = face_recognition.load_image_file(file)
        try:
            face_encoding = face_recognition.face_encodings(image)[0]
        except IndexError:
            UserException.responseError(500, "Image was corrupted!")
        return face_encoding

    def faceRecognition(unknown_face, id, embedding):
        if embedding:
            rpl = embedding.replace('[','').replace(']','').split()
            numpyImage = np.array(rpl)
            face_encoding = numpyImage.astype(np.float)
            known_face = [face_encoding]
            results = face_recognition.compare_faces(known_face, unknown_face, tolerance=0.45)

            if results[0] == True:
                return id
        return None


    def compareImages(imageEncoding, embeddings):
        for embedding in embeddings:
            id = FaceRecognition.faceRecognition(imageEncoding, embedding["Users_id"], embedding["Users_embedding"])
            if id:
                return id
        return None

