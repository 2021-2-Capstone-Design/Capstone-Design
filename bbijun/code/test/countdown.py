import cv2

cap = cv2.VideoCapture('./../../sample_dance/videoplayback.mp4')
fps = cap.get(cv2.CAP_PROP_FPS)
cam = cv2.VideoCapture(0)
cam.set(3,640)
cam.set(4,480)
width = int(cam.get(3))
height = int(cam.get(4))
fcc = cv2.VideoWriter_fourcc(*'FMP4')
out = cv2.VideoWriter('test.mp4',fcc,fps, (width,height),True)

while(cam.isOpened()):
    print("start")
    ret, frame = cam.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    out.write(frame)
    cv2.imshow('webcam', cv2.flip(frame,1))
    if cv2.waitKey(1) & 0xFF == 27:
        break

print("end")
cam.release()
cv2.destroyAllWindows()

    