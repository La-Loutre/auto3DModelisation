from Tkinter import *
from PIL import Image,ImageTk
import tkFileDialog
import Tkinter
import Image

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
        
    def addPoint1(self,event):
        canvasTmp=self.canvasImg1
        point=self.point1
        point[0]=int(event.x)
        point[1]=int(event.y)
        print(self.point0,self.point1)
        
    def addPoint0(self,event):
        canvasTmp=self.canvasImg0
        point=self.point0
        
        point[0]=int(event.x)
        point[1]=int(event.y)
        print(self.point0,self.point1)
        
    
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
        MAXWIDTH=400
        if(pictureNumber==0):
            self.img0=img
            ratio = MAXWIDTH/float(x); 
            height=int(float(y)*float(ratio))
            self.img0Thumbnail= img.resize((MAXWIDTH,height), Image.ANTIALIAS)
            canvasTmp=self.canvasImg0
            sideTmp=LEFT
            self.photo0=ImageTk.PhotoImage(self.img0Thumbnail)
            photoTmp=self.photo0
            (x1,y1)=self.img0Thumbnail.size
        else:
            self.img1=img
            ratio = MAXWIDTH/float(x); 
            height=int(float(y)*float(ratio))
            self.img1Thumbnail= img.resize((MAXWIDTH, height), Image.ANTIALIAS)
            canvasTmp=self.canvasImg1
            sideTmp=RIGHT
            self.photo1=ImageTk.PhotoImage(self.img1Thumbnail)
            photoTmp=self.photo1
            (x1,y1)=self.img1Thumbnail.size
            self.img1Thumbnail.show()
    
        canvasTmp.create_image((x1/2,y1/2),image=photoTmp)
        canvasTmp.config(width=x1,height=y1,scrollregion=(0,0,x1,y1))
        canvasTmp.pack(side=sideTmp)
        self.frame.pack()
        
root = Tk()
application = Application(root)

root.mainloop()
root.destroy()
