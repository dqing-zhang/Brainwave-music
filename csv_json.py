# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 11:46:59 2019

@author: Administrator
"""
import csv
import json

"""
功能  将csv格式转换为json格式文件
参数  filedir：csv文件所在目录加文件名
"""
def csv_json(filedir):
    csvdir = filedir + '.csv'
    jsondir = filedir + '.json'
    with open(csvdir, 'r') as fn:
        csvlist = list(csv.reader(fn))
        header = csvlist[0]
        del csvlist[0]
        datalist = []
        for row in csvlist:
            datadict = {}
            datadict[header[0]] = row[0]
            datadict[header[1]] = int(row[1])
            datadict[header[2]] = row[2]
            print(datadict)
            datalist.append(datadict)
    with open(jsondir, 'w') as f:
        json.dump(datalist, f)

if __name__ == '__main__':
    csv_json(".\YinYue\sleepingMusic")
    csv_json(".\YinYue\wakeUpMusic")
