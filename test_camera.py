
import cv2


# Here we build the code that calls other scripts to do all the work

def main():
    # Opening data stream
    cap = cv2.VideoCapture(0)
    
    while(cap.isOpened()):

        # Reading frame from stream
        ret, frame = cap.read()

        # Resizing image
        
        cv2.imshow('real', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    cap.release()
    cv2.destroyAllWindows()


main()