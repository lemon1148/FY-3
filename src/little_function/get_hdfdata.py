import h5py
import numpy as np


def get_hdfdata(file_path, data_path):
    """
    :param file_path:
    :param data_path:
    :return:
    """
    if type(file_path) == str:
        with h5py.File(file_path, 'r') as f1:
            data = np.array(f1[data_path])
            return data
    elif type(file_path) == list:
        if len(file_path) == 0:
            print('请输入数据地址')
        h, w = get_hdfdata(file_path[0], data_path).shape
        data = np.zeros(shape=(len(file_path), h, w), dtype=np.float32)
        for i in range(len(file_path)):
            data[i, :, :] = get_hdfdata(file_path[i], data_path)
        return data