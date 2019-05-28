
### Data Flow

converte coordenadas de blocos de 3 linhas  para uma lista de listas
converte cada lista para um dicionario filrando por regex
se te algum dado faltando ignora a linha


- Reads raw data from txt writes csv deduplicated complete coordinates
- Reads coordinates from csv
- Make a request to get address
- If matches saves in database coordinates relating `coordinates` and `address` tables


-----------
# ***FUTURE***
### get bearing and distance to convert to destination
* ***TODO*** Elastic search?
* ***TODO*** Postgres IS NEEEEEDEDD to create Indexes to do a fast search
* ***TODO*** Define a external volume in DOCKER for huge files of csv data

-----------

#### Project Requirements
- Docker
- Docker Compose

#### Configuring
DATABASE
To change database credentials edit `.env` file and set the `POSTGRES_USER` and `POSTGRES_PASSWORD`.

#### Project Architecture
Database using Postgresql
Codebase in Python 3.6
Jupyter notebook to execute project phases

## Extracting

## Transforming
## Loading

