import datetime
import os
import re
def find_nearest_files(folder_path, target_time, i):
    closest_files = []
    max_time_differences = [datetime.timedelta.max] * i

    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            # 使用正则表达式匹配文件名中的所有时间信息
            matches = re.findall(r"(\d{4}\d{2}\d{2})", file_name)  # 假设时间信息的格式为8位数字（YYYYMMDD）

            for match in matches:
                try:
                    file_time = datetime.datetime.strptime(match, "%Y%m%d")
                    time_difference = target_time - file_time

                    # 找到比当前最大时间差更小的时间差，将其插入到正确的位置
                    for j in range(i):
                        if time_difference.total_seconds() > 0 and time_difference < max_time_differences[j]:
                            max_time_differences.insert(j, time_difference)
                            closest_files.insert(j, os.path.join(root, file_name))
                            break
                except ValueError:
                    pass

    return closest_files[:i]