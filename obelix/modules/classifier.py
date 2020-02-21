import cv2


class Classifier(object):
    def  __init__(self, path):
        self.gobelet_cascade = cv2.CascadeClassifier()
        if not self.gobelet_cascade.load(path):
            print('--(!) Error loading gobelet cascade')
            exit(0)
    
    def detectAndDisplay(self,frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        
        gobelets = self.gobelet_cascade.detectMultiScale(gray)
        for (x,y,w,h) in gobelets:
            center = (int(x) + w//2, int(y) + h//2)
            cv2.circle(frame, center, 20, (255, 0, 0), 4)
        
        cv2.imshow('Gobelets', frame)

