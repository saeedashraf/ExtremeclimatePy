
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


def create_dic(*args):
    input_dict = {arg: None for arg in args}
    return input_dict

def create_dic_2(*argv):
    '''Function: creating a dictionary for each climate station'''

    #sa = [key for key in argv]

    # keys = ['fM', 'iPot', 'rSnow', 'dSnow', 'cPrec', 'dP', 'elev', 'lat', 'long', 'fileName']
    
    b = {arg: None for arg in argv}
    return b

argv =  ['DayTmin', 'TempTmax', 'TempTmin', 'DayTmax', 'Tmax_weight', 'Tmin_weight', 'elev', 'lat', 'long', 'fileName']
#argv = tuple(argv)


b = create_dic_2(argv)
print(b)




## Step 2: Function for initiating the main dictionary of climate stations
def create_dic():
    '''Function: creating a dictionary for each climate station'''

    a = {}
    # keys = ['fM', 'iPot', 'rSnow', 'dSnow', 'cPrec', 'dP', 'elev', 'lat', 'long', 'fileName']
    keys = ['DayTmin', 'TempTmax', 'TempTmin', 'DayTmax', 'Tmax_weight', 'Tmin_weight', 'elev', 'lat', 'long',
            'fileName']

    a = {key: None for key in keys}
    return a

b = create_dic()
print(b)


def initialize_input_dict(mainFolderHDNs):
    ''' This function returns a dictionary , and addresses of all folders'''

    '''Step 1'''
    rootFolder = mainFolderHDNs
    inputFolder = os.path.join(rootFolder, 'input')
    TmaxFolder = os.path.join(inputFolder, 'Tmax')
    TminFolder = os.path.join(inputFolder, 'Tmin')
    climate_ref_Folder = os.path.join(inputFolder, 'Climate_ref')
    climate_Ref_Folder_org = os.path.join(inputFolder, 'Climate_ref_no_randomness_0')
    climate_ref_Folder_rand_1 = os.path.join(inputFolder, 'Climate_ref_randomness_1')
    climate_ref_Folder_rand_2 = os.path.join(inputFolder, 'Climate_ref_randomness_2')