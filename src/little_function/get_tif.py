import numpy as np
import rasterio


def get_tif(file_paths):
    if type(file_paths)==str:
        try:
            with rasterio.open(file_paths) as tif_file:
                data = np.array(tif_file.read(1))
                return data
        except FileNotFoundError as e:
            print(f"Error: File not found - {str(e)}")
        except Exception as e:
            print(f"Error: {str(e)}")
    elif type(file_paths)==list:
        try:
            data_list = []
            for file_path in file_paths:
                with rasterio.open(file_path) as tif_file:
                    data = np.array(tif_file.read(1))
                    data_list.append(data)
            if len(data_list)==1:
                return np.array(data_list[0])
            else:
                return np.array(data_list)
        except FileNotFoundError as e:
            print(f"Error: File not found - {str(e)}")
        except Exception as e:
            print(f"Error: {str(e)}")
    else:
        print('格式错误')

    return None