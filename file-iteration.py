import os
import face_recognition

name_encodings = []
for image in os.listdir("Images"):
	if image.startswith("name"):
		name_image = face_recognition.face_encodings(image)
		encodings = face_recognition.face_encodings(name_image)[0]
		name_encodings.append(encodings)