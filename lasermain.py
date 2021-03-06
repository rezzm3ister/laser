from pickle import FALSE
from re import X
import cv2 as cv
import numpy as np
import serial
import serial.tools.list_ports
from multiprocessing import Process
from time import sleep

mode = 1
# 0 = drag on screen
# 1 = eye tracking

haarmode=1
# 0 = no glasses
# 1 = glasses


def getport():
  ports=list(serial.tools.list_ports.comports())
  return ports[0].device

ardu=serial.Serial(port=getport(),baudrate=9600,timeout=1)
hold=False
#pool=mp.Pool(mp.cpu_count())

mx=0
my=0
framex=0
framey=0
xbytes=0
ybytes=0

def sendtoardu():
 

  sx=int(np.interp(mx,[0,640],[120,60]))
  sy=int(np.interp(my,[0,480],[110,70]))

  ardu.write(bytes([255]))
  ardu.write(bytes([sx]))
  ardu.write(bytes([254]))
  ardu.write(bytes([sy]))

   
def click_event(event,x,y,flags,params):
  global hold, mx, my
  if event==cv.EVENT_LBUTTONDOWN:
    hold=1
    #sendtoardu(x,y)
    mx=x 
    my=y
  elif event == cv.EVENT_LBUTTONUP:
    hold=0

  elif event==cv.EVENT_MOUSEMOVE:
    if hold==True:
      #sendtoardu(x,y)
      mx=x 
      my=y

  else:
    hold=0
  

if __name__ == "__main__":
  vid=cv.VideoCapture(1) #trial and error to find the right cam
  if haarmode==1:
    eyecas=cv.CascadeClassifier('haareye.xml')
  else:
    eyecas=cv.CascadeClassifier('haarglasses.xml')

  framex=vid.get(cv.CAP_PROP_FRAME_WIDTH)
  framey=vid.get(cv.CAP_PROP_FRAME_HEIGHT)
  cv.namedWindow('img')
  while(True):
    ret,frame=vid.read()
    #frame=cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
        
    #cv.imshow('img',frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
      break
    if mode==0:
      cv.setMouseCallback('img',click_event)
      #sleep(0.01)
    elif mode==1:
      #ai here we go
      eyes=eyecas.detectMultiScale(frame,scaleFactor=1.1,minNeighbors=7)

      for(x,y,w,h) in eyes:
        mx=x+w/2
        my=y+h/2
        #cv.circle(frame,(250,250),radius=100,color=(0,0,126),thickness=-1)
        
        #cv.rectangle(frame,(x,y),(x+w,y+h),(0,0,255), thickness=5)
    #cv.circle(frame,(int(framex/2),int(framey/2)),radius=10,color=(255,0,0),thickness=-1)
    cv.circle(frame,(int(mx),int(my)),radius=10,color=(0,0,255),thickness=3)
    cv.imshow('img',frame)
    

    #print(mx,' ',my)
    sendtoardu()

    
  cv.destroyAllWindows()
