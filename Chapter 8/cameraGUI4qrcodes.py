#!/usr/bin/python3
#cameraGUI4qrcodes.py
import tkinter as TK
import qrcodeGUI as GUI

#Define Tkinter App
root=TK.Tk()
root.title("Camera GUI")
cam=GUI.cameraGUI(root)
TK.mainloop()
#End