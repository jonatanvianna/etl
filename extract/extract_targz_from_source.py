#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import logging
import tarfile
import os

from pathlib import Path

import requests
from requests import exceptions as  requests_exceptions

LOG_PATH = "/app/logs/"
LOG_FILENAME = "extract.log"

logging.basicConfig(
    filename=LOG_PATH + LOG_FILENAME,
    format="[%(asctime)s] [%(levelname)s] [%(message)s]",
)
logger = logging.getLogger()
logger.setLevel("INFO")


def extract_from_source(url, destination, extract):
    try:
        response = requests.get(url, timeout=10)
    except requests_exceptions.ConnectTimeout as exc:
        logger.critical(exc)
    except requests_exceptions.ConnectionError as exc:
        logger.critical(exc)
    except requests_exceptions.MissingSchema as exc:
        logger.critical(exc)
    except requests_exceptions.InvalidSchema as exc:
        logger.critical(exc)
    else:
        if response.status_code == 200:
            try:
                file_name = response.url.rsplit("/", 1)[1]
                logger.debug(f"File name extracted from response.url {file_name}")
                open(f"{destination}/{file_name}", 'wb').write(response.content)
                message = f"File downloaded from {url} to {destination}/{file_name}."
                logger.debug(message)
                if __name__ != "__main__":
                    print(message)
                if extract:
                    tar_file = tarfile.open(f"{destination}/{file_name}", "r:gz")
                    tar_file.extractall(path=destination)
                    message = f"Files extracted at {destination} directory."
                    logger.debug(message)
                    os.remove(f"{destination}/{file_name}")
                    if __name__ != "__main__":
                        print(message)
            except Exception as exc:
                message = f"Can't save {url} at {destination}: {exc}"
                if __name__ != "__main__":
                    print(message)
                logger.critical(message)
        else:
            message = f"Couldn't get {url}, status_code={response.status_code}"
            if __name__ != "__main__":
                print(message)
            logger.info(message)


def main():
    import argparse

    parser = argparse.ArgumentParser(
        prog="TarGz file Extractor",
        description="Extracts tar.gz files from data source URL",
        add_help=True,
    )
    parser.add_argument(
        "-u",
        "--url",
        dest="url",
        help="A URL from a tar.gz file.",
        required=True
    )
    parser.add_argument(
        "-d",
        "--destination-path",
        dest="destination_path",
        help="A path where to save file from sources.",
        default="."
    )
    parser.add_argument(
        "-e",
        "--extract",
        help="If the content must be extracted from tar.gz file.",
        action="store_true"
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

    logger.info(">>> Starting TarGz file Extractor.")
    args = parser.parse_args()

    if args.output:
        logger.debug("Showing logs on terminal.")
        root_logger = logging.getLogger()
        console_handler = logging.StreamHandler(os.sys.stdout)
        root_logger.addHandler(console_handler)

    if args.verbose:
        logger.info("Setting log level to DEBUG")
        logger.setLevel("DEBUG")

    extract_from_source(args.url, args.destination_path, args.extract)


if __name__ == "__main__":
    main()

# python extract/extract_targz_from_source.py --url=https://s3.amazonaws.com/dev.etl.python/datasets/data_points.tar.gz --destination=data_from_source --extract --verbose --output
