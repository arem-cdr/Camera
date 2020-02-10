import cv2
import time

def main():
    # Opening data stream
    cap = cv2.VideoCapture(0)
    i = 0
    t = time.time()
    while(cap.isOpened()):

        # Reading frame from stream
        ret, frame = cap.read()
        if(time.time()-t):
            t = time.time()
            cv2.imwrite(str(i)+".jpg", frame ) 
            i+=1
        cv2.circle(frame,(50,50),10,(255,0,0),10)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    cap.release()
    cv2.destroyAllWindows()


main()