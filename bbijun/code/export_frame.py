import cv2
video = cv2.VideoCapture("./sample_dance/videoplayback.mp4")
success,  image = video.read()
count = 0
while success:
    cv2.imwrite("./screenshot/frame%d.png"%count, image)
    success, image = video.read()
    print('Read a new frame: ', success)
    count+=1