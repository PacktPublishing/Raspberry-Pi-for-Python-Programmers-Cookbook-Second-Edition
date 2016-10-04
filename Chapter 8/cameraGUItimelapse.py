#!/usr/bin/python3
import tkinter as TK
from PIL import Image
import time
import subprocess
from tkinter import messagebox
import datetime

pv_size=320,240
CAM_OUTPUT=" --output "
CAM_PREVIEW="raspistill --nopreview --width 320 --height 240 --timeout 100 --rotation 90 --encoding gif"
CAM_NORMAL="raspistill --rotation 90 --timeout 100"
CAM_TL="raspistill --nopreview --width 320 --height 240 --timeout 100 --rotation 90"
PREVIEW_FILE="PREVIEW.gif"
DEFAULT_FILE="Image.jpg"
TEMP_FILE="PREVIEW.ppm"
NO_RESIZE=(0,0)
ENC_PROG="mencoder -nosound -ovc lavc -lavcopts vcodec=mpeg4:aspect=16/9:vbitrate=8000000 -vf scale=1920:1080 -o %s -mf type=jpeg:fps=24 mf://@image_list.txt"

def run(cmd):
    print("Run:"+cmd)
    subprocess.call([cmd], shell=True)

def getTKImage(filename,previewsize=(0,0)):
    encoding=str.split(filename,".")[1].lower()
    print("Image Encoding: %s"%encoding)
    try:
      if encoding=="gif" and previewsize==(0,0):
        theTKImage=TK.PhotoImage(file=filename)
      else:
          imageview=Image.open(filename)
          if previewsize!=(0,0):
            imageview.thumbnail(previewsize,Image.ANTIALIAS)
          imageview.save(TEMP_FILE,format='ppm')
          theTKImage=TK.PhotoImage(file=TEMP_FILE)
    except IOError:
      print("Unable to get: %s"%filename)
    print("Filename: %s"%filename)
    return theTKImage

def timestamp():
   ts=time.time() 
   return datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d_%H%M%S')

class frameGUI(TK.Frame):
    def __init__(self,parent):
      self.parent=parent
      TK.Frame.__init__(self,self.parent,background="white")
      self.numImageTL=TK.StringVar()
      self.peroidTL=TK.StringVar()
      self.totalTimeTL=TK.StringVar()
      self.genVideoTL=TK.IntVar()
      self.numImageTL.set(10)
      self.peroidTL.set(5)
      self.calcTLTotalTime()
      self.genVideoTL.set(1)
      labelnumImgTK=TK.Label(self.parent,text="TL:#Images")
      labelperoidTK=TK.Label(self.parent,text="TL:Delay")
      labeltotalTimeTK=TK.Label(self.parent,text="TL:TotalTime")
      self.numImgSpn=TK.Spinbox(self.parent,textvariable=self.numImageTL,from_=1, to=99999,width=5,command=self.calcTLTotalTime)
      self.peroidSpn=TK.Spinbox(self.parent,textvariable=self.peroidTL,from_=1, to=99999,width=5,command=self.calcTLTotalTime)
      self.totalTime=TK.Label(self.parent,textvariable=self.totalTimeTL)
      self.TLBtn=TK.Button(self.parent,text="TL GO!",command=self.timelapse)
      genChk=TK.Checkbutton(self.parent,text="GenVideo",command=self.genVideoChk,variable=self.genVideoTL)
      labelnumImgTK.grid(row=3,column=0)
      self.numImgSpn.grid(row=4,column=0)
      labelperoidTK.grid(row=3,column=1)
      self.peroidSpn.grid(row=4,column=1)
      labeltotalTimeTK.grid(row=3,column=2)
      self.totalTime.grid(row=4,column=2)
      self.TLBtn.grid(row=3,column=3)
      genChk.grid(row=4,column=3)

    def calcTLTotalTime(self):
      numImg=float(self.numImageTL.get())-1
      peroid=float(self.peroidTL.get())
      if numImg<0:
        numImg=1
      self.totalTimeTL.set(numImg*peroid)

    def timelapse(self):
      print("Timelapse")
      self.TLBtn['state'] = 'disabled'
      self.update()
      self.tstamp="TL"+timestamp()
      cmd=CAM_TL+" --timelapse "+str(float(self.peroidTL.get())*1000)
      cmd+=" --timeout "+str(float(self.totalTimeTL.get())*1000)
      cmd+=CAM_OUTPUT+self.tstamp+"_%03d.jpg"
      run(cmd)
      if self.genVideoTL.get() == 1:
        self.genTLVideo()
      self.TLBtn['state'] = 'active'
      TK.messagebox.showinfo("Timelapse Complete","Processing complete")
      self.update()
    def genVideoChk(self):
      if self.genVideoTL.get() == 1:
        TK.messagebox.showinfo("Generate Video Enabled","Video will be generated")
      else:
        TK.messagebox.showinfo("Generate Video Disabled","Only images will be generated")
    def genTLVideo(self):
      #ls "$fname"*.jpg > $dir/image_list.txt
      run("ls "+self.tstamp+"*.jpg > image_list.txt")
      run(ENC_PROG%(self.tstamp+".avi"))

class cameraGUI(TK.Frame):
    def __init__(self,parent):
      self.parent=parent
      TK.Frame.__init__(self,self.parent,background="white")
      self.count=0
      self.running = True
      self.parent.title("Camera GUI")
      self.previewUpdate = TK.IntVar()
      self.filename=TK.StringVar()
      self.canvas = TK.Canvas(self.parent, width=pv_size[0], height=pv_size[1])
      self.shutterBtn=TK.Button(self.parent,text="Shutter",command=self.shutter)
      exitBtn=TK.Button(self.parent,text="Exit",command=self.exit)
      previewChk=TK.Checkbutton(self.parent,text="Preview",variable=self.previewUpdate)
      labelFilename=TK.Label(self.parent,textvariable=self.filename)
      frameGUI(self.parent).grid(row=3,columnspan=4)
      self.canvas.grid(row=0,columnspan=4)
      self.shutterBtn.grid(row=1,column=0)
      previewChk.grid(row=2,column=0)
      labelFilename.grid(row=1,column=1,columnspan=2)
      exitBtn.grid(row=1,column=3)
      self.preview()
      
    def shutter(self):
      self.shutterBtn['state'] = 'disabled'
      self.update()
      if cam.previewUpdate.get() == 1:
        self.preview()
      else:
        self.normal()
      self.shutterBtn['state'] = 'active'
    def normal(self):
      self.count+=1
      name=timestamp()+".jpg"#"%02d"%(self.count)+DEFAULT_FILE
      self.filename.set(name)
      run(CAM_NORMAL+CAM_OUTPUT+self.filename.get())
      self.updateDisp(self.filename.get(),previewsize=pv_size)
    def preview(self):
      self.filename.set(PREVIEW_FILE)
      run(CAM_PREVIEW+CAM_OUTPUT+self.filename.get())
      self.updateDisp(self.filename.get())
    def updateDisp(self,filename,previewsize=NO_RESIZE):
      self.myImage=getTKImage(filename,previewsize)
      self.theImage=self.canvas.create_image(0, 0,anchor=TK.NW,image=self.myImage)
      self.update()
    def exit(self):
      exit()

#Define Tkinter App
root=TK.Tk()
root.title("Camera GUI")
#root.geometry("%dx%d+%d+%d"%(w,h,x,y))
cam=cameraGUI(root)
TK.mainloop()