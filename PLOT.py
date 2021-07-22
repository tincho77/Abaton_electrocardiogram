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
import heartpy as hp

samples = 4000
nfile = "test_data.txt" # EKG signal buffer
f=open(nfile,'r')


# Sabe EKG Signal on Buffer        
data = np.loadtxt('test_data.txt')
x = data

# Plot signal imput
plt.figure(1) 
plt.subplot(2,1,1)
plt.plot(x); plt.title('Noisy EKG Wave')
plt.xlabel('Time(s)'); plt.ylabel('Amplitude')

# Create a BPF
# design filter
nyq = 0.5 * samples # calculate the Nyquist frequency
cutoff=190 # Frequency cutoff (190Hz data of spectrum noise signal, frecuency of start the maximun peaks on wave)
order=5 # Order of filter
low = cutoff / nyq
b, a = sig.butter(order, low, btype='low', analog=False)

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

#analysis ECG
data = x
fs = 200.0 #example file 0 is sampled at 100.0 Hz

working_data, measures = hp.process(x_filt, fs, report_time=False)


print(measures['bpm']) #returns BPM value
print("BPM")
print(measures['rmssd']) # returns RMSSD HRV measure
print("RMSSD HRV")


# PLOT SHOW (Show on the screen)
plt.show()  