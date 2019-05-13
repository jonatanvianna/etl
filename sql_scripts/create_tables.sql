CREATE TABLE IF NOT EXISTS coordinate_points (
    id SERIAL PRIMARY KEY ,
    latitude_coordinate VARCHAR(20) NOT NULL,
    latitude_degree FLOAT NOT NULL,
    longitude_coordinate varchar(20) NOT NULL,
    longitude_degree FLOAT NOT NULL,
    distance_km FLOAT NOT NULL,
    bearing_degrees FLOAT NOT NULL
);
