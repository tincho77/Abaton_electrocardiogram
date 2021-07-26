from itertools import count
import serial.tools.list_ports
import binascii
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import style
from math import pi
import scipy.fftpack as sf
import scipy.signal as sig
from datetime import datetime
from time import time, sleep
import time
import heartpy as hp
import matplotlib.patches as mpatches

samples = 14000 # Number of samples
style.use('ggplot') # plot style

nfile = "test_data.txt" # EKG signal buffer
f=open(nfile,'w')
f.write("")

file = "test_time.txt" # EKG signal buffer
ftime=open(file,'w')
ftime.write("")

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
time.sleep(10)

i=0
out=0
index = count()


f=open(nfile,'a')
ftime = open(file,'a')
inicio = round(time.time() * 1000)
#Read EKG Signal
while i==0:
    
    if serialInst.in_waiting:    
        packet = serialInst.read()
        time_data =str((round(time.time() * 1000))-inicio)+'\n'
        data = str(int(binascii.hexlify(packet), base=16))
        data = data+'\n'
        f.write(data)
        ftime.write(time_data)
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
cutoff=400 # Frequency cutoff (190Hz data of spectrum noise signal, frecuency of start the maximun peaks on wave)
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

#analysis ECG

#if you have a ms-based timer:
mstimer_data = hp.get_data('test_time.txt')
fs = hp.get_samplerate_mstimer(mstimer_data)/1.3 #Correction factor to time of sample
print("fs= ")
print(fs)

#data = x
#fs = 200 #example file 0 is sampled at 100.0 Hz

working_data, measures = hp.process(x, fs, report_time=True)

print(measures['bpm']) #returns BPM value
print("BPM")
print(measures['rmssd']) # returns RMSSD HRV measure
print("RMSSD HRV")



# Show Signal EKG Filtered
plt.subplot(2,1,2)
plt.ylim(ymax = 250, ymin = 100)
plt.plot(x_filt)
plt.title('EKG Filtered Signal')
plt.xlabel('Time(s)')
plt.ylabel('Amplitude')
bpm_patch = mpatches.Patch(color="none", label=str("%.2f" % measures['bpm'])+" BPM")
hrv_patch = mpatches.Patch(color="none", label=str("%.2f" % measures['rmssd'])+" HRV")
plt.legend(handles=[bpm_patch,hrv_patch])
plt.tight_layout() 

#show heart ratepeak detection
data = x
working_data, measures = hp.process(data, fs)
hp.plotter(working_data, measures)

# PLOT SHOW (Show on the screen)
plt.show()   