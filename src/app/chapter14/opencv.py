from cv2 import COLOR_BGR2GRAY
from cv2 import CascadeClassifier
from cv2 import VideoCapture
from cv2 import cvtColor
from cv2 import data
from cv2 import destroyAllWindows
from cv2 import imshow
from cv2 import rectangle
from cv2 import waitKey


# Load the trained model
face_cascade = CascadeClassifier(
    data.haarcascades + "haarcascade_frontalface_default.xml"
)

# You may need to change the index depending on your computer and camera
video_capture = VideoCapture(1)


while True:
    # Get an image frame
    ret, frame = video_capture.read()

    # Convert it to grayscale and run detection
    gray = cvtColor(frame, COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray)

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        rectangle(
            img=frame,
            pt1=(x, y),
            pt2=(x + w, y + h),
            color=(0, 255, 0),
            thickness=2,
        )

    # Display the resulting frame
    imshow("Chapter 14 - OpenCV", frame)

    # Break when key "q" is pressed
    if waitKey(1) == ord("q"):
        break

video_capture.release()
destroyAllWindows()
