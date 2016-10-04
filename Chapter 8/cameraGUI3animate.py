#!/usr/bin/python3
#cameraGUI3animate.py
import tkinter as TK
import animateGUI as GUI

#Define Tkinter App
root=TK.Tk()
root.title("Camera GUI")
cam=GUI.cameraGUI(root)
TK.mainloop()
#End