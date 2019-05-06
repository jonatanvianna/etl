

import pyarrow as pr
import pandas as pa
import numpy as np
import re
import pdb



# data["redirect_to"] = re.sub(, "'.." + __match_groups.pop(), data["redirect_to"])


# TODO make a function to regex match


def convert_to_list(files, range_of_line=1):
    master_list = []
    for read_file in files:
        line_list = []
        with open(read_file, 'r') as file:
            if file.readable():
                count = range_of_line
                for line in file:
                    line_list.append(line.replace('\n', ''))
                    count -= 1
                    if not count:
                        master_list.append(line_list)
                        line_list = []
                        count = range_of_line
    return master_list


def convert_to_csv(master_list):
    COORDINATES = r'(\d+.?\d+.?\d+.?[S|N|W|E])\s*'
    DECIMAL = r'(-?\d+\.\d+)'
    CAPTURE_LONGITUDE = re.compile(rf'(\s*Longitude:)\s*{COORDINATES}{DECIMAL}')
    CAPTURE_LATITUDE = re.compile(rf'(\s*Latitude:\s*){COORDINATES}{DECIMAL}')
    CAPTURE_DISTANCE = re.compile(rf'(\s*Distance:\s*){DECIMAL}')
    CAPTURE_BEARING = re.compile(rf'(\s*Bearing:\s*){DECIMAL}')
    for n, line_list in enumerate(master_list):
        for i in line_list:
            latitude = re.search(CAPTURE_LATITUDE, i)
            longitude = re.search(CAPTURE_LONGITUDE, i)
            distance = re.search(CAPTURE_DISTANCE, i)
            bearing = re.search(CAPTURE_BEARING, i)
            # pdb.set_trace()
            if latitude:
                latitude_coordinate = latitude.group(2)
                latitude_degrees = latitude.group(3)

            elif longitude:
                longitude_coordinate = longitude.group(2)
                longitude_degrees = longitude.group(3)

            if distance:
                distance_km = distance.group(2)

            if bearing:
                bearing_degrees = bearing.group(2)

        print(f"{latitude_coordinate}, {latitude_degrees}, {longitude_coordinate}, {longitude_degrees}, {distance_km}, {bearing_degrees}")

        # assert len(line_list) == 3, f"Length of line_list is 3, but {len(line_list)}"
        # assert len(master_list) == 998, f"Length of master_list is 3, but {len(master_list)}"



ml = convert_to_list(['data_points_20180101.txt', 'data_points_20180102.txt', 'data_points_20180102.txt'], 3)

convert_to_csv(ml)
