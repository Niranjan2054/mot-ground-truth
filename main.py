import cv2
import os
import csv
class MOT_GT:
    def __init__(self):
        self.RECTANGLE_START = False
        self.RECTANGLE_END = False
        self.rectange = [[0,0],[0,0]]
        self.imageList = os.listdir("data")
        cv2.namedWindow(winname="Thumbnail")
        cv2.setMouseCallback("Thumbnail",self.get_point)
        self.image = None
        self.frameNumber = 0
        self.gt = []

    def set_start_point(self,x,y):
        self.rectange[0] = [x,y]
        self.RECTANGLE_START = True
    
    def set_end_point(self,x,y):
        self.rectange[1] = [x,y]
        self.RECTANGLE_END = True
    
    def rearrange_points(self):
        if self.rectange[0][0] > self.rectange[1][0]:
            self.rectange[0][0],self.rectange[1][0] = self.rectange[1][0],self.rectange[0][0]

        if self.rectange[0][1] > self.rectange[1][1]:
            self.rectange[0][1],self.rectange[1][1] = self.rectange[1][1],self.rectange[0][1]
    
    def get_point(self,event,x,y,flags,param):
        if event == cv2.EVENT_LBUTTONDOWN:
            if not self.RECTANGLE_START and not self.RECTANGLE_END:
                self.set_start_point(x,y)
            elif self.RECTANGLE_START and not self.RECTANGLE_END:
                self.set_end_point(x,y)
            if self.RECTANGLE_START and self.RECTANGLE_END:
                self.rearrange_points()
                if self.image is not None:
                    self.draw_rectangle()
                    cv2.imshow("Thumbnail",self.image)
                self.gt.append([self.frameNumber,int(input("Enter track id : ")),self.rectange[0][0],self.rectange[0][1],self.rectange[1][0],self.rectange[1][1],1,1,1])

                self.RECTANGLE_START = False
                self.RECTANGLE_END   = False
                self.rectange = [[0,0],[0,0]]

    def draw_rectangle(self):
        cv2.rectangle(self.image,tuple(self.rectange[0]),tuple(self.rectange[1]),(0,0,255),2)

    def save_in_file(self):
        with open('gt.txt', 'w') as f: 
            write = csv.writer(f) 
            write.writerows(self.gt)

    def run(self):
        for id,img in enumerate(self.imageList):
            self.frameNumber = id+1
            self.image = cv2.imread("data/"+str(self.frameNumber)+".jpg")
            while True:
                cv2.imshow("Thumbnail",self.image)
                if cv2.waitKey(10) & 0xFF == 27:
                    break
        cv2.destroyAllWindows()
        self.save_in_file()


mot = MOT_GT()
mot.run()