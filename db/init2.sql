CREATE EXTENSION IF NOT EXISTS dblink;

-- Create the database (no IF NOT EXISTS for databases in PostgreSQL)
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'crawler_db') THEN
        PERFORM dblink_exec('dbname=postgres', 'CREATE DATABASE crawler_db');
    END IF;
END $$;

-- Switch to the new database (PostgreSQL doesn't use `USE`, you need to connect manually)
\connect crawler_db2

-- Create tables
CREATE TABLE IF NOT EXISTS hash (
    id SERIAL PRIMARY KEY,
    hash VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS protocol (
    id SERIAL PRIMARY KEY, 
    protocol VARCHAR(10) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS large_content(
    id SERIAL PRIMARY KEY,
    header TEXT NOT NULL,
);

CREATE TABLE IF NOT EXISTS file (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    original_name TEXT NOT NULL,
    type_of_file VARCHAR(50) NOT NULL,
);

CREATE TABLE IF NOT EXISTS path (
    id SERIAL PRIMARY KEY,
    path TEXT NOT NULL,
    date_last_scan TIMESTAMP,
    date_creation TIMESTAMP NOT NULL,
    disabled BOOLEAN NOT NULL,
    tries INT NOT NULL,
    large BOOLEAN NOT NULL,
    file BOOLEAN NOT NULL,
    -- A path can own a file
    file_id INT,
    FOREIGN KEY (file_id)
    REFERENCES file (id)
    ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT unique_path_file UNIQUE (file_id, path),
    -- A path can owns a hash
    hash_id INT NOT NULL,
    FOREIGN KEY (hash_id)
    REFERENCES hash (id)
    ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT unique_path_hash UNIQUE (hash_id, path),
    -- A path can own a large content
    large_content_id INT,
    FOREIGN KEY (large_content_id)
    REFERENCES large_content (id)
    ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT unique_path_large_content UNIQUE (large_content_id, path)
);

CREATE TABLE IF NOT EXISTS hostname (
    id SERIAL PRIMARY KEY,
    hostname VARCHAR(80) NOT NULL,
    date_creation TIMESTAMP NOT NULL,
    disabled BOOLEAN NOT NULL,
    protocol_id INTEGER NOT NULL,
    path_id INTEGER NOT NULL,
    -- hostname owns a protocol
    FOREIGN KEY (protocol_id) 
    REFERENCES protocol (id)
    ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT unique_hostname_protocol UNIQUE (protocol_id, hostname),
    -- hostname owns a path 
    FOREIGN KEY (path_id) 
    REFERENCES path (id)
    ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT unique_hostname_path UNIQUE (path_id, hostname)
);



