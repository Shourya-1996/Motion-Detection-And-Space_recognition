import cv2
import pandas
import time
from datetime import datetime


first_frame = None
status_list = [None, None]
times = []
df = pandas.DataFrame(columns=['Start', 'End'])
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

video = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # 0 for input no. of camera
a = 0
while True:
    check, frame = video.read()
    a += 1
    status = 0
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    if ((a == 5) and (first_frame is None)):
        first_frame = gray
        continue
    if a > 5:
        delta_frame = cv2.absdiff(first_frame, gray)

        thresh_frame = cv2.threshold(
            delta_frame, 30, 255, cv2.THRESH_BINARY)[1]

        thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)

        # find the contours and area of that contour in threshold frames
        (cnts, _) = cv2.findContours(thresh_frame.copy(),
                                     cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in cnts:
            if cv2.contourArea(contour) < 20000:
                continue
            status = 1
            (x, y, w, h) = cv2.boundingRect(contour)
            frame = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)

        faces = face_cascade.detectMultiScale(gray,
                                              scaleFactor=1.1,
                                              minNeighbors=5)

        for x, y, w, h in faces:
            gray = cv2.rectangle(
                gray, (x, y), (x+w, y+h), (0, 255, 0), (3))
        status_list.append(status)
        status_list = status_list[-2:]  # to save memory

        # checking starting and endind of motion time
        if status_list[-1] == 1 and status_list[-2] == 0:
            times.append(datetime.now())
        if status_list[-1] == 0 and status_list[-2] == 1:
            times.append(datetime.now())

        cv2.imshow("Capturing, Press q to quit", gray)
        cv2.imshow("delta", delta_frame)
        cv2.imshow("threshold", thresh_frame)
        cv2.imshow('color frame', frame)
        key = cv2.waitKey(10)
        if key == ord('q'):
            if status == 1:
                times.append(datetime.now())
            break
        # print(status)

for i in range(0, len(times), 2):
    df = df.append({'Start': times[i], 'End': times[i+1]}, ignore_index=True)

df.to_csv('Times.csv')


print(status_list)
video.release()
cv2.destroyAllWindows()
