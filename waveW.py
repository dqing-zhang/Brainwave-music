# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 18:00:47 2019

@author: Administrator
"""

import wave
import numpy as np
import os
import struct

#读取wav文件
filepath = "./music/"
filename = os.listdir(filepath)
f = wave.open(filepath+filename[1], 'rb')

params = f.getparams()
nchannels, sampwidth, framerate, nframes = params[:4]
strData = f.readframes(nframes)
waveData = np.fromstring(strData, dtype=np.int16)
waveData = waveData*1.0/(max(abs(waveData)))
waveData = np.reshape(waveData,[nframes,nchannels])
f.close()

#写入wav文件
outData = waveData
outData = np.reshape(outData,[nframes*nchannels,1])
outfile = filepath + "out1.wav"
outwave = wave.open(outfile, 'wb')
nchannels = 2
sampwidth = 2
fs = 8000
data_size = len(outData)
framerate = int(fs)
nframes = data_size
comtype = "NONE"
compname = "not compressed"
outwave.setparams((nchannels, sampwidth, framerate, nframes, comtype, compname))
for v in outData:
    outwave.writeframes(struct.pack('h', int(v * 64000 / 2)))
outwave.close()






























