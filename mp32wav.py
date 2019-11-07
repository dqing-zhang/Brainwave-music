# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 15:59:49 2019

@author: Zhang Danqing
"""

import glob
import os
from pydub import AudioSegment

listmp3 = []
#遍历文件夹下.mp3文件,生成相对路径列表
def foreachMp3Dir(dirname):  
    for fn in glob.glob(dirname + os.sep + '*' ): # 获取dirname目录下的所有文件
        if os.path.isdir(fn):   # 如果结果为文件夹
            foreachDir(fn)   # 递归
        elif os.path.splitext(fn)[1] == '.mp3':
            listmp3.append(fn)
    return listmp3    

#提取文件名称，并组成一个新的.wav文件名
def wavName(mp3dir):
	filepath,fullflname = os.path.split(mp3dir) #将路径和文件名分开
	fname,ext = os.path.splitext(fullflname)#将文件名和其扩展名分开
	var = fname + '.wav'
	return filepath, fname, var

#将.mp3文件转换为.wav格式文件并进行保存
def mp32wav(mp3dir,filepath, var):
    path=filepath.split('\\')[2]
    wavdiro = '.\\wangYiYun\\wav\\' + path
    if not os.path.exists(wavdiro):
        os.makedirs(wavdiro)
    sound = AudioSegment.from_mp3(mp3dir)
    wavdir = wavdiro + os.sep + var
    sound.export(wavdir, format ='wav')      

if __name__ == '__main__':
    listmp3 = foreachMp3Dir('.\wangYiYun')
    for mp3dir in listmp3:
        filepath, fname, var = wavName(mp3dir)
        mp32wav(mp3dir,filepath, var)
        
        
    
