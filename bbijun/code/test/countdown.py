import cv2

cap = cv2.VideoCapture('./../sample_dance/videoplayback.mp4')
fps = cap.get(cv2.CAP_PROP_FPS)
cam = cv2.VideoCapture(0)
cam.set(3,1280)
cam.set(4,960)
width = int(cam.get(3))
height = int(cam.get(4))
fcc = cv2.VideoWriter_fourcc(*'FMP4')
out = cv2.VideoWriter('test.mp4',fcc,fps(width,height),True)
delay = int(1000/fps)
print(delay)
while(cap.isOpened()):
    ret, frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    out.write(frame)
    cv2.imshow('webcam',cv2.flip(frame,1))
    if cv2.waitKey(delay) & 0xFF == 27:
        break

    