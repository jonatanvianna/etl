

import pyarrow as pr
import pandas as pa
import numpy as np
import re

COORDINATES = r'(\d+.?\d+.?\d+.?[S|N|W|E])\s*'
DECIMAL = r'(-?\d+\.\d+)'
CAPTURE_LATITUDE = rf'(\s*Latitude:\s*){COORDINATES}{DECIMAL}'
CAPTURE_LONGITUDE = rf'(\s*Longitude:)\s*{COORDINATES}{DECIMAL}'
CAPTURE_DISTANCE = rf'(\s*Distance:\s*){DECIMAL}'
CAPTURE_BEARING = rf'(Bearing:\s*){DECIMAL}'

# data["redirect_to"] = re.sub(, "'.." + __match_groups.pop(), data["redirect_to"])


# TODO make a function to regex match
import pdb

def convert_to_list(files, range_of_line=1):

    master_list = []
    for read_file in files:
        line_list = []
        pdb.set_trace()
        with open(read_file, 'r') as file:
            if file.readable():
                count = range_of_line
                for line in file:
                    line_list.append(line.replace('\n', ''))
                    count -= 1
                    if not count:
                        if not len(line_list) == 3:
                            pdb.set_trace()
                        master_list.append(line_list)
                        line_list = []
                        count = range_of_line

        for n, line_list in enumerate(master_list):
            # for i in line_list:
            #     print(i.replace('\n', ''))
            print(n, line_list)
            assert len(line_list) == 3, f"Length of line_list is 3, but {len(line_list)}"
        # assert len(master_list) == 998, f"Length of master_list is 3, but {len(master_list)}"



convert_to_list(['data_points_20180101.txt', 'data_points_20180102.txt', 'data_points_20180102.txt'], 3)
