from itertools import count
import serial.tools.list_ports
import binascii
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import style

style.use('grayscale')
nfile = "test_data.txt"
f=open(nfile,'w')
f.write("")

ports = serial.tools.list_ports.comports()
serialInst = serial.Serial()

portList = []

for onePort in ports:
    portList.append(str(onePort))
    print(str(onePort))

val = input("select port: COM")

for x in range(0,len(portList)):
    if portList[x].startswith("COM" + str(val)):
        portVar = "COM" + str(val)
        print(portList[x])

serialInst.baudrate = 115200
serialInst.port = portVar
serialInst.open()
y_vals=[]
x_vals=[]

i=0
out=0
index = count()
while i==0:
    if serialInst.in_waiting:
        f=open(nfile,'a')
        packet = serialInst.read()
        data = str(int(binascii.hexlify(packet), base=16))
        data = data+'\n'
        f.write(data)
        out=next(index)
        print(str((out*100)/10000)+'%')
        if out==10000:
            i=1        
        
data = np.loadtxt('test_data.txt')


x = data
plt.title("Electrocardiogram")
plt.plot(x,'r--')
plt.show()       
    