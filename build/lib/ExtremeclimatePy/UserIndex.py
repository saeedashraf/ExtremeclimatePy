import numpy as np

class UserIndex:
    final_var_threshold = 10

    def __init__(self, Hmd, Pcp, Slr, Tmn, Tmx, Wnd):
        self.Hmd = Hmd
        self.Pcp = Pcp
        self.Slr = Slr
        self.Tmn = Tmn
        self.Tmx = Tmx
        self.Wnd = Wnd
        
    def compute_final_var(self):
        return 2*self.Hmd + self.Pcp**(1/2) + np.power(self.Slr, 1) + self.Tmn + (self.Tmx)/2 + self.Wnd

    def operatore_final_var(self):
        return UserIndex.final_var_threshold