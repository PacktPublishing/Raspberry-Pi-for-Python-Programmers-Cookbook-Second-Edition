#!/usr/bin/python3
#cameraGUI2timelapse.py
import tkinter as TK
import timelapseGUI as GUI

root=TK.Tk()
root.title("Camera GUI")
cam=GUI.cameraGUI(root)
TK.mainloop()
#End