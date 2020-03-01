import cv2


class CArea_Interest(object):
    def  __init__(self,interests):
        self.interest = interests
    def display(self,img):
        for key in self.interest.keys():
            point = self.interest[key]
            x = float(point['x'])
            y = float(point['y'])
            h = float(point['h'])
            w = float(point['w'])
            start_point = (x-w, y-h)
            end_point = (x+w, y+h)
            cv2.rect(img, start_point, end_point, (255, 0, 0) , 1)
            zone = img[int(y-h/2):int(y+h/2),int(x-w/2):int(x+w/2)]
            zonehsv = cv2.cvtColor(zone,cv2.COLOR_BGR2HSV)
            avg_color_per_row = np.average(zonehsv, axis=0)
            avg_color = np.average(avg_color_per_row, axis=0)
            print("Key ",key," ",avg_color)

    def extract(self,img):
        l = []
        for key in self.interest.keys():
            point = self.interest[key]
            x = float(point['x'])
            y = float(point['y'])
            h = float(point['h'])
            w = float(point['w'])
            expected_h = float(point['expected_h'])
            expected_s = float(point['expected_s'])
            expected_v = float(point['expected_v'])
            tolerated_error = float(point['tolerated_error'])
            zone = img[int(y-h/2):int(y+h/2),int(x-w/2):int(x+w/2)]
            zonehsv = cv2.cvtColor(zone,cv2.COLOR_BGR2HSV)
            avg_color_per_row = np.average(zonehsv, axis=0)
            avg_color = np.average(avg_color_per_row, axis=0)
            diffh =  abs(avg_color[0]-expected_h)
            diffs =  abs(avg_color[1]-expected_s)
            diffv =  abs(avg_color[2]-expected_v)
            if(diffh>tolerated_error):
                l.append(key)
        return l

    
class IPoint(object):
    def  __init__(self,x,y,w,h):
        self.x = x
        self.y = y 
        self.w = w
        self.h = h
    def save(self,img):
        self.zone = img[int(self.y-self.h/2):int(self.y+self.h/2),int(self.x-self.w/2):int(self.x+self.w/2)]
    def hasChanged(self):
        pass
        