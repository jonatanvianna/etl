#%% Change working directory from the workspace root to the ipynb file location. Turn this addition off with the DataScience.changeDirOnImportExport setting
import os
try:
    os.chdir(os.path.join(os.getcwd(), 'notebooks'))
    print(os.getcwd())
except:
    pass
#%% [markdown]
Extract Phase.
Receives a raw file containing geographical coordinates and saves it in a csv file.
#%% [markdown]
# ### 1.Reads a certain directory that contains coordinates/points data files

#%%

from extract.extract_targz_from_source import extract_from_source

source = "https://s3.amazonaws.com/dev.etl.python/datasets/data_points.tar.gz"
destination_path = "/app/data_from_source"
extract = True

extract_from_source(source, destination_path, extract)



#%% [markdown]
# ### Converts

#%%





def wrangle_points_to_list(files, line_range=3):
    """Iterates over a raw file containing coordinates in blocks of 3 lines

    :returns A list containing raw lines of coordinates
    """
    raw_points_list = []

    for read_file in files:
        line_list = []
        with open('../data/' + read_file, 'r') as file:
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

raw_points_list = wrangle_points_to_list(data_files, 3)
print(len(raw_points_list))






#%%
import re

COORDINATES = r'(\d+.?\d+.?\d+.?[S|N|W|E])\s*'
DECIMAL = r'(-?\d+\.?\d+)'
CAPTURE_LONGITUDE = re.compile(rf'(\s*Longitude:)\s*{COORDINATES}{DECIMAL}')
CAPTURE_LATITUDE = re.compile(rf'(\s*Latitude:\s*){COORDINATES}{DECIMAL}')
CAPTURE_DISTANCE = re.compile(rf'(\s*Distance:\s*){DECIMAL}')
CAPTURE_BEARING = re.compile(rf'(\s*Bearing:\s*){DECIMAL}')


def convert_data_coordinates(raw_points_list):
    """Converts raw coordinates into a list of type converted data.

    latitude_coordinate - str()
    latitude_degree - float()
    longitude_coordinate - str()
    longitude_degree - float()
    distance_km - float()
    bearing_degrees - float()

    :returns A list of dicts
    """
    converted_points_list = []
    for n, line_list in enumerate(raw_points_list):
        # Initializing variables, if no data is found a dash is placed
        latitude_coordinate = '-'
        latitude_degree = '-'
        longitude_coordinate = '-'
        longitude_degree = '-'
        distance_km = '-'
        bearing_degrees = '-'

        for line in line_list:
            latitude = re.search(CAPTURE_LATITUDE, line)
            longitude = re.search(CAPTURE_LONGITUDE, line)
            distance = re.search(CAPTURE_DISTANCE, line)
            bearing = re.search(CAPTURE_BEARING, line)

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


        points = [latitude_coordinate, latitude_degree, longitude_coordinate,
                  longitude_degree, distance_km, bearing_degrees ]


        if not '-' in points:
            converted_points_list.append({'latitude_coordinate': latitude_coordinate,
                     'latitude_degree': float(latitude_degree),
                     'longitude_coordinate': longitude_coordinate,
                     'longitude_degree': float(longitude_degree),
                     'distance_km': float(distance_km),
                     'bearing_degrees': float(bearing_degrees)})

    return converted_points_list

converted_points_list = convert_data_coordinates(raw_points_list)

#%% [markdown]
# ### Remove duplicates

#%%
def remove_duplicates(converted_points_list):
    """Removes duplicated coordinates

    :returns A list containing deduplicated dicts of coordinates
    """
    seen = set()
    deduplicated_points = []
    print(f'Before deduplication: {len(converted_points_list)}')
    for line in converted_points_list:
        line_tuple = tuple(line.items())
        if line_tuple not in seen:
            seen.add(line_tuple)
            deduplicated_points.append(line)
    print(f'After deduplication: {len(deduplicated_points)}')
    return deduplicated_points

deduplicated_points_list = remove_duplicates(converted_points_list)

#%% [markdown]
# ### Write to csv file

#%%
import csv

def write_points_to_csv(deduplicated_points_list, path='../normalizated_data/'):
    """Saves CSV files from a normalizated list of dict containing coorddinates"""

    with open(f'{path}data.csv', "w") as csv_file:
        fieldnames = ['latitude_coordinate',
                     'latitude_degree',
                     'longitude_coordinate',
                     'longitude_degree',
                     'distance_km',
                     'bearing_degrees']

        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        for line in deduplicated_points_list:
            writer.writerow({'latitude_coordinate': line.get('latitude_coordinate'),
                             'latitude_degree': line.get('latitude_degree'),
                             'longitude_coordinate': line.get('longitude_coordinate'),
                             'longitude_degree': line.get('longitude_degree'),
                             'distance_km': line.get('distance_km'),
                             'bearing_degrees': line.get('bearing_degrees')})

write_points_to_csv(deduplicated_points_list)

#%% [markdown]
# ### Connect to database

#%%
import dataset
from  decouple import config

db_user = config('POSTGRES_USER')
db_name = config('POSTGRES_DB')
db_password = config('POSTGRES_PASSWORD')
db_host = config('POSTGRES_HOST')
string_connection = f'postgresql://{db_user}:{db_password}@{db_host}:5432/{db_name}'
db = dataset.connect(string_connection)

print(f'Databases: {db.tables}')

#%% [markdown]
# ### Save all coordinates to database

#%%
coordinate_table = db['coordinate_points']

for i in deduplicated_points_list:

    coordinate_table.insert({'latitude_coordinate': i.get('latitude_coordinate'),
                             'latitude_degree': i.get('latitude_degree'),
                             'longitude_coordinate': i.get('longitude_coordinate'),
                             'longitude_degree': i.get('longitude_degree'),
                             'distance_km': i.get('distance_km'),
                             'bearing_degrees': i.get('bearing_degrees')})



