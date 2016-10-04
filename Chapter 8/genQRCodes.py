import pyqrcode
qr_code = pyqrcode.create("Once upon a time, there was a princess")
qr_code.png("Story.png")
print("Generated QR-Code")
print("Completed")