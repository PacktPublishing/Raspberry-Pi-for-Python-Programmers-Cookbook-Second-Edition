#!/usr/bin/python3
#qrcodeGUI
import tkinter as TK
from tkinter import messagebox
import subprocess
import cameraGUI as camGUI

class SET(camGUI.SET):
  QR_SIZE=(640,480)
  READ_QR="zbarimg "

class cameraGUI(camGUI.cameraGUI):
  def run_p(cmd):
    print("RunP:"+cmd)
    proc=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
    result=""
    for line in proc.stdout:
      result=str(line,"utf-8")
    return result

  def __init__(self,parent):
    super(cameraGUI,self).__init__(parent)
    self.parent=parent
    TK.Frame.__init__(self,self.parent,background="white")
    self.qrScan=TK.IntVar()
    self.qrRead=TK.IntVar()
    self.qrStream=TK.IntVar()
    self.resultQR=TK.StringVar()
    self.btnQrTxt=TK.StringVar()
    self.btnQrTxt.set("QR GO!")
    self.QRBtn=TK.Button(self.parent,textvariable=self.btnQrTxt,
                                              command=self.qrGet)
    readChk=TK.Checkbutton(self.parent,text="Read",
                               variable=self.qrRead)
    streamChk=TK.Checkbutton(self.parent,text="Stream",
                                 variable=self.qrStream)
    labelQR=TK.Label(self.parent,textvariable=self.resultQR)
    readChk.grid(row=3,column=0)
    streamChk.grid(row=3,column=1)
    self.QRBtn.grid(row=3,column=3)
    labelQR.grid(row=4,columnspan=4)
    self.scan=False

  def qrGet(self):
    if (self.scan==True):
      self.btnQrTxt.set("QR GO!")
      self.btnState("active")
      self.scan=False
    else:
      self.msg("Get QR Code")
      self.btnQrTxt.set("STOP")
      self.btnState("disabled")
      self.scan=True
      self.qrScanner()

  def qrScanner(self):
    found=False
    while self.scan==True:
      self.resultQR.set("Taking image...")
      self.update()
      cameraGUI.camCapture(SET.PREVIEW_FILE,SET.QR_SIZE)
      self.resultQR.set("Scanning for QRCode...")
      self.update()
      #check for QR code in image
      qrcode=cameraGUI.run_p(SET.READ_QR+SET.PREVIEW_FILE)
      if len(qrcode)>0:
        self.msg("Got barcode: %s"%qrcode)
        qrcode=qrcode.strip("QR-Code:").strip('\n')
        self.resultQR.set(qrcode)
        self.scan=False
        found=True
      else:
        self.resultQR.set("No QRCode Found")
    if found:
      self.qrAction(qrcode)
      self.btnState("active")
      self.btnQrTxt.set("QR GO!")
    self.update()

  def qrAction(self,qrcode):
    if self.qrRead.get() == 1:
      self.msg("Read:"+qrcode)
      cameraGUI.run("sudo flite -t '"+qrcode+"'")
    if self.qrStream.get() == 1:
      self.msg("Stream:"+qrcode)
      cameraGUI.run("omxplayer '"+qrcode+"'")
    if self.qrRead.get() == 0 and self.qrStream.get() == 0:
      TK.messagebox.showinfo("QR Code",self.resultQR.get())
#End
