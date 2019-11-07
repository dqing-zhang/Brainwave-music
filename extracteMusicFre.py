# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 11:41:45 2019

@author: zhang danqing
"""
import csv
import wave
import os
import glob
import numpy as np
from mp32wav import wavName, mp32wav

listwav = []
#遍历文件夹下.wav文件,生成相对路径列表
def foreachWavDir(dirname):  
    for fn in glob.glob(dirname + os.sep + '*' ): #获取dirname目录下的所有文件
        if os.path.isdir(fn):   # 如果结果为文件夹
            foreachDir(fn)   # 递归
        elif os.path.splitext(fn)[1] == '.wav':
            listwav.append(fn)
    return listwav  

#将wav音乐转换为波形数据
def get_wavdata(wavdir):
    f = wave.open(wavdir, 'rb')
    params = f.getparams()
    nchannels, sampwidth, framerate, nframes = params[:4]
    strData = f.readframes(nframes)
    waveData = np.fromstring(strData, dtype=np.int16)
    waveData = waveData*1.0/(max(abs(waveData)))
    waveData = np.reshape(waveData,[nframes,nchannels])
    f.close()
    print(nchannels)
    return waveData[:, 0], framerate

#提取wav波形数据的平均频率
def get_avFreq(waveData, framerate):
    F=[]            
    intervel = 1/(framerate-1)
    count = 0
    indx = 0
    num_data = len(waveData)
    for i in range(1, num_data):
        if waveData[i] * waveData[i-1] < 0:
            count += 1
            if count%2 == 1:
                item_T = intervel * (i-indx)
                item_F = 1/item_T
                indx = i+1
                F.append(item_F)
    avFreq = np.mean(F)
    print(avFreq)
    return avFreq

#将音乐名和对应的平均频率保存在csv文件中
def csvFile(musicfiledir):
    datalist = []
    listwav = foreachWavDir(musicfiledir)#获取wav文件列表
    for wavdir in listwav:
        musicdict = {}
        filepath,fullflname = os.path.split(wavdir) #将路径和文件名分开
        fname,ext = os.path.splitext(fullflname)#将文件名和其扩展名分开             
        waveData, framerate = get_wavdata(wavdir)  
        avFreq = get_avFreq(waveData, framerate)   
        musicdict['music_name'] = fname
        musicdict['average_frequency'] = avFreq
        datalist.append(musicdict)       
    headers = ['music_name', 'average_frequency']
    csv_name =  musicfiledir + 'list.csv'
    with open(csv_name, 'w', encoding='utf-8', newline='') as fp:
        writer = csv.DictWriter(fp, headers)
        writer.writeheader()
        writer.writerows(datalist)
    return datalist      

#返回数据列表
def dataList():
    wakedatalist = csvFile('.\YinYue\wav\wakeUpMusic')
    sleepdatalist = csvFile('.\YinYue\wav\SleepingMusic')
    return wakedatalist, sleepdatalist
           
if __name__ == '__main__':
    dataList()
    
    

        
		
    
    
    
    






