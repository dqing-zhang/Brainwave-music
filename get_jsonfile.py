# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 10:55:56 2019

@author: Zhang Danqing
"""

import json
import wave
import os
import glob
import numpy as np

#遍历文件夹下的所有.wav文件,生成相对路径列表
list_wav = []
def foreachWavDir(dirname):  
    try:
        for fn in glob.glob(dirname + os.sep + '*' ): #获取dirname目录下的所有文件
            if os.path.isdir(fn):   # 如果结果为文件夹
                foreachWavDir(fn)   # 递归
            elif os.path.splitext(fn)[1] == '.wav':
                list_wav.append(fn)
    except FileNotFoundError:
        msg = "sorry, the site " + dirname + "does not exist"
        print(msg)
    return list_wav  

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
    print(int(avFreq))
    return int(avFreq)

#读取txt文件中的url到一个列表中
def read_url(txtfile):
    url_dict={}
    with open(txtfile, 'rb') as f:
        for line in f.readlines():
            line = line.decode()
            url_one = line.strip('\n')  
            name_and_ext = url_one.split('/')[-1]
            name,ext = os.path.splitext(name_and_ext)
            url_dict[name] = url_one
    print(len(url_dict))
    return url_dict, len(url_dict)

#将音乐名和对应的平均频率保存在csv文件中
def jsonFile(musicfiledir):
    datalist = []
    list_wav = foreachWavDir(musicfiledir)#获取wav文件列表
    print(list_wav)
    url_name = musicfiledir + '.txt'
    url_dict, length = read_url(url_name)
    json_dir =  musicfiledir + '.json'
    for wavdir in list_wav:
        musicdict = {}
        filepath,fullflname = os.path.split(wavdir) #将路径和文件名分开
        fname,ext = os.path.splitext(fullflname)#将文件名和其扩展名分开             
        waveData, framerate = get_wavdata(wavdir)  
        avFreq = get_avFreq(waveData, framerate)   
        musicdict['music_name'] = fname
        musicdict['average_frequency'] = avFreq
        musicdict['url'] = url_dict[fname]
        datalist.append(musicdict)       
    with open(json_dir, 'w') as f:
        json.dump(datalist, f)
    return list_wav     
           
if __name__ == '__main__':
    list_wav = jsonFile('.\YinYue\wav\wakeUpMusic')
    list_wav = []
    jsonFile('.\YinYue\wav\sleepingMusic')