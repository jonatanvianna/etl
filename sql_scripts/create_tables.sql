CREATE TABLE IF NOT EXISTS coordinate_points (
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    distance_km FLOAT NOT NULL,
    bearing_degrees FLOAT NOT NULL,
    CONSTRAINT coordinate_points_pkey PRIMARY KEY (latitude, longitude)
);

CREATE  TABLE  IF NOT EXISTS addresses
(
    street_number TEXT NOT NULL,
    street_name TEXT,
    neighborhood TEXT,
    city TEXT,
    state TEXT,
    country TEXT,
    postal_code TEXT,
    latitude FLOAT,
    longitude FLOAT,
    FOREIGN KEY (latitude, longitude) REFERENCES coordinate_points (latitude, longitude),
    UNIQUE (latitude, longitude)
);
