
### Data fluxogram 

converte coordenadas de blocos de 3 linhas  para uma lista de listas
converte cada lista para um dicionario filrando por regex
se te algum dado faltando ifgnora a linha

- Reads raw data from txt writes csv deduplicated complete coordinates
- Reads coordinates from csv
- Make a request to get address
- If matches saves in database coordinates relating `coordinates` and `address` tables


-----------
# ***FUTURE***
### get bearing and distance to convert to destination  

-----------


* ***TODO*** improve regex to match integer and decimal number

* ***TODO*** data["redirect_to"] = re.sub(, "'.." + __match_groups.pop(), data["redirect_to"])

* ***TODO*** make a function to regex match

* ***TODO*** remove duplicated line using set

* ***TODO*** Elastic search?

* ***TODO*** Postgres IS NEEEEEDEDD to create Indexes to do a fast search

* ***TODO*** Define a Datawarehouse

* ***TODO*** Define a external volume for huge files of csv data

* ***TODO*** string connection in an .ENV file

* ***TODO*** Script for creating the database in docker-compose

* ***TODO*** encontrar api para calcular o destino


#### Project Requirements
- Docker
- Docker Compose

DATABASE
To change database credentials edit `.env` file and set the `POSTGRES_USER` and `POSTGRES_PASSWORD`.

#### Project Architecture
Database using Postgresql
Codebase in Python 3.6
jupyter notebook to execute project phases

## Extracting
## Transforming
## Loading


{'latitude_coordinate': '30°02′59″S', 'latitude_degree': '-30.04982864', 'longitude_coordinate': '51°12′05″W', 'longitude_degree': '-51.20150245', 'distance_km': '2.2959', 'bearing_degrees': '137.352'}
{'latitude_coordinate': '30°02′59″S', 'latitude_degree': '-30.04982864', 'longitude_coordinate': '51°12′05″W', 'longitude_degree': '-51.20150245', 'distance_km': '2.2959', 'bearing_degrees': '137.352'}


use coordenates to get:
address 

Load:
Writes to db


The databases are 




