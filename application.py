import face_recognition
import picamera
import numpy as np
import RPi.GPIO as GPIO
from time import sleep

#Variables
servoPIN = 16
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)

p = GPIO.PWM(servoPIN, 50)
p.start(2.5)

# Create camera object
camera = picamera.PiCamera()
camera.resolution = (320, 240)
output = np.empty((240, 320, 3), dtype=np.uint8)

# Load sample picture and encoding
print("Loading known face image(s)")
obama_image = face_recognition.load_image_file("Images/obama_small.jpg")
obama_face_encoding = face_recognition.face_encodings(obama_image)[0]
trump_image = face_recognition.load_image_file("Images/trump.jpg")
trump_encoding = face_recognition.face_encodings(trump_image)[0]
seder_image = face_recognition.load_image_file("Images/seder.jpg")
seder_encoding = face_recognition.face_encodings(seder_image)[0]
drew_image = face_recognition.load_image_file("Images/drew.jpg")
drew_encoding = face_recognition.face_encodings(drew_image)[0]
packard_image = face_recognition.load_image_file("Images/packard.jpg")
packard_encoding = face_recognition.face_encodings(packard_image)[0]

# Initialize variables
face_locations = []
face_encodings = []

while True:
    print("Capturing image.")
    # Grab a single frame of video 
    camera.capture(output, format="rgb")

    # Find all faces and face encodings in the current frame 
    face_locations = face_recognition.face_locations(output)
    print("Found {} faces in image.".format(len(face_locations)))
    face_encodings = face_recognition.face_encodings(output, face_locations)

    # Loop over each face found in the frame and test if recognized
    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        match = face_recognition.compare_faces([obama_face_encoding,trump_encoding,seder_encoding,packard_encoding,drew_encoding], face_encoding)
        name = "<Unknown Person>"

        if match[0]:
            name = "Barack Obama"
        if match[1]:
            name = "Donald Trump"
        if match[2]:
            name = "Sean Seder"
        if match[3]:
            name = "Josh Packard"
        if match[4]:
            name = "Drew Schaly"
        if name != "<Unknown Person>":
            try:
                sleep(2)
                p.ChangeDutyCycle(12.5)
                sleep(10)
                p.ChangeDutyCycle(2.5)
            except KeyboardInterrupt:
                p.stop()
                GPIO.cleanup()

        print("I see someone named {}!".format(name))




    

        
