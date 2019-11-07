# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 17:00:46 2019

@author: Zhang Danqing
"""
import os
import wave
import matplotlib.pyplot as plt
import numpy as np

filepath = r"./music/"
filename = os.listdir(filepath)

f = wave.open(filepath+filename[21], 'rb')
params = f.getparams()
#print(params)
nchannels, sampwidth, framerate, nframes = params[:4]
#声道数， 量化位数， 采样频率， 采样点数
strData = f.readframes(nframes)
waveData = np.fromstring(strData, dtype=np.int16)
waveData = waveData*1.0/(max(abs(waveData)))#幅值归一化
waveData = np.reshape(waveData, [nframes, nchannels])
f.close()
   
time = np.arange(0, nframes)*(1.0/framerate)
plt.figure()
plt.subplot(311)
plt.plot(time, waveData[:,0])
plt.xlabel("Time(s)")
plt.ylabel("Amplitude")
plt.title("Ch-1 wavedata")
plt.grid("on")

plt.subplot(313)
plt.plot(time, waveData[:,1])
plt.xlabel("Time(s)")
plt.ylabel("Amplitude")
plt.title("Ch-2 wavedata")
plt.grid("on")

