import serial
import serial.tools.list_ports

def getport():
  ports=list(serial.tools.list_ports.comports())
  return ports[0].device

ardu=serial.Serial(port=getport(),baudrate=9600,timeout=1)

while True:
  ardu.write(bytes([255]))
  ardu.write(bytes([90]))
  ardu.write(bytes([254]))
  ardu.write(bytes([90]))