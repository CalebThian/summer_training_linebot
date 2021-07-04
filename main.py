# -*- coding: utf-8 -*-
"""
Created on Fri Jul  2 22:04:20 2021

@author: caleb
"""

from PIL import Image
import cv2
import pytesseract

def get_name_from_img(img):
    img = cv2.imread(img,cv2.IMREAD_GRAYSCALE)
    (thresh, img_bw) = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    cv2.imshow("MY IMG",img_bw)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    global a
    a=img_bw
    print(img_bw)
    ImageText = pytesseract.image_to_string(img,lang = "chi_tra" )
    return ImageText

def get_name_from_list(path):
    with open(path,'r') as file:
        global namelist
        namelist = file.readlines()
        file.close()        


#if __name__ == '__main__':
with open("config.txt","r") as file:
    path = file.readline()
    path = file.readline()
    pytesseract.pytesseract.tesseract_cmd = r"D:\Tesseract-OCR\tesseract.exe"
    
    website_night = "https://docs.google.com/spreadsheets/d/1z735DZS2StVi9jKFGtxpdBYlP41RGYV9aM1ikFUkc08/edit#gid=0"
    website_weekend = "https://docs.google.com/spreadsheets/d/1FezG1Io3rTJLtkJNBIL9LVNbTVCma8iwJWxjRUWHZ9E/edit#gid=0"
    
    temp = file.readline()
    temp = file.readline()
    if temp == "夜間班":
        website = website_night
    else:
        website = website_weekend
        
    message_no = file.readline()
    message_no = file.readline()
    
    file.close()
    
get_name_from_list("namelist.txt")
