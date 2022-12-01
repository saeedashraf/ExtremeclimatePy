
# 1.take csv and txt files 
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



class read_inputdata:
    
    def __init__(self, root, *args, **kwargs):
        self.root = root
        self.args = args
        self.kwargs = kwargs  
    
    def _initiate_dict(self, *args, **kwargs):
        """returnes a tuple first element is a dictionary we later assign all the variables and second element is list of variables names"""
        tempdict = {self.arg: 'None' for self.arg in self.args}
        varName = [self.arg for self.arg in self.args]
        return tempdict
        
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
        print('*******1*********')
        print(varFolder)
        print('****************')
   
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

        print('******2**********')
        print(filesA[0])
        print(filesA[1])
        print('****************')
        print('******3**********')
        print(climate_ref_Files)
        print('****************')
        '''Step 3-4-5: Reading files inside Tmax folder '''
        #x1TmaxThershold
        #weights_Var = [ 'weights_' + (str(self.args[i])) for i in range (len(self.args))] 
        day_Var = [ 'day_' + (str(self.args[i])) for i in range (len(self.args))]
        xVarThershold = [ 'x' + str(i+1) + (str(self.args[i]) + 'Thershold') for i in range (len(self.args))]

        for i in range(len(self.args)):
            os.chdir(varFolder[i])                
            #with open(filesA[i][0], 'r') as file:
             #   weights_Var[i] = file.read()
            with open(filesA[i][1], 'r') as file:
                day_Var[i] = file.read()
            with open(filesA[i][2], 'r') as file:
                xVarThershold[i] = file.read()
        
            '''Step 3-4-5: Reading the lines of files inside Tmax folder'''
            #weights_Var[i] = weights_Var[i].replace('\n', '\t').split('\t')
            day_Var[i]  = day_Var[i] .replace('\n', '\t').split('\t')
            xVarThershold[i] = xVarThershold[i].replace('\n', '\t').split('\t')
        print('******4**********')
        #print(weights_Var)
        print(day_Var)
        print(xVarThershold)
        print('****************')
       
        '''Step 6: Reading the lines of files inside climate folder''' 
        os.chdir(climate_ref_Folder)
        #if any('.txt' in s for s in climate_ref_Files):
        #matching = [s for s in climate_ref_Files if ".txt" in s]
        climateTxtFiles = [(str(self.args[i])).lower() + '.txt' for i in range (len(self.args))] 
        climateData = [(str(self.args[i])).lower() + 'Data' for i in range (len(self.args))]
        
        print('********5********')
        print(climateTxtFiles)
        print(climateData)
        print('****************')


        for i in range(len(self.args)):
            with open(climateTxtFiles[i], 'r') as file:
                climateData[i] = file.read()
            climateData[i] =  climateData[i].split('\n')
            for j in range(len(climateData[i])):
                climateData[i][j] = climateData[i][j].split(',')

        print('******6**********')
        print(climateData)
        print('****************')

        '''Step 7: Initialazing the input dictionary of climate stations which holds the information of the stations'''
        #Should be updated for individual variables!! and not only pcp!
        nameStn = []
        for file in climate_ref_Files:
            if 'p.csv' in file:
                #nameStn.append('n_' + file[-25: -5])
                nameStn.append(file[-25: -5])

        print('******7**********')
        print(nameStn)
        print('****************')
        
        stnDicts = []
        for i in range(len(nameStn)):
            stnDicts.append(self._initiate_dict())


        print('******8**********')
        print(stnDicts)
        print('****************')

        '''Step 8: Assigning the file names to the dictionary'''
        for i in range (len(nameStn)):
            stnDicts[i]['fileName'] = nameStn[i]

        print('******9**********')
        print(stnDicts)
        print(stnDicts[0])
        print(stnDicts[1])
        print(day_Var)
        print(xVarThershold)
        #print(stnDicts[0]['fileName']) #tupple and stations
        print('********************************************')

        print(stnDicts[1]['fileName']) #tupple and stations

        print('********************************************')
        '''Step 9_1: Assigning the Tamx, Tmin, Hmd, Pcp, Slr and Wnd values'''

        _temp_DayVar= ['DayTmax', 'DayTmin']
        _temp_ValVar= ['ValTmax', 'ValTmin']
        _temp_DayVar= [ 'day_' + (str(self.args[i])) for i in range (len(self.args))]
        _temp_ValVar= [ 'x' + str(i+1) + (str(self.args[i]) + 'Thershold') for i in range (len(self.args))]
        for i in range(len(self.args)):
            for j, element in enumerate(day_Var[i]):
                for k in range (len(nameStn)):
                    if element == stnDicts[k]['fileName']:
                        print('helllloooo')
                        print(element)
                        print(day_Var[i][j+1])
                        stnDicts[k][_temp_DayVar[i]] = day_Var[i][j+1]
            for j, element in enumerate(xVarThershold[i]):
                for k in range (len(nameStn)):  
                    if element == stnDicts[k]['fileName']:
                        stnDicts[k][_temp_ValVar[i]] = xVarThershold[i][j+1]
            
        print(stnDicts)
        '''Step 10: Assigning the elevation, Lat and long to the dictionaries'''
        for i in range(len(stnDicts)):
            for j in range(1, len(pcpData)):
                
                #if pcpData[j][1][2:-1] == stnDicts[i]['fileName'][2:]:
                if pcpData[j][1][:-1] == stnDicts[i]['fileName'][:]:
                    stnDicts[i]['lat']= pcpData[j][2]
                    stnDicts[i]['long']= pcpData[j][3]
                    stnDicts[i]['elev']= pcpData[j][4]


#a = read_inputdata(r'C:\Saeid\Prj100\SA_47_CCHDNs_package\data\Zurich_kloten', 'Tmax','Tmin', day_Tmax0 = 0, day_Tmin=0)
a = read_inputdata(r'C:\Saeid\Prj100\SA_47_CCHDNs_package\data\Zurich_kloten', 'Tmax','Tmin')

b1 = a._initiate_dict()
print(b1)

c = a._initialize_input_dict()
#print(c)