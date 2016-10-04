#!/usr/bin/python3
#animateGUI.py
import tkinter as TK
from tkinter import messagebox
import time
import os
import cameraGUI as camGUI

class SET(camGUI.SET):
  TL_SIZE=(1920,1080)
  ENC_PROG="mencoder -nosound -ovc lavc -lavcopts"
  ENC_PROG+=" vcodec=mpeg4:aspect=16/9:vbitrate=8000000"
  ENC_PROG+=" -vf scale=%d:%d"%(TL_SIZE[0],TL_SIZE[1])
  ENC_PROG+=" -o %s -mf type=jpeg:fps=24 mf://@%s"
  LIST_FILE="image_list.txt"

class cameraGUI(camGUI.cameraGUI):
  def diff(a, b):
    b = set(b)
    return [aa for aa in a if aa not in b]

  def __init__(self,parent):
    super(cameraGUI,self).__init__(parent)
    self.parent=parent
    TK.Frame.__init__(self,self.parent,
                      background="white")
    self.theList = TK.Variable()
    self.imageListbox=TK.Listbox(self.parent,
                   listvariable=self.theList,
                       selectmode=TK.EXTENDED)
    self.imageListbox.grid(row=0, column=4,columnspan=2,
                              sticky=TK.N+TK.S+TK.E+TK.W)
    yscroll = TK.Scrollbar(command=self.imageListbox.yview,
                                        orient=TK.VERTICAL)
    yscroll.grid(row=0, column=6, sticky=TK.N+TK.S)
    self.imageListbox.configure(yscrollcommand=yscroll.set)
    self.trimBtn=TK.Button(self.parent,text="Trim",
                                  command=self.trim)
    self.trimBtn.grid(row=1,column=4)
    self.speed = TK.IntVar()
    self.speed.set(20)
    self.speedScale=TK.Scale(self.parent,from_=1,to=30,
                                  orient=TK.HORIZONTAL,
                                   variable=self.speed,
                                   label="Speed (fps)")
    self.speedScale.grid(row=2,column=4)
    self.genBtn=TK.Button(self.parent,text="Generate",
                                 command=self.generate)
    self.genBtn.grid(row=2,column=5)
    self.btnAniTxt=TK.StringVar()
    self.btnAniTxt.set("Animate")
    self.animateBtn=TK.Button(self.parent,
              textvariable=self.btnAniTxt,
                      command=self.animate)
    self.animateBtn.grid(row=1,column=5)
    self.animating=False
    self.updateList()

  def shutter(self):
    super(cameraGUI,self).shutter()
    self.updateList()

  def updateList(self):
    filelist=[]
    for files in os.listdir("."):
      if files.endswith(".jpg"):
        filelist.append(files)
    filelist.sort()
    self.theList.set(tuple(filelist))
    self.canvas.update()

  def generate(self):
    self.msg("Generate video...")
    cameraGUI.run("ls *.jpg > "+SET.LIST_FILE)
    filename=cameraGUI.timestamp()+".avi"
    cameraGUI.run(SET.ENC_PROG%(filename,SET.LIST_FILE))
    self.msg(filename)
    TK.messagebox.showinfo("Encode Complete",
                           "Video: "+filename)
  def trim(self):
    print("Trim List")
    selected = map(int,self.imageListbox.curselection())
    trim=cameraGUI.diff(range(self.imageListbox.size()),
                                                selected)
    for item in trim:
      filename=self.theList.get()[item]
      self.msg("Rename file %s"%filename)
      #We could delete os.remove() but os.rename() allows
      #us to change our minds (files are just renamed).
      os.rename(filename,
                filename.replace(".jpg",".jpg.bak"))
      self.imageListbox.selection_clear(0,
                      last=self.imageListbox.size())
    self.updateList()

  def animate(self):
    print("Animate Toggle")
    if (self.animating==True):
      self.btnAniTxt.set("Animate")
      self.animating=False
    else:
      self.btnAniTxt.set("STOP")
      self.animating=True
      self.doAnimate()

  def doAnimate(self):
    imageList=[]
    selected = self.imageListbox.curselection()
    if len(selected)==0:
      selected=range(self.imageListbox.size())
    print(selected)
    if len(selected)==0:
      TK.messagebox.showinfo("Error",
                      "There are no images to display!")
      self.animate()
    elif len(selected)==1:
      filename=self.theList.get()[int(selected[0])]
      self.updateDisp(filename,SET.PV_SIZE)
      self.animate()
    else:
      for idx,item in enumerate(selected):
        self.msg("Generate Image: %d/%d"%(idx+1,
                                        len(selected)))
        filename=self.theList.get()[int(item)]
        aImage=cameraGUI.getTKImage(filename,SET.PV_SIZE)
        imageList.append(aImage)
      print("Apply Images")
      canvasList=[]
      for idx,aImage in enumerate(imageList):
        self.msg("Apply Image: %d/%d"%(idx+1,
                                       len(imageList)))
        canvasList.append(self.canvas.create_image(0, 0,
                                  anchor=TK.NW,
                                  image=imageList[idx],
                                  state=TK.HIDDEN))
      self.cycleImages(canvasList)

  def cycleImages(self,canvasList):
    while (self.animating==True):
      print("Cycle Images")
      for idx,aImage in enumerate(canvasList):
        self.msg("Cycle Image: %d/%d"%(idx+1,
                                  len(canvasList)))
        self.canvas.itemconfigure(canvasList[idx],
                                  state=TK.NORMAL)
        if idx>=1:
          self.canvas.itemconfigure(canvasList[idx-1],
                                      state=TK.HIDDEN)
        elif len(canvasList)>1:
          self.canvas.itemconfigure(
                        canvasList[len(canvasList)-1],
                                      state=TK.HIDDEN)
        self.canvas.update()
        time.sleep(1/self.speed.get())
#End
