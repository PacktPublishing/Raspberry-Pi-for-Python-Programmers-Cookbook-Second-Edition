#!/usr/bin/python3
#cameraGUI.py
import tkinter as TK
from PIL import Image
import subprocess
import time
import datetime
import picamera as picam

class SET():
  PV_SIZE=(320,240)
  NORM_SIZE=(2592,1944)
  NO_RESIZE=(0,0)
  PREVIEW_FILE="PREVIEW.jpg"
  TEMP_FILE="PREVIEW.ppm"

class cameraGUI(TK.Frame):
  def run(cmd):
    print("Run:"+cmd)
    subprocess.call([cmd], shell=True)

  def camCapture(filename,size=SET.NORM_SIZE):
    with picam.PiCamera() as camera:
      camera.resolution = size
      print("Image: %s"%filename)
      camera.capture(filename)

  def getTKImage(filename,previewsize=SET.NO_RESIZE):
    encoding=str.split(filename,".")[1].lower()
    print("Image Encoding: %s"%encoding)
    try:
      if encoding=="gif" and previewsize==SET.NO_RESIZE:
        theTKImage=TK.PhotoImage(file=filename)
      else:
        imageview=Image.open(filename)
        if previewsize!=SET.NO_RESIZE:
          imageview.thumbnail(previewsize,Image.ANTIALIAS)
        imageview.save(SET.TEMP_FILE,format="ppm")
        theTKImage=TK.PhotoImage(file=SET.TEMP_FILE)
    except IOError:
      print("Unable to get: %s"%filename)
    return theTKImage

  def timestamp():
    ts=time.time() 
    tstring=datetime.datetime.fromtimestamp(ts)
    return tstring.strftime("%Y%m%d_%H%M%S")

  def __init__(self,parent):
    self.parent=parent
    TK.Frame.__init__(self,self.parent)
    self.parent.title("Camera GUI")
    self.previewUpdate = TK.IntVar()
    self.filename=TK.StringVar()
    self.canvas = TK.Canvas(self.parent,
                            width=SET.PV_SIZE[0],
                            height=SET.PV_SIZE[1])
    self.canvas.grid(row=0,columnspan=4)
    self.shutterBtn=TK.Button(self.parent,text="Shutter",
                                    command=self.shutter)
    self.shutterBtn.grid(row=1,column=0)
    exitBtn=TK.Button(self.parent,text="Exit",
                             command=self.exit)
    exitBtn.grid(row=1,column=3)
    previewChk=TK.Checkbutton(self.parent,text="Preview",
                              variable=self.previewUpdate)
    previewChk.grid(row=1,column=1)
    labelFilename=TK.Label(self.parent,
                           textvariable=self.filename)
    labelFilename.grid(row=2,column=0,columnspan=3)
    self.preview()

  def msg(self,text):
    self.filename.set(text)
    self.update()

  def btnState(self,state):
    self.shutterBtn["state"] = state

  def shutter(self):
    self.btnState("disabled")
    self.msg("Taking photo...")
    self.update()
    if self.previewUpdate.get() == 1:
      self.preview()
    else:
      self.normal()
    self.btnState("active")

  def normal(self):
    name=cameraGUI.timestamp()+".jpg"
    cameraGUI.camCapture(name,SET.NORM_SIZE)
    self.updateDisp(name,previewsize=SET.PV_SIZE)
    self.msg(name)

  def preview(self):
    cameraGUI.camCapture(SET.PREVIEW_FILE,SET.PV_SIZE)
    self.updateDisp(SET.PREVIEW_FILE)
    self.msg(SET.PREVIEW_FILE)

  def updateDisp(self,filename,previewsize=SET.NO_RESIZE):
    self.msg("Loading Preview...")
    self.myImage=cameraGUI.getTKImage(filename,previewsize)
    self.theImage=self.canvas.create_image(0,0,
                                  anchor=TK.NW,
                                  image=self.myImage)
    self.update()

  def exit(self):
    exit()
#End
