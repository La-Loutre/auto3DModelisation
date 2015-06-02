from Tkinter import *
from processing import *
from PIL import Image,ImageTk
import tkFileDialog
import Tkinter
import Image
import math
MAXWIDTH=400
DEBUG = True
GOLF_PATH="/home/louis/projetVoiture/voituresTraining/golf/"
camera0Angle=135
camera0BlindSpot=180-camera0Angle

camera1Angle=135
camera1BlindSpot=180-camera1Angle

widthCamera=0.2


class Application:
    def __init__(self,master):
        self.frame = Frame(master)
        self.master=master
        self.frame.pack()
        self.baseMenu=Menu(self.master)

        ##TMP
        self.point0=[0,0]
        self.point1=[0,0]
        ##
        ## Create img 0 & 1 canvas :
        self.canvasImg0 = Canvas(self.frame,width=300,height=100)
        self.canvasImg1 = Canvas(self.frame,width=300,height=100)
        self.canvasImg0.pack()
        self.canvasImg1.pack()
        ##

        ## Bind mouse with canvas :
        self.canvasImg0.bind("<Button-1>",self.addPoint0)
        self.canvasImg1.bind("<Button-1>",self.addPoint1)
        
        ##

        ### Create all submenus
        self.createFileMenu()
        ###
        self.master.config(menu=self.baseMenu)

        ##DEBUG part

        if DEBUG :
            self.refreshPicture(Image.open(GOLF_PATH+"DSC_1729.JPG"),0)
            self.refreshPicture(Image.open(GOLF_PATH+"DSC_1731.JPG"),1)
        
    def addPoint1(self,event):
        canvasTmp=self.canvasImg1
        point=self.point1
        point[0]=int(event.x)/self.ratio1
        point[1]=int(event.y)/self.ratio1
        print(self.point0,self.point1)
        print(angle(self.img1.size[0],self.point1[0],camera1Angle))
        dY=distanceY(angle(self.img0.size[0],self.point0[0],camera0Angle),angle(self.img1.size[0],self.point1[0],camera1Angle),widthCamera)
        print(dY)
        dX=distanceX(angle(self.img0.size[0],self.point0[0],camera0Angle),angle(self.img1.size[0],self.point1[0],camera1Angle),widthCamera,dY)
        print(dX)


        
    def addPoint0(self,event):
        canvasTmp=self.canvasImg0
        point=self.point0
        
        point[0]=int(event.x)/self.ratio0
        point[1]=int(event.y)/self.ratio0
        print(self.point0,self.point1)
        print(angle(self.img0.size[0],self.point0[0],camera0Angle))
    
    def createFileMenu(self):
        self.fileMenu=Menu(self.baseMenu)
        self.fileMenu.add_command(label="Load picture 1",command=lambda :self.loadPicture(0))
        self.fileMenu.add_command(label="Load picture 2",command=lambda :self.loadPicture(1))
        self.baseMenu.add_cascade(label="Files",menu=self.fileMenu)

    def getFileName(self):
        print("Load picture")
        ftypes= [('All files','*'),('Pictures files','*.png')]
        dlg = tkFileDialog.Open(self.frame,filetypes = ftypes)
        fileName=dlg.show()
        return fileName
    
    
    def loadPicture(self,pictureNumber=0):
        self.refreshPicture(Image.open(self.getFileName()),pictureNumber)
        
    def refreshPicture(self,img,pictureNumber=0):
        (x,y)=img.size
        if(pictureNumber==0):
            self.img0=cascadeClassifierDetection(img,"cas1.xml")
            ratio = MAXWIDTH/float(x); 
            self.ratio0=ratio
            height=int(float(y)*float(ratio))
            self.img0Thumbnail= self.img0.resize((MAXWIDTH,height), Image.ANTIALIAS)
            canvasTmp=self.canvasImg0
            sideTmp=LEFT
            self.photo0=ImageTk.PhotoImage(self.img0Thumbnail)
            photoTmp=self.photo0
            (x1,y1)=self.img0Thumbnail.size
            
        else:
            self.img1=cascadeClassifierDetection(img,"cas1.xml")
            ratio = MAXWIDTH/float(x); 
            self.ratio1=ratio
            height=int(float(y)*float(ratio))
            self.img1Thumbnail= self.img1.resize((MAXWIDTH, height), Image.ANTIALIAS)
            canvasTmp=self.canvasImg1
            sideTmp=RIGHT
            self.photo1=ImageTk.PhotoImage(self.img1Thumbnail)
            photoTmp=self.photo1
            (x1,y1)=self.img1Thumbnail.size
            #keypoints(self.img0,self.img1)

    
        canvasTmp.create_image((x1/2,y1/2),image=photoTmp)
        canvasTmp.config(width=x1,height=y1,scrollregion=(0,0,x1,y1))
        canvasTmp.pack(side=sideTmp)
        self.frame.pack()


root = Tk()
application = Application(root)

root.mainloop()
root.destroy()
