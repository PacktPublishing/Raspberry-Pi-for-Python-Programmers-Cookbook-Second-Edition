#!/usr/bin/python3
#openimage.py
import cv2

# Load a color image in grayscale
img = cv2.imread('testimage.jpg',0)
cv2.imshow('image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()

