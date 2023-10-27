import numpy as np
import pandas as pd
import os
def cal_EF(EFpath,gendata,emikind):
    """
    计算排放因子，年更新
    :param gendata:
    :param emikind:
    :return:
    """
    EFpath = os.path.join(EFpath)
    try:
        EFdata = pd.read_excel(EFpath, index_col=0)
    except FileNotFoundError:
        print('请将排放因子因子文件(排放因子质量.xlsx)放置在‘{}’文件夹下!'.format(os.path.abspath(EFpath)))
        exit()
    area_kind = np.array(EFdata.columns[:])
    EF = []
    for i in range(len(area_kind)):
        gen_temp = np.where((gendata == EFdata[area_kind[i]]['code']), EFdata[area_kind[i]][emikind], 0)
        EF.append(gen_temp)
    ef = np.nansum(EF, axis=0)
    ef[ef == np.nan] = 0
    return ef