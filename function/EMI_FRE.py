import numpy as np
import pandas as pd
from src import *
def cal_FRE(FRP):
    return FRP*24
def cal_CR(lc):
    cropvalue=9
    CR_crop, CR_other = 0.368,0.411
    return np.where((lc==cropvalue),CR_crop,CR_other)
def cal_EF(lc,EFpath):
    EFdata=pd.read_excel(EFpath,index_col=0)
    area_kind = np.array(EFdata.columns[:])
    EF = []
    for i in range(len(area_kind)):
        gen_temp = np.where(gendata)

def main():
