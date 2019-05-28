



# Table of Contents
1. [Project Definition](#definition)
    1.1 [Data flow](#runnidataflowng)
2. [Project Requirements](#requirements)
    2.1. [Running](#running)

# Project Definition {#definition}

converte coordenadas de blocos de 3 linhas  para uma lista de listas
converte cada lista para um dicionario filrando por regex
se te algum dado faltando ignora a linha

#### Data Flow {#dataflow}

- Reads raw data from txt writes csv deduplicated complete coordinates
- Reads coordinates from csv
- Make a request to get address
- If matches saves in database coordinates relating `coordinates` and `address` tables

### § Project Requirements {#requirements}

- Docker
- Docker Compose
- Google Maps API Key

To install `docker` refer to [docker installation](https://docs.docker.com/install/).
To install `docker-compose` refer to [docker-compose installation](https://docs.docker.com/compose/install/).
To get an API Key for Google Maps API, refer to [google documentation](https://developers.google.com/maps/documentation/embed/get-api-key).

#### § Configuring before running {#running}

- Database
To change database credentials edit `.env` and change `POSTGRES_USER` and `POSTGRES_PASSWORD`.
- Google Maps API Key
To add and API Key edit `.env` file and set on `GOOGLE_MAPS_API_KEY` var.

#### § Building the project

To build and run the project, after docker and docker-compose being installed, open your terminal window and run:
```bash
$ git clone git@github.com:jonatanvianna/etl.git
$ cd etl/
$ docker-compose up --build
```

Those commands will build and run containers to UP the project.

#### § Stopping and Rebuilding the project

To stop the project, use `ctrl+c` or `docker-compose stop`.
If you want to clean the project up, use: `docker-compose down -v`. This command will remove container, volumes and networks only for this project.
And finally to rebuild use: `docker-compose up --build`.

## § Running the project

The Project has two ways of use.

- Jupyter Notebooks (for presentation proposes)
- CLI

#### § Jupyter notebooks
To access the jupyter notebooks go for the local address [http://0.0.0.0:8888](http://0.0.0.0:8888/notebooks/notebooks/application.ipynb).
The notebooks have some hardcoded parameters for presentation. When using **CLI** mode, many parameters can vary, such as source of data, destination fd data, API Key etc.
Open the [applictation notebook](http://0.0.0.0:8888/notebooks/notebooks/application.ipynb), run all the cells and see all the data flow.

**Important:** This Project Functional Instance using a Digital Ocean Droplet at this address [http://104.248.223.237:8888](http://104.248.223.237:8888/notebooks/notebooks/application.ipynb) (in case of problems when running the project locally).

#### § CLI

**Run all 3 in sequence and you will go through all the process**:

##### # Extracting

Extract using `extract_source.py`

```bash
$ python extract_source.py \
    --url=https://s3.amazonaws.com/dev.etl.python/datasets/data_points.tar.gz \
    --destination=data_from_source \
    --extract --verbose --output

Setting log level to DEBUG
Starting new HTTPS connection (1): s3.amazonaws.com:443
https://s3.amazonaws.com:443 "GET /dev.etl.python/datasets/data_points.tar.gz HTTP/1.1" 200 72281
File name extracted from response.url data_points.tar.gz
File downloaded from https://s3.amazonaws.com/dev.etl.python/datasets/data_points.tar.gz to data_from_source/data_points.tar.gz.
Files extracted at data_from_source directory.
```
##### # Transforming 

Transform using `transform_csv.py` and `transform_db.py`.

```bash
$ python transform_csv.py \
    --files-path=data_from_source \
    --csv-write-path=normalized_data \
    --coordinate-block=3 \
    --verbose --output

Setting log level to DEBUG
Checking File(s)
CSV `data.csv` file saved at `/app/normalized_data`
```

```bash
$ python transform_db.py \
    --google-maps-key <your_googlemaps_api_key_here> \
    --path-to-csv=normalized_data/data.csv \
    --verbose --output

Setting log level to DEBUG
Checking CSV File.
Checking API Key.
Starting new HTTPS connection (1): maps.googleapis.com:443
https://maps.googleapis.com:443 "GET /maps/api/geocode/json?latlng=30.108499%2C-51.317228&key=<your_googlemaps_api_key_here> HTTP/1.1" 200 423
API Key OK <your_googlemaps_api_key_here>
Instantiating Converter
Starting new HTTPS connection (1): maps.googleapis.com:443
https://maps.googleapis.com:443 "GET /maps/api/geocode/json?latlng=-30.049829%2C-51.201502&location_type=ROOFTOP&result_type=street_address&key=<your_googlemaps_api_key_here> HTTP/1.1" 200 620
.
.
.
.
```

##### # Loading

In the loading phase you can visualize the data using this jupyper notebook bellow.

http://0.0.0.0:8888/notebooks/notebooks/display_data.ipynb

##### CLI Documentation

All 3 cli's have a `--help` that have instructions on how to use.

```bash
$ python extract_source.py --help
usage: TarGz file Extractor [-h] -u URL [-d DESTINATION_PATH] [-e] [-v] [-o]

Extracts tar.gz files from data source URL

optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL     A URL from a tar.gz file.
  -d DESTINATION_PATH, --destination-path DESTINATION_PATH
                        A path where to save file from sources.
  -e, --extract         If the content must be extracted from tar.gz file.
  -v, --verbose         Activates debug log level.
  -o, --output          Defines if logging should output on terminal.
```

```bash
$ python transform_csv.py --help
usage: Raw Geographical Coordinates to CSV [-h]
                                           [-p FILES_PATH | -f FILE_COORD]
                                           [-w WRITE_PATH]
                                           [-b COORDINATE_BLOCK] [-v] [-o]

Converts and saves geographical coordinates from a Raw file to CSV.

optional arguments:
  -h, --help            show this help message and exit
  -p FILES_PATH, --files-path FILES_PATH
                        A Path containing files with geographical coordinates.
  -f FILE_COORD, --file FILE_COORD
                        File containing geographical coordinates.
  -w WRITE_PATH, --csv-write-path WRITE_PATH
                        A path to where to write the csv file output.
  -b COORDINATE_BLOCK, --coordinate-block COORDINATE_BLOCK
                        Block coordinate range. The raw file may have the
                        coordinates divided in more than one line, so
                        passingthe range it can parse the coordinates
                        properly.
  -v, --verbose         Activates debug log level.
  -o, --output          Defines if logging should output on terminal.
```

```bash
$ python transform_db.py --help
usage: Geographical Coordinate to DataBase [-h] -p CSV_FILE_PATH [-v] [-o] -k
                                           API_KEY

Converts and saves geographical coordinates from a CSV file to Database.

optional arguments:
  -h, --help            show this help message and exit
  -p CSV_FILE_PATH, --path-to-csv CSV_FILE_PATH
                        Path to csv file containing geographical coordinates
  -v, --verbose         Activates debug log level.
  -o, --output          Defines if logging should output on terminal.
  -k API_KEY, --google-maps-key API_KEY
                        API key to use googlemaps
```

#### § Project Architecture

Database using Postgresql
Codebase in Python 3.6
Docker and Docker Compose
Jupyter

##### § Main modules usend in project

pandas
dataset
jupyter
argparse
googlemaps
requests

##### § Extras

Digital Ocean Instance ([student cupom by student github pack](https://education.github.com/pack)).

-----------
# ***FUTURE***
### get bearing and distance to convert to destination
* ***TODO*** Elastic search?
* ***TODO*** Postgres IS NEEEEEDEDD to create Indexes to do a fast search
* ***TODO*** Define a external volume in DOCKER for huge files of csv data

-----------
