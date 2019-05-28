#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import csv
import logging
import os
import re
from pathlib import Path

LOG_PATH = "/app/logs/"
LOG_FILENAME = "transform.log"

logging.basicConfig(
    filename=LOG_PATH + LOG_FILENAME,
    format="[%(asctime)s] [%(levelname)s] [%(message)s]",
)
logger = logging.getLogger()
logger.setLevel("INFO")


COORDINATES = r'(\d+.?\d+.?\d+.?[S|N|W|E])\s*'
DECIMAL = r'(-?\d+\.?\d+)'
CAPTURE_LONGITUDE = re.compile(rf'(\s*Longitude:)\s*{COORDINATES}{DECIMAL}')
CAPTURE_LATITUDE = re.compile(rf'(\s*Latitude:\s*){COORDINATES}{DECIMAL}')
CAPTURE_DISTANCE = re.compile(rf'(\s*Distance:\s*){DECIMAL}')
CAPTURE_BEARING = re.compile(rf'(\s*Bearing:\s*){DECIMAL}')
NORMALIZED_DATA_PATH = "/app/normalized_data"
NORMALIZED_DATA_FILE = "data.csv"


def get_data_files(path_directory):
    """Gets all files from a directory

    :returns A list containing data files names
    """
    file_path = Path(path_directory)
    if file_path.exists():
        files = os.listdir(path_directory)
        message = f"Files found {' '.join(f for f in files)}"
        if __name__ != '__main__':
            print(message)

        return files
    else:
        message = f"Directory not found '{path_directory}'"
        if __name__ != '__main__':
            print(message)
        logger.error(message)
        os.sys.exit(1)


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
                try:
                    for line in file:
                        line_list.append(line.replace('\n', ''))
                        count -= 1
                        if not count:
                            raw_points_list.append(line_list)
                            line_list = []
                            count = line_range
                except UnicodeDecodeError as exc:
                    logger.error(f"Error reading file \"{file.name}\" file is a binary: {exc}")
                    continue
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

        if '-' not in points:
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


def write_points_to_csv(deduplicated_points_list, path_to_csv=None):
    """Saves CSV files from a normalized list of dict containing coordinates"""
    if not path_to_csv:
        path_to_csv = f"{NORMALIZED_DATA_PATH}/{NORMALIZED_DATA_FILE}"
    try:
        with open(path_to_csv, "w") as csv_file:
            fieldnames = ['latitude', 'longitude', 'distance_km', 'bearing_degrees']

            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()

            for line in deduplicated_points_list:
                writer.writerow({'latitude': line.get('latitude'),
                                 'longitude': line.get('longitude'),
                                 'distance_km': line.get('distance_km'),
                                 'bearing_degrees': line.get('bearing_degrees')})
    except FileNotFoundError as exc:
        if __name__ != '__main__':
            print(exc)
        logger.critical(exc)

    message = f"CSV `{NORMALIZED_DATA_FILE}` file saved at `{NORMALIZED_DATA_PATH}`"
    if __name__ != '__main__':
        print(message)
    logger.info(message)


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
        default="."
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
        if data_files:
            raw_points_list = wrangle_points_to_list(data_files, args.coordinate_block)
        else:
            logger.critical(f"File path has no files: {args.file_path}")

    if args.file_coord:
        check_path(args.file_coord)
        raw_points_list = wrangle_points_to_list([args.file_coord], args.coordinate_block)

    converted_points_list = convert_data_coordinates(raw_points_list)
    deduplicated_points_list = remove_duplicates(converted_points_list)
    write_points_to_csv(deduplicated_points_list)


if __name__ == "__main__":
    main()

# python transform/transform_raw_to_csv.py \
#     --files-path=data_from_source \
#     --csv-write-path=normalized_data \
#     --coordinate-block=3 \
#     --verbose --output
