# !/usr/bin/env python3
# -*- encoding: utf-8 -*-

import logging
import os
from pathlib import Path

import dataset

from decouple import config

from geopy.distance import geodesic

from googlemaps import Client as GoogleMapsClient
from googlemaps.exceptions import ApiError

import pandas as pd

from sqlalchemy.exc import IntegrityError

LOG_PATH = "/app/logs/"
LOG_FILENAME = "transform.log"

logging.basicConfig(
    filename=LOG_PATH + LOG_FILENAME,
    format="[%(asctime)s] [%(levelname)s] [%(message)s]",
)
logger = logging.getLogger()
logger.setLevel("INFO")


class Converter:
    def __init__(self, api_key):
        self.api_key = api_key
        self.maps = GoogleMapsClient(key=api_key)
        logger.debug("Instantiating Converter")

    @staticmethod
    def is_address_valid(address):
        """
        Validates if an Address has complete information, if all address fields
        are filled with data.

        :param address: json containing all address components
        :return: bool
        """

        address_components = [
            "country",
            "state",
            "city",
            "neighborhood",
            "street_number",
            "street_name",
            "postal_code",
            "latitude",
            "longitude",
        ]
        address_keys = [*address.keys()]
        address_keys.sort()
        address_components.sort()
        if address_keys == address_components:
            return True
        return False

    @staticmethod
    def get_address_from_address_components(address_components):
        """
        Extracts data from address components returned from a query in googlemaps reverse_geocode api

        :param address_components: a dict with address components
        :return: a dict with transformed address
        """
        address = {}

        for component in address_components:
            component_types = component.get("types", "")

            if "country" in component_types:
                address.update({"country": component.get("long_name")})

            if "administrative_area_level_1" in component_types:
                address.update({"state": component.get("short_name")})

            if "administrative_area_level_2" in component_types:
                address.update({"city": component.get("long_name")})

            if "sublocality_level_1" in component_types:
                address.update({"neighborhood": component.get("long_name")})

            if "street_number" in component_types:
                address.update({"street_number": component.get("long_name")})

            if "route" in component_types:
                address.update({"street_name": component.get("long_name")})

            if "postal_code" in component_types:
                address.update({"postal_code": component.get("long_name")})

        if address:
            return address

    @staticmethod
    def get_coordinates_from_csv_file(file_path, csv_columns=None):
        """
        Read geographical coordinates from CSV file.
        If no specific columns are passed, id reads all columns from csv and
        the CSV file must have the following format:
        +------------+-----------+
        | latitude,  | longitude |  <- headers
        | -30.896756,| 51.987642 |  <- coordinates


        :param file_path: str
        :param csv_columns: list containing the header columns
        :return:
        """
        csv_dataset = pd.read_csv(file_path, usecols=csv_columns)
        return csv_dataset

    def get_address_from_coordinates(self, latitude, longitude):
        """Converts a latitude, longitude address coordinate in a valid address

        :param latitude: float
        :param longitude: float
        :return: dict
        """
        try:
            return self.maps.reverse_geocode(
                (latitude, longitude),
                result_type="street_address",
                location_type="ROOFTOP",
            )
        except ApiError as e:
            logger.critical(e.message)
            os.sys.exit(1)

    @staticmethod
    def save_to_database(coordinate, address):

        db_user = config("POSTGRES_USER")
        db_name = config("POSTGRES_DB")
        db_password = config("POSTGRES_PASSWORD")
        db_host = config("POSTGRES_HOST")
        string_connection = (
            f"postgresql://{db_user}:{db_password}@{db_host}:5432/{db_name}"
        )
        db = dataset.connect(string_connection)
        coordinate_table = db["coordinate_points"]
        addresses_table = db["addresses"]

        try:
            coordinate_table.insert(coordinate)
            addresses_table.insert(address)
            message = f"Address saved to database: {address}"
            if __name__ != '__main__':
                print(message)
            logger.info(message)
        except IntegrityError as exc:
            message = str(exc.orig).replace("\n", " ")
            if __name__ != '__main__':
                print(message)
            logger.critical(message)
        except Exception as exc:
            if __name__ != '__main__':
                print(exc)
            logger.critical(exc)

    # def get_destination(self, coordinate):
    #     # destination(point, bearing, distance=None):
    #     # distance = VincentyDistance(km=)
    #     # point = distance.destination(Point(coordinate["latitude"], coordinate["longitude"]), )
    #     # result = self.get_address_from_coordinates(point.latitude, point.longitude)

    #     import pdb; pdb.set_trace()
    #     origin = Point(coordinate["latitude"], coordinate["longitude"])
    #     geo = geodesic()
    #     destination = geo.destination(origin, coordinate["bearing_degrees"], coordinate["distance_km"])
    #     result = self.get_address_from_coordinates(destination.latitude, destination.longitude)

    def save_dataset_coordinates_to_database(self, dataset_coordinates):
        for (number, coordinate) in dataset_coordinates.iterrows():
            result = self.get_address_from_coordinates(
                coordinate["latitude"], coordinate["longitude"]
            )
            if result:
                address_components = result[0].get("address_components", "")
                if address_components:
                    complete_address = self.get_address_from_address_components(
                        address_components
                    )
                    if complete_address:
                        complete_address.update(
                            {
                                "latitude": coordinate["latitude"],
                                "longitude": coordinate["longitude"],
                            }
                        )
                        if self.is_address_valid(complete_address):
                            coordinate = {
                                "latitude": coordinate["latitude"],
                                "longitude": coordinate["longitude"],
                                "distance_km": coordinate["distance_km"],
                                "bearing_degrees": coordinate["bearing_degrees"],
                            }

                            addresses = {
                                "street_number": complete_address.get("street_number"),
                                "street_name": complete_address.get("street_name"),
                                "neighborhood": complete_address.get("neighborhood"),
                                "city": complete_address.get("city"),
                                "state": complete_address.get("state"),
                                "country": complete_address.get("country"),
                                "postal_code": complete_address.get("postal_code"),
                                "latitude": complete_address.get("latitude"),
                                "longitude": complete_address.get("longitude"),
                            }
                            # self.get_destination(coordinate)
                            self.save_to_database(coordinate, addresses)
            else:
                message = f"Address couldn't be saved to database. Data returned from reverse_geocode API: {result}"
                if __name__ != '__main__':
                    print(message)
                logger.warning(message)


def main():
    import argparse

    parser = argparse.ArgumentParser(
        prog="Geographical Coordinate to DataBase",
        description="Converts and saves geographical coordinates from a CSV file to Database.",
        add_help=True,
    )
    parser.add_argument(
        "-p",
        "--path-to-csv",
        dest="csv_file_path",
        help="Path to csv file containing geographical coordinates",
        required=True,
    )
    parser.add_argument(
        "-v", "--verbose", help="Activates debug log level.", action="store_true"
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Defines if logging should output on terminal.",
        action="store_true",
    )
    parser.add_argument(
        "-k",
        "--google-maps-key",
        dest="api_key",
        help="API key to use googlemaps",
        required=True,
    )
    # group = parser.add_mutually_exclusive_group()
    # group.add_argument(
    #     "-i",
    #     "--csv-column-indexes",
    #     dest="csv_column_indexes",
    #     help="Which CSV columns contain latitude and longitude"
    #     " e.g: `--columns-to-read=latitude_coordinate, longitude_coordinate`"
    #     " or  `--columns-to-read=1,3`",
    # )
    # group.add_argument(
    #     "-n",
    #     "--csv-column-names",
    #     dest="csv_column_names",
    #     help="Which CSV columns contain latitude and longitude"
    #     " e.g: `--columns-to-read=latitude_coordinate, longitude_coordinate`"
    #     " or  `--columns-to-read=1,3`",
    # )

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

    logger.info("Checking CSV File.")
    if args.csv_file_path:
        check_path = Path(args.csv_file_path)
        if not check_path.exists():
            message = "Path to csv not found."
            logger.critical(message)
            os.sys.exit(1)

    test_client = GoogleMapsClient(args.api_key)

    # if args.csv_column_names:
    #     try:
    #         logger.debug(f"Trying column names parsing {args.csv_column_names}")
    #         columns = list(tuple(args.csv_column_names.split(",")))
    #     except Exception:
    #         message = f"Error parsing columns: {args.csv_column_names}"
    #         logger.critical(message)
    #         os.sys.exit(1)
    #
    # if args.csv_column_indexes:
    #     try:
    #         logger.debug(f"Trying column indexes parsing {args.csv_column_indexes}")
    #         columns = tuple(args.csv_column_indexes.split(","))
    #         columns = list(map(int, columns))
    #     except Exception:
    #         message = f"Error parsing column indexes: {args.csv_column_indexes}"
    #         logger.critical(message)
    #         os.sys.exit(1)

    logger.info("Checking API Key.")
    try:
        test_client.reverse_geocode((30.1084987, -51.3172284))  # Porto Alegre, RS
    except ApiError as e:
        logger.critical(e.message)
        os.sys.exit(1)
    else:
        logger.debug(f"API Key OK {args.api_key}")

    converter = Converter(api_key=args.api_key)
    dataset_from_csv = converter.get_coordinates_from_csv_file(args.csv_file_path)
    converter.save_dataset_coordinates_to_database(dataset_from_csv)


if __name__ == "__main__":
    main()
    # AIzaSyCZ1RwYvtM-fbjWp7ZQnMggAVJVS9LJMFA
    # python transform/transform_csv_to_database.py --google-maps-key AIzaSyCZ1RwYvtM-fbjWp7ZQnMggAVJVS9LJMFA --path-to-csv=normalized_data/data.csv --verbose --output
