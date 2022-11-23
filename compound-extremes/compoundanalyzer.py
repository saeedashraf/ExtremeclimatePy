
# 1.take csv files 
# 2. read the variables and creat dictionary
# 3-

import os
import os.path
from datetime import datetime, date, timedelta
import numpy as np
import pandas as pd
import seaborn as sns
import shutil
import time
from matplotlib import pyplot as plt




class read_data:
    
    def __init__(self, root, *args, **kwargs):
        self.root = root
        self.args = args
        self.kwargs = kwargs  
    
    def _initial_dict(self):
        tempdict = {self.arg: 'None' for self.arg in self.args}
        varName = [self.arg for self.arg in self.args]
        return tempdict, varName
        
    def _initialize_input_dict(self):
        ''' This function returns a dictionary , and addresses of all folders'''
        
        '''Step 1''' 
        rootFolder = self.root
        inputFolder = os.path.join(rootFolder,'input')
        
        varFolder = []
        for i in range(len(self.args)):
            tempName = str(self.args[i]) + 'Folder'
            tempName = os.path.join(inputFolder, self.args[i])
            varFolder.append(tempName)
        print(varFolder)
   
        climate_ref_Folder = os.path.join(inputFolder, 'Climate_ref')
        climate_Ref_Folder_org = os.path.join(inputFolder, 'Climate_ref_no_randomness_0')
        climate_ref_Folder_rand_1 = os.path.join(inputFolder, 'Climate_ref_randomness_1')
        climate_ref_Folder_rand_2 = os.path.join(inputFolder, 'Climate_ref_randomness_2')

        '''Step 2: Reading all files' names inside the Tamx, Tmin, and climate folders'''  
        filesA = [ (str(self.args[i]) + 'Files') for i in range (len(self.args))]
        for i in range (len(self.args)): 
            for filename in os.walk(varFolder[i]):
                filesA[i] = filename[2]

        climate_ref_Files = list()
        for filename in os.walk(climate_ref_Folder):
            climate_ref_Files = filename[2]

        print(filesA[0])
        print(filesA[1])
        print(climate_ref_Files)
        '''Step 3-4-5: Reading files inside Tmax folder '''
        #x1TmaxThershold
        weights_Var = [ 'weights_' + (str(self.args[i])) for i in range (len(self.args))] 
        day_Var = [ 'day_' + (str(self.args[i])) for i in range (len(self.args))]
        xVarThershold = [ 'x' + str(i+1) + (str(self.args[i]) + 'Thershold') for i in range (len(self.args))]

        for i in range(len(self.args)):
            os.chdir(varFolder[i])                
            with open(filesA[i][0], 'r') as file:
                weights_Var[i] = file.read()
            with open(filesA[i][1], 'r') as file:
                day_Var[i] = file.read()
            with open(filesA[i][2], 'r') as file:
                xVarThershold[i] = file.read()
        
            '''Step 3-4-5: Reading the lines of files inside Tmax folder'''
            weights_Var[i] = weights_Var[i].replace('\n', '\t').split('\t')
            day_Var[i]  = day_Var[i] .replace('\n', '\t').split('\t')
            xVarThershold[i] = xVarThershold[i].replace('\n', '\t').split('\t')

        
        '''Step 6: Reading the lines of files inside climate folder''' 
        os.chdir(climate_ref_Folder)
        
        with open('pcp.txt', 'r') as file:
            pcpData = file.read()
        with open('tmp.txt', 'r') as file:
            tmpData = file.read()
            
        pcpData = pcpData.split('\n')
        
        for i in range(len(pcpData)):
            pcpData[i] = pcpData[i].split(',')
        


        print(weights_Var)
        print(day_Var)
        print(xVarThershold)



a = read_data(r'C:\Saeid\Prj100\SA_47_CCHDNs_package\data\Zurich_kloten', 'Tmax','Tmin')
b1, b2 = a._initial_dict()
print(b1)
print(b2)
c = a._initialize_input_dict()
#print(c)