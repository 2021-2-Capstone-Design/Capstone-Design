import cv2

cap = cv2.VideoCapture(0)
cap2 = cv2.VideoCapture('./../sample_dance/person_back.mp4')
fps = cap2.get(cv2.CAP_PROP_FPS)

fourcc = cv2.VideoWriter_fourcc(*'FMP4')
out = cv2.VideoWriter('./../extractsamples/test_save.mp4', fourcc, fps, (1280, 960))

while(True):
    ret, frame = cap.read()    # Read 결과와 frame
    if(ret) :
        out.write(frame)

        if cv2.waitKey(1) == ord('q'):
            out.release()
            break
cap.release()
cv2.destroyAllWindows()