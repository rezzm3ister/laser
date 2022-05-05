import serial

ardu=serial.Serial(port='COM3',baudrate=9600,timeout=1)
x=0
y=0
while(1):
  
  check=ardu.readline().strip();
  if(check==b'x'):
    x=int(ardu.readline().strip())
  elif(check==b'y'):
    y=int(ardu.readline().strip())
  print(x,' ',y)