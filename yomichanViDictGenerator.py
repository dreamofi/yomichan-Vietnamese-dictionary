#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 22:51:57 2019

@author: home
"""

import os, sqlite3, json, ray
import numpy as np

#Need to install ray package: 'pip install ray'

kanjidicPath = './yomichanJsonInput/kanjidic_english'
jmdictPath = './yomichanJsonInput/jmdict_english'

def getFileList(path):
    fileList = []
    for r, d, f in os.walk(path):
        for file in f:
            if all(['.json' in file, 'index' not in file, 'tag' not in file]):
                fileList.append(os.path.join(r, file))
    return fileList

kanjidicFile = getFileList(kanjidicPath)
jmdictFile = getFileList(jmdictPath)

#For modifying kanjidic2
def modifyKanjiDict(dict):
    connectDb = sqlite3.connect('./SQLiteDB/finalDBSHanVietSound_Production.sqlite')
    cursor= connectDb.cursor()
    for entry in dict:
        kanjiChar = entry[0]
        #print(kanjiChar)
        query = cursor.execute('SELECT field3 || " " || field4 FROM kanji where field1=?', (kanjiChar,))
        result = query.fetchall()
        if len(result) < 1:
            continue
        else:
            entry[4].append(result[0][0])

#for modifying jmdict
def modifyDict(dict):
    connectDb = sqlite3.connect('./SQLiteDB/finalDBSHanVietSound_Production.sqlite')
    cursor= connectDb.cursor()
    for entry in dict:
        word = entry[0]
        #print(kanjiChar)
        queryHanviet = cursor.execute('SELECT field2 || " " || field3 FROM hanviet where field1=?', (word,))
        resultHanviet = queryHanviet.fetchall()
        queryMeaning = cursor.execute('SELECT field2 FROM meaning where field1=?', (word,))
        resultMeaning = queryMeaning.fetchall()
        
        if len(resultHanviet) > 0:
            entry[5].append(resultHanviet[0][0])
        if len(resultMeaning) > 0:
            entry[5].append(resultMeaning[0][0])

@ray.remote        
def parseDict(file, isKanjiDict):
    if isKanjiDict == True:
        jsonOutputDir = './yomichanJsonOutput/kanjidic_vietnamese/'
    else:
        jsonOutputDir = './yomichanJsonOutput/jmdict_vietnamese/'
        
    for jsonFile in file:
        print('Processing: ', jsonFile)
        with open(jsonFile) as json_file:
            data = json_file.read()
        readData = json.loads(data)
        if isKanjiDict == True:
            modifyKanjiDict(readData)
        else:
            modifyDict(readData)
            
        file2Write = os.path.join(jsonOutputDir, os.path.basename(jsonFile))
        with open(file2Write, 'w') as jsonWrite:
            jsonWrite.write(json.dumps(readData, ensure_ascii=False))            
    return 'done'

#Single core parse    
#parseDict(kanjidicFile, True)
    
#Multithreading with 4 cores
def multiThreadParse(file, isKanjiDict):
    fileLength = len(file)
    
    #Split the file list for multithread processing
    if fileLength >= 4:
        splitFileList = np.array_split(file, 4)
    elif fileLength >= 3:
        splitFileList = np.array_split(file, 3)
    elif fileLength >= 2:
        splitFileList = np.array_split(file, 2)
    else:
        splitFileList = file
    
    # Start Ray.
    ray.shutdown()
    ray.init()
    
    result_rays = []
    
    for i in splitFileList:
        result_rays.append(parseDict.remote(i, isKanjiDict))
        
    # Wait for the tasks to complete and retrieve the results.
    results = ray.get(result_rays)
    print(results)

multiThreadParse(jmdictFile, False)