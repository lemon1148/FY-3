import datetime
import os

import numpy as np
import pandas as pd
from scipy.signal import convolve2d

from src.little_function.find_nearest_files import *
from src.little_function.get_hdfdata import get_hdfdata
from src.little_function.get_tif import get_tif
from src.pathlist import *
def dataselect(date,firedata):
    """
    ndvi，gfr数据筛选（根据日期）
    :return:
    """
    fire = firedata['FIRES']
    target_time = datetime.datetime(int(date[0]), int(date[1]), int(date[2]))
    ndvifilepath = find_nearest_files(NDVIpath, target_time, 1)
    try:
        ndvidata = get_tif(ndvifilepath).astype(float)
    except:
        print('缺少NDVI（{}年{}月）,请补充数据"{}"'.format(date[0], date[1], os.path.abspath(ndvifilepath)))
        exit()

    return fire, ndvidata

def calburndata(firepoint):
    """
    燃烧数据生成（根据筛选后的gfr生成燃烧火点数据）
    :return:
    """
    width, height = int(360 / 0.01), int(180 / 0.01)
    burndata = np.zeros((height, width))
    for index, row in firepoint.iterrows():
        Lat, Lon, FireGrade, FireReliability = row['Latitude'], row['Longitude'], row['FireGrade'], row[
            'FireReliability']
        row, col = int((height / 2) - (Lat / 0.01 - 1) - 1), int((width / 2) + (Lon / 0.01 - 1) - 1)
        burndata[row, col] += 1
    burndata = np.where(burndata != 0, 0.85, 0) + burndata * 0.05
    burndata[burndata > 1] = 1
    width, height = int(360 / 0.05), int(180 / 0.05)
    rf = int(0.05 / 0.01)
    resample_burndata = burndata.reshape((height, rf, width, rf)).mean(axis=(1, 3))
    return resample_burndata

def Convolution(burndata):
    # 锐化滤波器
    sharpen_kernel = [[-1, -1, -1],
                      [-1, 8, -1],
                      [-1, -1, -1]]
    # 进行边缘锐化处理
    sharpened_data = convolve2d(burndata, sharpen_kernel, mode='same', boundary='fill', fillvalue=0)
    # 提取边缘地区
    edge_data = np.where(sharpened_data < 0, -sharpened_data / 8, 0)
    area_data = 0.2 * edge_data + 0.8 * burndata
    return area_data

def burnarea(burndata, ndvidata):
    ndvidata[ndvidata < 0] = np.nan
    ndvidata = ndvidata / 10000
    NDVIv = np.nanmax(ndvidata)
    NDVIs = np.nanmin(ndvidata)
    C = (ndvidata - NDVIs) / (NDVIv - NDVIs)
    return burndata * C


def main(date,firedata):
    firepoint, ndvidata = dataselect(date,firedata)
    burndata = Convolution(calburndata(firepoint))
    burnedarea = burndata.astype(np.float32)

