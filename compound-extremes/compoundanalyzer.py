
# 1.take csv and txt files 
# 2. read the variables and creat dictionary
# 3- read text files, csvs, etc


import os
import os.path
from datetime import datetime, date, timedelta
import numpy as np
import pandas as pd
import seaborn as sns
import shutil
import time
from matplotlib import pyplot as plt


from datetime import timedelta, date

import collections

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
            #tempName = str(self.args[i]) + 'Folder'
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
        print("***********************************************CCC************************************************************")
        '''Step 10: Assigning the elevation, Lat and long to the dictionaries'''
        for i in range(len(stnDicts)):
            #print(climateData[i])
            for j in range(0, len(climateData[i])):
                print("*******")
                print(climateData[i][j])
                if climateData[i][j][1][:-1] == stnDicts[i]['fileName'][:]:
                    print("AA")
                    stnDicts[i]['lat']= climateData[i][j][2]
                    stnDicts[i]['long']= climateData[i][j][3]
                    stnDicts[i]['elev']= climateData[i][j][4]
        
        print("***************************************************AAAA********************************************************")
        print(stnDicts)
        return stnDicts, inputFolder, varFolder, climate_ref_Folder, \
            climate_Ref_Folder_org, climate_ref_Folder_rand_1, climate_ref_Folder_rand_2


#a = read_inputdata(r'C:\Saeid\Prj100\SA_47_CCHDNs_package\data\Zurich_kloten', 'Tmax','Tmin')

#b1 = a._initiate_dict()
#print(b1)

#c = a._initialize_input_dict()
#print(c)


class _helper:

    def __init__(self,src, dst, start_date, end_date, symlinks=False, ignore=None):
        self.src = src
        self.dst = dst
        self.start_date = start_date
        self.end_date = end_date
        self.symlinks = symlinks
        self.ignore=ignore


    def copytree(self):
        for item in os.listdir(self.src):
            s = os.path.join(self.src, item)
            d = os.path.join(self.dst, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, self.symlinks, self.ignore)
            else:
                shutil.copy2(s, d)
    ## 1st column as index: makaing date from 01 01 1981 to 2099 12 31
    from datetime import timedelta, date

    def daterange(self):
        for n in range(int ((self.end_date - self.start_date ).days + 1)):
            yield self.start_date + timedelta(n)


class RCP_Model:
    def __init__(self, xRCP, xClimateModel):
        self.input1 = round(xRCP)
        #self.input1 = xRCP
        self.input2 = xClimateModel  
        
    def rcpGenerator(self):
        if self.input1 == 1:
            RCP = str(2.6)
            rcpInt = 1
        if self.input1 == 2:
            RCP = str(4.5)
            rcpInt = 2
        if self.input1 == 3:
            RCP = str(8.5)
            rcpInt = 3
        return(RCP, rcpInt)

    
    def climateModel(self):
        a, b = RCP_Model.rcpGenerator(self)
        
        if b == 1:
            climateModel = round(self.input2*11)
            
        elif b == 2:
            climateModel = 11 + max(1,round(self.input2*25))
            
        else:
            climateModel = 36 + max(1, round(self.input2*31))
            
        return (int(climateModel))


class solver_CCD(read_inputdata):
    def __init__(self, root, xRCP, xClimateModel, Xfactor1, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.xRCP=xRCP
        self.xClimateModel = xClimateModel
        self.Xfactor1 = Xfactor1

    def _print(self):
        print(self.xRCP)
        print(self.xClimateModel)
        print(self.root)
        print(self.args)
        print(self.Xfactor1)
        print(self.kwargs)
        return

    def ccd_calc(self):

        caseStudyStns, inputFolder, varFolder, climateFolder, \
            climateFolder_org, climateFolder1, \
                 climateFolder2 = self._initialize_input_dict()

        
        xClimateRandomness = round(self.Xfactor1)

        if (xClimateRandomness == 1):
            os.chdir(climateFolder_org)
            src = os.getcwd()
            os.chdir(climateFolder)
            dst = os.getcwd()
            #copytree(src, dst)
            print('Original CH2018 is being used')
        elif (xClimateRandomness == 2) :
            os.chdir(climateFolder1)
            src = os.getcwd()
            os.chdir(climateFolder)
            dst = os.getcwd()
            #copytree(src, dst)
            print('Random Climate realization version 1 is being used')
        else:
            os.chdir(climateFolder2)
            src = os.getcwd()
            os.chdir(climateFolder)
            dst = os.getcwd()
            #copytree(src, dst)
            print('Random Climate realization version 2 is being used')

        
        os.chdir(climateFolder)
        fnames = os.listdir()
        #randomness_pcp_tmp(fnames, Xfactor1)

        print('HDNs_DMDU: Matching the station names values with CSV files!')   
        
        '''Matching the station names values in the dictionary of stations with CSV files in Climate folder of the case Study'''
        
        _VarCaseStudy = [ [] for i in range (len(self.args))]


        print("TTTTTTT")
        print(_VarCaseStudy)
        print(type(_VarCaseStudy[0]))


        varCaseStudy  = collections.OrderedDict()
        dfvar  = collections.OrderedDict()
        for i in range(len(_VarCaseStudy)):
            #d["{0}".format( 'x' + str(i+1) + (str(self.args[i]) + 'Thershold'))] = []
            varCaseStudy["{0}".format(str(self.args[i]) + 'CaseStudy')] = []
        
        print(varCaseStudy)

        ### t.csv should be changed for tmin.csv and tmax.csv at the moment we read both in a same file but this should chamnge in future 


        if (xClimateRandomness == 1):
            for i in range(len(_VarCaseStudy)):
                #for j in range(len(caseStudyStns)):
                    #d[i].append(os.path.join(climateFolder, caseStudyStns[j]['fileName'] + 't.csv'))
                for key, value in varCaseStudy.items():
                    varCaseStudy[key].append(os.path.join(climateFolder_org, caseStudyStns[i]['fileName'] + 't.csv'))

        if (xClimateRandomness == 2):
            for i in range(len(_VarCaseStudy)):
                for key, value in varCaseStudy.items():
                    varCaseStudy[key].append(os.path.join(climateFolder1, caseStudyStns[i]['fileName'] + 't.csv'))

        if (xClimateRandomness == 3):
            for i in range(len(_VarCaseStudy)):
                for key, value in varCaseStudy.items():
                    varCaseStudy[key].append(os.path.join(climateFolder2, caseStudyStns[i]['fileName'] + 't.csv'))
                    #dfvar['df' + "{0}".format(str(self.args[i]))] = [None for _ in range(len(d[key]))]        
        
        varCaseStudykeys = list(varCaseStudy.keys())

        print(varCaseStudy)
        print(varCaseStudy[key])
        print('HDNs_DMDU: Building a database for each csv file (tmp, pcp, hmd, slr, wnd)!')
        
        '''Step 6: building a database for each precipitation and temperature file in Climate folder and saving them in a list'''

        dfvar  = collections.OrderedDict()
        for i in range(len(_VarCaseStudy)):
            dfvar['df' + "{0}".format(str(self.args[i]))] = [None for _ in range(len(varCaseStudy[key]))]
        
        dfvarkeys = list(dfvar.keys())
        print(dfvarkeys)

        print(dfvar)
        print(dfvar[dfvarkeys[1]][0])

        for i in range(len(dfvar)):
            for j in range(len(dfvar[dfvarkeys[i]])):
                dfvar[dfvarkeys[i]][j] = pd.read_csv(varCaseStudy[varCaseStudykeys[i]][j])

 

CCD = solver_CCD(r'C:\Saeid\Prj100\SA_47_CCHDNs_package\data\Zurich_kloten', 3, 22, 0.87, 'Tmax','Tmin')
y = CCD.ccd_calc()




print("********************************EEEEENNNNNDDDDD********************************")

