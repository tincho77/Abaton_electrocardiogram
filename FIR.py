import matplotlib.pyplot as plt
import numpy as np
from math import log10, pi
import scipy.fftpack as sf
import scipy.signal as sig

plt.close('all')

# Genarate signal (change for te EKG signal of MOD-EKG board)
Fs = 100
t = 1
n = np.arange(0,t,1/Fs)
f = 10
x = np.sin(2*pi*f*n)
# Generate a noise
y = np.random.normal(0, 0.8, np.size(x)) # AWGN
x = x + y # Noisy singnal

# Plot signal imput
plt.figure(1) 
plt.subplot(2,1,1)
plt.plot(n,x); plt.title('Noisy Sinusoidal Wave')
plt.xlabel('Time(s)') 
plt.ylabel('Amplitude')


# Take spectral analysis
X_f = abs(sf.fft(x))
l = np.size(x)
fr = (Fs/2)*np.linspace(0,1,l)
xl_m = (2/1)*abs(X_f[0:np.size(fr)])

plt.subplot(2,1,2)
plt.plot(fr,20*np.log10(xl_m))
plt.title('Spectrum of Noisy signal')
plt.xlabel('Frequency(Hz)')
plt.ylabel('Magnitude')
plt.tight_layout()

# Create a BPF
o = 5
fc = np.array([8,12])
wc = 2*fc/Fs;
[b,a] = sig.butter(o, wc, btype='bandpass')

# Filter response
[W,h] = sig.freqz(b,a, worN= 1024)

W = Fs* W/(2*pi)

plt.figure(2)
plt.subplot(2,1,1)
plt.plot(W, 20*np.log10(h))
plt.title('Filter Freq. Response')
plt.xlabel('Frequency(Hz)')
plt.ylabel('Magnitude')

# Filter signal
x_filt = sig.lfilter(b,a,x)

plt.subplot(2,1,2)
plt.plot(n,x_filt)
plt.title('Filtered Signal')
plt.xlabel('Time(s)')
plt.ylabel('Amplitude')
plt.tight_layout()


# PLOT SHOW
plt.show()