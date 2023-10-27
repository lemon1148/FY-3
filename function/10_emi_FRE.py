import numpy as np
import pandas as pd
from src.pathlist import *
from src.cal.cal_EF import cal_EF
def cal_FRE(FRP):
    return FRP*24
def cal_CR(lc):
    cropvalue=9
    CR_crop, CR_other = 0.368,0.411
    return np.where((lc==cropvalue),CR_crop,CR_other)

def main(emikind):
    EF = cal_EF(EFpath,gendata,emikind)
