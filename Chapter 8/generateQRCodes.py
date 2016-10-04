#!/usr/bin/python3
#generateQRCodes.py
import pyqrcode
valid=False
print("QR-Code generator")
while(valid==False):
    inputpages=input("How many pages?")
    try:
      PAGES=int(inputpages)
      valid=True
    except ValueError:
      print("Enter valid number.")
      pass
print("Creating QR-Codes for "+str(PAGES)+" pages:")
for i in range(PAGES):
  file="page%03d"%(i+1)
  qr_code = pyqrcode.create(file+".mp3")
  qr_code.png(file+".png")
  print("Generated QR-Code for "+file)
print("Completed")
#End