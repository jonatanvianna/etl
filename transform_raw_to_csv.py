


import logging
import os
from pathlib import Path

from googlemaps import Client as GoogleMapsClient
from googlemaps.exceptions import ApiError

import pandas as pd


LOG_PATH = "/app/logs/"
LOG_FILENAME = "extract.log"

logging.basicConfig(
    filename=LOG_PATH + LOG_FILENAME,
    format="[%(asctime)s] [%(levelname)s] [%(message)s]",
)
logger = logging.getLogger()
logger.setLevel("INFO")



import pyarrow.parquet as pr
import pandas as pa
import numpy as np
import pdb
import csv
import dataset
from decouple import config
import os
import re
from  unipath import Path


COORDINATES = r'(\d+.?\d+.?\d+.?[S|N|W|E])\s*'
DECIMAL = r'(-?\d+\.?\d+)'
CAPTURE_LONGITUDE = re.compile(rf'(\s*Longitude:)\s*{COORDINATES}{DECIMAL}')
CAPTURE_LATITUDE = re.compile(rf'(\s*Latitude:\s*){COORDINATES}{DECIMAL}')
CAPTURE_DISTANCE = re.compile(rf'(\s*Distance:\s*){DECIMAL}')
CAPTURE_BEARING = re.compile(rf'(\s*Bearing:\s*){DECIMAL}')


def get_data_files(path_directory):
    """Gets all files from a directory

    :returns A list containing data files names
    """
    return os.listdir(path_directory)


def wrangle_points_to_list(files, line_range=3):
    """
    Iterates over a raw file containing coordinates in blocks of 3 lines

    :param files:
    :param line_range:
    :returns A list containing raw lines of coordinates
    """
    raw_points_list = []
    for read_file in files:
        line_list = []
        with open(read_file, 'r') as file:
            if file.readable():
                count = line_range
                for line in file:
                    line_list.append(line.replace('\n', ''))
                    count -= 1
                    if not count:
                        raw_points_list.append(line_list)
                        line_list = []
                        count = line_range
    return raw_points_list


def convert_data_coordinates(raw_points_list):
    """Converts raw coordinates into a list of converted data.

    latitude - float()
    longitude - float()
    distance_km - float()
    bearing_degrees - float()

    :returns A list of dicts
    """

    converted_points_list = []

    for n, line_list in enumerate(raw_points_list):
        # Initializing variables, if no data is found a dash is placed
        latitude = '-'
        longitude = '-'
        distance_km = '-'
        bearing_degrees = '-'

        for line in line_list:
            latitude_capture = re.search(CAPTURE_LATITUDE, line)
            longitude_capture = re.search(CAPTURE_LONGITUDE, line)
            distance_capture = re.search(CAPTURE_DISTANCE, line)
            bearing_capture = re.search(CAPTURE_BEARING, line)

            if latitude_capture:
                latitude = latitude_capture.group(3)

            elif longitude_capture:
                longitude = longitude_capture.group(3)

            if distance_capture:
                distance_km = distance_capture.group(2)

            if bearing_capture:
                bearing_degrees = bearing_capture.group(2)

        points = [latitude, longitude, distance_km, bearing_degrees]

        if not '-' in points:
            try:
                converted_points_list.append({
                    'latitude': float(latitude),
                    'longitude': float(longitude),
                    'distance_km': float(distance_km),
                    'bearing_degrees': float(bearing_degrees)}
                )
            except ValueError as e:
                print(e)
                os.sys.exit(1)
    pdb.set_trace()
    return converted_points_list


def remove_duplicates(converted_points_list):
    """Removes duplicated coordinates

    :returns A list containing deduplicated dicts of coordinates
    """
    seen = set()
    deduplicated_points = []
    for line in converted_points_list:
        line_tuple = tuple(line.items())
        if line_tuple not in seen:
            seen.add(line_tuple)
            deduplicated_points.append(line)
    return deduplicated_points


def write_points_to_csv(deduplicated_points_list, path='normalized_data/'):
    """Saves CSV files from a normalized list of dict containing coordinates"""

    with open(f'{path}data.csv', "w") as csv_file:
        fieldnames = ['latitude',
                     'longitude',
                     'distance_km',
                     'bearing_degrees']

        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for line in deduplicated_points_list:
            writer.writerow({'latitude': line.get('latitude'),
                             'longitude': line.get('longitude'),
                             'distance_km': line.get('distance_km'),
                             'bearing_degrees': line.get('bearing_degrees')})





def main():
    import argparse

    parser = argparse.ArgumentParser(
        prog="Raw Geographical Coordinates to CSV",
        description="Converts and saves geographical coordinates from a Raw file to CSV.",
        add_help=True,
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-p",
        "--files-path",
        dest="files_path",
        help="A Path containing files with geographical coordinates.",
    )
    group.add_argument(
        "-f",
        "--file",
        dest="file_coord",
        help="File containing geographical coordinates."
    )
    parser.add_argument(
        "-w",
        "--csv-write-path",
        dest="write_path",
        help="A path to where to write the csv file output."
    )
    parser.add_argument(
        "-b",
        "--coordinate-block",
        dest="coordinate_block",
        help="Block coordinate range. The raw file may have the"
             "coordinates divided in more than one line, so passing"
             "the range it can parse the coordinates properly",
        type=int
    )
    parser.add_argument(
        "-v",
        "--verbose",
        help="Activates debug log level.",
        action="store_true"
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Defines if logging should output on terminal.",
        action="store_true",
    )

    logger.info(">>> Starting the Coordinate Converter.")
    args = parser.parse_args()

    if args.output:
        logger.debug("Showing logs on terminal.")
        root_logger = logging.getLogger()
        console_handler = logging.StreamHandler(os.sys.stdout)
        root_logger.addHandler(console_handler)

    if args.verbose:
        logger.info("Setting log level to DEBUG")
        logger.setLevel("DEBUG")

    def check_path(path):
        path_obj = Path(path)
        logger.info("Checking File(s)")
        if not path_obj.exists():
            message = "Path not found."
            logger.critical(message)
            os.sys.exit(1)
    if not args.coordinate_block:
        args.coordinate_block = 1

    if args.files_path:
        files_path = args.files_path
        check_path(files_path)
        data_files = []
        for file in get_data_files(files_path):
            data_files.append(f"{files_path}/{file}")
        raw_points_list = wrangle_points_to_list(data_files, args.coordinate_block)

    if args.file_coord:
        check_path(args.file_coord)
        raw_points_list = wrangle_points_to_list([args.file_coord], args.coordinate_block)

    print(len(raw_points_list))
    converted_points_list = convert_data_coordinates(raw_points_list)
    print(len(converted_points_list))
    deduplicated_points_list = remove_duplicates(converted_points_list)
    print(len(deduplicated_points_list))
    write_points_to_csv(deduplicated_points_list)
    # print(f'Databases: {db.tables}')
    # coordinate_table = db['coordinate_points']
    from psycopg2 import OperationalError
    # from sqlalchemy.exc import OperationalError






if __name__ == "__main__":
    main()

# python transform_raw_to_csv.py --files-path=data --file=data/data_points_20180101.txt --coordinate-block=3 --verbose --output
# python transform_raw_to_csv.py -p=data -f=data/data_points_20180101.txt -w=normalized_data -b=3 -v -o
