import cv2
import os

class MOT_GT:
    def __init__(self):
        self.RECTANGLE_START = False
        self.RECTANGLE_END = False
        self.rectange = [[0,0],[0,0]]
        self.imageList = os.listdir("data")
        cv2.namedWindow(winname="Thumbnail")
        cv2.setMouseCallback("Thumbnail",self.get_point)
        self.image = None

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
            print(self.rectange)
        if event == cv2.EVENT_LBUTTONUP:
            if self.RECTANGLE_START and self.RECTANGLE_END:
                self.rearrange_points()
                if self.image is not None:
                    self.draw_rectangle()
                self.RECTANGLE_START = False
                self.RECTANGLE_END   = False
                self.rectange = [[0,0],[0,0]]

    def draw_rectangle(self):
        cv2.rectangle(self.image,tuple(self.rectange[0]),tuple(self.rectange[1]),(0,0,255),2)

    def run(self):
        self.image = cv2.imread("data/"+self.imageList[0])

        while True:
            cv2.imshow("Thumbnail",self.image)
            if cv2.waitKey(10) & 0xFF == 27:
                break
        cv2.destroyAllWindows()

mot = MOT_GT()
mot.run()