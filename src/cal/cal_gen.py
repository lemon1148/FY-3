import numpy as np
import pandas as pd
def cal_gen(IGBPDATA, TC):
    """
           将IGBP分类进行再分类
           TC数据采用2020年数据，IGBP分类数据年更新
           :param IGBPDATA:
           :param TC:
           :return:
           """
    h, w = IGBPDATA.shape
    temp = np.zeros(shape=(h, w), dtype=np.float32)

    # 对IGBP第一类细分
    IGBP1 = np.where((IGBPDATA == 1), 1, 0)
    temp[:round((90 - 50) * h / 180), :] = 5
    gen15 = temp * IGBP1
    temp = np.where((temp == 5), 0, 6)
    gen16 = temp * IGBP1
    del IGBP1

    # 对IGBP第二类细分
    IGBP2 = np.where((IGBPDATA == 2), 1, 0)
    temp = 0 * temp
    temp[round((90 - 23.5) * h / 180):round((90 + 23.5) * h / 180), :] = 3
    gen23 = temp * IGBP2
    temp = np.where((temp == 3), 0, 4)
    gen24 = temp * IGBP2
    del IGBP2

    # 对IGBP第三类细分
    IGBP3 = np.where((IGBPDATA == 3), 1, 0)
    temp = 0 * temp
    temp[:round((90 - 50) * h / 180), :] = 5
    gen35 = temp * IGBP3
    temp = np.where((temp == 5), 0, 4)
    gen34 = temp * IGBP3
    del IGBP3

    # 对IGBP第四类细分
    IGBP4 = np.where((IGBPDATA == 4), 1, 0)
    gen44 = 4 * IGBP4
    del IGBP4

    # 对IGBP第五类细分
    IGBP5 = np.where((IGBPDATA == 5), 1, 0)
    temp = 0 * temp
    temp[:round((90 - 50) * h / 180), :] = 5
    gen55 = temp * IGBP5
    temp = 0 * temp
    temp[round((90 - 23.5) * h / 180):round((90 + 23.5) * h / 180), :] = 3
    gen53 = temp * IGBP5
    temp = 0 * temp
    temp[round((90 - 50) * h / 180):round((90 - 23.5) * h / 180), :] = temp[round((90 + 23.5) * h / 180):, :] = 4
    gen54 = temp * IGBP5
    del IGBP5

    # 对IGBP第六七八类合并
    IGBP6 = np.where((IGBPDATA == 6) | (IGBPDATA == 7) | (IGBPDATA == 8), 1, 0)
    gen62 = 2 * IGBP6
    del IGBP6

    # 对IGBP第九 十 十一 十四 十六类合并
    IGBP9 = np.where((IGBPDATA == 9) | (IGBPDATA == 10) | (IGBPDATA == 11) | (IGBPDATA == 14) | (IGBPDATA == 16), 1,
                     0)
    gen91 = 1 * IGBP9
    del IGBP9
    # 对IGBP第十二类合并
    IGBP12 = np.where((IGBPDATA == 12), 1, 0)
    gen129 = 9 * IGBP12
    del IGBP12

    # 对IGBP第十三类分类
    IGBP13 = np.where((IGBPDATA == 13), 1, 0)

    tc1 = np.where((TC < 0.4), 1, 0)
    tc2 = np.where((TC > 0.4) & (TC < 0.6), 1, 0)
    tc3 = np.where((TC > 0.6), 1, 0)
    gen1310 = 10 * IGBP13 * tc1
    gen132 = 2 * IGBP13 * tc2

    temp1 = 0 * temp
    temp1[:round((90 - 50) * h / 180), :] = 1
    gen135 = temp1 * IGBP13 * tc3 * 5
    temp2 = 0 * temp
    temp2[round((90 - 30) * h / 180):round((90 + 30) * h / 180), :] = 1
    gen133 = temp2 * IGBP13 * tc3 * 3
    temp[:, :] = 1
    temp3 = temp - temp1 - temp2
    gen134 = temp3 * IGBP13 * tc3 * 4
    del IGBP13
    gen = gen15 + gen16 + gen23 + gen24 + gen34 + gen35 + gen44 + gen53 + gen54 + gen55 + gen62 + gen91 + gen129 + gen133 + gen134 + gen135 + gen132 + gen1310
    return gen