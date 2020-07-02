#!/usr/bin/env python
import cv2
import os
from os import listdir
from os.path import isfile, join
import numpy as np
import random

# Format for annotations: <object-class> <x_center> <y_center> <width> <height>
# img =cv2.imread('/home/mkz/FLIR_test/FLIR_00001.jpeg', cv2.IMREAD_GRAYSCALE)
onlyfiles = [f for f in listdir("/home/vamsi/ToDel_FLIR/video/thermal_8_bit/") if isfile(join("/home/vamsi/ToDel_FLIR/video/thermal_8_bit/", f))]
# cv2.imshow('image',img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
# cv2.imwrite('/home/mkz/FLIR_test/Stretched/FLIR_00001.jpeg',img)
# print("done")


print('No. of Files: ', len(onlyfiles))
ManF = open("/home/vamsi/ToDel_FLIR/manifest.txt","a+")
for idx in range(len(onlyfiles)):
    Input_img =cv2.imread('/home/vamsi/ToDel_FLIR/video/thermal_8_bit/'+onlyfiles[idx], cv2.IMREAD_GRAYSCALE)
    for sdx in range(3): # Supplemental Files
        OutputImg=np.zeros((512,512*5))
        randomPos=random.randint(1,512*5-642)
        OutputImg[:,randomPos:randomPos+640]=Input_img
        SupplFileName=onlyfiles[idx][0:-5]+'a'+str(sdx)+'.jpeg'
        cv2.imwrite('/home/vamsi/ToDel_FLIR/Stretched/'+SupplFileName,OutputImg)
        print(onlyfiles[idx],sdx)
        ### Create Text File names
        tempFileName='/home/vamsi/ToDel_FLIR/video/converted/thermal_8_bit/'+onlyfiles[idx][0:-5]+'.txt'
        if os.path.isfile(tempFileName):
            # data/flirData/training/thermal_8_bit/
            ManifestLine='data/flirData/training/thermal_8_bit/'+onlyfiles[idx][0:-5]+'a'+str(sdx)+'.jpeg'+'\n'
            ManF.write(ManifestLine)
            with open(tempFileName,"r") as SourceF:
                with open('/home/vamsi/ToDel_FLIR/Annotations_Str/'+onlyfiles[idx][0:-5]+'a'+str(sdx)+'.txt', "w+") as DestF:
                    for line in SourceF:
                        l = line.split()
                        objClass=l[0] # Unchanged
                        Box_x=(float(l[1])*640+randomPos)/(512*5)
                        Box_x=str(Box_x) # Convert to string
                        Box_y=l[2] # Unchanged
                        BoxWidth=(float(l[3])*640)/(512*5)
                        BoxWidth=str(BoxWidth)
                        BoxHeight=l[4] #Unchanged
                        outLine=objClass+' '+Box_x[0:5]+' '+Box_y+' '+BoxWidth[0:5]+' '+BoxHeight+'\n'
                        DestF.write(outLine)
                    DestF.close()
                SourceF.close()
ManF.close()
print("done")