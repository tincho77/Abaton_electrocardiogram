from itertools import count
import serial.tools.list_ports
import binascii
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import style
from math import pi
import scipy.fftpack as sf
import scipy.signal as sig
import time

samples = 4000 # Number of samples
style.use('ggplot') # plot style

nfile = "test_data.txt" # EKG signal buffer
f=open(nfile,'w')
f.write("")

# Port initialization
ports = serial.tools.list_ports.comports()
serialInst = serial.Serial()

portList = []

# Show list of PORTS
for onePort in ports:
    portList.append(str(onePort))
    print(str(onePort))

# Select PORT
val = input("select port: COM")

for x in range(0,len(portList)):
    if portList[x].startswith("COM" + str(val)):
        portVar = "COM" + str(val)
        print(portList[x])

# Set PORT selected
serialInst.baudrate = 115200
serialInst.port = portVar
serialInst.open()
y_vals=[]
x_vals=[]

# Wait of user place fingers on sensors
time.sleep(3)

i=0
out=0
index = count()

#Read EKG Signal
while i==0:
    if serialInst.in_waiting:
        f=open(nfile,'a')
        packet = serialInst.read()
        data = str(int(binascii.hexlify(packet), base=16))
        data = data+'\n'
        f.write(data)
        out=next(index)
        print(str((out*100)/samples)+'%')
        if out==samples:
            i=1        

# Sabe EKG Signal on Buffer        
data = np.loadtxt('test_data.txt')
x = data

# Plot signal imput
plt.figure(1) 
plt.subplot(2,1,1)
plt.plot(x); plt.title('Noisy EKG Wave')
plt.xlabel('Time(s)'); plt.ylabel('Amplitude')


# Take spectral analysis
X_f = abs(sf.fft(x))
l = np.size(x)
fr = (samples/2)*np.linspace(0,1,l)
xl_m = (2/1)*abs(X_f[0:np.size(fr)])

# Show Spectral analysis result
plt.subplot(2,1,2)
plt.plot(fr,20*np.log10(xl_m))
plt.title('Spectrum of Noisy signal')
plt.xlabel('Frequency(Hz)')
plt.ylabel('Magnitude')
plt.tight_layout()
    
# Create a BPF
# design filter
nyq = 0.5 * samples # calculate the Nyquist frequency
cutoff=200 # Frequency cutoff
order=5 # Order of filter
low = cutoff / nyq
b, a = sig.butter(order, low, btype='low', analog=False)

# Filter response
[W,h] = sig.freqz(b,a, worN= 1024)
W = samples* W

# Show Filter Response
plt.figure(2)
plt.subplot(2,1,1)
plt.plot(W, 20*np.log10(h))
plt.title('Filter Freq. Response')
plt.xlabel('Frequency(Hz)')
plt.ylabel('Magnitude')

# Filter signal
x_filt = sig.lfilter(b,a,x)

# Show Signal EKG Filtered
plt.subplot(2,1,2)
plt.ylim(ymax = 250, ymin = 100)
plt.plot(x_filt)
plt.title('EKG Filtered Signal')
plt.xlabel('Time(s)')
plt.ylabel('Amplitude')
plt.tight_layout() 

# PLOT SHOW (Show on the screen)
plt.show()   