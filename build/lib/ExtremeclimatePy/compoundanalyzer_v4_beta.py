import os
import os.path
from datetime import datetime, date, timedelta
import numpy as np
import pandas as pd
import seaborn as sns
import shutil
import time
from matplotlib import pyplot as plt
import collections


class read_inputdata:
    
    def __init__(self, root, deepuncertainty_rand, *args, **kwargs):
        self.root = root
        self.deepuncertainty_rand = int(deepuncertainty_rand)
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
        climate_ref_Folder_rand = []
        for i in range(1, self.deepuncertainty_rand + 1):
            climate_ref_Folder_rand.append(os.path.join(inputFolder, 'Climate_ref_randomness_' + str(i)))


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
            if (str(self.args[0].lower()) + '.csv') in file:
                #nameStn.append('n_' + file[-25: -5])
                #nameStn.append(file[-25: (-4-(len(self.args[0])))])  # this line of the code is hard coded. the name of the file
                nameStn.append(file[: (-4-(len(self.args[0])))]) #len(self.args[0]) >> 0 means only Pcp for instance >> all the parameters should be 3 letters

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
        '''Step 9_1: Assigning the Tamx, Tmin, Hmd, Pcp, Slr, Wnd, etc values'''

        #_temp_DayVar= ['DayTmax', 'DayTmin']
       # _temp_ValVar= ['ValTmax', 'ValTmin']
        _temp_DayVar= [ 'day_' + (str(self.args[i])) for i in range (len(self.args))]
        _temp_ValVar= [ 'x' + str(i+1) + (str(self.args[i]) + 'Thershold') for i in range (len(self.args))]
        for i in range(len(self.args)):
            for j, element in enumerate(day_Var[i]):
                for k in range (len(nameStn)):
                    if element == stnDicts[k]['fileName']:
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
                if climateData[i][j][1][:-3] == stnDicts[i]['fileName'][:]:  # -1 to -3 fpr three letters before .csv
                    print("AA")
                    stnDicts[i]['lat']= climateData[i][j][2]
                    stnDicts[i]['long']= climateData[i][j][3]
                    stnDicts[i]['elev']= climateData[i][j][4]
        
        print("***************************************************AAAA********************************************************")
        print(stnDicts)


        return stnDicts, inputFolder, varFolder, climate_ref_Folder, \
            climate_Ref_Folder_org, climate_ref_Folder_rand

class initilizer:

    def __init__(self, start_date, end_date, symlinks=False, ignore=None):
        #self.src = src
        #self.dst = dst
        self.start_date = start_date
        self.end_date = end_date
        self.symlinks = symlinks
        self.ignore = ignore


    def copytree(self):
        for item in os.listdir(self.src):
            s = os.path.join(self.src, item)
            d = os.path.join(self.dst, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, self.symlinks, self.ignore)
            else:
                shutil.copy2(s, d)
    ## 1st column as index: makaing date from 01 01 1981 to 2099 12 31
    #from datetime import timedelta, date

    def daterange(self):
        for n in range(int ((self.end_date - self.start_date ).days + 1)):
            yield self.start_date + timedelta(n)


class RCP_Model:
    def __init__(self, xRCP, xClimateModel, nRCP26, nRCP45, nRCP85):
        self.input1 = round(xRCP)
        #self.input1 = xRCP
        self.input2 = xClimateModel
        self.nRCP26 = nRCP26
        self.nRCP45 = nRCP45
        self.nRCP85 = nRCP85
        
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

    
    def climateModel_(self): # 11, 25, 31 are for MeteoSwiss data only
        a, b = RCP_Model.rcpGenerator(self)
        
        if b == 1:
            climateModel = round(self.input2*self.nRCP26)
            
        elif b == 2:
            climateModel = self.nRCP26 + max(1,round(self.input2*self.nRCP45))
            
        else:
            climateModel = self.nRCP26 + self.nRCP45 + max(1, round(self.input2*self.nRCP85))
            
        return (int(climateModel))


class solver_CCD(read_inputdata):
    #def __init__(self, root, start_date, end_date, xRCP, xClimateModel, Xfactor1, nRCP26, nRCP45, nRCP85, deepuncertainty_rand, *args, **kwargs):
    def __init__(self, root, start_date, end_date, xRCP, xClimateModel, nRCP26, nRCP45, nRCP85, deepuncertainty_rand, *args, **kwargs):
        super().__init__(root, deepuncertainty_rand, *args, **kwargs)
        self.start_date = start_date
        self.end_date = end_date
        self.xRCP=xRCP
        self.xClimateModel = xClimateModel
        #self.Xfactor1 = Xfactor1
        self.nRCP26 = nRCP26
        self.nRCP45 = nRCP45
        self.nRCP85 = nRCP85
        #self.deepuncertainty_rand = deepuncertainty_rand

    def _print(self):
        print(self.xRCP)
        print(self.xClimateModel)
        print(self.root)
        print(self.args)
        #print(self.Xfactor1)
        print(self.kwargs)
        return

    def ccd_calc(self):

        caseStudyStns, inputFolder, varFolder, climateFolder, \
            climateFolder_org, climateFolder_rands = self._initialize_input_dict()

        #xClimateRandomness = round(self.Xfactor1)
        xClimateRandomness = round(self.deepuncertainty_rand)

        if (xClimateRandomness == 1):
            os.chdir(climateFolder_org)
            src = os.getcwd()
            os.chdir(climateFolder)
            dst = os.getcwd()
            #copytree(src, dst)
            print('Original CH2018 is being used')
        else:
            os.chdir(climateFolder_rands[xClimateRandomness - 1])
            src = os.getcwd()
            os.chdir(climateFolder)
            dst = os.getcwd()
            #copytree(src, dst)
            print('Random Climate realization version n is being used')

        print('HDNs_DMDU: Matching the station names values with CSV files!')   
        
        '''Matching the station names values in the dictionary of stations with CSV files in Climate folder of the case Study'''
        
        _VarCaseStudy = [ [] for i in range (len(self.args))] # IMPORTANT !!! we should change and ask useres to gice us the number


        print("TTTTTTT")
        print(_VarCaseStudy)
        print(type(_VarCaseStudy[0]))


        varCaseStudy  = collections.OrderedDict()
        for i in range(len(caseStudyStns)):
            for j in range(len(_VarCaseStudy)):
                #d["{0}".format( 'x' + str(i+1) + (str(self.args[i]) + 'Thershold'))] = []
                varCaseStudy["{0}".format(str(self.args[j]) + 'CaseStudy' + '_stn_' + str(i))] = []

        varCaseStudykeys = list(varCaseStudy.keys())

        print(varCaseStudy)

        ### t.csv should be changed for tmin.csv and tmax.csv at the moment we read both in a same file but this should chamnge in future 


        if (xClimateRandomness == 1):
            for i in range(len(caseStudyStns)):
                for j in range(len(self.args)):

                    varCaseStudy[varCaseStudykeys[i*len(self.args)+j]].append(os.path.join(climateFolder_org, caseStudyStns[i]['fileName'] +  str(self.args[j]).lower() + '.csv'))

        else:
            #for i in range(len(varCaseStudy)):
            for i in range(len(caseStudyStns)):
                for j in range(len(self.args)):
                     # change varCaseStudy to caseStudyStns
                #for key, value in varCaseStudy.items():
                #for key, value in varCaseStudy.items():
                    varCaseStudy[varCaseStudykeys[i*len(self.args)+j]].append(os.path.join(climateFolder_rands[self.deepuncertainty_rand-1], caseStudyStns[i]['fileName'] +  str(self.args[j]).lower() + '.csv'))


        print(varCaseStudy)
        #print(varCaseStudy[key]) # print Valus of the last key in Dict
        print('HDNs_DMDU: Building a database for each csv file (tmp, pcp, hmd, slr, wnd, etc)!')
        
        '''Step 6: building a database for each precipitation and temperature file in Climate folder and saving them in a list'''
        '''6.1 reading the csv files as databases'''
        dfvar  = collections.OrderedDict()
        #for i in range(len(_VarCaseStudy)):
        for i in range(len(caseStudyStns)):
            for j in range(len(self.args)):
                #dfvar['df' + "{0}".format(str(self.args[i]))] = [None for _ in range(len(varCaseStudy[key]))]
                dfvar['df_' + "{0}".format(str(self.args[j] + "_stn_" + str(i)))] = [None]
        
        print(dfvar)
        dfvarkeys = list(dfvar.keys())
        print(dfvarkeys)
        #print(dfvar[dfvarkeys[1]][0])

        dfvarCol  = collections.OrderedDict()
        for i in range(len(caseStudyStns)):
            for j in range(len(self.args)): 
            #d["{0}".format( 'x' + str(i+1) + (str(self.args[i]) + 'Thershold'))] = []
            #dfvarCol['df' + "{0}".format(str(self.args[j]) + 'Col')] = [None for _ in range(len(varCaseStudy[key]))]
                dfvarCol['df' + "{0}".format(str(self.args[j]) + 'Col_' + 'stn_' + str(i))] = [None]

        dfvarColKey = list(dfvarCol.keys())
        
        #dfvarCol = ['df' + "{0}".format(str(self.args[i]) + 'Col') for i in range(len(self.args))]
        '''6.2 where we read the CSV files'''
        
        for i in range(len(caseStudyStns)):
            for j in range(len(self.args)):
                dfvar[dfvarkeys[i*len(self.args)+j]][0] = pd.read_csv(varCaseStudy[varCaseStudykeys[i*len(self.args)+j]][0])
                dfvarCol[dfvarColKey[i*len(self.args)+j]][0] = dfvar[dfvarkeys[i*len(self.args)+j]][0].columns

        
        '''6.2 making a header for output files'''
        print('end 111')

        '''6.3 defining the length of simulations and scenarios'''
        # for Generalization "/ 2" should be corrected because it is for Tmax Tmin
        scenariosLength = int(len(dfvarCol[dfvarColKey[0]][0])-1)
        #simulationLength = len(dfvar[0][dfvarCol[0]]) - 1
        #simulationLength = len(dfvar[dfvarkeys[0]][0]) - 1 # has all columns and returnd the number of rows
        simulationLength = len(dfvar[dfvarkeys[0]][0]) # has all columns and returnd the number of rows

            
        '''Reading the beginning and end of the simulation''' 

        dateList = []
        _temp_helper = initilizer(self.start_date, self.end_date)

        for single_date in _temp_helper.daterange():
            dateList.append(single_date.strftime("%m/%d/%Y"))
        
        start_year = _temp_helper.start_date.year
        end_year = _temp_helper.end_date.year + 1
        print(start_year)
        print(end_year)
        #print(dateList)

        seasonList = []
        for n in range (start_year, end_year + 1, 1):
            seasonList.append(str(n))
        
        print(scenariosLength)
        print(simulationLength)
        print('HDNs_DMDU: Finish reading Running the input CSVs!')
        print('HDNs_DMDU: START Part 1 Running the model, looking for extreme events and printing the output!')


        '''################################ PART1 ################################'''
        '''*******************************Running the model for each climate station:***********************************'''

        todayVar = collections.OrderedDict()
        univariant_extremes = collections.OrderedDict()
        is_extreme_Compound = collections.OrderedDict()
        len_extreme_Compound = collections.OrderedDict()
        total = collections.OrderedDict()

        for i in range(len(self.args)):
            #univariant_extremes['is_extreme_' + "{0}".format(str(self.args[i]))] = [0 for _ in range(simulationLength)] # use k for + "_stns" + str(k)
            todayVar['today' + "{0}".format(str(self.args[i]))] = 0 
        
        for k in range(len(caseStudyStns)):
            for i in range(len(self.args)):
                univariant_extremes['is_extreme_' + "{0}".format(str(self.args[i] + "_stns_" + str(k)))] = [0 for _ in range(simulationLength)] # use k for + "_stns" + str(k)
        
        for k in range(len(caseStudyStns)):
            is_extreme_Compound['is_extreme_Compound_stn_' + "{0}".format(str(k))] = [0 for _ in range(simulationLength)]
            len_extreme_Compound['len_extreme_Compound_stn_' + "{0}".format(str(k))] = [0 for _ in range(simulationLength)]
            total['total_' + "{0}".format(str(k))] = np.zeros([simulationLength, (2*len(self.args) + 2)])
            

        todayVar_keys = list(todayVar.keys())
        univariant_extremes_keys = list(univariant_extremes.keys())
        is_extreme_Compound_keys = list(is_extreme_Compound.keys())
        len_extreme_Compound_keys = list(len_extreme_Compound.keys())
        total_keys = list(total.keys())

        
        print("XXXXXXXX")
        print(univariant_extremes_keys)
        print(todayVar_keys)
        print("XXXXXXXX")
        caseStudyStns_keys = list(caseStudyStns[0].keys()) # why = 0? no matter [0] or [1] because the variables are same for N stations  
        print(caseStudyStns_keys[4])
        print(caseStudyStns_keys[6])
        print(caseStudyStns_keys)
        print("XXXXXXXX")


        '''RCP and Climate Model Controler'''
        rcp_Model = RCP_Model(self.xRCP, self.xClimateModel, self.nRCP26, self.nRCP45, self.nRCP85)
        RCP, intRCP = rcp_Model.rcpGenerator()
        climateModel = rcp_Model.climateModel_()

        print(RCP)
        print(intRCP)
        print(climateModel)
        
        '''***********************************For the FIRST DAY of Simulation ONLY:*************************************'''
        '''Running the model for each Stations:'''
        for k in range(len(caseStudyStns)):       
            '''Running the model for each climate scenario:'''
            for j in range(climateModel, climateModel + 1, 1):
                '''Running the model for each Variable:'''
                for i in range(len(self.args)):#i for variable Tmax or Tmin k for stations (0t.csv and 1t.csv), j for climate model meaning the clomun of csv file
                    todayVar[todayVar_keys[i]] = round(dfvar[dfvarkeys[k*len(self.args)+i]][0][dfvarCol[dfvarColKey[k*len(self.args)+i]][0][j]].iloc[0], 2) \
                    if (dfvar[dfvarkeys[k*len(self.args)+i]][0][dfvarCol[dfvarColKey[k*len(self.args)+i]][0][j]].iloc[0] != -99) else 0

                    total[total_keys[k]][0,i] = todayVar[todayVar_keys[i]]

                # '''Tmax Tmin all variables, check the condition of the first day:'''
                    if ( todayVar[todayVar_keys[i]]) >= float(caseStudyStns[k][caseStudyStns_keys[len(self.args) + 1 + 2*i]]):# 1 is for file name in ccaseStudyStansday_Var[i][j+1]

                        univariant_extremes[univariant_extremes_keys[k*len(self.args)+i]][0] = 1


                    else: univariant_extremes[univariant_extremes_keys[k*len(self.args)+i]][0] = 0

        _no_compound_vars = 0 
        for k in range(len(caseStudyStns)): #20230201
            for i in range(len(self.args)):
                _no_compound_vars +=  univariant_extremes[univariant_extremes_keys[k*len(self.args)+i]][0] ### should be range(1) for generalization ?
            if _no_compound_vars == len(self.args): # (univariant_extremes[univariant_extremes_keys[k*len(self.args)+i]][0] == 1) and ( univariant_extremes[univariant_extremes_keys[k*(i+1)+1]][0] == 1):
                is_extreme_Compound[is_extreme_Compound_keys[k]][0] = 1
            else: is_extreme_Compound[is_extreme_Compound_keys[k]][0] = 0

            len_extreme_Compound[len_extreme_Compound_keys[k]][0] = 1 if (is_extreme_Compound[is_extreme_Compound_keys[k]][0] == 1) else 0

            '''storing  values in a list for the first day ready fo printing in the csv file:'''
            for i in range(len(self.args)):
                total[total_keys[k]][0,(len(self.args) + i)] = round(univariant_extremes[univariant_extremes_keys[k*len(self.args)+i]][0], 2)

            
            total[total_keys[k]][0,(2*len(self.args) + 0)] = round(is_extreme_Compound[is_extreme_Compound_keys[k]][0],2)
            total[total_keys[k]][0,(2*len(self.args) + 1)] = round(len_extreme_Compound[len_extreme_Compound_keys[k]][0],2)

        print('Done first day')


        '''***********************************For the SECOND DAY to the END DAY of Simulation:***********************************'''
        for t in range(2, simulationLength + 1, 1):
            for k in range(len(caseStudyStns)):       
                '''Running the model for each climate scenario:'''
                for j in range(climateModel, climateModel + 1, 1):
                    '''Running the model for each Variable:'''
                    for i in range(len(self.args)):#i for variable Tmax or Tmin k for stations (0t.csv and 1t.csv), j for climate model meaning the clomun of csv file

                        todayVar[todayVar_keys[i]] = round(dfvar[dfvarkeys[k*len(self.args)+i]][0][dfvarCol[dfvarColKey[k*len(self.args)+i]][0][j]].iloc[t-1], 2) \
                        if (dfvar[dfvarkeys[k*len(self.args)+i]][0][dfvarCol[dfvarColKey[k*len(self.args)+i]][0][j]].iloc[t-1] != -99) else 0

                        total[total_keys[k]][t-1,i] = todayVar[todayVar_keys[i]]
                        #total[total_keys[k]][0,i] = todayVar[todayVar_keys[i]]


                    # '''Tmax Tmin all variables, check the condition of the first day:'''
                        if ( todayVar[todayVar_keys[i]]) >= float(caseStudyStns[k][caseStudyStns_keys[len(self.args) + 1 + 2*i]]):

                            univariant_extremes[univariant_extremes_keys[k*len(self.args)+i]][t-1] = 1


                        else: univariant_extremes[univariant_extremes_keys[k*len(self.args)+i]][t-1] = 0

            _no_compound_vars = 0 
            for k in range(len(caseStudyStns)): #20230201
                for i in range(len(self.args)):
                    _no_compound_vars +=  univariant_extremes[univariant_extremes_keys[k*len(self.args)+i]][t-1] ### should be range(1) for generalization ?
                if _no_compound_vars == len(self.args): # (univariant_extremes[univariant_extremes_keys[k*len(self.args)+i]][0] == 1) and ( univariant_extremes[univariant_extremes_keys[k*(i+1)+1]][0] == 1):
                    is_extreme_Compound[is_extreme_Compound_keys[k]][t-1] = 1
                else: is_extreme_Compound[is_extreme_Compound_keys[k]][t-1] = 0

                #len_extreme_Compound[len_extreme_Compound_keys[k]][0] = 1 if (is_extreme_Compound[is_extreme_Compound_keys[k]][0] == 1) else 0
                len_extreme_Compound[len_extreme_Compound_keys[k]][t-1] = (len_extreme_Compound[len_extreme_Compound_keys[k]][t-2] + is_extreme_Compound[is_extreme_Compound_keys[k]][t-1]) \
                if (is_extreme_Compound[is_extreme_Compound_keys[k]][t-1] == 1) else 0
                '''storing  values in a list for the first day ready fo printing in the csv file:'''
                for i in range(len(self.args)):
                    total[total_keys[k]][t-1,(len(self.args) + i)] = round(univariant_extremes[univariant_extremes_keys[k*len(self.args)+i]][t-1], 2)


                total[total_keys[k]][t-1,(2*len(self.args) + 0)] = round(is_extreme_Compound[is_extreme_Compound_keys[k]][t-1],2)
                total[total_keys[k]][t-1,(2*len(self.args) + 1)] = round(len_extreme_Compound[len_extreme_Compound_keys[k]][t-1],2)
        
        print('Done all days')


        '''Saving the Outputs of total list in a CSV file in a specific path'''
        
        for k in range(len(caseStudyStns)):

            ## 1st row for the column names:
            columnsDF0 = ['DATE']
            columnsDF = []

            
            nameHeader =  dfvarCol[dfvarColKey[k*len(self.args)]][0][climateModel-1] #dfvarCol[dfvarColKey[0]][0][134] 

            for i in range(len(self.args)):
                columnsDF.append('today_' + "{0}".format(str(self.args[i])) + '_' + nameHeader)

            for i in range(len(self.args)):
                columnsDF.append('is_' + "{0}".format(str(self.args[i])) + '_exEv_' + nameHeader) 

            columnsDF.append('Are_ALL_VARs_exEve_' + nameHeader)
            columnsDF.append('Length_ALL_VARs_exEve_' + nameHeader)


            '''******Extreme analyses daily******'''
            dfnew0 = pd.DataFrame(dateList, columns = columnsDF0)
            dfnew1 = pd.DataFrame(total[total_keys[k]], columns = columnsDF)
            df1 = pd.concat([dfnew0, dfnew1], axis=1, sort=False)


            if os.path.isdir(os.path.join(self.root, 'Outputs_ExtremeclimatePy')):
                pass
            else: os.mkdir(os.path.join(self.root, 'Outputs_ExtremeclimatePy'))


            '''Make CSvs for daily extreme Outputs'''
            outfolder =os.path.join(self.root, 'Outputs_ExtremeclimatePy') 
            outfileName = 'Total_daily_' + caseStudyStns[k]['fileName'] + '.csv' ##
            outputFile = os.path.join(outfolder, outfileName )
            df1.to_csv(outputFile, index = False)
        
        print('Done.... end of calculations')
    #print("Goodbye!")

###### START Of the API ######
#from datetime import date
#from ExtremeclimatePy import compoundanalyzer_v4_beta

# root = r'.\examples\CC_3vars_PCP_TMN_TMX' 
# start_date = date(1981, 1, 1)
# end_date = date(2099, 12, 31)
# xRCP = 3
# xClimateModel = 0.99
# nRCP26 = 12
# nRCP45 = 25
# nRCP85 = 31
# deepuncertainty_rand = 5

# CCD = compoundanalyzer_v4_beta.solver_CCD(root, start_date, end_date, xRCP, xClimateModel, nRCP26, nRCP45, nRCP85, deepuncertainty_rand, 'Pcp', 'Tmn','Tmx')
# CCD_Pcp_Tmn_Tmx = CCD.ccd_calc()


