import cv2 as cv
import numpy as np
import serial
import serial.tools.list_ports

framex=0
framey=0

def getport():
  ports=list(serial.tools.list_ports.comports())
  return ports[0].device

ardu=serial.Serial(port=getport(),baudrate=9600,timeout=1)

if __name__=="__main__":
  vid=cv.VideoCapture(1)
  framex=vid.get(cv.CAP_PROP_FRAME_WIDTH)
  framey=vid.get(cv.CAP_PROP_FRAME_HEIGHT)
  x=0
  y=0
  while(1):
    check=ardu.readline().strip();
    if(check==b'x'):
      x=int(ardu.readline().strip())
    elif(check==b'y'):
      y=int(ardu.readline().strip())
    print(x,' ',y)
    #write on a paper when the laser goes off screen to get angles