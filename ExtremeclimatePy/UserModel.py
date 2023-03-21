import numpy as np

class UserModel:
    final_var_threshold = 12
    operator_final_var = "gte"

    def __init__(self, Hmd, Pcp, Slr, Tmn, Tmx, Wnd):
        self.Hmd = Hmd
        self.Pcp = Pcp
        self.Slr = Slr
        self.Tmn = Tmn
        self.Tmx = Tmx
        self.Wnd = Wnd
        
    def compute_final_var(self):
        ''' Please change the following output according to your study'''
        
        return  float(0.735*self.Tmx + 0.0374* self.Hmd + 0.00292*self.Tmx*self.Hmd + \
                      7.619*(self.Slr/1000) - 4.557*((self.Slr/1000)*(self.Slr/1000)) - 0.0572*self.Wnd)
        #return .... 

    def threshold_final_var(self):
        return UserModel.final_var_threshold
    
    def operator_fina_var(self):
         return UserModel.operator_final_var