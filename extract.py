import pyarrow.parquet as pr
import pandas as pa
import numpy as np
import pdb
from typing import Union, Any, List, Optional, cast
import re

COORDINATES = r'(\d+.?\d+.?\d+.?[S|N|W|E])\s*'
DECIMAL = r'(-?\d+\.?\d+)'
CAPTURE_LONGITUDE = re.compile(rf'(\s*Longitude:)\s*{COORDINATES}{DECIMAL}')
CAPTURE_LATITUDE = re.compile(rf'(\s*Latitude:\s*){COORDINATES}{DECIMAL}')
CAPTURE_DISTANCE = re.compile(rf'(\s*Distance:\s*){DECIMAL}')
CAPTURE_BEARING = re.compile(rf'(\s*Bearing:\s*){DECIMAL}')


# pr.write_to_dataset()

def convert_to_list(files: List[str], range_of_line: int = 1) -> List[List[str]]:
    master_list = []
    for read_file in files:
        line_list = []
        with open('../data/' + read_file, 'r') as file:
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


def convert_coordinate_list_to_csv(master_list: List[List[str]]) -> None:
    """Converts a file of coordinates into a csv file"""

    # with open('data.csv', 'w') as csv_file:

    for n, line_list in enumerate(master_list):
        # Initializing variables, if none is used a dash is placed
        latitude_coordinate = '-'
        latitude_degree = '-'
        longitude_coordinate = '-'
        longitude_degree = '-'
        distance_km = '-'
        bearing_degrees = '-'

        for i in line_list:
            latitude = re.search(CAPTURE_LATITUDE, i)
            longitude = re.search(CAPTURE_LONGITUDE, i)
            distance = re.search(CAPTURE_DISTANCE, i)
            bearing = re.search(CAPTURE_BEARING, i)

            # pdb.set_trace()
            if latitude:
                latitude_coordinate = latitude.group(2)
                latitude_degree = latitude.group(3)

            elif longitude:
                longitude_coordinate = longitude.group(2)
                longitude_degree = longitude.group(3)

            if distance:
                distance_km = distance.group(2)

            if bearing:
                bearing_degrees = bearing.group(2)

        print(f" {n} {latitude_coordinate}, {latitude_degree}, {longitude_coordinate}, {longitude_degree}, {distance_km}, {bearing_degrees}")

        # assert len(line_list) == 3, f"Length of line_list is 3, but {len(line_list)}"
        # assert len(master_list) == 998, f"Length of master_list is 3, but {len(master_list)}"
