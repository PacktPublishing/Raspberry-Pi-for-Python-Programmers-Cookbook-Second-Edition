#!/usr/bin/python3
#timelapseGUI.py
import tkinter as TK
from tkinter import messagebox
import cameraGUI as camGUI
import time

class SET(camGUI.SET):
  TL_SIZE=(1920,1080)
  ENC_PROG="mencoder -nosound -ovc lavc -lavcopts"
  ENC_PROG+=" vcodec=mpeg4:aspect=16/9:vbitrate=8000000"
  ENC_PROG+=" -vf scale=%d:%d"%(TL_SIZE[0],TL_SIZE[1])
  ENC_PROG+=" -o %s -mf type=jpeg:fps=24 mf://@%s"
  LIST_FILE="image_list.txt"

class cameraGUI(camGUI.cameraGUI):
  def camTimelapse(filename,size=SET.TL_SIZE,
                    timedelay=10,numImages=10):
    with camGUI.picam.PiCamera() as camera:
      camera.resolution = size
      for count, name in \
            enumerate(camera.capture_continuous(filename)):
        print("Timelapse: %s"%name)
        if count == numImages:
          break
        time.sleep(timedelay)

  def __init__(self,parent):
    super(cameraGUI,self).__init__(parent)
    self.parent=parent
    TK.Frame.__init__(self,self.parent,background="white")
    self.numImageTL=TK.StringVar()
    self.peroidTL=TK.StringVar()
    self.totalTimeTL=TK.StringVar()
    self.genVideoTL=TK.IntVar()
    labelnumImgTK=TK.Label(self.parent,text="TL:#Images")
    labelperoidTK=TK.Label(self.parent,text="TL:Delay")
    labeltotalTimeTK=TK.Label(self.parent,
                              text="TL:TotalTime")
    self.numImgSpn=TK.Spinbox(self.parent,
                       textvariable=self.numImageTL,
                       from_=1,to=99999,
                       width=5,state="readonly",
                       command=self.calcTLTotalTime)
    self.peroidSpn=TK.Spinbox(self.parent,
                       textvariable=self.peroidTL,
                       from_=1,to=99999,width=5,
                       command=self.calcTLTotalTime)
    self.totalTime=TK.Label(self.parent,
                       textvariable=self.totalTimeTL)
    self.TLBtn=TK.Button(self.parent,text="TL GO!",
                             command=self.timelapse)
    genChk=TK.Checkbutton(self.parent,text="GenVideo",
                             command=self.genVideoChk,
                             variable=self.genVideoTL)
    labelnumImgTK.grid(row=3,column=0)
    self.numImgSpn.grid(row=4,column=0)
    labelperoidTK.grid(row=3,column=1)
    self.peroidSpn.grid(row=4,column=1)
    labeltotalTimeTK.grid(row=3,column=2)
    self.totalTime.grid(row=4,column=2)
    self.TLBtn.grid(row=3,column=3)
    genChk.grid(row=4,column=3)
    self.numImageTL.set(10)
    self.peroidTL.set(5)
    self.genVideoTL.set(1)
    self.calcTLTotalTime()

  def btnState(self,state):
    self.TLBtn["state"] = state
    super(cameraGUI,self).btnState(state)

  def calcTLTotalTime(self):
    numImg=float(self.numImageTL.get())-1
    peroid=float(self.peroidTL.get())
    if numImg<0:
      numImg=1
    self.totalTimeTL.set(numImg*peroid)

  def timelapse(self):
    self.msg("Running Timelapse")
    self.btnState("disabled")
    self.update()
    self.tstamp="TL"+cameraGUI.timestamp()
    cameraGUI.camTimelapse(self.tstamp+'{counter:03d}.jpg',
                           SET.TL_SIZE,
                           float(self.peroidTL.get()),
                           int(self.numImageTL.get()))
    if self.genVideoTL.get() == 1:
      self.genTLVideo()
    self.btnState("active")
    TK.messagebox.showinfo("Timelapse Complete",
                           "Processing complete")
    self.update()

  def genVideoChk(self):
    if self.genVideoTL.get() == 1:
      TK.messagebox.showinfo("Generate Video Enabled",
                             "Video will be generated")
    else:
      TK.messagebox.showinfo("Generate Video Disabled",
                          "Only images will be generated")

  def genTLVideo(self):
    self.msg("Generate video...")
    cameraGUI.run("ls "+self.tstamp+"*.jpg > "
                                +SET.LIST_FILE)
    cameraGUI.run(SET.ENC_PROG%(self.tstamp+".avi",
                                      SET.LIST_FILE))
    self.msg(self.tstamp+".avi")
#End
