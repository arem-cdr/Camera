import cv2 as cv


def detectAndDisplay(frame):
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    gray = cv.equalizeHist(gray)
    
    gobelets = gobelet_cascade.detectMultiScale(gray)
    for (x,y,w,h) in gobelets:
        center = (x + w//2, y + h//2)
        frame = cv.circle(frame, center, (w//2, h//2), (255, 0, 0), 4)
       
    cv.imshow('Gobelets', frame)

gobelet_cascade_file = ""
gobelet_cascade = cv.CascadeClassifier()
if not gobelet_cascade.load(gobelet_cascade_file):
    print('--(!)Error loading gobelet cascade')
    exit(0)

cap = cv.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if frame is None:
        break
    detectAndDisplay(frame)
    if cv.waitKey(10) == 27:
        break