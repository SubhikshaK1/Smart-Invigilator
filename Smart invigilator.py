print("please wait... Camera will start ...")

# importing the required packages
#pip install numpy
#pip install opencv-python
#pip install Pillow --upgrade

#in command prompt pip install pydrive
'''google it- google developer console
Create a new project in Google Developer Console by clicking “CREATE PROJECT”.
You can give your project a name or leave it as default.
Enable APIs and Services by clicking the “ENABLE APIS AND SERVICES” as indicated by the red circle.
Search “Google Drive” in the API library
Click the “Google Drive API” icon and then click “ENABLE”, which will enable your Google Drive API service.
Create credentials by clicking the “CREATE CREDENTIALS” icon
click “client ID” as that’s the Python program needs. Then click “CREATE” and download the JSON file.
Rename the file as client_scerets.json, cut and paste the file in your python folder.

https://docs.google.com/document/d/1SefeL_n7kXF4BcgfMuT0t6B49lob_fnCt8WcOVNqMVQ/edit?usp=sharing

'''



#Required packages are imported
import cv2
from cv2 import VideoWriter
from cv2 import VideoWriter_fourcc
import datetime
from PIL import ImageGrab
import numpy as np
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth


# Turning on the webcam 
webcam = cv2.VideoCapture(0)

#webcam video file name- date,month,year,Hour,minutes,seconds along with extension as .avi
x = datetime.datetime.now()
y=x.strftime("%d_%b_%Y_%H_%M_%S")
d="."
ext=(y,"avi")
z=d.join(ext)
print("file name to be saved is ",z)


# VideoWriter object for webcam video
video = VideoWriter(z, VideoWriter_fourcc(*'MP42'), 25.0, (640, 480))
# syntax: VideoWriter(file_path, fourcc, fps, (w, h))

#imported VideoWriter_fourcc converts from a string (four chars) to an int. For example, cv2. VideoWriter_fourcc(*'MP42') gives an int for codec MP42 
#fps: Defined frame rate of the output video stream (25.0)
#frameSize: Size of the video frames (640, 480)

#Video conversion from a string (four chars) to an int
fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')

#screen recording video file name- S date,month,year,Hour,minutes,seconds along with extension as .avi
c=x.strftime("S %d_%b_%Y_%H_%M_%S")
ext1=(c,"avi")
sfilename=d.join(ext1)
print("Screen recording file name to be saved is ",sfilename)

#frame rate for screen recording 
fps = 20.0
#frameSize for screen recording
width =1920
height =1080

#VideoWriter object for screen recording
screen_video = cv2.VideoWriter(sfilename, fourcc, 20.0, (width, height))

print("press q to stop recording and upload to drive")
while True:
    # capturing the frame from the webcam
    relay_on, frame = webcam.read()
    
    # if webcam stream is ok
    if relay_on:
        #frame is displayed
        cv2.imshow('Webcam relay', frame)
        
        # writing the webcam relay video into the frame
        video.write(frame)

    #To screen record screenshot is taken as 
    screenshot = ImageGrab.grab(bbox=(0, 0, width, height))
    #bbox: specifies which region to be copied. [By default entire screen is copied]
    
    #screenshot is converted to a numpy array
    screenshot_np = np.array(screenshot)

    #COLOR_BGR2RGB - conversion of BGR(Blue, Green, Red) to RGB(Red, Green, Blue)
    screenshot_final = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2RGB)
    
    # Screen recoding is displayed
    cv2.imshow('Screen recording', screenshot_final)
    
    #Writing the screen recording video into the the VideoWriter object for screen recording in specifed timestamped file name 
    screen_video.write(screenshot_final)
    
    # To stop both the recording 'q' should be pressed
    if cv2.waitKey(1) == ord('q'):
        break


#Webcam is turned off
webcam.release()

#Sends the webcam video to specified timestamped file name
video.release()

#Sends the screen recording video to specified S timestamped file name
screen_video.release()

#Closes the frames(Webcam relay, Screen recording) 
cv2.destroyAllWindows()


#The Google authentication
gauth = GoogleAuth()

# Creates local webserver and automatically handles authentication.
gauth.LocalWebserverAuth()	
drive = GoogleDrive(gauth)

#directory of the python file and client_scerets.json
directory="H:\Python prg"
import os
filename=os.path.join(directory,z)
print(filename)

vfile=drive.CreateFile({'title':z})
vfile.SetContentFile(filename)
vfile.Upload()

screenfilename=os.path.join(directory,sfilename)
print(screenfilename)

svfile=drive.CreateFile({'title':sfilename})
svfile.SetContentFile(screenfilename)
svfile.Upload()
