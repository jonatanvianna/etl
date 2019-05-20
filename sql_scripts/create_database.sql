-- On container build it creates the database if it doesn't exists.

CREATE EXTENSION IF NOT EXISTS dblink;
--
DO
$do$
BEGIN
   IF EXISTS (SELECT FROM pg_database WHERE datname = '4all') THEN
      RAISE NOTICE 'Database already exists';  -- optional
   ELSE
      PERFORM dblink_exec('dbname=' || current_database()  -- current db
                        , 'CREATE DATABASE 4all');
   END IF;
END
$do$;
