
import cv2

def main():
    # Opening data stream
    cap = cv2.VideoCapture(0)
    sizex = 1
    sizey = 1
    while(cap.isOpened()):

        # Reading frame from stream
        ret, frame = cap.read()
        resized = cv2.resize(frame, (0, 0), fx=sizex,fy=sizey)
        cv2.imshow('real', resized)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    cap.release()
    cv2.destroyAllWindows()


main()